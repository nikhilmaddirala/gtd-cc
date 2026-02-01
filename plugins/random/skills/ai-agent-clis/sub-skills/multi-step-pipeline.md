---
description: Build multi-step workflows using session continuation for shared context
---

# Multi-step pipeline

## Process

- Capture `session_id` from the first step's JSON output
- Use `--resume "$session_id"` for subsequent steps that need prior context
- Start a new session (no `--resume`) when a step doesn't need prior context
- Use `--fork-session` to branch into parallel follow-ups from a shared analysis

## Patterns

```bash
# Step 1: analyze
session_id=$(claude -p "Analyze the codebase for TODO comments and technical debt" \
  --output-format json --allowedTools "Read,Grep,Glob" | jq -r '.session_id')

# Step 2: prioritize (continues with full context from step 1)
claude -p "Prioritize these issues by severity and effort" \
  --resume "$session_id" --output-format json | jq -r '.result' > /tmp/priorities.md

# Step 3: fix the top issue (new session, reads the priorities file)
claude -p "Read /tmp/priorities.md and fix the highest-priority issue" \
  --allowedTools "Read,Edit,Bash" --max-turns 15
```

```bash
# Fork into parallel follow-ups from shared analysis
session_id=$(claude -p "Analyze this codebase" --output-format json | jq -r '.session_id')

claude -p "Focus on security issues" --resume "$session_id" --fork-session &
claude -p "Focus on performance issues" --resume "$session_id" --fork-session &
wait
```
