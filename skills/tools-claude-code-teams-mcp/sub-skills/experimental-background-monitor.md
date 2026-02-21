# Experimental opencode external orchestrator

## Overview

Run an external harness against `opencode serve` (HTTP API / SDK) so monitoring and control continue outside the lead chat turn loop. This approximates native always-on orchestration.

## When to use

- You want continuous monitoring while still chatting normally
- You want explicit separation between lead chat and orchestration runtime
- You are testing push-like behavior via server events + async prompts

## Core idea

- `opencode serve` is the runtime
- Harness process subscribes to server events (`/event`)
- Harness drives a dedicated session with async prompts (`/session/:id/prompt_async`)
- The dedicated session uses `claude-teams-*` MCP tools for team operations

## Process

Preferred implementation in this repo:

```bash
./scripts/opencode-teams-orchestrator.py --base-url http://127.0.0.1:4098 --loops 0
```

Script location:

- `tools-claude-code-teams-mcp/scripts/opencode-teams-orchestrator.py`

### Step 1: start or reuse server

```bash
opencode serve --port 4098
```

### Step 2: create dedicated orchestrator session

```bash
curl -sS -X POST http://127.0.0.1:4098/session \
  -H 'content-type: application/json' \
  -d '{"title":"claude-teams-orchestrator"}'
```

Capture the returned `id` as `SESSION_ID`.

### Step 3: launch harness loop

Harness responsibilities:

- Subscribe to `GET /event` (SSE)
- On relevant events, send `POST /session/:id/prompt_async` to trigger checks
- Keep a local event cursor/log for dedupe

Trigger prompt pattern:

```text
Check claude-teams inbox for unread teammate messages. Summarize new items briefly.
If any message is unsafe or rogue, send shutdown_request and confirm team config cleanup.
```

### Step 4: inspect outcomes

- Read session messages via `GET /session/:id/message`
- Confirm actions via `claude-teams_read_config` and `claude-teams_read_inbox`

### Step 5: stop harness

- Stop harness process
- Keep server running if teammates still need opencode backend

## Minimal behavior contract

- Watch continuously until explicitly stopped
- Report each new teammate message once (dedupe)
- Escalate unsafe output immediately
- Never run destructive shell actions without explicit user instruction

## Notes

- This is external orchestration, not native built-in push from `claude-teams-mcp`
- It can feel push-like because the harness is always running
- The same pattern can be implemented with the JS SDK instead of raw HTTP

## Troubleshooting

- No events: verify server reachable at `http://127.0.0.1:4098/global/health`
- No MCP actions in session: verify `claude-teams` MCP is enabled in opencode config
- Prompt_async accepted but no response yet: check `GET /session/:id/message` for completion
