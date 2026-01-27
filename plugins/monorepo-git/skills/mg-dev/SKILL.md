---
name: mg-dev
description: Feature worktree development skill. Use when working in a .worktrees/* directory to implement issues, commit changes, and create PRs.
---

# mg-dev

## Overview

This skill handles all development operations within feature worktrees. It provides everything needed to implement an issue and prepare it for merge back to main.

CRITICAL: This skill only operates within feature worktrees (`.worktrees/*`). For main worktree operations, use the mg-main skill.


## Context

User is in a feature worktree working on a specific issue. The worktree was created by `mg-main/start.md` and is linked to a GitHub issue.


## Sub-skills

CRITICAL: You MUST load the appropriate sub-skill from the `sub-skills/` directory when routing is needed.

- **work.md**: Read issue context and implement the plan
- **finish.md**: Finalize work, push branch, create PR linked to issue
- **commit.md**: Create conventional commits during development
- **status.md**: Show branch diff and linked issue info


## Process

1. Detect current worktree and linked issue
2. Determine user intent from their request
3. Load the appropriate sub-skill
4. Verification: Confirm sub-skill completed successfully


## Guidelines

- NEVER switch worktrees or touch main branch
- All operations stay within current feature worktree
- Issue is found via branch name pattern: `issue/{N}-{slug}`
- Commits don't need warnings (we're not on main)
- PR creation links to issue with "Closes #N" for auto-close


## Appendix

### Worktree detection

```bash
# Check if in feature worktree
pwd | grep -q ".worktrees/" && echo "feature" || echo "main"
```

### Issue lookup

```bash
# Get issue number from branch name
BRANCH=$(git branch --show-current)
ISSUE_NUM=$(echo $BRANCH | sed 's|issue/\([0-9]*\)-.*|\1|')

# Fetch issue from GitHub
gh issue view ${ISSUE_NUM} --json number,title,body,comments
```

### PR linking

When creating a PR, include "Closes #N" in the body to auto-close the issue on merge:

```bash
gh pr create --title "feat: Title" --body "...

Closes #${ISSUE_NUM}"
```
