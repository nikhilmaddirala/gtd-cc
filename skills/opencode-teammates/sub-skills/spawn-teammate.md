# spawn-teammate

Use this flow when the user asks to start a teammate process.

## Steps

- create teammate and seed inbox via spawn script:
  - `./scripts/spawn.sh --team <team> --name <agent> --prompt "<goal>"`
- verify teammate presence:
  - `./scripts/team.py show --team <team>`
- verify first message arrived:
  - `./scripts/inbox.py read --team <team> --agent <agent> --unread-only --no-mark-read`
- publish verbose operator snapshot:
  - `./scripts/lead.py status-report --team <team> --max-messages 10`

## Options

- `--model <model-name>`
- `--agent-type <type>`
- `--cwd <path>`
- `--plan-mode-required`
- `--server-url <url>`
- `--runtime <headless|tui>`
- `--target-pane <pane-id>`
- `--target-window <window-id>`

## Notes

- spawn script records `tmuxPaneId` in team config
- spawn script creates an opencode session via `opencode serve` HTTP API
- bootstrap prompt is pushed to the opencode session with `prompt_async`
- initial prompt is also written to the teammate inbox for deterministic replay
- teammates are opencode-only for now
- default runtime is `headless` (session-only, no tmux pane)
- use `--runtime tui` when you need to interact with teammate UI directly
- default placement uses the team's anchored lead window (`leadWindowId` in config)
- when `leadWindowId` is missing or stale, spawn resolves through `leadPaneId`
- this prevents teammate panes from following whichever human window is currently active
- use `--target-pane` or `--target-window` only when you intentionally want an override
- spawn inherits lead config env (`OPENCODE_CONFIG`, `XDG_CONFIG_HOME`, `OPENCODE_THEME`) for consistent TUI theme/config
