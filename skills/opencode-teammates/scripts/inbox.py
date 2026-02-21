#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

from __future__ import annotations

import argparse
import json
import time

from opencode_api import OpenCodeAPIError, prompt_async

from common import (
    assert_team_scope,
    current_member_name,
    current_role,
    emit,
    ensure_inbox,
    file_lock,
    inbox_path,
    load_config,
    lock_path_for_team,
    now_iso,
    read_json,
    write_json_atomic,
)


def ensure(team: str, agent: str) -> dict:
    path = ensure_inbox(team, agent)
    return {"success": True, "path": str(path)}


def append(team: str, agent: str, message: dict) -> None:
    path = ensure_inbox(team, agent)
    with file_lock(lock_path_for_team(team)):
        messages = read_json(path, [])
        messages.append(message)
        write_json_atomic(path, messages, indent=None)


def upsert_by_summary(team: str, agent: str, message: dict) -> bool:
    """Replace existing unread message with same from+summary.

    Returns True when a prior message was replaced, False when appended is needed.
    """
    path = ensure_inbox(team, agent)
    with file_lock(lock_path_for_team(team)):
        messages = read_json(path, [])
        replaced = False
        target_from = message.get("from")
        target_summary = message.get("summary")
        if target_from and target_summary:
            for item in reversed(messages):
                if (
                    item.get("from") == target_from
                    and item.get("summary") == target_summary
                    and not item.get("read", False)
                ):
                    item.update(message)
                    replaced = True
                    break
        if replaced:
            write_json_atomic(path, messages, indent=None)
            return True
        messages.append(message)
        write_json_atomic(path, messages, indent=None)
        return False


def send(
    team: str,
    from_name: str,
    to: str,
    text: str,
    summary: str,
    color: str,
    replace_summary: bool,
) -> dict:
    assert_team_scope(team)
    cfg = load_config(team)
    target_member: dict | None = None
    for member in cfg.get("members", []):
        if isinstance(member, dict) and member.get("name") == to:
            target_member = member
            break
    members = {m.get("name") for m in cfg.get("members", []) if isinstance(m, dict)}
    if from_name not in members:
        raise ValueError(f"Unknown sender {from_name!r}")
    if to not in members:
        raise ValueError(f"Unknown recipient {to!r}")
    if from_name != "team-lead" and to != "team-lead":
        raise ValueError("Teammates can only direct-message team-lead")
    if not text.strip():
        raise ValueError("Message text must not be empty")
    if not summary.strip():
        raise ValueError("Message summary must not be empty")

    if current_role() == "teammate":
        member = current_member_name()
        if not member or from_name != member:
            raise PermissionError("Teammate session can only send as itself")
        if to != "team-lead":
            raise PermissionError("Teammate session can only message team-lead")

    msg = {
        "from": from_name,
        "text": text,
        "timestamp": now_iso(),
        "read": False,
        "summary": summary,
    }
    if color:
        msg["color"] = color
    replaced = (
        upsert_by_summary(team, to, msg)
        if replace_summary
        else (append(team, to, msg) or False)
    )
    pushed = False
    if isinstance(target_member, dict):
        session_id = target_member.get("opencodeSessionId")
        if isinstance(session_id, str) and session_id:
            agent_type = target_member.get("agentType")
            if not isinstance(agent_type, str) or not agent_type:
                agent_type = "build"
            model = target_member.get("model")
            if not isinstance(model, str):
                model = ""
            try:
                prompt_async(session_id, text, agent=agent_type, model=model)
                pushed = True
            except OpenCodeAPIError:
                pushed = False
    return {
        "success": True,
        "to": to,
        "summary": summary,
        "pushed_to_session": pushed,
        "replaced_unread": replaced,
    }


def broadcast(
    team: str, from_name: str, text: str, summary: str, replace_summary: bool
) -> dict:
    assert_team_scope(team)
    if from_name != "team-lead":
        raise ValueError("Only team-lead can broadcast")
    if current_role() == "teammate":
        raise PermissionError("Teammate session cannot broadcast")
    cfg = load_config(team)
    count = 0
    pushed = 0
    replaced = 0
    for member in cfg.get("members", []):
        if not isinstance(member, dict):
            continue
        name = member.get("name")
        if not isinstance(name, str) or name == "team-lead":
            continue
        payload = {
            "from": "team-lead",
            "text": text,
            "timestamp": now_iso(),
            "read": False,
            "summary": summary,
        }
        if replace_summary:
            if upsert_by_summary(team, name, payload):
                replaced += 1
        else:
            append(team, name, payload)
        session_id = member.get("opencodeSessionId")
        if isinstance(session_id, str) and session_id:
            agent_type = member.get("agentType")
            if not isinstance(agent_type, str) or not agent_type:
                agent_type = "build"
            model = member.get("model")
            if not isinstance(model, str):
                model = ""
            try:
                prompt_async(session_id, text, agent=agent_type, model=model)
                pushed += 1
            except OpenCodeAPIError:
                pass
        count += 1
    return {
        "success": True,
        "count": count,
        "pushed_to_sessions": pushed,
        "replaced_unread": replaced,
    }


def read(team: str, agent: str, unread_only: bool, mark_as_read: bool) -> dict:
    assert_team_scope(team)
    _ = load_config(team)
    if current_role() == "teammate":
        member = current_member_name()
        if not member or agent != member:
            raise PermissionError("Teammate session can only read its own inbox")
    path = ensure_inbox(team, agent)
    with file_lock(lock_path_for_team(team)):
        messages = read_json(path, [])
        selected = (
            [m for m in messages if not m.get("read", False)]
            if unread_only
            else list(messages)
        )
        if mark_as_read and selected:
            selected_ids = {id(item) for item in selected}
            for item in messages:
                if id(item) in selected_ids:
                    item["read"] = True
            write_json_atomic(path, messages, indent=None)
    return {"messages": selected, "count": len(selected)}


def shutdown_request(team: str, recipient: str, reason: str) -> dict:
    assert_team_scope(team)
    if current_role() == "teammate":
        raise PermissionError("Teammate session cannot request shutdown")
    cfg = load_config(team)
    target_member: dict | None = None
    for member in cfg.get("members", []):
        if isinstance(member, dict) and member.get("name") == recipient:
            target_member = member
            break
    if not isinstance(target_member, dict):
        raise ValueError(f"Unknown recipient {recipient!r}")

    request_id = f"shutdown-{int(time.time() * 1000)}@{recipient}"
    payload = {
        "type": "shutdown_request",
        "requestId": request_id,
        "from": "team-lead",
        "reason": reason,
        "timestamp": now_iso(),
    }
    append(
        team,
        recipient,
        {
            "from": "team-lead",
            "text": json.dumps(payload, ensure_ascii=True),
            "timestamp": now_iso(),
            "read": False,
            "summary": "shutdown_request",
        },
    )
    pushed = False
    session_id = target_member.get("opencodeSessionId")
    if isinstance(session_id, str) and session_id:
        model = target_member.get("model")
        if not isinstance(model, str):
            model = ""
        try:
            prompt_async(
                session_id,
                json.dumps(payload, ensure_ascii=True),
                target_member.get("agentType", "build"),
                model,
            )
            pushed = True
        except OpenCodeAPIError:
            pushed = False
    return {
        "success": True,
        "request_id": request_id,
        "recipient": recipient,
        "pushed_to_session": pushed,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inbox operations for teammate orchestration"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ensure = sub.add_parser("ensure")
    p_ensure.add_argument("--team", required=True)
    p_ensure.add_argument("--agent", required=True)

    p_send = sub.add_parser("send")
    p_send.add_argument("--team", required=True)
    p_send.add_argument("--from-name", required=True)
    p_send.add_argument("--to", required=True)
    p_send.add_argument("--text", required=True)
    p_send.add_argument("--summary", required=True)
    p_send.add_argument("--color", default="")
    p_send.add_argument("--no-replace-summary", action="store_true")

    p_bcast = sub.add_parser("broadcast")
    p_bcast.add_argument("--team", required=True)
    p_bcast.add_argument("--from-name", default="team-lead")
    p_bcast.add_argument("--text", required=True)
    p_bcast.add_argument("--summary", required=True)
    p_bcast.add_argument("--no-replace-summary", action="store_true")

    p_read = sub.add_parser("read")
    p_read.add_argument("--team", required=True)
    p_read.add_argument("--agent", required=True)
    p_read.add_argument("--unread-only", action="store_true")
    p_read.add_argument("--no-mark-read", action="store_true")

    p_shutdown = sub.add_parser("shutdown-request")
    p_shutdown.add_argument("--team", required=True)
    p_shutdown.add_argument("--recipient", required=True)
    p_shutdown.add_argument("--reason", default="")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.cmd == "ensure":
            result = ensure(args.team, args.agent)
        elif args.cmd == "send":
            result = send(
                args.team,
                args.from_name,
                args.to,
                args.text,
                args.summary,
                args.color,
                not args.no_replace_summary,
            )
        elif args.cmd == "broadcast":
            result = broadcast(
                args.team,
                args.from_name,
                args.text,
                args.summary,
                not args.no_replace_summary,
            )
        elif args.cmd == "read":
            result = read(
                args.team, args.agent, args.unread_only, not args.no_mark_read
            )
        elif args.cmd == "shutdown-request":
            result = shutdown_request(args.team, args.recipient, args.reason)
        else:
            raise ValueError(f"Unsupported command: {args.cmd}")
        emit(result)
        return 0
    except Exception as exc:
        emit({"success": False, "error": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
