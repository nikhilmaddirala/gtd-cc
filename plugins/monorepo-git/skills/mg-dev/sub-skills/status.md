---
description: Show branch status and linked task info in feature worktree
---

# Status

## Overview

Show current branch status with task context.


## Context

User wants to see progress in their feature worktree.


## Process

1. Show branch status
   ```bash
   git status --short
   git log main..HEAD --oneline
   ```

2. Show linked task info
   - Find task file via branch name
   - Display task title and status

3. Verification: Status displayed with task context


## Guidelines

- Focus on what's changed since branching from main
- Show task context for orientation
- Suggest next action based on state
