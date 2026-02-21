---
description: Dispatch a task programmatically via the Claude Agent SDK (Python or TypeScript), or via CLI shorthand
---

# Claude Code dispatch

SDK-first. Use the Claude Agent SDK for full programmatic control. For simple one-off dispatches, use the CLI shorthand at the bottom.

## Two APIs — pick the right one

- `query()`: fire-and-forget. Each call creates a new session, returns `AsyncIterator[Message]`. Use for one-off tasks where you don't need follow-ups.
- `ClaudeSDKClient`: persistent session. Supports multi-turn conversations, interrupts, hooks, and custom tools. Use for interactive dispatch, loops, and follow-ups.

## Process

- Pick API: `query()` for one-off, `ClaudeSDKClient` for interactive/multi-turn
- Pick model: `haiku` for cheap tasks, `sonnet` for quality, `opus` for max quality
- Pass plugins: `plugins=[{"type": "local", "path": "/path/to/plugin"}]` to load a plugin's skills
  - Or `system_prompt` (string or preset with `append`) to inject raw instructions
  - Or just write a clear prompt
- Set `allowed_tools`: only list tools that need approval (Bash, Write, Edit, WebFetch)
  - Read-only tools (Read, Glob, Grep) are auto-allowed
- Set `max_turns` as a safety cap
- For `query()`: iterate the async message stream, check for `ResultMessage`
- For `ClaudeSDKClient`: call `query()` then `receive_response()`, use `isinstance()` checks on messages

## Message handling

Messages are typed dataclasses. Use `isinstance()` checks, not `hasattr()`:

```python
from claude_agent_sdk import (
    AssistantMessage, TextBlock, ToolUseBlock, ResultMessage, SystemMessage,
)

# Inside your message loop:
if isinstance(message, AssistantMessage):
    for block in message.content:
        if isinstance(block, TextBlock):
            print(block.text, end="", flush=True)
        elif isinstance(block, ToolUseBlock):
            print(f"  [tool] {block.name}")
elif isinstance(message, ResultMessage):
    print(f"\nResult: {message.result}")
    print(f"Session: {message.session_id}")
    print(f"Cost: ${message.total_cost_usd}")
elif isinstance(message, SystemMessage) and message.subtype == "init":
    session_id = message.data.get("session_id")
```

## Common patterns

### Python — fire-and-forget with `query()`

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def main():
    async for message in query(
        prompt="Use the web-fetch skill to download https://example.com/article and save to ./article.md",
        options=ClaudeAgentOptions(
            allowed_tools=["Bash", "Write", "WebFetch"],
            max_turns=10,
            plugins=[{"type": "local", "path": "/path/to/plugins/web-research"}],
        )
    ):
        if isinstance(message, ResultMessage):
            print(message.result)

asyncio.run(main())
```

### Python — interactive multi-turn with `ClaudeSDKClient`

```python
import asyncio
from claude_agent_sdk import (
    ClaudeSDKClient, ClaudeAgentOptions,
    AssistantMessage, TextBlock, ToolUseBlock, ResultMessage,
)

async def main():
    options = ClaudeAgentOptions(
        model="sonnet",
        max_turns=15,
        allowed_tools=["Bash", "Write", "Edit", "WebFetch"],
        cwd="/path/to/project",
    )

    async with ClaudeSDKClient(options=options) as client:
        # First task
        await client.query("Add input validation to the /users POST endpoint")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text, end="", flush=True)
                    elif isinstance(block, ToolUseBlock):
                        print(f"  [tool] {block.name}")
            elif isinstance(message, ResultMessage):
                print(f"\nDone: {message.result}")

        # Follow-up — agent remembers full context
        await client.query("Now add tests for the validation you just wrote")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text, end="", flush=True)

asyncio.run(main())
```

### Python — sandboxed autonomous agent

For code-writing tasks in isolated directories (e.g., worktrees):

```python
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async for message in query(
    prompt="Make the changes described below. ...",
    options=ClaudeAgentOptions(
        model="haiku",
        max_turns=15,
        permission_mode="acceptEdits",
        plugins=[{"type": "local", "path": "/path/to/plugin"}],
        cwd="/path/to/worktree",
    )
):
    if isinstance(message, ResultMessage):
        print(message.result)
```

### TypeScript — basic dispatch

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Use the web-fetch skill to download https://example.com/article and save to ./article.md",
  options: {
    allowedTools: ["Bash", "Write", "WebFetch"],
    maxTurns: 10,
    plugins: [{ type: "local", path: "/path/to/plugins/web-research" }],
  }
})) {
  if ("result" in message) console.log(message.result);
}
```

## CLI shorthand

For simple fire-and-forget dispatches, `claude -p` avoids writing a script:

```bash
# Basic dispatch
claude -p "Summarize the auth module" \
  --model haiku \
  --output-format json | jq -r '.result'

# With a plugin skill
claude -p "Use the web-fetch skill to download https://example.com/article and save to ./article.md" \
  --model haiku \
  --plugin-dir /path/to/plugins/web-research \
  --allowedTools "Bash" "Write" "WebFetch" \
  --max-turns 10 \
  --output-format json | jq -r '.result'
```

Session continuation: `--continue` (last session) or `--resume <session_id>` (specific session).

Use prefix matching for tool permissions: `"Bash(git diff *)"` (space before `*` matters).

## Lookups

- Full SDK options table, prerequisites: `references/claude-sdk-options.md`
- Full CLI flag table (28 flags): `references/claude-code-flags.md`
- Models and costs: `references/providers-models.md`
- Upstream doc URLs: `references/sources.md`
