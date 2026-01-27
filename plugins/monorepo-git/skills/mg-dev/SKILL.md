---
name: mg-dev
description: Feature worktree development skill. Use when working in a .worktrees/* directory to implement tasks, commit changes, and create PRs.
---

# mg-dev

## Overview

This skill handles all development operations within feature worktrees. It provides everything needed to implement a task and prepare it for merge back to main.

CRITICAL: This skill only operates within feature worktrees (`.worktrees/*`). For main worktree operations, use the mg-main skill.


## Context

User is in a feature worktree working on a specific task. The worktree was created by `mg-main/start.md` and is linked to a task file in `30-para/tasks/`.


## Sub-skills

CRITICAL: You MUST load the appropriate sub-skill from the `sub-skills/` directory when routing is needed.

- **work.md**: Read task context and implement the plan
- **finish.md**: Finalize work, push branch, create PR
- **commit.md**: Create conventional commits during development
- **status.md**: Show branch diff and linked task info


## Process

1. Detect current worktree and linked task
2. Determine user intent from their request
3. Load the appropriate sub-skill
4. Verification: Confirm sub-skill completed successfully


## Guidelines

- NEVER switch worktrees or touch main branch
- All operations stay within current feature worktree
- Task file is found via branch name pattern: `task/{id}-{slug}`
- Commits don't need warnings (we're not on main)
- PR creation is the signal that work is ready for merge


## Appendix

### Worktree detection

```bash
# Check if in feature worktree
pwd | grep -q ".worktrees/" && echo "feature" || echo "main"
```

### Task file lookup

```bash
# Get task ID from branch name
BRANCH=$(git branch --show-current)
TASK_ID=$(echo $BRANCH | sed 's|task/\([0-9]*\)-.*|\1|')

# Find task file in main worktree
ls ../30-para/tasks/task-${TASK_ID}-*.md
```
