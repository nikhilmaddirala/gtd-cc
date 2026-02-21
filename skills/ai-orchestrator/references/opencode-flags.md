---
description: Opencode CLI flags, environment variables, and useful commands
---

# Opencode CLI reference

## Run flags

| Flag | Short | Purpose |
|------|-------|---------|
| `--model` | `-m` | Model in `provider/model` format |
| `--continue` | `-c` | Continue last session |
| `--session` | `-s` | Continue specific session ID |
| `--format` | | `default` or `json` |
| `--file` | `-f` | Attach file(s) to message |
| `--agent` | | Use a specific agent |
| `--attach` | | Connect to running `opencode serve` instance |
| `--share` | | Share the session |
| `--title` | | Title for the session |
| `--command` | | Command to run, use message for args |
| `--port` | | Port for local server |

## Serve flags

`--port`, `--hostname`, `--mdns`, `--cors`

## Environment variables

| Variable | Purpose |
|----------|---------|
| `OPENCODE_DISABLE_CLAUDE_CODE` | Disable reading `.claude/` (prompt + skills) |
| `OPENCODE_DISABLE_CLAUDE_CODE_PROMPT` | Disable reading `~/.claude/CLAUDE.md` |
| `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS` | Disable loading `.claude/skills` |
| `OPENCODE_SERVER_PASSWORD` | Enable basic auth for serve/web |
| `OPENCODE_CONFIG` | Path to config file |
| `OPENCODE_CONFIG_CONTENT` | Inline JSON config |
| `OPENCODE_PERMISSION` | Inline JSON permissions config |

Global flags: `--help`, `--version`, `--print-logs`, `--log-level` (DEBUG, INFO, WARN, ERROR)

## Useful commands

```bash
# List available models (check for free tier)
opencode models
opencode models --verbose  # includes cost info

# Check usage stats
opencode stats --days 7

# Session management
opencode session list
opencode session list --format json

# Export/import sessions
opencode export <sessionID>
opencode import session.json
```

## Authentication

Stored in `~/.local/share/opencode/auth.json`. For serve mode with auth:

```bash
OPENCODE_SERVER_PASSWORD=secret opencode serve --port 4096 &
sleep 3
opencode run --attach http://opencode:secret@localhost:4096 "Task here"
```
