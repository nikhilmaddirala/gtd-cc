---
description: Merge PR via GitHub, cleanup worktree, close issue
---

# Merge

## Overview

Merge a completed PR into main and clean up the associated worktree and branch.

## Process

- Find PR for the issue
  ```bash
  gh pr list --head "issue/${N}-" --json number,url,state,headRefName
  ```

- Verify PR is ready
  ```bash
  gh pr checks ${PR_NUM}
  ```
  - Check PR state is open
  - Check CI status

- Merge PR (issue auto-closes via "Closes #N")
  ```bash
  gh pr merge ${PR_NUM} --squash --delete-branch
  ```

- Pull main to get the merge
  ```bash
  git pull origin main
  ```

- Cleanup worktree
  ```bash
  git worktree remove .worktrees/issue-${N}
  ```

- Cleanup local branch
  ```bash
  git branch -d issue/${N}-* 2>/dev/null || true
  ```

- Verify issue is closed
  ```bash
  gh issue view ${N} --json state,labels
  ```
  - If not auto-closed, manually close and add `status-done`

- Report: "PR #N merged. Issue #N closed. Worktree cleaned up."

## Guidelines

- Only run from main worktree
- Use `--squash` for clean history
- Issue auto-closes via "Closes #N" in PR body
- Clean up both worktree and local branch

## Error handling

- **PR not found**: "No PR found for issue #N. Run `/gh-work N` first."
- **Failing checks**: "PR has failing checks. Fix before merging."
- **Merge conflicts**: "PR has conflicts. Run `/gh-work N` to rebase and resolve."
