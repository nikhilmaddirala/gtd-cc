---
description: Show quick working tree status for the monorepo
---

# Status

## Overview

This sub-skill provides a quick git status overview focused on the working tree. For subtree sync status, use `/mg-subtree-status`.

## Context

User wants to see the current state of the repository before committing or pushing.

## Process

### 1. Basic status

```bash
git status
git log --oneline -5
git branch -vv
```

### 2. Changed files summary

```bash
# Show changes grouped by top-level directory
git status --short
```

Present a concise summary:
- Staged changes (ready to commit)
- Unstaged modifications
- Untracked files

### 3. Action prompt

Based on state, suggest next action:

- If there are staged or unstaged changes:
  > "Run `/mg-commit` to commit these changes"

- If working directory is clean but ahead of origin:
  > "Run `/mg-push` to push commits"

- If working directory is clean and up-to-date:
  > "Working directory clean, nothing to do"

- If user asks about subtrees:
  > "For subtree sync status, run `/mg-subtree-status`"

## Guidelines

- Keep output brief and actionable
- Always provide a clear next-step prompt
- Do NOT check subtree sync state here (use `/mg-subtree-status` for that)
- Focus on working tree status for quick daily checks
