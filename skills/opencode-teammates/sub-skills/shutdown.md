# shutdown

Use this flow when stopping a teammate.

## Graceful path

- send shutdown request:
  - `./scripts/inbox.py shutdown-request --team <team> --recipient <agent> --reason "<optional>"`
- poll lead inbox:
  - `./scripts/inbox.py read --team <team> --agent team-lead --unread-only`
- remove teammate and reset their pending tasks:
  - `./scripts/team.py remove-member --team <team> --name <agent> --reset-tasks --cleanup-session`

## Force path

- if tmux process remains, kill manually:
  - `tmux kill-pane -t <pane-id>` or `tmux kill-window -t <window-id>`

## Verify

- `./scripts/team.py show --team <team>`
- `./scripts/doctor.py check --team <team>`
- publish verbose operator snapshot:
  - `./scripts/lead.py status-report --team <team> --max-messages 10`
