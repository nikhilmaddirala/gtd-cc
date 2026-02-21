# opencode-teammates

## Overview

Skill for running agent-team workflows in OpenCode without relying on an external MCP server implementation. A reverse engineered version of https://github.com/cs50victor/claude-code-teams-mcp/ implemented as a skill instead of mcp.

This implementation is intentionally opencode-only for now. Teammate sessions are created and driven via `opencode serve` APIs.

This skill reproduces the practical behavior of Claude Teams MCP using skill orchestration plus local scripts:

- team lifecycle management
- teammate spawning and shutdown
- inbox-based messaging
- task tracking with dependencies and ownership
- safety checks and recovery workflows

## Goals

- keep the same mental model as `claude-code-teams-mcp`: one team, many teammates, shared tasks, explicit message passing - https://github.com/cs50victor/claude-code-teams-mcp/
- use filesystem state as source of truth
- make behavior deterministic and inspectable
- keep workflow portable across local OpenCode sessions
- keep implementation simple by standardizing on a single runtime backend

## Non-goals

- replacing MCP as a generic cross-client API surface
- perfect protocol parity with Claude Code internals
- background daemons beyond what the host runtime already provides

## User guide

### Core concepts

- team: named coordination unit with one lead and zero or more teammates
- inbox: per-agent message log for commands, updates, and control signals
- task: work item with status, ownership, and dependency edges
- teammate runtime: spawned agent process (headless by default, optional tmux TUI) that reads inbox and reports progress
- teammate runtime: opencode session created through `opencode serve`, optionally attached in tmux

### Typical workflow

- initialize a team
- spawn one or more teammates with focused prompts (headless by default, `--runtime tui` when interactive panes are needed)
- create and assign tasks
- poll teammate inboxes and process updates
- approve or reject plans when required
- request graceful shutdown, then force cleanup if needed

### Runtime requirements

- `opencode serve` running locally or remotely
- `OPENCODE_SERVER_URL` exported when not using `http://127.0.0.1:4098`
- `tmux` available when using TUI runtime (`--runtime tui`)
- teams are anchored to the lead tmux window (`leadWindowId`) so teammate panes stay in team context even if humans switch windows

### Recommended execution pattern

- keep prompts narrow and role-specific
- poll inboxes continuously during active work
- keep one task in `in_progress` per teammate unless parallelism is intentional
- always verify teammate removal in team config after shutdown
- use `./scripts/lead.py status-report --team <team> --max-messages 10` after each operation for a verbose operator snapshot

## Architecture

### Storage layout

State is persisted under standard Claude/OpenCode-style directories:

```text
~/.claude/
├── teams/<team-name>/
│   ├── config.json
│   └── inboxes/
│       ├── team-lead.json
│       ├── <teammate>.json
│       └── .lock
└── tasks/<team-name>/
    ├── 1.json
    ├── 2.json
    └── .lock
```

### Data model summary

- team config: team metadata, lead member record, teammate member records
- inbox messages: plain messages and structured control messages (`shutdown_request`, `shutdown_approved`, task assignment)
- tasks: status (`pending`, `in_progress`, `completed`, `deleted`), owner, `blocks`, `blockedBy`, optional metadata

### Safety and consistency

- atomic writes for config and state updates
- file locks for concurrent readers and writers
- validation rules for status transitions and dependency cycles
- best-effort cleanup for partial spawn and shutdown failures

## Skill structure

```text
skills/opencode-teammates/
├── SKILL.md
├── README.md
├── sub-skills/
│   ├── create-team.md
│   ├── spawn-teammate.md
│   ├── assign-task.md
│   ├── message.md
│   ├── shutdown.md
│   └── status.md
├── scripts/
│   ├── team.py
│   ├── inbox.py
│   ├── tasks.py
│   ├── spawn.sh
│   ├── lead.py
│   └── doctor.py
└── templates/
    ├── teammate-bootstrap.md
    ├── task-assignment.md
    └── shutdown-request.md
```

## Sub-skill responsibilities

- create-team: create team state, seed lead member, initialize directories and locks
- spawn-teammate: validate inputs, create teammate record, spawn runtime, seed initial inbox message
- assign-task: create and update tasks, validate dependencies, notify owner
- message: route direct and broadcast messages with policy checks
- shutdown: graceful shutdown handshake, then cleanup and fallback kill path
- status: inspect config, inboxes, tasks, and runtime health for anomalies

## Operational policy

- one source of truth: files on disk represent current state
- explicit transitions: no hidden state changes
- conservative failure handling: keep data valid even when runtime commands fail
- human-readable logs: prefer debuggable JSON and concise status output
- teammate sessions are role-scoped via env vars (`OPENCODE_TEAM_ROLE`, `OPENCODE_TEAM_TEAM`, `OPENCODE_TEAM_MEMBER`) so worker sessions cannot run lead-only lifecycle actions through team scripts

## Validation checklist

- team create and delete works end to end
- teammate spawn writes config and inbox state correctly
- inbox reads honor unread filtering and mark-as-read behavior
- task status transitions reject invalid regressions
- dependency graph rejects cycles
- shutdown removes teammate and resets owned non-completed tasks
- recovery commands detect and report orphaned runtime artifacts

## Roadmap

- implement base scripts with schema parity
- add tmux spawn and kill wrappers plus runtime checks
- add sub-skill orchestration prompts
- add parity tests mirroring MCP repo test scenarios
- add doctor and repair workflow for stale state

## ISSUES

- [ ] Teammate sessions now inherit lead config environment (`OPENCODE_CONFIG`, `XDG_CONFIG_HOME`, `OPENCODE_THEME`) so theme matches lead configuration.
- [ ] Everytime opencode spawns it spits some output to the terminal window - e.g. if I spawn opencode in one pane and immediately switch to the left pane - i see some random text characters there while opencode is loading - this is not specific to this skill but a major issue.
- [ ] Teammate spawn now resolves anchored lead window robustly (with `leadPaneId` fallback) and fails fast if anchor resolution fails.


## Incident note

- 2026-02-11T17:06:52Z: I spawned teammates successfully, but coordination failed because workers were instructed to wait for explicit assignment and I initially sent only a generic kickoff, causing no actionable progress reports. I was also not able to shut down teammates afterwards.
- Implemented guardrails:
  - `doctor.py` enforces initial assignment and assignment-ack SLAs for active teammates.
  - `doctor.py` marks teams unhealthy when active teammates are silent beyond timeout.
  - timeout knobs: `OPENCODE_TEAM_INITIAL_ASSIGNMENT_TIMEOUT_MS`, `OPENCODE_TEAM_ASSIGNMENT_ACK_TIMEOUT_MS`, `OPENCODE_TEAM_SILENCE_TIMEOUT_MS`.

## References

- https://github.com/cs50victor/claude-code-teams-mcp
- https://code.claude.com/docs/en/agent-teams
