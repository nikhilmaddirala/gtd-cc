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

### Sandboxed autonomous agents (recommended for code-writing tasks)

When dispatching an agent to write code in a specific directory (e.g., a git worktree), combine `--dangerously-skip-permissions` with sandbox to get full autonomy within safe boundaries.

```bash
# 1. Create a .claude/settings.json in the target directory with sandbox enabled
TARGET="/path/to/worktree"
mkdir -p "$TARGET/.claude"
cat > "$TARGET/.claude/settings.json" << 'EOF'
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "allowUnsandboxedCommands": false
  }
}
EOF

# 2. Run with skip-permissions — sandbox restricts Bash to cwd
claude -p "Make the changes described below. Use absolute paths starting with $TARGET for all edits. ..." \
  -d "$TARGET" \
  --dangerously-skip-permissions \
  --model haiku \
  --verbose \
  --max-turns 15
```

How this works:
- `--dangerously-skip-permissions` — no permission prompts, agent acts immediately
- Sandbox `enabled: true` — OS-level restriction (macOS Seatbelt / Linux bubblewrap) confines Bash to the cwd and subdirectories
- `allowUnsandboxedCommands: false` — prevents the agent from escaping the sandbox via `dangerouslyDisableSandbox` on Bash calls
- `-d $TARGET` — sets cwd so the sandbox boundary is the target directory

Limitations:
- The sandbox only restricts **Bash** at the OS level. `Edit` and `Write` tools are not sandboxed — they can write anywhere when `--dangerously-skip-permissions` is active
- To restrict `Edit`/`Write`, you must give explicit absolute paths in the prompt. The agent will follow your instructions but there's no OS-level enforcement
- If strict `Edit`/`Write` isolation is needed, use path-scoped `--allowedTools` (see below) but note the compatibility issues with headless mode

### Path-scoped tool permissions (alternative approach)

Use path specifiers on `Edit` and `Write` in `--allowedTools` for tool-level write restrictions. This restricts both Bash-based and native tool writes.

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
- **Headless compatibility**: in testing, path-scoped `--allowedTools` with `Edit($PATH/**)` caused agents to ask for confirmation rather than auto-allowing — which stalls headless mode since there's no user to approve. This may be model-dependent (observed with haiku)
- **Cannot combine with `--dangerously-skip-permissions`**: skip-permissions overrides allowedTools, so the path restriction is ignored
- `-d` sets the working directory but does not restrict file access — the agent can still read and write anywhere via absolute paths
- When spawning agents in worktrees or subdirectories, the agent may follow CLAUDE.md references or relative paths that resolve outside the intended directory

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

## Headless vs Task tool agents

When dispatching work from within a Claude Code session, there are two approaches:

- **Task tool (subagent)**: runs inside the parent session. Cannot prompt for permissions — only tools pre-allowed in `.claude/settings.json` `permissions.allow` work. Edit/Write/Bash are typically not in the allow list, so background Task agents can only do read-only research. Foreground Task agents share the interactive prompt but block the parent.
- **`claude -p` (headless CLI)**: runs as a separate process with its own permissions. Full write access via `--dangerously-skip-permissions` or `--allowedTools`. Use this when the agent needs to write code.

Prefer `claude -p` over the Task tool for any agent that needs to modify files.

## Observability and debugging

- Always use `--verbose` when developing/debugging agent dispatch — it shows full turn-by-turn tool calls and results
- `--output-format text` (default) only shows the final message — you can't see what the agent did or why it failed
- `--output-format stream-json` with `--verbose` gives full structured logs for background tasks
- When an agent "completes" but didn't actually make changes, check the verbose output — common causes:
  - Agent asked for confirmation it couldn't get (headless mode + insufficient permissions)
  - Agent hallucinated success without calling tools
  - Agent hit max turns retrying permission errors

## Prompting for reliable headless execution

Headless agents can't ask clarifying questions, so the prompt must be unambiguous:

- Give **explicit absolute paths** to every file that needs editing — don't rely on the agent discovering them
- Give **exact code blocks** to insert/replace — don't make the agent figure out the content
- Include a **verification step** in the prompt (e.g., "after editing, run grep -n to verify")
- Say "do not ask for confirmation" if the agent tends to be overly cautious
- Avoid vague instructions like "model after X" — instead, show exactly what the result should look like

## Full reference

For upstream docs: `developer-docs/claude-code-docs/`.
