## TLDR

One or two sentences summarizing whether the PR is on track.

## Merge Blockers

Issues that must be addressed before merge. Include:
- Brief description of the issue
- Reference to README.md requirement or bug evidence
- Link to specific code

Example with issues:

1. Missing error logging in API handler (README.md says errors must be logged)

https://github.com/owner/repo/blob/1d54823877c4de72b2316a64032a54afc404e619/src/api.ts#L45-L52

2. Validation missing on user input (caused by incomplete refactor in auth module)

https://github.com/owner/repo/blob/1d54823877c4de72b2316a64032a54afc404e619/src/auth.ts#L20-L28

When no issues found:

No merge blockers identified. Code is ready for merge.

## Nice-to-Haves

Non-blocking suggestions. Only include if there are meaningful improvements that don't prevent merge.

Example:

- Consider extracting repeated validation logic into a shared helper

## Final Decision

- Approve
- Approve w/ Nits (if only nice-to-haves, no blockers)
- Request Changes (if merge blockers exist)