# Claude Code headless reference

## Basic usage

```bash
# Simple prompt (text output)
claude -p "What does the auth module do?"

# JSON output with session metadata
claude -p "Summarize this project" --output-format json

# Pipe content in
cat error.log | claude -p "Explain these errors"

# Extract just the result text
claude -p "Summarize this project" --output-format json | jq -r '.result'
```

## Key flags for headless use

| Flag | Purpose | Example |
|------|---------|---------|
| `-p`, `--print` | Run non-interactively | `claude -p "query"` |
| `--output-format` | `text`, `json`, `stream-json` | `--output-format json` |
| `--json-schema` | Structured output matching a schema | `--json-schema '{"type":"object",...}'` |
| `--allowedTools` | Auto-approve specific tools | `--allowedTools "Read,Edit,Bash"` |
| `--disallowedTools` | Remove tools from context | `--disallowedTools "Edit"` |
| `--tools` | Restrict which tools are available | `--tools "Bash,Edit,Read"` |
| `--model` | Select model (`sonnet`, `opus`, or full name) | `--model sonnet` |
| `--max-turns` | Limit agentic turns | `--max-turns 5` |
| `--max-budget-usd` | Cap API spend | `--max-budget-usd 2.00` |
| `--continue`, `-c` | Continue most recent conversation | `claude -p "..." --continue` |
| `--resume`, `-r` | Resume specific session by ID/name | `--resume "$session_id"` |
| `--append-system-prompt` | Add instructions (keeps defaults) | `--append-system-prompt "Be concise"` |
| `--system-prompt` | Replace entire system prompt | `--system-prompt "You are a reviewer"` |
| `--system-prompt-file` | Replace prompt from file (print mode only) | `--system-prompt-file ./prompt.txt` |
| `--append-system-prompt-file` | Append from file (print mode only) | `--append-system-prompt-file ./rules.txt` |
| `--mcp-config` | Load MCP servers | `--mcp-config ./mcp.json` |
| `--strict-mcp-config` | Only use MCP from `--mcp-config` | `--strict-mcp-config` |
| `--agents` | Define subagents via JSON | See below |
| `--agent` | Use a specific agent | `--agent my-agent` |
| `--dangerously-skip-permissions` | Skip all permission prompts | Use with caution |
| `--fallback-model` | Fallback when primary overloaded | `--fallback-model sonnet` |
| `--add-dir` | Add extra working directories | `--add-dir ../lib ../apps` |
| `--plugin-dir` | Load plugins from directory | `--plugin-dir ./my-plugins` |
| `--verbose` | Show full turn-by-turn output | Useful for debugging |
| `--no-session-persistence` | Don't save session to disk | For ephemeral tasks |
| `--session-id` | Use specific UUID for session | `--session-id "550e8400-..."` |
| `--input-format` | Input format (`text`, `stream-json`) | `--input-format stream-json` |
| `--include-partial-messages` | Include streaming events | Requires `stream-json` |
| `--permission-mode` | Start in specific permission mode | `--permission-mode plan` |

## Structured output with JSON schema

```bash
claude -p "Extract function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
  | jq '.structured_output'
```

## Tool permissions

```bash
# Allow specific tools
claude -p "Run tests and fix failures" --allowedTools "Bash,Read,Edit"

# Allow git commands with prefix matching (space before * is important)
claude -p "Create a commit for staged changes" \
  --allowedTools "Bash(git diff *)" "Bash(git log *)" "Bash(git commit *)"

# Skip all permissions (for trusted automation)
claude -p "Fix the lint errors" --dangerously-skip-permissions
```

## Session continuation

```bash
# Capture session ID for later
session_id=$(claude -p "Start reviewing auth module" --output-format json | jq -r '.session_id')

# Resume that specific session
claude -p "Now check for SQL injection" --resume "$session_id"

# Or just continue the most recent
claude -p "Now check for SQL injection" --continue
```

## Custom subagents via CLI

```bash
claude -p "Review this codebase" --agents '{
  "security-reviewer": {
    "description": "Security expert. Use proactively after code changes.",
    "prompt": "You are a senior security engineer. Focus on OWASP top 10.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

Agent fields: `description` (required), `prompt` (required), `tools` (optional, inherits all), `model` (optional: `sonnet`, `opus`, `haiku`, `inherit`).

## System prompt customization

- `--append-system-prompt` - safest; adds to Claude Code defaults
- `--system-prompt` - replaces everything; use when you need full control
- `--system-prompt-file` / `--append-system-prompt-file` - load from files (print mode only)
- The append flags can be combined with replacement flags

## Streaming

```bash
# Stream tokens as they're generated
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```
