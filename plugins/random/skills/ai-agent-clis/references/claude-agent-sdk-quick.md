# Claude Agent SDK quick reference

The SDK provides programmatic control beyond what CLI flags offer: streaming callbacks, tool approval hooks, and native message objects.

## Python

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def run_agent():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Bash"],
            max_turns=10
        )
    ):
        print(message)

asyncio.run(run_agent())
```

Install: `pip install claude-agent-sdk` or `uv add claude-agent-sdk`

## TypeScript

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Find and fix the bug in auth.py",
  options: { allowedTools: ["Read", "Edit", "Bash"] }
})) {
  console.log(message);
}
```

Install: `npm install @anthropic-ai/claude-agent-sdk`

## When to use SDK vs CLI

- Use CLI (`claude -p`) when: you need a quick one-off task, shell piping, or simple JSON output
- Use SDK when: you need streaming callbacks, tool approval hooks, multi-turn pipelines in code, or integration into a larger application

## Prerequisites

- Claude Code must be installed and authenticated (SDK uses its runtime)
- Node.js 18+ (TypeScript) or Python 3.10+

## Key options

- `allowed_tools` / `allowedTools` - tools that execute without permission prompts
- `max_turns` / `maxTurns` - limit agent loop iterations
- `permission_mode` / `permissionMode` - control permission behavior
- `mcp_servers` / `mcpServers` - configure MCP servers
- `hooks` - event-driven callbacks
- `agents` - define subagents

For full SDK documentation, see `references/claude-agent-sdk-docs/`.
