# Setting up Langfuse with Claude Code

Complete guide to enabling LLM observability for Claude Code sessions using a Stop hook.

## Overview

Claude Code provides a hooks system that lets you run scripts after each response. By configuring a Stop hook, you can automatically send conversation traces to Langfuse for debugging, cost tracking, and analytics.

## Architecture

```
Claude Code Session
    ↓ (writes conversation to ~/.claude/projects/*.jsonl)
Stop Hook triggers
    ↓ (reads new messages from JSONL)
langfuse_hook.py
    ↓ (creates traces via Langfuse SDK)
Langfuse Cloud/Self-hosted
```

## Prerequisites

- Langfuse account (cloud at us.cloud.langfuse.com or self-hosted)
- Python 3.11+ with uv available
- Claude Code installed

## Step 1: Create the hook script

Create `~/.claude/hooks/langfuse_hook.py` with uv inline metadata:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "langfuse>=3.0.0",
# ]
# ///
```

The full script should:
1. Read the most recent transcript from `~/.claude/projects/<project>/*.jsonl`
2. Parse messages into turns (user → assistant → tool_results)
3. Create Langfuse traces with `propagate_attributes` for session grouping
4. Track state to avoid reprocessing old messages

Reference implementation: `dragonix/modules/home/ai/claude/hooks/langfuse_hook.py`

## Step 2: Register the hook globally

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/langfuse_hook.py",
            "timeout": 300
          }
        ]
      }
    ]
  }
}
```

## Step 3: Enable tracing per project

Create `.claude/settings.json` (or `.claude/settings.local.json` for secrets) in your project:

```json
{
  "env": {
    "TRACE_TO_LANGFUSE": "true",
    "LANGFUSE_PUBLIC_KEY": "pk-lf-...",
    "LANGFUSE_SECRET_KEY": "sk-lf-...",
    "LANGFUSE_HOST": "https://us.cloud.langfuse.com",
    "CC_LANGFUSE_DEBUG": "false"
  }
}
```

Note: Use `settings.local.json` for secrets (not committed to git).

## Critical: session_id must use propagate_attributes

The official Langfuse guide puts `session_id` in metadata, which does NOT enable session grouping. The correct pattern:

```python
from langfuse import Langfuse, propagate_attributes

with langfuse.start_as_current_span(name=trace_name, ...) as span:
    # propagate_attributes sets trace-level attributes
    with propagate_attributes(
        session_id=session_id,
        user_id=user_id,
        tags=["model:opus", "project:myproject"],
        version=claude_code_version,
    ):
        # Child observations inherit session_id
        with langfuse.start_as_current_observation(...):
            ...
```

Without `propagate_attributes`, your Sessions view will be empty.

## Enriched trace schema

Our hook captures rich metadata from Claude Code transcripts:

### From transcript top-level fields
- `version` - Claude Code version (e.g., `2.1.4`)
- `cwd` - working directory
- `gitBranch` - active git branch

### From message.usage
- `input_tokens` - new input tokens
- `cache_read_input_tokens` - tokens read from prompt cache (bulk of context)
- `cache_creation_input_tokens` - tokens written to cache
- `output_tokens` - output tokens
- `service_tier` - API service tier

### Derived fields
- `model_family` - simplified: `opus`, `sonnet`, `haiku`
- `project_name` - derived from transcript file path
- `user_id` - from `$USER` environment variable

### Tags for filtering
- `model:opus`, `model:sonnet`, `model:haiku`
- `project:<name>`
- `branch:<name>`

## Debugging

Enable debug logging:
```json
"CC_LANGFUSE_DEBUG": "true"
```

Check logs:
```bash
tail -f ~/.claude/state/langfuse_hook.log
```

Check state (processed messages):
```bash
cat ~/.claude/state/langfuse_state.json | jq
```

## Known issues and fixes

### 1. session_id in metadata doesn't enable session grouping

**Problem**: The [official Claude Code guide](https://langfuse.com/integrations/other/claude-code) puts `session_id` in `metadata`:

```python
# WRONG - sessions view will be empty
with langfuse.start_as_current_span(
    name=f"Turn {turn_num}",
    metadata={"session_id": session_id},  # This does NOT work
) as span:
```

**Fix**: Use `propagate_attributes()` inside the span:

```python
# CORRECT - sessions are properly grouped
with langfuse.start_as_current_span(name=trace_name, ...) as span:
    with propagate_attributes(session_id=session_id):
        # Child observations inherit session_id
```

**Status**: Upstream issue pending at [langfuse/langfuse-docs](https://github.com/langfuse/langfuse-docs)

### 2. Generic "Turn N" naming is unhelpful

**Problem**: The official guide names every trace `f"Turn {turn_num}"`, making it impossible to identify traces in the dashboard.

**Fix**: Use the first line of the user's message:

```python
trace_name = user_text.strip().split("\n")[0][:80] if user_text.strip() else f"Turn {turn_num}"
```

### 3. Input tokens are massively undercounted

**Problem**: The guide only uses `message.usage.input_tokens`, but this is just new tokens. The actual context includes:
- `cache_read_input_tokens` — tokens read from prompt cache (typically 100k+)
- `cache_creation_input_tokens` — tokens written to cache

**Fix**: Sum all input token types:

```python
total_input = (
    usage.get("input_tokens", 0)
    + usage.get("cache_read_input_tokens", 0)
    + usage.get("cache_creation_input_tokens", 0)
)
```

Store the breakdown in metadata for precise cost calculation later.

### 4. curl auth fails on NixOS (base64 line breaks)

**Problem**: On NixOS and some Linux systems, `base64` adds line breaks which corrupt the Authorization header:

```bash
# FAILS - base64 adds newlines
curl -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" ...
```

**Fix**: Use explicit base64 encoding with `-w0`:

```bash
AUTH=$(echo -n "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" | base64 -w0)
curl -H "Authorization: Basic ${AUTH}" ...
```

## Limitations

- **Timing is approximate**: The Stop hook runs after the response, so all span timestamps are near-identical. Real latency data would require proxy-level integration.
- **Cost is approximate**: Langfuse calculates cost from total tokens but doesn't distinguish cache pricing tiers:
  - Cache reads are ~90% cheaper than new input
  - Cache creation is ~25% more expensive than new input
  - Use metadata breakdown (`cache_read_tokens`, `new_input_tokens`, `cache_creation_tokens`) for precise cost
- **No TTFT**: Time-to-first-token cannot be captured post-hoc.

## Nix/home-manager setup (optional)

For declarative, reproducible setup across machines:

```nix
# In your home-manager config
home.file.".claude/hooks/langfuse_hook.py" = {
  source = ./hooks/langfuse_hook.py;
  executable = true;
};

# Hook registration via settings.json symlink
home.file.".claude/settings.json" = {
  source = ./claude-settings.json;
};
```

## Verification

After setup, use Claude Code normally. Then verify traces appear:

```bash
AUTH=$(echo -n "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" | base64 -w0)
curl -s -H "Authorization: Basic ${AUTH}" \
  "$LANGFUSE_HOST/api/public/traces?limit=3" | \
  jq '.data[] | {name, sessionId, userId, tags}'
```

You should see:
- `name` - first line of your message
- `sessionId` - UUID grouping the conversation
- `userId` - your system username
- `tags` - `["model:opus", "project:...", "branch:..."]`

## References

- [Claude Code Integration Guide](https://langfuse.com/integrations/other/claude-code) (official, but has session_id bug)
- [Sessions Documentation](https://langfuse.com/docs/observability/features/sessions)
- [Python SDK v3](https://langfuse.com/changelog/2025-06-05-python-sdk-v3-generally-available)
