---
description: Plan a task and create an isolated worktree for implementation
---

# Start

## Overview

Prepares a task for implementation: explores codebase, creates plan, sets up worktree.


## Context

User has a task and wants to start working on it. Task file must exist in `30-para/tasks/`.


## Process

1. Load task file
   ```bash
   TASK_FILE=$(ls 30-para/tasks/task-{id}-*.md)
   ```
   - Extract goal and context

2. Explore and plan
   - Read relevant code based on task description
   - Identify files to modify
   - Create implementation plan in task file under `## Plan` section

3. Create worktree
   ```bash
   git branch task/{id}-{slug} main
   git worktree add .worktrees/task-{id} task/{id}-{slug}
   ```

4. Update task frontmatter
   - Set `task-status: doing`
   - Add `git-branch` and `git-worktree` fields

5. Verification: Worktree created and user prompted to cd into it


## Guidelines

- Always create plan before worktree
- Worktree directory: `.worktrees/task-{id}`
- Branch naming: `task/{id}-{slug}`
