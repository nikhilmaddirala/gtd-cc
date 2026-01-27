---
description: Finalize work in feature worktree - commit, push, create PR linked to issue
---

# Finish

## Overview

Finalize work in the current feature worktree by creating a pull request linked to the issue. Does NOT merge or touch main.


## Context

User has completed implementation and wants to prepare for merge.


## Process

1. Extract issue number from branch
   ```bash
   BRANCH=$(git branch --show-current)
   ISSUE_NUM=$(echo $BRANCH | sed 's|issue/\([0-9]*\)-.*|\1|')
   ```

2. Final commit (if uncommitted changes exist)
   ```bash
   git add -A
   git commit -m "type(scope): final changes"
   ```

3. Push branch to remote
   ```bash
   git push -u origin $(git branch --show-current)
   ```

4. Get issue title for PR
   ```bash
   ISSUE_TITLE=$(gh issue view ${ISSUE_NUM} --json title --jq '.title')
   ```

5. Create pull request linked to issue
   ```bash
   gh pr create \
     --title "feat: ${ISSUE_TITLE}" \
     --body "$(cat <<EOF
   ## Summary

   Implements #${ISSUE_NUM}

   ## Changes

   - List key changes here

   ## Testing

   - How to test these changes

   ---
   Closes #${ISSUE_NUM}
   EOF
   )"
   ```

6. Update issue status to review
   ```bash
   gh issue edit ${ISSUE_NUM} --remove-label "status-doing" --add-label "status-review"
   ```

7. Verification: PR created and URL displayed to user


## Guidelines

- NEVER switch worktrees or touch main branch
- PR body MUST include "Closes #N" to auto-close issue on merge
- PR title should match conventional commit format
- Update issue label to `status-review`
- Use `--draft` flag if work needs review before merge


## Example

```
User: "/mg-dev-finish"

1. Branch: issue/42-add-dark-mode-support → Issue #42
2. [Commit any remaining changes]
3. git push -u origin issue/42-add-dark-mode-support
4. Issue title: "Add dark mode support"
5. gh pr create --title "feat: Add dark mode support" --body "...Closes #42"
6. gh issue edit 42 --add-label "status-review"

Output:
"PR created: https://github.com/user/repo/pull/15
Issue #42 moved to status-review

Next: Return to main worktree and run /mg-main-merge 42"
```
