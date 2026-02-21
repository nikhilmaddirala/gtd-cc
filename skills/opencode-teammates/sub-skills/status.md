# status

Use this flow to inspect active team health and repair drift.

## Health check

- run: `./scripts/doctor.py check --team <team>`
- SLA tuning (optional env vars):
  - `OPENCODE_TEAM_INITIAL_ASSIGNMENT_TIMEOUT_MS` (default 120000)
  - `OPENCODE_TEAM_ASSIGNMENT_ACK_TIMEOUT_MS` (default 180000)
  - `OPENCODE_TEAM_SILENCE_TIMEOUT_MS` (default 300000)

## Quick drilldown

- team config: `./scripts/team.py show --team <team>`
- task list: `./scripts/tasks.py list --team <team>`
- lead unread inbox: `./scripts/inbox.py read --team <team> --agent team-lead --unread-only`

## Verbose operator report

- default to a concise but complete status report after team operations:
  - active members and runtime metadata from `team.py show`
  - tasks grouped by status and owner from `tasks.py list`
  - latest unread lead inbox messages from `inbox.py read`
  - health verdict and findings from `doctor.py check`

## Common issues

- missing inbox file for active member
- task owner references removed member
- dependency points to missing task id
- teammate removed from config but tmux pane still exists
- active teammate has no initial assignment beyond SLA
- active teammate has assignment but no ack/progress beyond SLA
- active teammate silent beyond SLA timeout

## Repair sequence

- fix config and membership first
- fix task ownership and dependency references next
- clear orphan runtime artifacts last
