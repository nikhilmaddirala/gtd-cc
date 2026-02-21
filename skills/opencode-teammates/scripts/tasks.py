#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path
from typing import Any

from common import (
    assert_team_scope,
    current_member_name,
    current_role,
    emit,
    file_lock,
    list_tasks,
    load_config,
    lock_path_for_tasks,
    next_task_id,
    read_json,
    tasks_dir,
    write_json_atomic,
)


STATUS_ORDER = {"pending": 0, "in_progress": 1, "completed": 2}


def task_path(team: str, task_id: str) -> Path:
    return tasks_dir(team) / f"{task_id}.json"


def require_task(team: str, task_id: str) -> dict[str, Any]:
    path = task_path(team, task_id)
    if not path.exists():
        raise FileNotFoundError(f"Task {task_id!r} not found")
    data = read_json(path, {})
    if not isinstance(data, dict):
        raise ValueError(f"Invalid task file: {path}")
    return data


def parse_list_arg(value: str) -> list[str]:
    if not value.strip():
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def dependency_map(team: str) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}
    for task in list_tasks(team):
        tid = str(task.get("id", ""))
        graph[tid] = [str(dep) for dep in task.get("blockedBy", [])]
    return graph


def would_create_cycle(team: str, task_id: str, add_blocked_by: list[str]) -> bool:
    graph = dependency_map(team)
    graph.setdefault(task_id, [])
    for dep in add_blocked_by:
        graph[task_id].append(dep)

    visited: set[str] = set()
    stack: set[str] = set()

    def dfs(node: str) -> bool:
        if node in stack:
            return True
        if node in visited:
            return False
        visited.add(node)
        stack.add(node)
        for nxt in graph.get(node, []):
            if dfs(nxt):
                return True
        stack.remove(node)
        return False

    return dfs(task_id)


def validate_status_transition(
    team: str, task: dict[str, Any], new_status: str
) -> None:
    if new_status == "deleted":
        return
    if new_status not in STATUS_ORDER:
        raise ValueError(f"Invalid status {new_status!r}")
    old_status = str(task.get("status", "pending"))
    if STATUS_ORDER[new_status] < STATUS_ORDER.get(old_status, 0):
        raise ValueError(f"Cannot transition from {old_status!r} to {new_status!r}")

    blockers = [str(dep) for dep in task.get("blockedBy", [])]
    if new_status in {"in_progress", "completed"} and blockers:
        for dep in blockers:
            dep_task = require_task(team, dep)
            if dep_task.get("status") != "completed":
                raise ValueError(
                    f"Cannot set status to {new_status!r}: blocked by task {dep} (status={dep_task.get('status')!r})"
                )


def create_task(
    team: str, subject: str, description: str, active_form: str, metadata_json: str
) -> dict:
    _ = load_config(team)
    if not subject.strip():
        raise ValueError("Task subject must not be empty")
    tdir = tasks_dir(team)
    tdir.mkdir(parents=True, exist_ok=True)

    metadata = json.loads(metadata_json) if metadata_json else None
    task = {
        "id": next_task_id(team),
        "subject": subject,
        "description": description,
        "activeForm": active_form,
        "status": "pending",
        "blocks": [],
        "blockedBy": [],
        "owner": None,
        "metadata": metadata,
    }
    with file_lock(lock_path_for_tasks(team)):
        write_json_atomic(task_path(team, task["id"]), task)
    return task


def update_task(
    team: str,
    task_id: str,
    status: str,
    owner: str,
    subject: str,
    description: str,
    active_form: str,
    add_blocks: list[str],
    add_blocked_by: list[str],
    metadata_json: str,
) -> dict:
    _ = load_config(team)
    assert_team_scope(team)
    path = task_path(team, task_id)
    with file_lock(lock_path_for_tasks(team)):
        task = require_task(team, task_id)

        if current_role() == "teammate":
            member = current_member_name()
            if not member:
                raise PermissionError("Teammate session missing OPENCODE_TEAM_MEMBER")
            if str(task.get("owner") or "") not in {"", member}:
                raise PermissionError("Teammate can only update own tasks")
            if owner and owner != member:
                raise PermissionError("Teammate cannot assign tasks to other members")
            if any(
                [
                    subject,
                    description,
                    active_form,
                    metadata_json,
                    add_blocks,
                    add_blocked_by,
                ]
            ):
                raise PermissionError(
                    "Teammate cannot change task structure or metadata"
                )
            if status and status not in {"pending", "in_progress", "completed"}:
                raise PermissionError("Teammate cannot delete tasks")

        for ref in add_blocks + add_blocked_by:
            _ = require_task(team, ref)
            if ref == task_id:
                raise ValueError("Task cannot depend on itself")
        if add_blocked_by and would_create_cycle(team, task_id, add_blocked_by):
            raise ValueError("Dependency update would create a circular dependency")

        if subject:
            task["subject"] = subject
        if description:
            task["description"] = description
        if active_form:
            task["activeForm"] = active_form

        if owner:
            members = {
                m.get("name")
                for m in load_config(team).get("members", [])
                if isinstance(m, dict)
            }
            if owner not in members:
                raise ValueError(f"Owner {owner!r} not in team")
            task["owner"] = owner

        blocks = set(str(item) for item in task.get("blocks", []))
        blocked_by = set(str(item) for item in task.get("blockedBy", []))

        for dep in add_blocks:
            blocks.add(dep)
            dep_task = require_task(team, dep)
            dep_blocked = set(str(item) for item in dep_task.get("blockedBy", []))
            dep_blocked.add(task_id)
            dep_task["blockedBy"] = sorted(dep_blocked, key=lambda x: int(x))
            write_json_atomic(task_path(team, dep), dep_task)

        for dep in add_blocked_by:
            blocked_by.add(dep)
            dep_task = require_task(team, dep)
            dep_blocks = set(str(item) for item in dep_task.get("blocks", []))
            dep_blocks.add(task_id)
            dep_task["blocks"] = sorted(dep_blocks, key=lambda x: int(x))
            write_json_atomic(task_path(team, dep), dep_task)

        task["blocks"] = sorted(blocks, key=lambda x: int(x))
        task["blockedBy"] = sorted(blocked_by, key=lambda x: int(x))

        if metadata_json:
            incoming = json.loads(metadata_json)
            current = task.get("metadata") or {}
            if not isinstance(current, dict):
                current = {}
            for key, value in incoming.items():
                if value is None:
                    current.pop(key, None)
                else:
                    current[key] = value
            task["metadata"] = current if current else None

        if status:
            validate_status_transition(team, task, status)
            if status == "deleted":
                unlink_deleted_task(team, task_id)
                task["status"] = "deleted"
                return task
            task["status"] = status

            if status == "completed":
                for other in list_tasks(team):
                    oid = str(other.get("id"))
                    if oid == task_id:
                        continue
                    ob = [x for x in other.get("blockedBy", []) if str(x) != task_id]
                    if len(ob) != len(other.get("blockedBy", [])):
                        other["blockedBy"] = ob
                        write_json_atomic(task_path(team, oid), other)

        write_json_atomic(path, task)
    return task


def unlink_deleted_task(team: str, task_id: str) -> None:
    for other in list_tasks(team):
        oid = str(other.get("id"))
        if oid == task_id:
            continue
        changed = False
        blocks = [x for x in other.get("blocks", []) if str(x) != task_id]
        blocked_by = [x for x in other.get("blockedBy", []) if str(x) != task_id]
        if len(blocks) != len(other.get("blocks", [])):
            other["blocks"] = blocks
            changed = True
        if len(blocked_by) != len(other.get("blockedBy", [])):
            other["blockedBy"] = blocked_by
            changed = True
        if changed:
            write_json_atomic(task_path(team, oid), other)
    task_path(team, task_id).unlink(missing_ok=True)


def get_task(team: str, task_id: str) -> dict:
    _ = load_config(team)
    assert_team_scope(team)
    return require_task(team, task_id)


def reset_owner(team: str, owner: str) -> dict:
    count = 0
    _ = load_config(team)
    with file_lock(lock_path_for_tasks(team)):
        for task in list_tasks(team):
            if task.get("owner") == owner:
                task["owner"] = None
                if task.get("status") != "completed":
                    task["status"] = "pending"
                write_json_atomic(task_path(team, str(task.get("id"))), task)
                count += 1
    return {"success": True, "reset": count}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Task state operations for teammate orchestration"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_create = sub.add_parser("create")
    p_create.add_argument("--team", required=True)
    p_create.add_argument("--subject", required=True)
    p_create.add_argument("--description", default="")
    p_create.add_argument("--active-form", default="")
    p_create.add_argument("--metadata-json", default="")

    p_update = sub.add_parser("update")
    p_update.add_argument("--team", required=True)
    p_update.add_argument("--id", required=True)
    p_update.add_argument("--status", default="")
    p_update.add_argument("--owner", default="")
    p_update.add_argument("--subject", default="")
    p_update.add_argument("--description", default="")
    p_update.add_argument("--active-form", default="")
    p_update.add_argument("--add-blocks", default="")
    p_update.add_argument("--add-blocked-by", default="")
    p_update.add_argument("--metadata-json", default="")

    p_get = sub.add_parser("get")
    p_get.add_argument("--team", required=True)
    p_get.add_argument("--id", required=True)

    p_list = sub.add_parser("list")
    p_list.add_argument("--team", required=True)

    p_reset = sub.add_parser("reset-owner")
    p_reset.add_argument("--team", required=True)
    p_reset.add_argument("--owner", required=True)

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if current_role() == "teammate":
            assert_team_scope(args.team)
            if args.cmd in {"create", "reset-owner"}:
                raise PermissionError(f"Teammate sessions cannot run {args.cmd}")
        if args.cmd == "create":
            result = create_task(
                args.team,
                args.subject,
                args.description,
                args.active_form,
                args.metadata_json,
            )
        elif args.cmd == "update":
            result = update_task(
                team=args.team,
                task_id=args.id,
                status=args.status,
                owner=args.owner,
                subject=args.subject,
                description=args.description,
                active_form=args.active_form,
                add_blocks=parse_list_arg(args.add_blocks),
                add_blocked_by=parse_list_arg(args.add_blocked_by),
                metadata_json=args.metadata_json,
            )
        elif args.cmd == "get":
            result = get_task(args.team, args.id)
        elif args.cmd == "list":
            _ = load_config(args.team)
            result = {"tasks": list_tasks(args.team)}
        elif args.cmd == "reset-owner":
            result = reset_owner(args.team, args.owner)
        else:
            raise ValueError(f"Unsupported command: {args.cmd}")
        emit(result)
        return 0
    except Exception as exc:
        emit({"success": False, "error": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
