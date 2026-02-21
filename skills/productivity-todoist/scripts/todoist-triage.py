#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["todoist-api-python>=3.1.0"]
# ///
"""
Batch triage Todoist tasks.

Usage:
    ./todoist-triage.py < decisions.json

decisions.json format:
[
    {"action": "drop", "task_name": "Task to drop"},
    {"action": "complete", "task_name": "Task actually done"},
    {"action": "reschedule", "task_name": "Task", "due_date": "2026-04-15"},
    {"action": "reschedule", "task_name": "Task", "due_string": "next monday"},
    {"action": "someday", "task_name": "Task to defer indefinitely"},
    {"action": "someday", "task_name": "Task", "new_content": "New task name"}
]

Actions:
- drop: Add "dropped" label and close (archived but marked as intentionally skipped)
- complete: Just close (task was actually done)
- reschedule: Update due date
- someday: Add "someday" label, remove due date, optionally rename

Token read from ~/.config/todoist-cli/config.json.
"""

import json
import sys
from pathlib import Path

from todoist_api_python.api import TodoistAPI

TOKEN_PATH = Path.home() / ".config" / "todoist-cli" / "config.json"

DROPPED_LABEL = "dropped"
SOMEDAY_LABEL = "someday"


def load_token() -> str:
    if not TOKEN_PATH.exists():
        print(f"Error: token file not found at {TOKEN_PATH}", file=sys.stderr)
        print("Run: npx @doist/todoist-cli auth token YOUR_TOKEN", file=sys.stderr)
        sys.exit(1)
    data = json.loads(TOKEN_PATH.read_text())
    token = data.get("api_token", "")
    if not token:
        print(f"Error: no api_token in {TOKEN_PATH}", file=sys.stderr)
        sys.exit(1)
    return token


def collect_pages(iterator) -> list:
    results = []
    for page in iterator:
        results.extend(page)
    return results


def find_task_by_name(tasks: list, name: str):
    name_lower = name.lower()
    for task in tasks:
        if name_lower in task.content.lower():
            return task
    return None


def drop_task(api: TodoistAPI, task) -> None:
    existing_labels = list(task.labels) if task.labels else []
    if DROPPED_LABEL not in existing_labels:
        existing_labels.append(DROPPED_LABEL)
    api.update_task(task_id=task.id, labels=existing_labels)
    api.close_task(task_id=task.id)


def complete_task(api: TodoistAPI, task) -> None:
    api.close_task(task_id=task.id)


def reschedule_task(api: TodoistAPI, task, due_date: str | None = None, due_string: str | None = None) -> None:
    if due_date:
        api.update_task(task_id=task.id, due_date=due_date)
    elif due_string:
        api.update_task(task_id=task.id, due_string=due_string)
    else:
        raise ValueError("Must provide either due_date or due_string")


def someday_task(api: TodoistAPI, task, new_content: str | None = None) -> None:
    existing_labels = list(task.labels) if task.labels else []
    if SOMEDAY_LABEL not in existing_labels:
        existing_labels.append(SOMEDAY_LABEL)
    kwargs: dict = {"labels": existing_labels, "due_string": "no date"}
    if new_content:
        kwargs["content"] = new_content
    api.update_task(task_id=task.id, **kwargs)


def main():
    decisions = json.load(sys.stdin)

    token = load_token()
    api = TodoistAPI(token)

    tasks = collect_pages(api.get_tasks())
    print(f"Fetched {len(tasks)} active tasks")

    for decision in decisions:
        action = decision["action"]
        task_name = decision["task_name"]

        task = find_task_by_name(tasks, task_name)
        if not task:
            print(f"  Task not found: {task_name}")
            continue

        if action == "drop":
            drop_task(api, task)
            print(f"  Dropped: {task.content}")

        elif action == "complete":
            complete_task(api, task)
            print(f"  Completed: {task.content}")

        elif action == "reschedule":
            due_date = decision.get("due_date")
            due_string = decision.get("due_string")
            reschedule_task(api, task, due_date=due_date, due_string=due_string)
            new_due = due_date or due_string
            print(f"  Rescheduled: {task.content} -> {new_due}")

        elif action == "someday":
            new_content = decision.get("new_content")
            someday_task(api, task, new_content=new_content)
            if new_content:
                print(f"  Someday: {task.content} -> {new_content}")
            else:
                print(f"  Someday: {task.content}")

        else:
            print(f"  Unknown action: {action}")


if __name__ == "__main__":
    main()
