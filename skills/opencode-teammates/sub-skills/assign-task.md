# assign-task

Use this flow for task creation, assignment, and dependency updates.

## Create

- `./scripts/tasks.py create --team <team> --subject "<subject>" --description "<desc>"`

## Update

- assign owner:
  - `./scripts/tasks.py update --team <team> --id <task-id> --owner <agent>`
- status transition:
  - `./scripts/tasks.py update --team <team> --id <task-id> --status in_progress`
- add dependencies:
  - `./scripts/tasks.py update --team <team> --id <task-id> --add-blocked-by 1,2`

## Validate

- list tasks: `./scripts/tasks.py list --team <team>`
- send explicit assignment to owner inbox (required for SLA checks):
  - `./scripts/inbox.py send --team <team> --from-name team-lead --to <agent> --summary task-assignment --text "Task <id>: <what to do>"`
- require teammate ack/progress back to lead after assignment:
  - `./scripts/inbox.py read --team <team> --agent team-lead --unread-only`
- sync completion from teammate done message:
  - `./scripts/lead.py sync-done --team <team> --from-agent <agent> --summary <done-summary> --task-id <task-id>`
- verify health: `./scripts/doctor.py check --team <team>`
- publish verbose operator snapshot:
  - `./scripts/lead.py status-report --team <team> --max-messages 10`

## Rules enforced by script

- no circular dependencies
- no backward status transitions
- blocked tasks cannot move to `in_progress` or `completed`
