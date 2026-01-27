---
description: Finalize work in feature worktree - commit, push, create PR
---

# Finish

## Overview

Finalize work in the current feature worktree by creating a pull request. Does NOT merge or touch main.


## Context

User has completed implementation and wants to prepare for merge.


## Process

1. Final commit (if uncommitted changes exist)
   ```bash
   git add -A
   git commit -m "type(scope): final changes"
   ```

2. Push branch to remote
   ```bash
   git push -u origin $(git branch --show-current)
   ```

3. Create pull request
   ```bash
   gh pr create --fill
   ```

4. Verification: PR created and URL displayed to user


## Guidelines

- NEVER switch worktrees or touch main branch
- PR is the signal that work is ready for review/merge
- Use `--draft` flag if work needs review before merge
