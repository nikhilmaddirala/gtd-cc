---
description: Dispatch a task to a headless Claude Code instance via `claude -p`
---

# Claude Code headless

## Process

- Determine the model: `--model haiku` for cheap tasks, `sonnet` for quality, `opus` for max quality
- Determine how to pass the skill/prompt:
  - If a plugin skill is needed: `--plugin-dir /path/to/plugin`
  - If raw instructions are needed: `--append-system-prompt "..."` or `--append-system-prompt-file`
  - If no skill is needed: just write a clear prompt
- Determine which tools need permission approval via `--allowedTools`:
  - Read-only tools (Read, Glob, Grep) are auto-allowed — don't list them
  - Tools that modify state need explicit approval: `Bash`, `Write`, `Edit`, `WebFetch`
  - Use prefix matching for scoped commands: `"Bash(git diff *)"` (space before `*` is important)
- Set safety caps: `--max-turns` and `--max-budget-usd`
- Put context (target paths, URLs, instructions) in the prompt itself
- Use `--output-format json` when you need to parse the result with `jq`
- Run the command and check the result
- If incomplete: use `--continue` (last session) or `--resume <session_id>` (specific session)

## Patterns

### Basic dispatch

```bash
claude -p "Summarize the auth module" \
  --model haiku \
  --output-format json | jq -r '.result'
```

### Piping content in

```bash
cat error.log | claude -p "Explain these errors"
```

### Dispatch with a plugin skill

```bash
claude -p "Use the web-fetch skill to download https://example.com/article and save to ./article.md" \
  --model haiku \
  --plugin-dir /path/to/plugins/web-research \
  --allowedTools "Bash" "Write" "WebFetch" \
  --max-turns 10 \
  --output-format json | jq -r '.result'
```

### Session continuation

```bash
# Capture session ID
session_id=$(claude -p "Start reviewing auth module" --output-format json | jq -r '.session_id')

# Resume with more instructions
claude -p "Now check for SQL injection" --resume "$session_id"

# Or continue the most recent session
claude -p "Now check for SQL injection" --continue
```

### Structured output

```bash
claude -p "Extract function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
  | jq '.structured_output'
```

### Tool permissions

```bash
# Allow specific tools
claude -p "Run tests and fix failures" --allowedTools "Bash,Read,Edit"

# Allow git commands with prefix matching (space before * is important)
claude -p "Create a commit for staged changes" \
  --allowedTools "Bash(git diff *)" "Bash(git log *)" "Bash(git commit *)"

# Skip all permissions (for trusted automation)
claude -p "Fix the lint errors" --dangerously-skip-permissions
```

### Custom subagents via CLI

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

### Streaming

```bash
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

## Flag reference

| Flag | Purpose | Example |
|------|---------|---------|
| `-p`, `--print` | Run non-interactively | `claude -p "query"` |
| `--output-format` | `text`, `json`, `stream-json` | `--output-format json` |
| `--json-schema` | Structured output matching a schema | `--json-schema '{"type":"object",...}'` |
| `--allowedTools` | Auto-approve specific tools | `--allowedTools "Read,Edit,Bash"` |
| `--disallowedTools` | Remove tools from context | `--disallowedTools "Edit"` |
| `--tools` | Restrict which tools are available | `--tools "Bash,Edit,Read"` |
| `--model` | Select model (`haiku`, `sonnet`, `opus`, or full name) | `--model sonnet` |
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
| `--agents` | Define subagents via JSON | See subagents pattern |
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

## System prompt customization

- `--append-system-prompt` — safest; adds to Claude Code defaults
- `--system-prompt` — replaces everything; use when you need full control
- `--system-prompt-file` / `--append-system-prompt-file` — load from files (print mode only)
- The append flags can be combined with replacement flags

## Full reference

For upstream docs: `developer-docs/claude-code-docs/`.
