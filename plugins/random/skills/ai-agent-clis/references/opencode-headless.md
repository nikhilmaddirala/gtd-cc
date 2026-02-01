# Opencode headless reference

## Basic usage

```bash
# Simple prompt
opencode run "Explain how closures work in JavaScript"

# With model selection (provider/model format)
opencode run -m anthropic/claude-sonnet-4-5-20250929 "Review this code"

# Continue a session
opencode run --continue "Now fix the issues you found"

# JSON output
opencode run --format json "Summarize the project"

# Attach a file
opencode run -f ./error.log "Explain these errors"
```

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

## Persistent server pattern

Opencode supports a server mode that avoids MCP cold boot on every run:

```bash
# Terminal 1: start headless server
opencode serve --port 4096

# Terminal 2+: run commands against it (instant MCP access)
opencode run --attach http://localhost:4096 "Explain async/await"
opencode run --attach http://localhost:4096 "Now show me an example"
```

Serve flags: `--port`, `--hostname`, `--mdns`, `--cors`

Set `OPENCODE_SERVER_PASSWORD` to enable HTTP basic auth.

## Other useful commands

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

## Key environment variables

| Variable | Purpose |
|----------|---------|
| `OPENCODE_DISABLE_CLAUDE_CODE` | Disable reading `.claude/` (prompt + skills) |
| `OPENCODE_DISABLE_CLAUDE_CODE_PROMPT` | Disable reading `~/.claude/CLAUDE.md` |
| `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS` | Disable loading `.claude/skills` |
| `OPENCODE_SERVER_PASSWORD` | Enable basic auth for serve/web |
| `OPENCODE_CONFIG` | Path to config file |
| `OPENCODE_CONFIG_CONTENT` | Inline JSON config |
| `OPENCODE_PERMISSION` | Inline JSON permissions config |

## Global flags

`--help`, `--version`, `--print-logs`, `--log-level` (DEBUG, INFO, WARN, ERROR)

For full documentation, see `references/opencode-docs/`.
