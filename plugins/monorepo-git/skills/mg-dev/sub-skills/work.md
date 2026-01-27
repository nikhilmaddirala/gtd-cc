---
description: Read task context and implement the plan in the feature worktree
---

# Work

## Overview

Read the linked task file and implement the plan created during `mg-main/start.md`.


## Context

User has a feature worktree with a plan ready. They want to implement the task.


## Process

1. Find linked task file
   ```bash
   BRANCH=$(git branch --show-current)
   TASK_ID=$(echo $BRANCH | sed 's|task/\([0-9]*\)-.*|\1|')
   TASK_FILE=$(ls ../30-para/tasks/task-${TASK_ID}-*.md)
   ```

2. Read task context
   - Goal section
   - Plan section (created by start.md)

3. Implement the plan
   - Make changes as specified
   - Use `commit.md` to commit logical chunks

4. Verification: All plan items implemented and committed


## Guidelines

- Follow the plan created during `/mg-start`
- Commit frequently in logical chunks
- Keep commits focused and conventional
