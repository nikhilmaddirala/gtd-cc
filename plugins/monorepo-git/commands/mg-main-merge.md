---
name: mg-main-merge
description: Merge a feature branch to main and cleanup the worktree
---

# Merge Task

## Overview

This command merges a completed feature branch and cleans up.

CRITICAL: You MUST use the mg-main skill's `merge` sub-skill for this task.


## Context

User provides task ID. Pass to skill invocation: $ARGUMENTS


## Process

1. Load the mg-main skill's `merge` sub-skill
2. Execute the merge workflow:
   - Merge feature branch to main
   - Remove worktree and branch
   - Update task status to done
3. Suggest push and publish
