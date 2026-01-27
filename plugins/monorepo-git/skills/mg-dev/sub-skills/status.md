---
description: Show branch status and linked issue info in feature worktree
---

# Status

## Overview

Show current branch status with issue context.


## Context

User wants to see progress in their feature worktree.


## Process

1. Extract issue number from branch
   ```bash
   BRANCH=$(git branch --show-current)
   ISSUE_NUM=$(echo $BRANCH | sed 's|issue/\([0-9]*\)-.*|\1|')
   ```

2. Show branch status
   ```bash
   git status --short
   git log main..HEAD --oneline
   ```

3. Show linked issue info
   ```bash
   gh issue view ${ISSUE_NUM} --json number,title,labels,state
   ```
   - Display issue title
   - Display current status label
   - Display if PR exists

4. Check for existing PR
   ```bash
   gh pr list --head $(git branch --show-current) --json number,url,state
   ```

5. Verification: Status displayed with issue context


## Guidelines

- Focus on what's changed since branching from main
- Show issue context for orientation
- Suggest next action based on state:
  - No commits yet → "Start implementing with /mg-dev-work"
  - Has commits, no PR → "Ready to create PR with /mg-dev-finish"
  - Has PR → "PR exists, waiting for review/merge"


## Example

```
User: "/mg-dev-status" or "status"

Output:
"Branch: issue/42-add-dark-mode-support
Issue: #42 - Add dark mode support
Status: status-doing

Changes (3 commits ahead of main):
  abc1234 feat(theme): add dark mode context
  def5678 feat(ui): add theme toggle button
  ghi9012 fix(theme): persist preference

Working tree:
  M  src/theme.ts
  M  src/App.tsx
  A  src/components/ThemeToggle.tsx

No PR created yet.
→ Run /mg-dev-finish to push and create PR"
```
