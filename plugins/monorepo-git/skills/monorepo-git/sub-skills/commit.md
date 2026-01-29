---
description: Analyze changes, create logical commits with conventional format, optionally push
---

# Commit

## Overview

Analyze repository changes, create logical commits using conventional format, and optionally push to remote.

## Process

- Check status
  ```bash
  git status
  git diff --stat
  git log -5 --oneline
  ```

- Group changes logically
  - Subtrees should be in separate commits (never mix different subtree directories)
  - Group related changes together (same feature/fix/topic)
  - Split unrelated changes within the same directory

- Present commit plan BEFORE executing
  - Show recommended grouping with commit messages and file lists
  - Ask: "Does this grouping look good?"
  - ONLY execute after approval

- Commit each group
  ```bash
  git add <files>
  git commit -m "type(scope): description"
  ```
  Types: feat, fix, docs, style, refactor, test, chore

- Verify
  ```bash
  git status
  ```
  Should show "nothing to commit, working tree clean"

- Offer push
  ```bash
  git fetch origin
  git log --oneline origin/main..HEAD
  git push origin main
  ```
  If rejected: `git pull --rebase origin main` then push again.

## Guidelines

- Always get user approval before committing
- If pre-commit hook fails, fix and create NEW commit (never amend)
- Push only affects monorepo remote — for subtrees, use the subtree sub-skill
