---
name: mg-main-start
description: Plan an issue and create an isolated worktree for implementation
---

# Start Issue

## Overview

This command prepares an issue for implementation by creating a plan and worktree.

CRITICAL: You MUST use the mg-main skill's `start` sub-skill for this task.


## Context

User provides issue number. Pass to skill invocation: $ARGUMENTS


## Process

1. Load the mg-main skill's `start` sub-skill
2. Execute the start workflow:
   - Load issue from GitHub
   - Explore codebase and create plan
   - Post plan as issue comment
   - Create worktree and branch
   - Update issue labels
3. Prompt user to cd into worktree
