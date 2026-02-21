# message

Use this flow for direct and broadcast communication through inbox JSON files.

## Direct message

- `./scripts/inbox.py send --team <team> --from-name team-lead --to <agent> --summary "<summary>" --text "<message>"`

## Broadcast

- `./scripts/inbox.py broadcast --team <team> --from-name team-lead --summary "<summary>" --text "<message>"`

## Read updates

- lead unread messages:
  - `./scripts/inbox.py read --team <team> --agent team-lead --unread-only`
- teammate unread messages without marking read:
  - `./scripts/inbox.py read --team <team> --agent <agent> --unread-only --no-mark-read`

## Notes

- teammates should normally message `team-lead`
- use `summary` for compact routing and triage
- when recipient has `opencodeSessionId`, `send` and `broadcast` also push text to the live opencode session
- `send` and `broadcast` replace an unread message with the same `from` + `summary` by default (prevents stale queue buildup)
- use `--no-replace-summary` when you intentionally want multiple queued messages with same summary
