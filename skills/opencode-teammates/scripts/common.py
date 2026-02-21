#!/usr/bin/env python3

from __future__ import annotations

import contextlib
import json
import os
import re
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

try:
    import fcntl
except ImportError:  # pragma: no cover
    fcntl = None


VALID_NAME_RE = re.compile(r"^[A-Za-z0-9_-]+$")
COLOR_PALETTE = ["blue", "green", "yellow", "purple", "orange", "pink", "cyan", "red"]


def current_role() -> str:
    value = os.environ.get("OPENCODE_TEAM_ROLE", "team-lead").strip()
    return value or "team-lead"


def current_team_scope() -> str:
    return os.environ.get("OPENCODE_TEAM_TEAM", "").strip()


def current_member_name() -> str:
    return os.environ.get("OPENCODE_TEAM_MEMBER", "").strip()


def assert_team_scope(team: str) -> None:
    scoped = current_team_scope()
    if scoped and scoped != team:
        raise PermissionError(
            f"This session is scoped to team {scoped!r}, not {team!r}"
        )


def assert_lead_only(action: str, team: str) -> None:
    assert_team_scope(team)
    if current_role() == "teammate":
        raise PermissionError(f"Teammate sessions cannot run {action}")


def claude_root() -> Path:
    env = os.environ.get("OPENCODE_TEAM_HOME", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    return (Path.home() / ".claude").resolve()


def teams_root() -> Path:
    return claude_root() / "teams"


def tasks_root() -> Path:
    return claude_root() / "tasks"


def team_dir(team: str) -> Path:
    return teams_root() / team


def tasks_dir(team: str) -> Path:
    return tasks_root() / team


def config_path(team: str) -> Path:
    return team_dir(team) / "config.json"


def inbox_dir(team: str) -> Path:
    return team_dir(team) / "inboxes"


def inbox_path(team: str, agent: str) -> Path:
    return inbox_dir(team) / f"{agent}.json"


def lock_path_for_team(team: str) -> Path:
    return inbox_dir(team) / ".lock"


def lock_path_for_tasks(team: str) -> Path:
    return tasks_dir(team) / ".lock"


def now_ms() -> int:
    return int(time.time() * 1000)


def now_iso() -> str:
    dt = datetime.now(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt.microsecond // 1000:03d}Z"


def new_session_id() -> str:
    return str(uuid.uuid4())


def validate_name(name: str, label: str = "name") -> None:
    if not VALID_NAME_RE.match(name):
        raise ValueError(
            f"Invalid {label}: {name!r}. Use letters, numbers, hyphen, underscore"
        )
    if len(name) > 64:
        raise ValueError(f"{label} too long ({len(name)} chars, max 64)")


def ensure_dirs(team: str) -> None:
    team_dir(team).mkdir(parents=True, exist_ok=True)
    inbox_dir(team).mkdir(parents=True, exist_ok=True)
    tasks_dir(team).mkdir(parents=True, exist_ok=True)
    lock_path_for_team(team).touch(exist_ok=True)
    lock_path_for_tasks(team).touch(exist_ok=True)


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    text = path.read_text().strip()
    if not text:
        return default
    return json.loads(text)


def write_json_atomic(path: Path, payload: Any, indent: int | None = 2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=True, indent=indent)
            handle.write("\n")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


@contextlib.contextmanager
def file_lock(lock_path: Path) -> Iterator[None]:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, "a+", encoding="utf-8") as handle:
        if fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def load_config(team: str) -> dict[str, Any]:
    path = config_path(team)
    if not path.exists():
        raise FileNotFoundError(f"Team {team!r} not found")
    data = read_json(path, {})
    if not isinstance(data, dict):
        raise ValueError(f"Invalid team config: {path}")
    return data


def write_config(team: str, config: dict[str, Any]) -> None:
    write_json_atomic(config_path(team), config)


def list_tasks(team: str) -> list[dict[str, Any]]:
    tdir = tasks_dir(team)
    items: list[dict[str, Any]] = []
    for file in tdir.glob("*.json"):
        try:
            int(file.stem)
        except ValueError:
            continue
        data = read_json(file, {})
        if isinstance(data, dict):
            items.append(data)
    items.sort(key=lambda task: int(str(task.get("id", "0"))))
    return items


def next_task_id(team: str) -> str:
    max_id = 0
    for file in tasks_dir(team).glob("*.json"):
        try:
            max_id = max(max_id, int(file.stem))
        except ValueError:
            continue
    return str(max_id + 1)


def ensure_inbox(team: str, agent: str) -> Path:
    path = inbox_path(team, agent)
    if not path.exists():
        write_json_atomic(path, [], indent=None)
    return path


def assign_color(config: dict[str, Any]) -> str:
    members = config.get("members", [])
    teammate_count = 0
    for member in members:
        if (
            isinstance(member, dict)
            and member.get("name") != "team-lead"
            and "prompt" in member
        ):
            teammate_count += 1
    return COLOR_PALETTE[teammate_count % len(COLOR_PALETTE)]


def emit(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=True, indent=2))
