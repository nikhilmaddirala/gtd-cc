#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

from __future__ import annotations

import argparse
from collections import Counter

from doctor import check as doctor_check

from common import (
    assert_lead_only,
    emit,
    file_lock,
    inbox_path,
    lock_path_for_team,
    read_json,
    write_json_atomic,
    load_config,
    list_tasks,
)
from tasks import update_task


def sync_done(
    team: str,
    from_agent: str,
    summary: str,
    task_id: str,
    mark_read: bool,
) -> dict:
    assert_lead_only("sync-done", team)
    path = inbox_path(team, "team-lead")
    with file_lock(lock_path_for_team(team)):
        messages = read_json(path, [])
        match_index = -1
        for i in range(len(messages) - 1, -1, -1):
            msg = messages[i]
            if (
                isinstance(msg, dict)
                and msg.get("from") == from_agent
                and msg.get("summary") == summary
            ):
                match_index = i
                break
        if match_index == -1:
            return {
                "success": False,
                "matched": False,
                "reason": f"No message from {from_agent!r} with summary {summary!r}",
            }
        msg = messages[match_index]
        if mark_read and isinstance(msg, dict):
            msg["read"] = True
            write_json_atomic(path, messages, indent=None)

    task = update_task(
        team=team,
        task_id=task_id,
        status="completed",
        owner="",
        subject="",
        description="",
        active_form="",
        add_blocks=[],
        add_blocked_by=[],
        metadata_json="",
    )
    return {
        "success": True,
        "matched": True,
        "task_id": task_id,
        "task_status": task.get("status"),
    }


def status_report(team: str, max_messages: int) -> dict:
    assert_lead_only("status-report", team)
    cfg = load_config(team)
    tasks = list_tasks(team)

    members = [m for m in cfg.get("members", []) if isinstance(m, dict)]
    teammates = [m for m in members if m.get("name") != "team-lead"]
    active_teammates = [m for m in teammates if bool(m.get("isActive", False))]

    status_counts = Counter(str(task.get("status", "pending")) for task in tasks)
    owner_counts = Counter(
        str(task.get("owner") or "unassigned")
        for task in tasks
        if str(task.get("status", "pending")) != "completed"
    )

    with file_lock(lock_path_for_team(team)):
        lead_messages = read_json(inbox_path(team, "team-lead"), [])

    unread = [
        msg
        for msg in lead_messages
        if isinstance(msg, dict) and not bool(msg.get("read", False))
    ]
    latest_unread = unread[-max_messages:] if max_messages > 0 else []

    health = doctor_check(team)

    return {
        "success": True,
        "team": team,
        "members": {
            "total": len(members),
            "teammates": len(teammates),
            "activeTeammates": len(active_teammates),
            "activeNames": [
                str(m.get("name"))
                for m in active_teammates
                if isinstance(m.get("name"), str)
            ],
        },
        "tasks": {
            "total": len(tasks),
            "byStatus": {
                "pending": status_counts.get("pending", 0),
                "in_progress": status_counts.get("in_progress", 0),
                "completed": status_counts.get("completed", 0),
                "deleted": status_counts.get("deleted", 0),
            },
            "openByOwner": dict(sorted(owner_counts.items())),
        },
        "leadInbox": {
            "unreadCount": len(unread),
            "latestUnread": latest_unread,
        },
        "health": {
            "ok": bool(health.get("ok", False)),
            "findings": health.get("findings", []),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lead automation helpers")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_sync = sub.add_parser("sync-done")
    p_sync.add_argument("--team", required=True)
    p_sync.add_argument("--from-agent", required=True)
    p_sync.add_argument("--summary", required=True)
    p_sync.add_argument("--task-id", required=True)
    p_sync.add_argument("--no-mark-read", action="store_true")

    p_report = sub.add_parser("status-report")
    p_report.add_argument("--team", required=True)
    p_report.add_argument("--max-messages", type=int, default=10)

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.cmd == "sync-done":
            result = sync_done(
                team=args.team,
                from_agent=args.from_agent,
                summary=args.summary,
                task_id=args.task_id,
                mark_read=not args.no_mark_read,
            )
        elif args.cmd == "status-report":
            result = status_report(
                team=args.team, max_messages=max(0, int(args.max_messages))
            )
        else:
            raise ValueError(f"Unsupported command: {args.cmd}")
        emit(result)
        return 0 if result.get("success") else 2
    except Exception as exc:
        emit({"success": False, "error": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
