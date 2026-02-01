---
name: ai-agent-clis
description: Orchestrate AI agent CLI tools (Claude Code, Opencode, Gemini CLI) headlessly from within a Claude Code session. Covers CLI flags, SDK usage, workflow recipes, and cost optimization for agent-calling-agent patterns.
---

# AI agent CLI orchestration

## Overview

Dispatch tasks from within a Claude Code session to other Claude Code or Opencode instances via CLI or SDK. The primary pattern is: pick a tool and model, load the right skill via `--plugin-dir`, construct the command, run it, verify output.

### Quick start

```bash
# Claude Code headless — dispatch a skill to a cheap model
claude -p "Use the web-fetch skill to download https://example.com/article and save to ./article.md" \
  --model haiku \
  --plugin-dir /path/to/plugins/web-research \
  --allowedTools "Bash" "Write" "WebFetch" \
  --output-format json | jq -r '.result'

# Opencode headless — same task with a free model
opencode run "Download https://example.com/article and save as ./article.md" \
  --model opencode/gpt-5-nano
```


## Context

User wants to run AI agent CLIs programmatically. They may need to execute a single headless task, build a multi-step pipeline, or optimize costs across tools.


## Sub-skills

Each sub-skill is an atomic operation for dispatching a task via a specific tool. After picking the tool and model (Step 1), load the appropriate sub-skill:

- **claude-code-cli.md**: dispatch via `claude -p` — plugin loading, tool permissions, session continuation, structured output
- **opencode-cli.md**: dispatch via `opencode run` — free models, serve/attach pattern, skill auto-discovery
- **claude-agent-sdk.md**: dispatch via Claude Agent SDK (Python/TypeScript) — streaming, hooks, programmatic control
- **opencode-sdk.md**: dispatch via Opencode JS/TS SDK (placeholder)
- **gemini-cli.md**: dispatch via Gemini CLI for free-quota tasks (placeholder)


## Process

### Step 1: pick tool and model

- Pick the tool based on the task needs (see appendix "When to use which tool")
  - `claude -p` is the default — best toolset, skill loading via `--plugin-dir`, structured JSON output
  - `opencode run` — when you want free/cheap models or the serve/attach pattern
  - Claude Agent SDK — when you need programmatic control (Python/TypeScript)
- Pick the model based on task complexity
  - Mechanical/simple tasks → `--model haiku` (Claude Code) or `opencode/gpt-5-nano` (Opencode, free)
  - Tasks needing reasoning → `--model sonnet` or `--model opus`
  - Read `references/providers-models.md` for available models and cost tiers

### Step 2: determine how to pass the skill

- If a skill/plugin is needed, use `--plugin-dir /path/to/plugin` to make its skills available in `-p` mode
- Skills and slash commands do NOT work in `-p` mode without `--plugin-dir`
- For Opencode: skills in `.claude/skills/` are auto-discovered; if elsewhere, symlink into a discovery root
- If no skill is needed, just write a clear prompt

### Step 3: configure flags

Most flags have good defaults. Only set what you need:

- `--allowedTools` — only list tools that need permission approval (Bash, Write, WebFetch). Read-only tools (Read, Glob, Grep) are auto-allowed
- `--max-turns` — safety cap to prevent runaway loops (default is usually fine for simple tasks)
- `--max-budget-usd` — cost cap for expensive tasks
- `--output-format json` — required when piping output to `jq` or another step
- Put context (target paths, URLs, specific instructions) in the prompt itself, not in flags

### Step 4: present plan and get approval

- Tell the user: "I will call `claude -p` / `opencode run` with these flags and this prompt"
- Get approval before running

### Step 5: run, verify, iterate

- Run the command
- Check output files or JSON result
- If incomplete, continue with `--continue` (last session) or `--resume <session_id>` (specific session)
- If the agent ran out of turns, resume with a higher `--max-turns`


## Examples

End-to-end walkthroughs of real tasks. Read these to understand the full workflow pattern:

- **execute-content-extraction-skill.md**: dispatch a web-fetch task to headless Claude Code, Agent SDK, and Opencode — covers plugin loading, model selection, tool permissions, and iteration


## Resources

### references/ — condensed reference docs (read on demand)

- **providers-models.md**: available providers, model aliases, and cost optimization strategy
- **plugins-skills.md**: cross-compatibility analysis between Claude Code and OpenCode plugin/skill systems

### developer-docs/ — upstream documentation snapshots (read when references aren't enough)

- **claude-code-docs/**: 52 files from code.claude.com (last updated 2026-02-01)
- **claude-agent-sdk-docs/**: 16 files from platform.claude.com (last updated 2026-02-01)
- **opencode-docs/**: 34 files from opencode.ai (last updated 2026-02-01)


## Guidelines

- Prefer `claude -p` as the default tool; it has the most complete headless feature set
- Use `--plugin-dir` to load skills in `-p` mode; `--append-system-prompt` is a fallback for injecting raw text
- Only specify `--allowedTools` for tools that need permission (Bash, Write, WebFetch); read-only tools are auto-allowed
- Always use `--output-format json` when piping between steps; parse with `jq`
- Use `--max-turns` and `--max-budget-usd` to prevent runaway costs
- Route cheap tasks to free/haiku models, quality tasks to sonnet/opus with budget caps
- Opencode reads `.claude/skills` by default; disable with `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=true` if needed


## Appendix

### When to use which tool

- `claude -p` — best default; full Claude Code toolset, skill loading via `--plugin-dir`, structured JSON output, session continuation, tool permissions
- Claude Agent SDK (Python/TypeScript) — when you need programmatic control, streaming callbacks, multi-turn pipelines, or structured outputs via code
- `opencode run` — when you want free/cheap models (rotating free tier), different provider access, or the attach/serve pattern for persistent servers
- Gemini CLI — daily free quota for web research tasks (TODO: add reference docs)

### TODOs

- [ ] Add Gemini CLI docs from https://geminicli.com/docs/
