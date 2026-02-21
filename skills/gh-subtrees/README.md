# gh-subtrees

## Overview

- Subtree publishing to standalone GitHub repos
- Project graduation from lab to production
- Subtree remote health diagnostics

## Current workflow hardening

The current bidirectional sync workflow is now documented with stronger safety rules in `sub-skills/sync.md`:

- Added preflight checks (clean index on `main`, no local subtree edits mixed into sync)
- Added explicit direction classification for `A`, `D`, `M`, `R`, `C`
- Kept push-before-pull ordering to avoid writing to `main` while sync worktrees exist
- Added pull-list-based rsync excludes so remote-newer paths are not overwritten during push
- Switched pull copy guidance to use temporary worktree + rsync (better metadata fidelity than `git show > file`)
- Added post-pull verification note (status can lag until git-sync/manual commit)

## Recommended workflow changes (strategic)

The existing approach can work, but it remains operationally complex because both monorepo and standalone repos accept active writes.

If you want less brittleness long-term, consider one of these models:

- Monorepo-authoritative publish model
  - Edits happen in monorepo only
  - Standalone repos are publish artifacts
  - Eliminates bidirectional reconciliation logic

- Standalone-authoritative model
  - Collaborator repos are source of truth
  - Monorepo pulls snapshots for orchestration/context
  - Eliminates push-side overwrite risk

- Stateful bidirectional model
  - Keep current topology, but track explicit sync state per subtree
  - Use last-synced markers and three-way decisions instead of timestamp heuristics
  - Most flexible, but highest implementation complexity

Given the collaborator constraint (you in monorepo, collaborators in standalone repos), the best practical next step is to keep the current process but evolve toward explicit per-subtree sync state and conflict queues.

## git-subrepo option

`git-subrepo` is a practical way to implement stateful bidirectional sync without maintaining custom file-level classifiers. The `gh-subrepo` skill (at `../gh-subrepo/`) provides the complete workflow and documentation.

How `git-subrepo` helps vs current rsync and heuristic process:

- Tracks explicit sync metadata in `<subdir>/.gitrepo` plus internal subrepo refs
- Uses pull and push operations that are commit-aware instead of inferring direction from `A/D/M` file states
- Reduces overwrite risk from whole-tree mirroring and `rsync --delete`
- Keeps collaboration natural in standalone repos while still allowing monorepo-first editing
- Supports conflict handling through normal git merge or rebase flows
- Handles mixed commits (subrepo + other files) via worktree cleanup pattern for clean standalone history

Tradeoffs:

- Adds a tool dependency outside core git
- Requires `.gitrepo` files in managed subdirectories
- Pull integration is typically squashed in monorepo history
- Needs pilot rollout and operational guardrails before broad adoption
- Mixed commits require explicit cleanup for clean standalone history (see gh-subrepo worktree pattern)

Suggested migration approach:

- Start with one pilot subtree only
- Confirm current subtree is in sync before cutover
- Install and verify `git-subrepo` on all machines and agent environments
- Run `git subrepo init <subdir> -r <remote-url> -b <branch>` for an existing subtree
- Commit the new `.gitrepo` file
- Validate bidirectional flow with `git subrepo pull <subdir>` and `git subrepo push <subdir>`
- Update skill and scripts to use `git subrepo status/pull/push` as the source of truth
- Roll out incrementally subtree by subtree

## Migration guide

Use this flow to migrate one existing subtree from rsync-based sync to `git-subrepo`.

- Choose a project with moderate activity and low blast radius
- Announce a short cutover window to collaborators for that project
- Run the current sync process first so monorepo and standalone repo match at cutover start
- Install `git-subrepo` everywhere this operation runs and verify with `git subrepo version`
- Decide target location for pilot:
  - keep existing path: `40-code/41-subtrees/<project>`
  - or move to new lane: `40-code/415-subrepos/<project>`
- If moving to `415-subrepos`, move first and commit the move:
  - `git mv 40-code/41-subtrees/<project> 40-code/415-subrepos/<project>`
  - `git commit -m "chore(<project>): move to 415-subrepos for subrepo pilot"`
- Initialize subrepo tracking from monorepo root:
  - `git subrepo init <target-subdir> -r <repo-url> -b <branch>`
- Understand `.gitrepo` file semantics:
  - created automatically by `git subrepo init` in `<target-subdir>/.gitrepo`
  - stores subrepo metadata (remote URL, branch, method, sync refs)
  - do not hand-author from scratch; generate with `init` and only edit intentionally
- Commit `.gitrepo` in monorepo:
  - `git add <target-subdir>/.gitrepo`
  - `git commit -m "chore(<project>): initialize git-subrepo metadata"`
- Record or confirm compatibility metadata:
  - `git remote add remote-<project> <repo-url>` if missing
  - add or verify URL in `40-code/41-subtrees.yaml` (or successor config)
- Validate initial health:
  - `git subrepo status <target-subdir>`
  - expect managed status, no fatal errors
- Execute remote-to-monorepo pull test:
  - create a small collaborator-side commit in standalone repo
  - run `git subrepo pull <target-subdir>`
  - confirm pulled content appears under `<target-subdir>`
- Execute monorepo-to-remote push test:
  - edit a small non-critical file under `<target-subdir>`
  - run `git subrepo push <target-subdir>`
  - confirm commit appears in standalone repo
- After successful tests, mark the project as subrepo-managed and stop using rsync-based sync for it
- For future development, use `gh-subrepo` skill commands instead of `gh-subtrees`
- Note: Mixed commits (touching both subrepo and other files) are handled via worktree cleanup pattern — see `../gh-subrepo/references/manual-workflow.md` section "Clean Push with Mixed Commits (Worktree Pattern)"

Rollback path if pilot fails:

- Stop running `git subrepo pull/push` for that project
- Revert or remove the `.gitrepo` file commit in monorepo
- Return the project to the old sync workflow for a single release cycle
- Capture failure mode, then retry with improved guardrails

## Pilot checklist

Readiness checklist:

- pilot project chosen and repo URL documented
- target path decided (`41-subtrees` or `415-subrepos`)
- collaborator freeze window agreed
- monorepo and standalone repo are in sync before cutover
- monorepo working tree is clean and index has no staged changes
- `git-subrepo` installed and `git subrepo version` works on all required machines
- ownership assigned for pull test, push test, and rollback owner

Execution checklist:

- if using `415-subrepos`, path moved with `git mv` and move commit completed
- `git subrepo init <target-subdir> -r <repo-url> -b <branch>` completed
- `<target-subdir>/.gitrepo` exists
- `.gitrepo` committed in monorepo (this is required; it is the state anchor)
- `git subrepo status <target-subdir>` returns healthy output
- pull test passed:
  - collaborator commit created in standalone repo
  - `git subrepo pull <target-subdir>` completed
  - pulled content verified locally
- push test passed:
  - local change created under `<target-subdir>`
  - `git subrepo push <target-subdir>` completed
  - commit verified in standalone repo
- no staged index left on monorepo `main` after tests

Exit checklist:

- pilot marked as subrepo-managed in team docs
- old rsync sync path disabled for pilot project
- scripts and skills updated to use `gh-subrepo` skill instead of `gh-subtrees`
- runbook notes captured (successes, failures, conflict patterns, automation gaps)
- rollback outcome documented if rollback used
- go/no-go decision recorded for next subtree migration
- team trained on `gh-subrepo` workflow, especially mixed commits handling via worktree pattern

## Roadmap / TODOs

- ~~Status script and publish skill don't detect monorepo deletions as publishable changes~~ Fixed: replaced publish with rsync-based sync. Status script now shows any diff as "files differ" without guessing direction. The sync sub-skill uses `git log --diff-filter=D` + AI review to distinguish monorepo deletions from remote additions.
