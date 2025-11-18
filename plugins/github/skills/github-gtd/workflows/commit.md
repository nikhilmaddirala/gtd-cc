---
description: Create a git commit with conventional message format
allowed_tools:
  - Bash(git add:*)
  - Bash(git status:*)
  - Bash(git commit:*)
---

## Overview

Help create well-structured git commits with descriptive conventional format messages that clearly communicate the intent of changes.

## Context

Repository state:
- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your Task

**Goal**: Commit all uncommitted changes with descriptive conventional commit messages.

**Process**:
1. Understand the git context and changes made
2. Determine appropriate commit structure (usually 1 commit, but up to 2-3 if significant changes warrant separation)
3. Create commits with clear, conventional format messages
4. Ensure all uncommitted changes are committed

## Guidelines

- Keep commits focused and logical
- Use conventional commit format (e.g., `feat:`, `fix:`, `docs:`, `refactor:`)
- Keep messages concise but descriptive
- Generally aim for a single commit; use multiple commits only when changes are distinct in purpose

## Success Criteria

- ✅ All uncommitted changes are committed
- ✅ Commit messages follow conventional format
- ✅ Number of commits is minimal (1-3 maximum)
