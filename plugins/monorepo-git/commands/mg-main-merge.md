---
name: mg-main-merge
description: Merge a PR via GitHub and cleanup the worktree
---

# Merge Issue

## Overview

This command merges a completed PR and cleans up the worktree.

CRITICAL: You MUST use the mg-main skill's `merge` sub-skill for this task.


## Context

User provides issue number. Pass to skill invocation: $ARGUMENTS


## Process

1. Load the mg-main skill's `merge` sub-skill
2. Execute the merge workflow:
   - Find and merge PR via `gh pr merge`
   - Remove worktree and local branch
   - Issue auto-closes via "Closes #N" in PR
3. Suggest push and publish
