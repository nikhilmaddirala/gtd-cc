---
name: mg-dev-finish
description: Finalize work in feature worktree - commit, push, create PR
---

# Finish Task

## Overview

This command finalizes work by creating a pull request.

CRITICAL: You MUST use the mg-dev skill's `finish` sub-skill for this task.


## Context

If the user has provided any additional context, pass that into the skill invocation: $ARGUMENTS


## Process

1. Load the mg-dev skill's `finish` sub-skill
2. Execute the finish workflow:
   - Final commit if needed
   - Push branch to remote
   - Create pull request
3. Display PR URL and suggest switching to main for merge
