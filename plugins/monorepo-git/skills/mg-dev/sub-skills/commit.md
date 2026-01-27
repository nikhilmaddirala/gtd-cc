---
description: Create conventional commits in feature worktree
---

# Commit

## Overview

Create conventional commits during development. No warnings needed - we're in a feature branch.


## Context

User has changes to commit while working in a feature worktree.


## Process

1. Check changes
   ```bash
   git status --short
   git diff --stat
   ```

2. Stage and commit
   ```bash
   git add -A
   git commit -m "type(scope): description"
   ```

3. Verification: Commit created successfully


## Guidelines

- Use conventional commit format: `type(scope): description`
- Types: feat, fix, refactor, docs, chore
- Commit frequently in logical chunks
- No warnings about main branch (we're in feature worktree)
