#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
TEMPLATE_FILE="$ROOT_DIR/templates/teammate-bootstrap.md"

TEAM=""
NAME=""
PROMPT=""
BACKEND="opencode"
MODEL="opencode/gpt-5-nano"
AGENT_TYPE="build"
CWD="$(pwd)"
PLAN_MODE=false
OPENCODE_SERVER_URL="${OPENCODE_SERVER_URL:-http://127.0.0.1:4098}"
RUNTIME_MODE="${OPENCODE_TEAMMATE_RUNTIME:-headless}"
TARGET_PANE=""
TARGET_WINDOW=""
RESOLVED_TARGET_PANE=""
RESOLVED_TARGET_WINDOW=""

usage() {
  cat <<EOF
Usage:
  $0 --team <name> --name <agent> --prompt <text> [options]

Options:
  --backend <opencode>           Default: opencode
  --model <model>                Default: opencode/gpt-5-nano
  --agent-type <type>            Default: build
  --cwd <path>                   Default: current directory
  --plan-mode-required           Set plan mode flag in config
  --server-url <url>             Default: OPENCODE_SERVER_URL or http://127.0.0.1:4098
  --runtime <headless|tui>       Default: OPENCODE_TEAMMATE_RUNTIME or headless
  --target-pane <pane-id>        Split a specific pane (example: %12)
  --target-window <window-id>    Split inside specific window (example: @3)
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --team)
      TEAM="$2"
      shift 2
      ;;
    --name)
      NAME="$2"
      shift 2
      ;;
    --prompt)
      PROMPT="$2"
      shift 2
      ;;
    --backend)
      BACKEND="$2"
      shift 2
      ;;
    --server-url)
      OPENCODE_SERVER_URL="$2"
      shift 2
      ;;
    --runtime)
      RUNTIME_MODE="$2"
      shift 2
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    --agent-type)
      AGENT_TYPE="$2"
      shift 2
      ;;
    --cwd)
      CWD="$2"
      shift 2
      ;;
    --plan-mode-required)
      PLAN_MODE=true
      shift
      ;;
    --target-pane)
      TARGET_PANE="$2"
      shift 2
      ;;
    --target-window)
      TARGET_WINDOW="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$TEAM" || -z "$NAME" || -z "$PROMPT" ]]; then
  echo "Missing required arguments" >&2
  usage
  exit 1
fi

if [[ "$BACKEND" != "opencode" ]]; then
  echo "Unsupported backend: $BACKEND (opencode only)" >&2
  exit 1
fi

if [[ -n "$TARGET_PANE" && -n "$TARGET_WINDOW" ]]; then
  echo "Use only one of --target-pane or --target-window" >&2
  exit 1
fi

if [[ "$RUNTIME_MODE" != "headless" && "$RUNTIME_MODE" != "tui" ]]; then
  echo "Unsupported runtime: $RUNTIME_MODE (use headless or tui)" >&2
  exit 1
fi

if [[ "$RUNTIME_MODE" == "headless" && ( -n "$TARGET_PANE" || -n "$TARGET_WINDOW" ) ]]; then
  echo "--target-pane/--target-window are only valid with --runtime tui" >&2
  exit 1
fi

if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo "Missing template file: $TEMPLATE_FILE" >&2
  exit 1
fi

WRAPPED_PROMPT=$(python3 - <<PY
from pathlib import Path
template = Path(r"$TEMPLATE_FILE").read_text(encoding="utf-8")
print(template.replace("{{TEAM_NAME}}", r"$TEAM").replace("{{AGENT_NAME}}", r"$NAME").replace("{{PROMPT}}", r"$PROMPT"))
PY
)

PLAN_FLAG=()
if [[ "$PLAN_MODE" == "true" ]]; then
  PLAN_FLAG=(--plan-mode-required)
fi

if ! command -v opencode >/dev/null 2>&1; then
  echo "Missing binary on PATH: opencode" >&2
  exit 1
fi

if [[ "$RUNTIME_MODE" == "tui" ]]; then
  if ! command -v tmux >/dev/null 2>&1; then
    echo "Missing binary on PATH: tmux" >&2
    exit 1
  fi
fi

SESSION_ID=$(PYTHONPATH="$SCRIPT_DIR" OPENCODE_SERVER_URL="$OPENCODE_SERVER_URL" TEAM="$TEAM" NAME="$NAME" python3 - <<'PY'
import os
from opencode_api import OpenCodeAPIError, create_session, health
try:
    health()
    sid = create_session(f"{os.environ['NAME']}@{os.environ['TEAM']}")
except OpenCodeAPIError as exc:
    raise SystemExit(str(exc))
print(sid)
PY
)

"$SCRIPT_DIR/team.py" add-member \
  --team "$TEAM" \
  --name "$NAME" \
  --prompt "$PROMPT" \
  --model "$MODEL" \
  --agent-type "$AGENT_TYPE" \
  --backend-type "$BACKEND" \
  --opencode-session-id "$SESSION_ID" \
  --cwd "$CWD" \
  "${PLAN_FLAG[@]}" >/dev/null

"$SCRIPT_DIR/inbox.py" ensure --team "$TEAM" --agent "$NAME" >/dev/null
BOOTSTRAP_FILE="$(mktemp)"
"$SCRIPT_DIR/inbox.py" send \
  --team "$TEAM" \
  --from-name team-lead \
  --to "$NAME" \
  --summary bootstrap \
  --text "$WRAPPED_PROMPT" > "$BOOTSTRAP_FILE"

BOOTSTRAP_PUSHED=$(BOOTSTRAP_FILE="$BOOTSTRAP_FILE" python3 - <<'PY'
import json
import os
from pathlib import Path
payload = json.loads(Path(os.environ['BOOTSTRAP_FILE']).read_text())
print('true' if payload.get('pushed_to_session') else 'false')
PY
)
rm -f "$BOOTSTRAP_FILE"

if [[ "$RUNTIME_MODE" == "tui" && -z "$TARGET_PANE" && -z "$TARGET_WINDOW" ]]; then
  read -r RESOLVED_TARGET_PANE RESOLVED_TARGET_WINDOW <<<"$(PYTHONPATH="$SCRIPT_DIR" TEAM="$TEAM" python3 - <<'PY'
import os
import subprocess
from common import load_config

cfg = load_config(os.environ["TEAM"])
lead_pane = (cfg.get("leadPaneId") or "").strip()
lead_window = (cfg.get("leadWindowId") or "").strip()

def run(args):
    return subprocess.run(args, check=False, capture_output=True, text=True)

def has_target(kind: str, target: str) -> bool:
    if not target:
        return False
    if kind == "pane":
        proc = run(["tmux", "list-panes", "-a", "-F", "#{pane_id}"])
    else:
        proc = run(["tmux", "list-windows", "-F", "#{window_id}"])
    if proc.returncode != 0:
        return False
    return target in {line.strip() for line in proc.stdout.splitlines()}

resolved_pane = ""
resolved_window = ""
if has_target("pane", lead_pane):
    proc = run(["tmux", "display-message", "-p", "-t", lead_pane, "#{window_id}"])
    if proc.returncode == 0:
        resolved_pane = lead_pane
        resolved_window = proc.stdout.strip()

if not resolved_window and has_target("window", lead_window):
    resolved_window = lead_window

print(f"{resolved_pane} {resolved_window}".strip())
PY
)"
  if [[ -z "$RESOLVED_TARGET_PANE" && -z "$RESOLVED_TARGET_WINDOW" ]]; then
    echo "Could not resolve anchored lead tmux window for team $TEAM." >&2
    echo "Run team.py set-anchor --team $TEAM --window-id @<window> --pane-id %<pane>." >&2
    exit 1
  fi
fi

if [[ "$RUNTIME_MODE" == "tui" && -n "$TARGET_PANE" ]]; then
  RESOLVED_TARGET_PANE="$TARGET_PANE"
fi
if [[ "$RUNTIME_MODE" == "tui" && -n "$TARGET_WINDOW" ]]; then
  RESOLVED_TARGET_WINDOW="$TARGET_WINDOW"
fi

if [[ "$RUNTIME_MODE" == "tui" && -n "$RESOLVED_TARGET_PANE" ]]; then
  if ! tmux display-message -p -t "$RESOLVED_TARGET_PANE" '#{pane_id}' >/dev/null 2>&1; then
    echo "Could not resolve target pane $RESOLVED_TARGET_PANE for team $TEAM." >&2
    exit 1
  fi
fi

if [[ "$RUNTIME_MODE" == "tui" && -n "$RESOLVED_TARGET_WINDOW" ]]; then
  if ! tmux display-message -p -t "$RESOLVED_TARGET_WINDOW" '#{window_id}' >/dev/null 2>&1; then
    echo "Could not resolve anchored lead tmux window for team $TEAM." >&2
    echo "Run team.py set-anchor --team $TEAM --window-id @<window> --pane-id %<pane>." >&2
    exit 1
  fi
fi

EXTRA_ENV=$(PYTHONPATH="$SCRIPT_DIR" TEAM="$TEAM" python3 - <<'PY'
import os
import re
import shlex
from pathlib import Path
from common import load_config

cfg = load_config(os.environ["TEAM"])
lead_env = cfg.get("leadEnv") if isinstance(cfg, dict) else None
if not isinstance(lead_env, dict):
    lead_env = {}

def pick(key: str) -> str:
    value = lead_env.get(key)
    if isinstance(value, str) and value.strip():
        return value.strip()
    value = os.environ.get(key, "")
    return value.strip() if isinstance(value, str) else ""

home = pick("HOME") or str(Path.home())
xdg_config_home = pick("XDG_CONFIG_HOME") or str(Path(home) / ".config")
opencode_config = pick("OPENCODE_CONFIG")
if not opencode_config:
    fallback = Path(xdg_config_home) / "opencode" / "opencode.jsonc"
    if fallback.exists():
        opencode_config = str(fallback)

opencode_theme = pick("OPENCODE_THEME")
if not opencode_theme and opencode_config:
    try:
        text = Path(opencode_config).read_text(encoding="utf-8", errors="ignore")
        match = re.search(r'"theme"\s*:\s*"([^"]+)"', text)
        if match and match.group(1).strip():
            opencode_theme = match.group(1).strip()
    except Exception:
        pass

resolved = {
    "HOME": home,
    "XDG_CONFIG_HOME": xdg_config_home,
    "OPENCODE_CONFIG": opencode_config,
    "OPENCODE_THEME": opencode_theme,
    "COLORTERM": pick("COLORTERM"),
    "TERM": pick("TERM"),
}

if opencode_theme:
    resolved["OPENCODE_CONFIG_CONTENT"] = '{"theme":"' + opencode_theme.replace('"', '\\"') + '"}'

env_pairs = [
    f"{key}={shlex.quote(value)}"
    for key, value in resolved.items()
    if isinstance(value, str) and value.strip()
]

print(" ".join(env_pairs))
PY
)

SPAWN_CMD="$EXTRA_ENV OPENCODE_TEAM_ROLE=teammate OPENCODE_TEAM_TEAM=$(printf '%q' "$TEAM") OPENCODE_TEAM_MEMBER=$(printf '%q' "$NAME") opencode attach $(printf '%q' "$OPENCODE_SERVER_URL") -s $(printf '%q' "$SESSION_ID") --dir $(printf '%q' "$CWD")"
PANE_ID=""

if [[ "$RUNTIME_MODE" == "tui" ]]; then
  if [[ -n "$RESOLVED_TARGET_PANE" ]]; then
    PANE_ID=$(tmux split-window -dP -t "$RESOLVED_TARGET_PANE" -F '#{pane_id}')
  elif [[ -n "$RESOLVED_TARGET_WINDOW" ]]; then
    PANE_ID=$(tmux split-window -dP -t "$RESOLVED_TARGET_WINDOW" -F '#{pane_id}')
  elif [[ -n "${USE_TMUX_WINDOWS:-}" ]]; then
    PANE_ID=$(tmux new-window -dP -F '#{pane_id}' -n "@opencode-teammate | $NAME")
  else
    PANE_ID=$(tmux split-window -dP -F '#{pane_id}')
  fi

  tmux set-option -pt "$PANE_ID" allow-passthrough off >/dev/null 2>&1 || true
  tmux send-keys -t "$PANE_ID" "$SPAWN_CMD" C-m
fi

"$SCRIPT_DIR/team.py" set-runtime \
  --team "$TEAM" \
  --name "$NAME" \
  --tmux-pane-id "$PANE_ID" \
  --is-active >/dev/null

TEAM="$TEAM" NAME="$NAME" BACKEND="$BACKEND" RUNTIME_MODE="$RUNTIME_MODE" OPENCODE_SERVER_URL="$OPENCODE_SERVER_URL" SESSION_ID="$SESSION_ID" PANE_ID="$PANE_ID" BOOTSTRAP_PUSHED="$BOOTSTRAP_PUSHED" python3 - <<'PY'
import os
import json
flag = os.environ.get("BOOTSTRAP_PUSHED", "false").lower() == "true"
runtime = os.environ.get("RUNTIME_MODE", "headless")
print(json.dumps({
    "success": True,
    "team": os.environ["TEAM"],
    "name": os.environ["NAME"],
    "backend": os.environ["BACKEND"],
    "runtime": runtime,
    "opencodeServerUrl": os.environ["OPENCODE_SERVER_URL"],
    "opencodeSessionId": os.environ["SESSION_ID"],
    "tmuxPaneId": os.environ["PANE_ID"],
    "headless": runtime == "headless",
    "bootstrapPushedToSession": flag
}, ensure_ascii=True, indent=2))
PY
