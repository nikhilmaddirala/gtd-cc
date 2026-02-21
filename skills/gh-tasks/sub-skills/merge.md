---
description: Merge PR via GitHub, cleanup worktree and branch, verify issue closure
---

# merge

## Overview

Merge a completed PR into main and clean up all associated artifacts (worktree, branch). The issue auto-closes via "Closes #N" in the PR body.


## Process

1. Resolve which PR to merge from natural language input:
   - List open PRs: `gh pr list --state open`
   - If user input clearly matches one PR (by number, issue number, title keyword, or branch), use it
   - If ambiguous, present a numbered list and ask the user to confirm
   - If given an issue number, find the matching PR:
     ```bash
     gh pr list --head "issue-<N>-" --json number,headRefName
     ```

2. Merge and cleanup (delegate to script):
   ```bash
   scripts/merge.sh <pr-number>
   ```
   The script handles: squash merge, worktree removal, branch cleanup, and issue closure verification.

3. Report and suggest next steps:
   - "PR #N merged. Issue #N closed. Worktree cleaned up."
   - Suggest checking if affected subtrees need publishing


## Guidelines

- Only run from main worktree (not from inside a feature worktree)
- The script commits any pending git-sync changes before pulling, so dirty working tree on main is handled automatically
- The script checks mergeability before any destructive operations (worktree/branch cleanup happens after merge, not before)
- If the script fails on merge conflicts: run `work` sub-skill to rebase and resolve
- If the script fails on CI checks: fix before merging
- If no PR is found for the issue: run `work` sub-skill first


## Recovery

If the script exits after the GitHub merge succeeded but before cleanup finished:

- Pull main: `git add -A && git commit -m "chore: sync" && git pull origin main`
- Prune refs: `git fetch --prune origin`
- Remove worktree: `git worktree remove .worktrees/<branch> --force`
- Delete local branch: `git branch -D <branch>`
- Verify issue closed: `gh issue view <N> --json state`
