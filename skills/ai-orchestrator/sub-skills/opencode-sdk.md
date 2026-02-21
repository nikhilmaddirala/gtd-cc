---
description: Dispatch a task programmatically via the Opencode JS/TS SDK, or via CLI shorthand
---

# Opencode dispatch

SDK-first. Use the Opencode SDK for programmatic session management. For simple one-off dispatches, use the CLI shorthand at the bottom.

## Process

- Start or connect to an Opencode server (`opencode serve --port 4096`)
- Create a client: `createOpencode({ port: 4096 })`
- Create a session, then send prompts via `client.session.prompt()`
- Specify model using `providerID` + `modelID` format
- Available models:
  - Free: `opencode/gpt-5-nano`, `opencode/glm-4.7-free`, `opencode/kimi-k2.5-free`
  - Paid: depends on authenticated providers (run `opencode models` to list)

## Common patterns

### TypeScript basic dispatch

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
      text: "Download https://example.com/article and save as ./article.md"
    }]
  }
})

console.log(result)
```

## CLI shorthand

For simple dispatches, `opencode run` avoids the server setup:

```bash
# Basic dispatch with free model
opencode run "Explain the auth module" \
  --model opencode/gpt-5-nano

# Paid model for quality tasks
opencode run "Review this codebase for security issues" \
  --model openai/gpt-5.2-codex
```

Skill discovery: Opencode auto-discovers skills from `.claude/skills/` and `.opencode/skills/`. If the skill lives elsewhere, symlink it: `ln -s /path/to/skill .claude/skills/<name>`.

Session continuation: `--continue` (last session) or `--session <id>` (specific session).

Opencode has no `--allowedTools` or `--max-budget-usd` — control costs via model selection.

### Serve/attach pattern (avoid MCP cold boot)

```bash
# Start server once
opencode serve --port 4096 &
sleep 3

# Run tasks against it (instant MCP access)
opencode run --attach http://localhost:4096 "First task"
opencode run --attach http://localhost:4096 "Second task"

kill %1  # stop server
```

## Lookups

- Run/serve flags, env vars, useful commands: `references/opencode-flags.md`
- Models and costs: `references/providers-models.md`
- Upstream doc URLs: `references/sources.md`

## Status

SDK patterns still being established. See `examples/dispatch-web-fetch.md` for a working example.
