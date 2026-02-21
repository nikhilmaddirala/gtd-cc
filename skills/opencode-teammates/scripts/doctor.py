#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import os
import subprocess

from common import emit, ensure_inbox, inbox_path, list_tasks, load_config
from opencode_api import OpenCodeAPIError, session_status


def tmux_target_exists(target: str) -> bool:
    if not target:
        return False
    if target.startswith("@"):
        cmd = ["tmux", "list-windows", "-F", "#{window_id}"]
    else:
        cmd = ["tmux", "list-panes", "-a", "-F", "#{pane_id}"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            return False
        return target in {line.strip() for line in proc.stdout.splitlines()}
    except Exception:
        return False


def env_int(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        parsed = int(raw)
    except ValueError:
        return default
    return parsed if parsed >= 0 else default


def parse_timestamp_ms(value: str) -> int | None:
    text = (value or "").strip()
    if not text:
        return None
    try:
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return int(dt.timestamp() * 1000)
    except Exception:
        return None


def read_inbox_messages(team: str, agent: str) -> list[dict]:
    path = ensure_inbox(team, agent)
    payload = []
    try:
        from common import read_json

        data = read_json(path, [])
        if isinstance(data, list):
            payload = [item for item in data if isinstance(item, dict)]
    except Exception:
        payload = []
    return payload


def check(team: str) -> dict:
    cfg = load_config(team)
    findings: list[dict] = []
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    initial_assignment_timeout_ms = env_int(
        "OPENCODE_TEAM_INITIAL_ASSIGNMENT_TIMEOUT_MS", 120000
    )
    assignment_ack_timeout_ms = env_int(
        "OPENCODE_TEAM_ASSIGNMENT_ACK_TIMEOUT_MS", 180000
    )
    teammate_silence_timeout_ms = env_int("OPENCODE_TEAM_SILENCE_TIMEOUT_MS", 300000)

    members = [m for m in cfg.get("members", []) if isinstance(m, dict)]
    names = {m.get("name") for m in members}
    lead_inbox = read_inbox_messages(team, "team-lead")

    for member in members:
        name = member.get("name")
        if not isinstance(name, str):
            findings.append(
                {
                    "level": "error",
                    "kind": "invalid-member",
                    "message": "Member missing valid name",
                }
            )
            continue
        path = ensure_inbox(team, name)
        if not path.exists():
            findings.append(
                {
                    "level": "error",
                    "kind": "missing-inbox",
                    "member": name,
                    "path": str(inbox_path(team, name)),
                }
            )
        pane = member.get("tmuxPaneId", "")
        active = bool(member.get("isActive", False))
        if active and pane and not tmux_target_exists(pane):
            findings.append(
                {
                    "level": "warn",
                    "kind": "orphan-runtime",
                    "member": name,
                    "tmuxPaneId": pane,
                    "message": "Config says active but tmux target was not found",
                }
            )
        session_id = member.get("opencodeSessionId")
        if isinstance(session_id, str) and session_id:
            try:
                state = session_status(session_id)
                if state == "unknown":
                    findings.append(
                        {
                            "level": "warn",
                            "kind": "unknown-session",
                            "member": name,
                            "opencodeSessionId": session_id,
                        }
                    )
            except OpenCodeAPIError as exc:
                findings.append(
                    {
                        "level": "warn",
                        "kind": "session-check-failed",
                        "member": name,
                        "message": str(exc),
                    }
                )

        if name == "team-lead":
            continue

        joined_at = member.get("joinedAt")
        if not isinstance(joined_at, int):
            joined_at = now_ms

        teammate_inbox = read_inbox_messages(team, name)
        assignment_msgs = [
            msg
            for msg in teammate_inbox
            if str(msg.get("from")) == "team-lead"
            and "assignment" in str(msg.get("summary", "")).lower()
        ]
        latest_assignment_ms = None
        for msg in assignment_msgs:
            ts = parse_timestamp_ms(str(msg.get("timestamp", "")))
            if ts is None:
                continue
            if latest_assignment_ms is None or ts > latest_assignment_ms:
                latest_assignment_ms = ts

        teammate_reports = [msg for msg in lead_inbox if str(msg.get("from")) == name]
        latest_report_ms = None
        for msg in teammate_reports:
            ts = parse_timestamp_ms(str(msg.get("timestamp", "")))
            if ts is None:
                continue
            if latest_report_ms is None or ts > latest_report_ms:
                latest_report_ms = ts

        if (
            active
            and initial_assignment_timeout_ms > 0
            and latest_assignment_ms is None
        ):
            if now_ms - joined_at > initial_assignment_timeout_ms:
                findings.append(
                    {
                        "level": "error",
                        "kind": "missing-initial-assignment",
                        "member": name,
                        "ageMs": now_ms - joined_at,
                        "timeoutMs": initial_assignment_timeout_ms,
                        "message": "Teammate is active but has no assignment message",
                    }
                )

        if (
            active
            and assignment_ack_timeout_ms > 0
            and latest_assignment_ms is not None
            and (
                latest_report_ms is None
                or (
                    latest_report_ms is not None
                    and latest_report_ms < latest_assignment_ms
                )
            )
        ):
            if now_ms - latest_assignment_ms > assignment_ack_timeout_ms:
                findings.append(
                    {
                        "level": "error",
                        "kind": "missing-assignment-ack",
                        "member": name,
                        "lastAssignmentAtMs": latest_assignment_ms,
                        "timeoutMs": assignment_ack_timeout_ms,
                        "message": "No teammate progress/ack was reported after assignment",
                    }
                )

        if active and teammate_silence_timeout_ms > 0:
            candidate_times = [joined_at]
            if latest_assignment_ms is not None:
                candidate_times.append(latest_assignment_ms)
            if latest_report_ms is not None:
                candidate_times.append(latest_report_ms)
            last_signal_ms = max(candidate_times)
            if now_ms - last_signal_ms > teammate_silence_timeout_ms:
                findings.append(
                    {
                        "level": "error",
                        "kind": "silent-teammate-timeout",
                        "member": name,
                        "lastSignalAtMs": last_signal_ms,
                        "ageMs": now_ms - last_signal_ms,
                        "timeoutMs": teammate_silence_timeout_ms,
                    }
                )

    tasks = list_tasks(team)
    task_ids = {str(task.get("id")) for task in tasks}
    for task in tasks:
        tid = str(task.get("id"))
        owner = task.get("owner")
        if owner and owner not in names:
            findings.append(
                {
                    "level": "error",
                    "kind": "invalid-owner",
                    "taskId": tid,
                    "owner": owner,
                }
            )
        for dep in task.get("blockedBy", []):
            if str(dep) not in task_ids:
                findings.append(
                    {
                        "level": "error",
                        "kind": "missing-dependency",
                        "taskId": tid,
                        "blockedBy": str(dep),
                    }
                )
        for dep in task.get("blocks", []):
            if str(dep) not in task_ids:
                findings.append(
                    {
                        "level": "error",
                        "kind": "missing-block-target",
                        "taskId": tid,
                        "blocks": str(dep),
                    }
                )

    return {
        "team": team,
        "memberCount": len(members),
        "taskCount": len(tasks),
        "ok": len(findings) == 0,
        "findings": findings,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Health checks for opencode teammate skill state"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check")
    p_check.add_argument("--team", required=True)

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.cmd == "check":
            result = check(args.team)
        else:
            raise ValueError(f"Unsupported command: {args.cmd}")
        emit(result)
        return 0 if result.get("ok", False) else 2
    except Exception as exc:
        emit({"success": False, "error": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
