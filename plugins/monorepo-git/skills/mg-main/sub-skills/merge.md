---
description: Merge a feature branch via PR and cleanup the worktree
---

# Merge

## Overview

Merge a completed feature branch into main via PR and clean up the worktree. Run from main worktree only.


## Context

User has a PR ready (created by `/mg-dev-finish`) and wants to merge it.


## Process

1. Identify issue and PR
   ```bash
   # Find branch and worktree from issue number
   BRANCH="issue/${N}-*"
   WORKTREE=".worktrees/issue-${N}"

   # Find PR for this branch
   gh pr list --head "issue/${N}-" --json number,url,state,headRefName
   ```

2. Verify PR is ready
   - Check PR state is open
   - Check CI status (if applicable)
   ```bash
   gh pr checks ${PR_NUM}
   ```

3. Merge PR (issue auto-closes via "Closes #N")
   ```bash
   gh pr merge ${PR_NUM} --squash --delete-branch
   ```
   - `--squash` creates a single commit from all PR commits
   - `--delete-branch` removes the remote branch after merge
   - Issue auto-closes because PR body contains "Closes #N"

4. Pull main to get the merge
   ```bash
   git pull origin main
   ```

5. Cleanup worktree
   ```bash
   git worktree remove ${WORKTREE}
   ```

6. Cleanup local branch (if still exists)
   ```bash
   git branch -d issue/${N}-* 2>/dev/null || true
   ```

7. Verify issue is closed
   ```bash
   gh issue view ${N} --json state,labels
   ```
   - Should show state: CLOSED
   - Label should be `status-done` (set manually if not)

8. Verification: PR merged, worktree removed, issue closed


## Guidelines

- Only run from main worktree
- Use `--squash` to keep history clean (configurable)
- Issue auto-closes via "Closes #N" in PR body
- If issue doesn't auto-close, manually close it
- Clean up both worktree and local branch


## Example

```
User: "/mg-main-merge 42"

1. Find PR for issue/42-* branch → PR #15
2. gh pr checks 15 → all passing
3. gh pr merge 15 --squash --delete-branch
4. git pull origin main
5. git worktree remove .worktrees/issue-42
6. gh issue view 42 → state: CLOSED

Output:
"PR #15 merged successfully!
Issue #42 closed automatically.
Worktree .worktrees/issue-42 removed.
Branch issue/42-add-dark-mode-support deleted.

✓ Task complete"
```


## Error handling

- **PR not found**: "No PR found for issue #N. Did you run /mg-dev-finish?"
- **PR has failing checks**: "PR #N has failing checks. Review and fix before merging."
- **Merge conflicts**: "PR #N has merge conflicts. Resolve in the worktree first."
- **Issue didn't auto-close**: Manually add `status-done` label and close issue
