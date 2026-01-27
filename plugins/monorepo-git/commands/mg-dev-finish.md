---
name: mg-dev-finish
description: Finalize work in feature worktree - commit, push, create PR linked to issue
---

# Finish Issue

## Overview

This command finalizes work by creating a pull request linked to the issue.

CRITICAL: You MUST use the mg-dev skill's `finish` sub-skill for this task.


## Context

If the user has provided any additional context, pass that into the skill invocation: $ARGUMENTS


## Process

1. Load the mg-dev skill's `finish` sub-skill
2. Execute the finish workflow:
   - Final commit if needed
   - Push branch to remote
   - Create pull request with "Closes #N"
   - Update issue label to status-review
3. Display PR URL and suggest switching to main for merge
