# create-team

Use this flow when the user wants to initialize, inspect, or remove a team.

## Create

- run `./scripts/team.py create --team <name> --description "<desc>"`
- verify with `./scripts/team.py show --team <name>`
- run `./scripts/doctor.py check --team <name>`
- publish verbose operator snapshot:
  - `./scripts/lead.py status-report --team <name> --max-messages 10`

## Delete

- run `./scripts/team.py delete --team <name>`
- if deletion is blocked due to active teammates, run shutdown workflow first

## Notes

- team names must match `[A-Za-z0-9_-]+`
- lead member is auto-created as `team-lead`
- task and inbox lock files are initialized automatically
