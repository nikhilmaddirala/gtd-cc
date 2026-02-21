---
description: Dispatch a task to Gemini CLI for free-quota web research and general tasks
---

# Gemini CLI dispatch

## When to use

- Daily free quota makes it useful for bulk/low-priority tasks at zero cost
- Good for web research tasks where Gemini's grounding in Google Search is an advantage
- No SDK available yet — CLI only

## Process

- Authenticate: `gemini auth login` (one-time setup)
- Pass the prompt directly as an argument
- Use `--model` to select a Gemini model (default is the latest available)
- Gemini CLI does not support plugin/skill loading — include all instructions in the prompt
- Output goes to stdout; redirect or pipe as needed

## Common patterns

### Basic dispatch

```bash
gemini "Summarize the key points from https://example.com/article"
```

### With model selection

```bash
gemini --model gemini-2.5-flash "Explain this error: $(cat error.log)"
```

## Lookups

- Models and costs: `references/providers-models.md`
- Upstream docs: TODO (download from geminicli.com/docs/)

## Status

Minimal coverage. Awaiting upstream docs download and real usage patterns. See SKILL.md roadmap.
