---
description: Merge a feature branch to main and cleanup the worktree
---

# Merge

## Overview

Merge a completed feature branch into main and clean up the worktree. Run from main worktree only.


## Context

User has a PR ready (created by `mg-dev/finish.md`) and wants to merge it.


## Process

1. Identify task
   - From task ID, find branch: `task/{id}-{slug}`
   - Find worktree: `.worktrees/task-{id}`

2. Merge branch
   ```bash
   git merge task/{id}-{slug} --no-ff -m "Merge task/{id}-{slug}"
   ```

3. Cleanup
   ```bash
   git worktree remove .worktrees/task-{id}
   git branch -d task/{id}-{slug}
   ```

4. Update task file
   - Set `task-status: done`
   - Remove `git-branch` and `git-worktree` fields

5. Verification: Branch merged, worktree removed, task marked done


## Guidelines

- Only run from main worktree
- Use `--no-ff` to preserve merge history
- Clean up worktree and branch after merge
