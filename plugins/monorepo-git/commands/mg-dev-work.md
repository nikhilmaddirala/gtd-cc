---
name: mg-dev-work
description: Read issue context and implement the plan in the current feature worktree
---

# Work on Issue

## Overview

This command implements the issue plan in the current feature worktree.

CRITICAL: You MUST use the mg-dev skill's `work` sub-skill for this task.


## Context

If the user has provided any additional context, pass that into the skill invocation: $ARGUMENTS


## Process

1. Load the mg-dev skill's `work` sub-skill
2. Execute the work workflow:
   - Extract issue number from branch name
   - Fetch issue and plan from GitHub
   - Implement the plan
   - Commit changes along the way
3. When done, suggest running `/mg-dev-finish`
