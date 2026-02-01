---
description: Dispatch a task programmatically via the Claude Agent SDK (Python or TypeScript)
---

# Claude Agent SDK

## Process

- Determine the language: Python (`claude_agent_sdk`) or TypeScript (`@anthropic-ai/claude-agent-sdk`)
- Determine how to pass the skill/prompt:
  - Use `plugin_dirs` / `pluginDirs` to load a plugin's skills
  - Use `system_prompt_suffix` / `systemPromptSuffix` to inject raw instructions
  - Or just write a clear prompt
- Set `allowed_tools` / `allowedTools` for tools that need permission (same as CLI: Bash, Write, Edit, WebFetch)
- Set `max_turns` / `maxTurns` as a safety cap
- Iterate over the async message stream and check for the `result` attribute
- Use SDK when you need: streaming callbacks, tool approval hooks, multi-turn pipelines in code, or integration into a larger application

## When to use SDK vs CLI

- Use CLI (`claude -p`) when: you need a quick one-off task, shell piping, or simple JSON output
- Use SDK when: you need streaming callbacks, tool approval hooks, multi-turn pipelines in code, or integration into a larger application

## Patterns

### Python — basic dispatch

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Bash"],
            max_turns=10,
        )
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

### Python — with plugin skill

```python
async for message in query(
    prompt="Use the web-fetch skill to download https://example.com/article and save to ./article.md",
    options=ClaudeAgentOptions(
        allowed_tools=["Bash", "Write", "WebFetch"],
        max_turns=10,
        plugin_dirs=["/path/to/plugins/web-research"],
    )
):
    if hasattr(message, "result"):
        print(message.result)
```

### TypeScript — basic dispatch

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Find and fix the bug in auth.py",
  options: {
    allowedTools: ["Read", "Edit", "Bash"],
    maxTurns: 10,
  }
})) {
  if ("result" in message) console.log(message.result);
}
```

### TypeScript — with plugin skill

```typescript
for await (const message of query({
  prompt: "Use the web-fetch skill to download https://example.com/article and save to ./article.md",
  options: {
    allowedTools: ["Bash", "Write", "WebFetch"],
    maxTurns: 10,
    pluginDirs: ["/path/to/plugins/web-research"],
  }
})) {
  if ("result" in message) console.log(message.result);
}
```

## Key options

- `allowed_tools` / `allowedTools` — tools that execute without permission prompts
- `max_turns` / `maxTurns` — limit agent loop iterations
- `plugin_dirs` / `pluginDirs` — load plugins (and their skills) from directories
- `permission_mode` / `permissionMode` — control permission behavior
- `mcp_servers` / `mcpServers` — configure MCP servers
- `hooks` — event-driven callbacks (PreToolUse, PostToolUse, Stop, etc.)
- `agents` — define subagents with custom prompts and tools

## Prerequisites

- Claude Code must be installed and authenticated (SDK uses its runtime)
- Python 3.10+ (`pip install claude-agent-sdk`) or Node.js 18+ (`npm install @anthropic-ai/claude-agent-sdk`)

## Full reference

For upstream docs: `developer-docs/claude-agent-sdk-docs/`.
