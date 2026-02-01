---
description: Dispatch a task to a headless Opencode instance via `opencode run`
---

# Opencode headless

## Process

- Determine the model using `provider/model` format:
  - Free models: `opencode/gpt-5-nano`, `opencode/glm-4.7-free`, `opencode/kimi-k2.5-free`
  - Paid models depend on authenticated providers (run `opencode models` to list)
  - Read `references/providers-models.md` for available models
- Determine how skills are loaded:
  - Opencode auto-discovers skills from `.claude/skills/` and `.opencode/skills/`
  - If the skill lives elsewhere, symlink it into a discovery root:
    - Project: `ln -s /path/to/skill .claude/skills/<name>`
    - Global: `ln -s /path/to/skill ~/.config/opencode/skills/<name>`
  - To disable Claude Code skill loading: `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=true`
- Opencode has no `--allowedTools` or `--max-budget-usd` — control costs via model selection
- Use `--format json` for machine-readable output
- Put context (target paths, URLs, instructions) in the prompt itself
- Run the command and check the result
- If incomplete: use `--continue` (last session) or `--session <id>` (specific session)
- For repeated runs: use the serve/attach pattern to avoid MCP cold boot

## Patterns

### Basic dispatch

```bash
opencode run "Explain the auth module" \
  --model opencode/gpt-5-nano
```

### With model selection

```bash
# Free model for simple tasks
opencode run "Summarize this file" --model opencode/gpt-5-nano

# Paid model for quality tasks (requires authenticated provider)
opencode run "Review this codebase for security issues" --model openai/gpt-5.2-codex
```

### Attaching files

```bash
opencode run -f ./error.log "Explain these errors"
```

### Session continuation

```bash
# Continue the last session
opencode run --continue "Now fix the issues you found"

# Continue a specific session
opencode run --session "$SESSION_ID" "Focus on the auth module"
```

### Serve/attach pattern (avoid MCP cold boot)

```bash
# Start server once
opencode serve --port 4096 &
sleep 3

# Run tasks against it (instant MCP access)
opencode run --attach http://localhost:4096 "First task"
opencode run --attach http://localhost:4096 "Second task"

kill %1  # stop server
```

### With authentication

```bash
OPENCODE_SERVER_PASSWORD=secret opencode serve --port 4096 &
sleep 3
opencode run --attach http://opencode:secret@localhost:4096 "Task here"
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

Serve flags: `--port`, `--hostname`, `--mdns`, `--cors`

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

Global flags: `--help`, `--version`, `--print-logs`, `--log-level` (DEBUG, INFO, WARN, ERROR)

## Full reference

For upstream docs: `developer-docs/opencode-docs/`.
