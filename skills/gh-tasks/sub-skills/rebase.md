---
description: Squash-rebase feature branch onto main to make it mergeable
---

# rebase

## Overview

Squash all feature branch commits into one, then rebase onto current `origin/main`. This makes the branch mergeable without replaying git-sync noise commits individually.

Use this when a PR is unmergeable (behind main), or before marking work complete.


## Process

1. Navigate to the worktree for the issue:
   ```bash
   cd .worktrees/issue-<N>-*
   ```

2. Commit any uncommitted work:
   ```bash
   git add -A && git commit -m "chore: save work before rebase"
   ```

3. Run the squash-rebase script:
   ```bash
   scripts/rebase.sh
   ```
   The script:
   - Fetches `origin/main`
   - Finds the merge-base (where the branch diverged)
   - Squashes all commits since the merge-base into one
   - Rebases that single commit onto `origin/main`

4. If the script reports a conflict:
   - Resolve the conflict (only one round since all commits are squashed)
   - `git add -A && git rebase --continue`

5. Push the rebased branch:
   ```bash
   git push --force-with-lease
   ```

6. Verify mergeability:
   ```bash
   gh api repos/{owner}/{repo}/pulls/<PR_NUM> --jq '.mergeable_state'
   ```
   Expected: `clean` or `unstable` (not `dirty`)


## Guidelines

- Must run from inside a feature worktree, not main
- Safe to run multiple times (idempotent: if already up-to-date, exits immediately)
- Uses `--force-with-lease` (not `--force`) so it won't overwrite unexpected remote changes
- After rebase, the branch has exactly one commit on top of main (the squashed feature work)
