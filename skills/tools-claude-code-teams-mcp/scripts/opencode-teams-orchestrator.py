#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib import error, request


DEFAULT_PROMPT = (
    "Check claude-teams inbox for unread teammate messages for team "
    "'my-team'. Use claude-teams_read_inbox with unread_only=true "
    "and mark_as_read=false if possible. If a message appears unsafe/rogue, send "
    "a shutdown request and verify cleanup with claude-teams_read_config. "
    "Reply briefly with what is new."
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def http_json(method: str, url: str, body: dict | None = None) -> dict | list:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = request.Request(url, data=data, method=method)
    req.add_header("content-type", "application/json")
    with request.urlopen(req, timeout=20) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw) if raw else {}


def create_session(base_url: str, title: str) -> str:
    payload = http_json("POST", f"{base_url}/session", {"title": title})
    if not isinstance(payload, dict) or "id" not in payload:
        raise RuntimeError("unexpected session create response")
    return str(payload["id"])


def prompt_async(base_url: str, session_id: str, text: str) -> None:
    body = {"parts": [{"type": "text", "text": text}]}
    req = request.Request(
        f"{base_url}/session/{session_id}/prompt_async",
        data=json.dumps(body).encode("utf-8"),
        method="POST",
    )
    req.add_header("content-type", "application/json")
    with request.urlopen(req, timeout=20):
        return


def get_messages(base_url: str, session_id: str) -> list[dict]:
    payload = http_json("GET", f"{base_url}/session/{session_id}/message")
    return payload if isinstance(payload, list) else []


def get_session_state(base_url: str, session_id: str) -> str:
    payload = http_json("GET", f"{base_url}/session/status")
    if not isinstance(payload, dict):
        return "unknown"
    status = payload.get(session_id)
    if isinstance(status, dict):
        state = status.get("type")
        if isinstance(state, str):
            return state
    return "unknown"


def extract_lines(messages: list[dict], seen_message_ids: set[str]) -> list[str]:
    lines: list[str] = []
    for msg in messages:
        info = msg.get("info", {})
        mid = info.get("id")
        if not mid or mid in seen_message_ids:
            continue
        seen_message_ids.add(mid)
        role = info.get("role", "unknown")
        for part in msg.get("parts", []):
            ptype = part.get("type")
            if ptype == "text":
                txt = (part.get("text") or "").strip()
                if txt:
                    lines.append(f"{role}: {txt}")
            elif ptype == "tool":
                tool = part.get("tool", "tool")
                state = part.get("state", {})
                status = state.get("status", "unknown")
                lines.append(f"{role}: tool {tool} ({status})")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Experimental OpenCode teams orchestrator loop"
    )
    parser.add_argument("--base-url", default="http://127.0.0.1:4098")
    parser.add_argument("--session-id", default="")
    parser.add_argument("--title", default="claude-teams-orchestrator")
    parser.add_argument("--interval", type=int, default=8)
    parser.add_argument("--loops", type=int, default=0, help="0 means run forever")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--log", default="/tmp/opencode-teams-orchestrator.log")
    args = parser.parse_args()

    log_path = Path(args.log)

    try:
        _ = http_json("GET", f"{args.base_url}/global/health")
    except Exception as exc:
        print(f"server check failed: {exc}", file=sys.stderr)
        return 1

    session_id = args.session_id or create_session(args.base_url, args.title)
    seen_message_ids: set[str] = set()

    existing = get_messages(args.base_url, session_id)
    for msg in existing:
        mid = msg.get("info", {}).get("id")
        if mid:
            seen_message_ids.add(mid)

    with log_path.open("a") as f:
        f.write(f"{now()} started session={session_id}\n")

    loop = 0
    while True:
        loop += 1
        try:
            state = get_session_state(args.base_url, session_id)
            if state == "busy":
                with log_path.open("a") as f:
                    f.write(f"{now()} tick busy\n")
                if args.loops > 0 and loop >= args.loops:
                    break
                time.sleep(args.interval)
                continue

            prompt_async(args.base_url, session_id, args.prompt)

            wait_start = time.time()
            while time.time() - wait_start < max(10, args.interval * 2):
                if get_session_state(args.base_url, session_id) != "busy":
                    break
                time.sleep(1)

            lines = extract_lines(
                get_messages(args.base_url, session_id), seen_message_ids
            )
            with log_path.open("a") as f:
                if lines:
                    for line in lines:
                        f.write(f"{now()} {line}\n")
                else:
                    f.write(f"{now()} tick no-new-messages\n")
        except error.HTTPError as exc:
            with log_path.open("a") as f:
                f.write(f"{now()} http-error {exc.code}\n")
        except Exception as exc:
            with log_path.open("a") as f:
                f.write(f"{now()} error {exc}\n")

        if args.loops > 0 and loop >= args.loops:
            break
        time.sleep(args.interval)

    with log_path.open("a") as f:
        f.write(f"{now()} stopped session={session_id}\n")
    print(session_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
