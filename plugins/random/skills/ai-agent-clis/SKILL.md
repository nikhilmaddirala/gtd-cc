---
name: ai-agent-clis
description: Orchestrate AI agent CLI tools (Claude Code, Opencode, Gemini CLI) headlessly from within a Claude Code session. Covers CLI flags, SDK usage, workflow recipes, and cost optimization for agent-calling-agent patterns.
---

# AI agent CLI orchestration

## Overview

Coordinate tasks across AI agent CLI tools headlessly. This skill is for dispatching work from within a Claude Code session to other Claude Code or Opencode instances via CLI or SDK.


## Context

User wants to run AI agent CLIs programmatically. They may need to execute a single headless task, build a multi-step pipeline, or optimize costs across tools.


## Sub-skills

Load the appropriate sub-skill from `sub-skills/` when the user needs a specific workflow pattern.

- **piping-and-chaining.md**: pipe output between agent instances
- **parallel-tasks.md**: run multiple agents concurrently
- **cost-optimized-routing.md**: route tasks by cost tier across tools
- **ci-cd-integration.md**: GitHub Actions and CI pipeline patterns
- **multi-step-pipeline.md**: session continuation pipelines
- **batch-with-server.md**: opencode serve for batch operations


## Process

- Understand the user request from the context
- Determine which AI agent CLI tool and model best fits the task (see "When to use which tool" below)
- Determine which agent skill/prompt best fits the task
- If user needs a specific workflow pattern, load the appropriate sub-skill
- If user needs CLI flag details, read the appropriate reference from `references/`
- Apply cost strategy: prefer free/cheap models for simple tasks


## Resources

- **references/claude-code-headless.md**: all `claude -p` flags, structured output, tool permissions, sessions, subagents
- **references/claude-agent-sdk-quick.md**: Python and TypeScript SDK usage
- **references/opencode-headless.md**: `opencode run` flags, serve/attach pattern, env vars
- **references/claude-code-docs/**: 52 upstream doc files (last updated 2026-02-01)
- **references/claude-agent-sdk-docs/**: 16 upstream doc files (last updated 2026-02-01)
- **references/opencode-docs/**: 34 upstream doc files (last updated 2026-02-01)


## Guidelines

- Prefer `claude -p` as the default tool; it has the most complete headless feature set
- Always use `--output-format json` when piping between steps; parse with `jq`
- Use `--max-turns` and `--max-budget-usd` to prevent runaway costs
- Claude Code skills and slash commands do NOT work in `-p` mode; use `--append-system-prompt` to inject instructions
- Opencode reads `.claude/CLAUDE.md` and skills by default; disable with `OPENCODE_DISABLE_CLAUDE_CODE=true` if needed
- Route cheap tasks to free models (Opencode free tier, Gemini CLI quota), expensive tasks to Claude Opus with budget caps


## Appendix

### When to use which tool

- `claude -p` - best default; full Claude Code toolset, structured JSON output, session continuation, tool permissions
- Claude Agent SDK (Python/TypeScript) - when you need programmatic control, streaming callbacks, multi-turn pipelines, or structured outputs via code
- `opencode run` - when you want free/cheap models (rotating free tier), different provider access, or the attach/serve pattern for persistent servers
- Gemini CLI - daily free quota for web research tasks (TODO: add reference docs)

### Quick start

```bash
# Claude Code headless
claude -p "Summarize the auth module" --output-format json | jq -r '.result'

# Opencode headless
opencode run "Explain how closures work in JavaScript"

# Claude Agent SDK (Python)
python -c "
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions
async def main():
    async for msg in query(prompt='List all TODO comments', options=ClaudeAgentOptions(allowed_tools=['Read', 'Grep', 'Glob'])):
        print(msg)
asyncio.run(main())
"
```

### Cost reference

- Claude Code: ~$6/developer/day subscription, ~$100-200/month API
- Opencode: rotating free models (check `opencode models`)
- Gemini CLI: daily free quota
- Use `--max-budget-usd` to cap any single task

### Plugin and skill differences

- Claude Code: reads `CLAUDE.md` + `.claude/` plugins in headless mode; use `--plugin-dir` for custom paths, `--mcp-config` for MCP
- Opencode: reads `opencode.json` + optionally `.claude/` files; MCP via `opencode.json` or `opencode mcp add`

### TODOs

- Add Gemini CLI docs from https://geminicli.com/docs/
- Add reference on user's subscriptions, API keys, and preferences
