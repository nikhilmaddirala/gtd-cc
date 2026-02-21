---
description: Claude Agent SDK key options, prerequisites, and additional patterns
---

# Claude Agent SDK reference

## Two APIs

| Feature | `query()` | `ClaudeSDKClient` |
|---------|-----------|-------------------|
| Session | New session each call | Persistent session |
| Multi-turn | No (single exchange) | Yes (multiple `query()` + `receive_response()`) |
| Interrupts | No | Yes (`interrupt()`) |
| Hooks | No | Yes |
| Custom tools | No | Yes |
| Use case | Fire-and-forget one-off tasks | Interactive conversations, loops, follow-ups |

## Key options (`ClaudeAgentOptions`)

| Option | Python | TypeScript | Purpose |
|--------|--------|-----------|---------|
| Tools | `allowed_tools` | `allowedTools` | Tools that execute without permission prompts |
| Turn limit | `max_turns` | `maxTurns` | Limit agent loop iterations |
| Plugins | `plugins` | `plugins` | Load plugins from local paths: `[{"type": "local", "path": "..."}]` |
| Permissions | `permission_mode` | `permissionMode` | Control permission behavior |
| MCP | `mcp_servers` | `mcpServers` | Configure MCP servers |
| Hooks | `hooks` | `hooks` | Event-driven callbacks (PreToolUse, PostToolUse, Stop, etc.) |
| Agents | `agents` | `agents` | Define subagents with custom prompts and tools |
| Settings | `setting_sources` | `settingSources` | Which filesystem settings to load (`"user"`, `"project"`, `"local"`) |
| Resume | `resume` | `resume` | Session ID to resume a previous conversation |
| Budget | `max_budget_usd` | `maxBudgetUsd` | Maximum cost cap in USD |
| Model | `model` | `model` | Claude model alias (`haiku`, `sonnet`, `opus`) or full model name |
| CWD | `cwd` | `cwd` | Working directory for the agent |

## Message types

| Type | When it appears | Key fields |
|------|----------------|------------|
| `SystemMessage` | Start of session (`subtype == "init"`) | `data` dict with `session_id`, `plugins`, `slash_commands` |
| `AssistantMessage` | Agent response | `content`: list of `TextBlock`, `ToolUseBlock`, `ThinkingBlock`, `ToolResultBlock` |
| `UserMessage` | User input echo | `content` |
| `ResultMessage` | End of query | `result`, `session_id`, `total_cost_usd`, `is_error`, `num_turns` |
| `StreamEvent` | Partial updates (opt-in) | `event` dict (requires `include_partial_messages=True`) |

## Prerequisites

- Claude Code must be installed and authenticated (SDK uses its runtime)
- Python 3.10+ (`pip install claude-agent-sdk`) or Node.js 18+ (`npm install @anthropic-ai/claude-agent-sdk`)

## SDK vs CLI comparison

- CLI (`claude -p`): quick one-off tasks, shell piping, simple JSON output
- SDK: streaming callbacks, tool approval hooks, multi-turn pipelines in code, integration into larger applications

## Additional patterns

### Python — fire-and-forget with plugin

```python
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

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
```

### Python — interactive multi-turn with ClaudeSDKClient

```python
from claude_agent_sdk import (
    ClaudeSDKClient, ClaudeAgentOptions,
    AssistantMessage, TextBlock, ToolUseBlock, ResultMessage,
)

async with ClaudeSDKClient(options=ClaudeAgentOptions(
    allowed_tools=["Bash", "Write", "Edit"],
    max_turns=15,
    cwd="/path/to/project",
)) as client:
    await client.query("Add input validation to the /users endpoint")
    async for message in client.receive_response():
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
                elif isinstance(block, ToolUseBlock):
                    print(f"  [tool] {block.name}")
        elif isinstance(message, ResultMessage):
            print(f"\nDone: {message.result}")

    # Follow-up in same session — agent remembers context
    await client.query("Now add tests for that validation")
    async for message in client.receive_response():
        ...
```

### TypeScript — with plugin skill

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
