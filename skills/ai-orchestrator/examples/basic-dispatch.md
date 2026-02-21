---
description: Simplest orchestration pattern — dispatch a task, stream output, interact with the agent mid-execution
---

# Basic dispatch with interaction

Dispatch an arbitrary task to an agent, watch it work, and redirect it when needed.

## With Claude Agent SDK (Python)

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["claude-agent-sdk"]
# ///

import asyncio
from claude_agent_sdk import (
    ClaudeSDKClient, ClaudeAgentOptions,
    AssistantMessage, TextBlock, ToolUseBlock, ResultMessage,
)


async def print_response(client: ClaudeSDKClient):
    """Stream and print the agent's response."""
    async for message in client.receive_response():
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="", flush=True)
                elif isinstance(block, ToolUseBlock):
                    print(f"  [tool] {block.name}")

        if isinstance(message, ResultMessage):
            print(f"\n\nResult: {message.result}")
            print(f"Cost: ${message.total_cost_usd}")


async def main():
    # ClaudeSDKClient maintains a persistent session.
    # Every query() call shares the same conversation context,
    # so the agent remembers what it did in previous exchanges.
    options = ClaudeAgentOptions(
        model="sonnet",
        max_turns=15,
        # Only tools that modify state need explicit approval.
        # Read, Glob, Grep are auto-allowed.
        allowed_tools=["Bash", "Write", "Edit", "WebFetch"],
        # Load a plugin so the agent has access to its skills.
        # Omit if the agent doesn't need any skill.
        # plugins=[{"type": "local", "path": "/path/to/plugins/web-research"}],
    )

    async with ClaudeSDKClient(options=options) as client:
        # Dispatch the task
        await client.query("Add input validation to the /users POST endpoint")
        await print_response(client)

        # Follow up — agent remembers everything from the first task
        # User says: "also add tests for the validation"
        await client.query("Now add tests for the validation you just wrote.")
        await print_response(client)

        # Another follow-up — still in the same conversation
        # User says: "the email regex is wrong, fix it"
        await client.query("The email regex rejects valid emails with + in them. Fix it.")
        await print_response(client)


asyncio.run(main())
```

## With Opencode SDK (TypeScript)

```typescript
import { createOpencode } from "@opencode-ai/sdk"

const { client } = await createOpencode({ port: 4096 })

// Create a persistent session
const session = await client.session.create({
  body: { title: "Add input validation" }
})

// Dispatch the task
const result = await client.session.prompt({
  path: { id: session.id },
  body: {
    model: { providerID: "opencode", modelID: "gpt-5-nano" },
    parts: [{ type: "text", text: "Add input validation to the /users POST endpoint" }]
  }
})
console.log(result)

// Follow up in the same session — agent remembers everything
const result2 = await client.session.prompt({
  path: { id: session.id },
  body: {
    model: { providerID: "opencode", modelID: "gpt-5-nano" },
    parts: [{ type: "text", text: "Now add tests for the validation you just wrote." }]
  }
})
console.log(result2)
```

## How the orchestrator uses this

When the user says "do X", the orchestrator:

- Creates a `ClaudeSDKClient` with appropriate options
- Calls `client.query(prompt)` and streams the response via `client.receive_response()`
- The client maintains the session automatically

When the user says "tell it to also do Y":

- The orchestrator calls `client.query("Y")` on the same client — the agent resumes with full context of what it already did

When the user says "that's wrong, fix Z":

- Same mechanism — `client.query("Z is wrong because ... Fix it.")`

The `ClaudeSDKClient` is the state. No session IDs to track, no files, no side-channels, no restarts.

## Configuration quick reference

| What | Claude SDK | Opencode SDK |
|------|-----------|-------------|
| Model | `model="sonnet"` | `providerID: "opencode", modelID: "gpt-5-nano"` |
| Turn limit | `max_turns=15` | not available (model-dependent) |
| Tool permissions | `allowed_tools=["Bash", "Write"]` | not available (all tools allowed) |
| Skill loading | `plugins=[{"type": "local", "path": "..."}]` | auto-discovers from `.claude/skills/` |
| Multi-turn | `ClaudeSDKClient` (persistent session) | send new prompt to same `session.id` |
| Cost cap | `max_budget_usd=1.0` | not available (control via model choice) |
| Interrupt | `await client.interrupt()` | not available via SDK |
