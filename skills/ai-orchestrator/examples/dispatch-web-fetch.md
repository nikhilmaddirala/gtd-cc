---
description: End-to-end walkthrough dispatching a web-fetch task via Claude Code CLI, Agent SDK, Opencode CLI, and Opencode SDK
---

# Dispatch a skill to a headless agent instance

## Scenario

User says: "use web-fetch skill to download this article and save it to /home/user/refs/article.md: https://example.com/blog/interesting-post"

This example shows how to dispatch this task to headless agent instances using Claude Code CLI, Claude Agent SDK, and Opencode.


## With Claude Code CLI headless

### Determine the plan

- Task is simple (fetch one page, save as markdown) so use a cheap model
- Use `--model haiku` for cost efficiency (`haiku`, `sonnet`, and `opus` are valid aliases; full model name also works e.g. `claude-haiku-4-5-20251001`)
- The web-fetch skill is part of the web-research plugin; use `--plugin-dir` to load the plugin so the skill is available
- `--allowedTools` only needs tools that require permission approval; read-only tools (Read, Glob, Grep) are auto-allowed. We need: `Bash` (for curl/jina), `Write` (to save the file), `WebFetch`
- There is no `--cwd` flag in Claude Code; put the target path in the prompt instead

### Construct and run the command

```bash
claude -p "Use the web-fetch skill to download https://example.com/blog/interesting-post and save it as markdown to /home/user/refs/article.md" \
  --model haiku \
  --plugin-dir /path/to/plugins/web-research \
  --allowedTools "Bash" "Write" "WebFetch" \
  --max-turns 10 \
  --output-format json \
  | jq -r '.result'
```


## With Claude Agent SDK

### Python

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def main():
    async for message in query(
        prompt="Use the web-fetch skill to download https://example.com/blog/interesting-post and save it as markdown to /home/user/refs/article.md",
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

### TypeScript

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Use the web-fetch skill to download https://example.com/blog/interesting-post and save it as markdown to /home/user/refs/article.md",
  options: {
    allowedTools: ["Bash", "Write", "WebFetch"],
    maxTurns: 10,
    plugins: [{ type: "local", path: "/path/to/plugins/web-research" }],
  }
})) {
  if ("result" in message) console.log(message.result);
}
```


## With Opencode headless

### Determine the plan

- Opencode reads `.claude/skills` by default, so if the web-fetch skill is installed there, it is auto-discovered
- If the skill lives elsewhere (e.g. in a plugin directory outside the project), symlink it into a discovery root:
  - `ln -s /path/to/plugins/web-research/skills/web-fetch .claude/skills/web-fetch`
  - Or globally: `ln -s /path/to/plugins/web-research/skills/web-fetch ~/.config/opencode/skills/web-fetch`
- Use `--model` with `provider/model` format (e.g. `openrouter/anthropic/claude-haiku-4.5` or a free model like `opencode/gpt-5-nano`)

### Construct and run the command

```bash
opencode run "Use the web-fetch skill to download https://example.com/blog/interesting-post and save it as markdown to /home/user/refs/article.md" \
  --model opencode/gpt-5-nano
```


## With Opencode SDK

```typescript
import { createOpencode } from "@opencode-ai/sdk"

const { client } = await createOpencode({ port: 4096 })

const session = await client.session.create({
  body: { title: "Fetch article" }
})

const result = await client.session.prompt({
  path: { id: session.id },
  body: {
    model: { providerID: "opencode", modelID: "gpt-5-nano" },
    parts: [{
      type: "text",
      text: "Use the web-fetch skill to download https://example.com/blog/interesting-post and save it as markdown to /home/user/refs/article.md"
    }]
  }
})

console.log(result)
```
