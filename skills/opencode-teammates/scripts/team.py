#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

from __future__ import annotations

import argparse
import os
import re
import subprocess
from pathlib import Path

from opencode_api import OpenCodeAPIError, abort_session, delete_session

from common import (
    assert_lead_only,
    assign_color,
    config_path,
    emit,
    ensure_dirs,
    file_lock,
    load_config,
    lock_path_for_tasks,
    lock_path_for_team,
    new_session_id,
    now_ms,
    read_json,
    tasks_dir,
    validate_name,
    write_config,
)


def detect_tmux_anchor() -> tuple[str, str]:
    if not os.environ.get("TMUX"):
        return "", ""
    pane_from_env = os.environ.get("TMUX_PANE", "").strip()
    if pane_from_env:
        try:
            pane_check = subprocess.run(
                ["tmux", "display-message", "-p", "-t", pane_from_env, "#{pane_id}"],
                check=False,
                capture_output=True,
                text=True,
            )
            if (
                pane_check.returncode == 0
                and pane_check.stdout.strip() == pane_from_env
            ):
                window = subprocess.run(
                    [
                        "tmux",
                        "display-message",
                        "-p",
                        "-t",
                        pane_from_env,
                        "#{window_id}",
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                if window.returncode == 0 and window.stdout.strip():
                    return window.stdout.strip(), pane_from_env
        except Exception:
            pass
    try:
        window = subprocess.run(
            ["tmux", "display-message", "-p", "#{window_id}"],
            check=False,
            capture_output=True,
            text=True,
        )
        pane = subprocess.run(
            ["tmux", "display-message", "-p", "#{pane_id}"],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        return "", ""
    window_id = window.stdout.strip() if window.returncode == 0 else ""
    pane_id = pane.stdout.strip() if pane.returncode == 0 else ""
    return window_id, pane_id


def capture_lead_env() -> dict[str, str]:
    keys = [
        "HOME",
        "XDG_CONFIG_HOME",
        "OPENCODE_CONFIG",
        "OPENCODE_THEME",
        "COLORTERM",
        "TERM",
    ]
    captured: dict[str, str] = {}
    for key in keys:
        value = os.environ.get(key, "").strip()
        if value:
            captured[key] = value

    home = captured.get("HOME") or str(Path.home())
    xdg_config_home = captured.get("XDG_CONFIG_HOME")
    if not xdg_config_home:
        xdg_config_home = str(Path(home) / ".config")
        captured["XDG_CONFIG_HOME"] = xdg_config_home

    if "OPENCODE_CONFIG" not in captured:
        candidate = Path(xdg_config_home) / "opencode" / "opencode.jsonc"
        if candidate.exists():
            captured["OPENCODE_CONFIG"] = str(candidate)

    config_path = captured.get("OPENCODE_CONFIG", "").strip()
    config_theme = ""
    if config_path:
        try:
            text = Path(config_path).read_text(encoding="utf-8", errors="ignore")
            match = re.search(r'"theme"\s*:\s*"([^"]+)"', text)
            if match and match.group(1).strip():
                config_theme = match.group(1).strip()
        except Exception:
            config_theme = ""

    if config_theme:
        captured["OPENCODE_THEME"] = config_theme
    elif "OPENCODE_THEME" not in captured:
        value = os.environ.get("OPENCODE_THEME", "").strip()
        if value:
            captured["OPENCODE_THEME"] = value
    return captured


def create_team(team: str, description: str, lead_session_id: str | None) -> dict:
    validate_name(team, "team name")
    if config_path(team).exists():
        raise ValueError(f"Team {team!r} already exists")

    ensure_dirs(team)
    session = lead_session_id or new_session_id()
    now = now_ms()
    lead_window_id, lead_pane_id = detect_tmux_anchor()
    config = {
        "name": team,
        "description": description,
        "createdAt": now,
        "leadAgentId": f"team-lead@{team}",
        "leadSessionId": session,
        "leadWindowId": lead_window_id,
        "leadPaneId": lead_pane_id,
        "leadEnv": capture_lead_env(),
        "members": [
            {
                "agentId": f"team-lead@{team}",
                "name": "team-lead",
                "agentType": "team-lead",
                "model": "opencode",
                "joinedAt": now,
                "tmuxPaneId": "",
                "cwd": str(Path.cwd()),
                "subscriptions": [],
            }
        ],
    }
    with file_lock(lock_path_for_team(team)):
        write_config(team, config)
    return {
        "success": True,
        "team_name": team,
        "team_file_path": str(config_path(team)),
        "lead_agent_id": f"team-lead@{team}",
    }


def delete_team(team: str) -> dict:
    cfg = load_config(team)
    teammates = [
        m
        for m in cfg.get("members", [])
        if isinstance(m, dict) and m.get("name") != "team-lead"
    ]
    if teammates:
        raise ValueError(
            f"Cannot delete {team!r}: {len(teammates)} teammate(s) still active"
        )

    for root in (config_path(team).parent, tasks_dir(team)):
        if root.exists():
            for child in sorted(root.glob("**/*"), reverse=True):
                if child.is_file() or child.is_symlink():
                    child.unlink(missing_ok=True)
                elif child.is_dir():
                    child.rmdir()
            root.rmdir()
    return {"success": True, "team_name": team}


def list_teams() -> dict:
    base = config_path("x").parents[1]
    teams = []
    if base.exists():
        for item in sorted(base.iterdir()):
            if item.is_dir() and (item / "config.json").exists():
                teams.append(item.name)
    return {"teams": teams}


def add_member(
    team: str,
    name: str,
    prompt: str,
    model: str,
    agent_type: str,
    backend_type: str,
    cwd: str,
    plan_mode_required: bool,
    tmux_pane_id: str,
    opencode_session_id: str,
) -> dict:
    if backend_type != "opencode":
        raise ValueError("Only opencode teammates are supported")
    validate_name(name, "member name")
    if name == "team-lead":
        raise ValueError("team-lead is reserved")
    cfg = load_config(team)
    names = {m.get("name") for m in cfg.get("members", []) if isinstance(m, dict)}
    if name in names:
        raise ValueError(f"Member {name!r} already exists")

    color = assign_color(cfg)
    member = {
        "agentId": f"{name}@{team}",
        "name": name,
        "agentType": agent_type,
        "model": model,
        "prompt": prompt,
        "color": color,
        "planModeRequired": plan_mode_required,
        "joinedAt": now_ms(),
        "tmuxPaneId": tmux_pane_id,
        "cwd": cwd,
        "subscriptions": [],
        "backendType": backend_type,
        "opencodeSessionId": opencode_session_id or None,
        "isActive": bool(tmux_pane_id),
    }

    with file_lock(lock_path_for_team(team)):
        cfg = load_config(team)
        cfg.setdefault("members", []).append(member)
        write_config(team, cfg)
    return member


def remove_member(
    team: str, name: str, reset_tasks: bool, cleanup_session: bool
) -> dict:
    if name == "team-lead":
        raise ValueError("Cannot remove team-lead")
    cfg = load_config(team)
    session_id = ""
    members = cfg.get("members", [])
    before = len(members)
    for member in members:
        if isinstance(member, dict) and member.get("name") == name:
            sid = member.get("opencodeSessionId")
            if isinstance(sid, str):
                session_id = sid
            break
    cfg["members"] = [
        m for m in members if not (isinstance(m, dict) and m.get("name") == name)
    ]
    if len(cfg["members"]) == before:
        raise ValueError(f"Member {name!r} not found")
    with file_lock(lock_path_for_team(team)):
        write_config(team, cfg)

    reset_count = 0
    if reset_tasks:
        with file_lock(lock_path_for_tasks(team)):
            for task_file in tasks_dir(team).glob("*.json"):
                try:
                    int(task_file.stem)
                except ValueError:
                    continue
                task = read_json(task_file, {})
                if task.get("owner") == name:
                    task["owner"] = None
                    if task.get("status") != "completed":
                        task["status"] = "pending"
                    from common import write_json_atomic

                    write_json_atomic(task_file, task)
                    reset_count += 1

    session_cleanup = "skipped"
    if cleanup_session and session_id:
        try:
            abort_session(session_id)
            delete_session(session_id)
            session_cleanup = "deleted"
        except OpenCodeAPIError:
            session_cleanup = "failed"

    return {
        "success": True,
        "removed": name,
        "reset_tasks": reset_count,
        "session_cleanup": session_cleanup,
    }


def set_runtime(team: str, name: str, tmux_pane_id: str, is_active: bool) -> dict:
    cfg = load_config(team)
    updated = None
    for member in cfg.get("members", []):
        if isinstance(member, dict) and member.get("name") == name:
            member["tmuxPaneId"] = tmux_pane_id
            member["isActive"] = is_active
            updated = member
            break
    if updated is None:
        raise ValueError(f"Member {name!r} not found")
    with file_lock(lock_path_for_team(team)):
        write_config(team, cfg)
    return updated


def set_anchor(team: str, window_id: str, pane_id: str) -> dict:
    if not window_id.strip():
        raise ValueError("window_id must not be empty")
    cfg = load_config(team)
    cfg["leadWindowId"] = window_id.strip()
    cfg["leadPaneId"] = pane_id.strip()
    with file_lock(lock_path_for_team(team)):
        write_config(team, cfg)
    return {
        "success": True,
        "team": team,
        "leadWindowId": cfg.get("leadWindowId", ""),
        "leadPaneId": cfg.get("leadPaneId", ""),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage local teammate team config")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_create = sub.add_parser("create")
    p_create.add_argument("--team", required=True)
    p_create.add_argument("--description", default="")
    p_create.add_argument("--lead-session-id", default="")

    p_delete = sub.add_parser("delete")
    p_delete.add_argument("--team", required=True)

    p_show = sub.add_parser("show")
    p_show.add_argument("--team", required=True)

    sub.add_parser("list")

    p_add = sub.add_parser("add-member")
    p_add.add_argument("--team", required=True)
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--prompt", required=True)
    p_add.add_argument("--model", default="opencode/gpt-5-nano")
    p_add.add_argument("--agent-type", default="build")
    p_add.add_argument("--backend-type", default="opencode")
    p_add.add_argument("--cwd", default=str(Path.cwd()))
    p_add.add_argument("--plan-mode-required", action="store_true")
    p_add.add_argument("--tmux-pane-id", default="")
    p_add.add_argument("--opencode-session-id", default="")

    p_remove = sub.add_parser("remove-member")
    p_remove.add_argument("--team", required=True)
    p_remove.add_argument("--name", required=True)
    p_remove.add_argument("--reset-tasks", action="store_true")
    p_remove.add_argument("--cleanup-session", action="store_true")

    p_set = sub.add_parser("set-runtime")
    p_set.add_argument("--team", required=True)
    p_set.add_argument("--name", required=True)
    p_set.add_argument("--tmux-pane-id", default="")
    p_set.add_argument("--is-active", action="store_true")

    p_anchor = sub.add_parser("set-anchor")
    p_anchor.add_argument("--team", required=True)
    p_anchor.add_argument("--window-id", required=True)
    p_anchor.add_argument("--pane-id", default="")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.cmd in {
            "create",
            "delete",
            "add-member",
            "remove-member",
            "set-runtime",
            "set-anchor",
        }:
            assert_lead_only(args.cmd, args.team)
        if args.cmd == "create":
            result = create_team(
                args.team, args.description, args.lead_session_id or None
            )
        elif args.cmd == "delete":
            result = delete_team(args.team)
        elif args.cmd == "show":
            result = load_config(args.team)
        elif args.cmd == "list":
            result = list_teams()
        elif args.cmd == "add-member":
            result = add_member(
                team=args.team,
                name=args.name,
                prompt=args.prompt,
                model=args.model,
                agent_type=args.agent_type,
                backend_type=args.backend_type,
                cwd=args.cwd,
                plan_mode_required=args.plan_mode_required,
                tmux_pane_id=args.tmux_pane_id,
                opencode_session_id=args.opencode_session_id,
            )
        elif args.cmd == "remove-member":
            result = remove_member(
                args.team,
                args.name,
                args.reset_tasks,
                args.cleanup_session,
            )
        elif args.cmd == "set-runtime":
            result = set_runtime(
                args.team, args.name, args.tmux_pane_id, args.is_active
            )
        elif args.cmd == "set-anchor":
            result = set_anchor(args.team, args.window_id, args.pane_id)
        else:
            raise ValueError(f"Unsupported command: {args.cmd}")
        emit(result)
        return 0
    except Exception as exc:
        emit({"success": False, "error": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
