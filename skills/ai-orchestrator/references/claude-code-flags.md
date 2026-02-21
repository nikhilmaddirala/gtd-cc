---
description: Claude Code headless CLI flag reference, system prompt options, observability, and prompting tips
---

# Claude Code headless reference

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
| `--agents` | Define subagents via JSON | See subagents pattern below |
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

## Tool permissions

```bash
# Allow specific tools
claude -p "Run tests and fix failures" --allowedTools "Bash,Read,Edit"

# Prefix matching (space before * is important)
claude -p "Create a commit" \
  --allowedTools "Bash(git diff *)" "Bash(git log *)" "Bash(git commit *)"

# Skip all permissions (trusted automation only)
claude -p "Fix the lint errors" --dangerously-skip-permissions
```

## Path-scoped tool permissions

```bash
WORKTREE="/path/to/worktree"
claude -p "Make changes to the project" \
  -d "$WORKTREE" \
  --allowedTools \
    "Edit($WORKTREE/**)" \
    "Write($WORKTREE/**)" \
    "Read" "Glob" "Grep" \
  --max-turns 15
```

Known issues:
- Path-scoped `--allowedTools` with `Edit($PATH/**)` may cause agents to ask for confirmation rather than auto-allowing in headless mode (model-dependent, observed with haiku)
- Cannot combine with `--dangerously-skip-permissions` (skip-permissions overrides allowedTools)

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

## Structured output

```bash
claude -p "Extract function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
  | jq '.structured_output'
```

## Session continuation

```bash
# Capture session ID
session_id=$(claude -p "Start reviewing auth module" --output-format json | jq -r '.session_id')

# Resume with more instructions
claude -p "Now check for SQL injection" --resume "$session_id"

# Or continue the most recent session
claude -p "Now check for SQL injection" --continue
```

## Streaming

```bash
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

## Headless vs Task tool agents

- **Task tool (subagent)**: runs inside the parent session. Cannot prompt for permissions — only tools in `.claude/settings.json` `permissions.allow` work. Background Task agents can only do read-only research.
- **`claude -p` (headless CLI)**: separate process with its own permissions. Full write access via `--dangerously-skip-permissions` or `--allowedTools`. Use this when the agent needs to modify files.

## Observability and debugging

- Always use `--verbose` when developing/debugging — shows full turn-by-turn tool calls
- `--output-format text` (default) only shows the final message
- `--output-format stream-json` with `--verbose` gives full structured logs
- Common failure causes when agent "completes" without changes:
  - Agent asked for confirmation it couldn't get (headless + insufficient permissions)
  - Agent hallucinated success without calling tools
  - Agent hit max turns retrying permission errors

## Prompting for reliable headless execution

- Give explicit absolute paths to every file that needs editing
- Give exact code blocks to insert/replace
- Include a verification step in the prompt (e.g., "after editing, run grep -n to verify")
- Say "do not ask for confirmation" if the agent tends to be overly cautious
- Avoid vague instructions like "model after X" — show exactly what the result should look like
