---
name: mg-main-start
description: Plan a task and create an isolated worktree for implementation
---

# Start Task

## Overview

This command prepares a task for implementation by creating a plan and worktree.

CRITICAL: You MUST use the mg-main skill's `start` sub-skill for this task.


## Context

User provides task ID. Pass to skill invocation: $ARGUMENTS


## Process

1. Load the mg-main skill's `start` sub-skill
2. Execute the start workflow:
   - Load task file
   - Explore codebase and create plan
   - Create worktree and branch
   - Update task status
3. Prompt user to cd into worktree
