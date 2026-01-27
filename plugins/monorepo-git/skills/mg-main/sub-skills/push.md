---
description: Push to monorepo remote only (no subtree logic)
---

# Push

## Overview

This sub-skill pushes commits to the monorepo remote only. It does NOT handle subtree pushes - use `/mg-publish` for that.

## Context

User wants to push committed changes to the monorepo. This is a fast operation for daily development velocity.

## Process

### 1. Pre-push check

```bash
git status
```

If uncommitted changes exist: Stop and suggest user commit first with `/mg-commit`.

### 2. Check remote status

```bash
git fetch origin
git log --oneline origin/main..HEAD
```

Show how many commits will be pushed.

### 3. Push monorepo

```bash
git push origin main
```

If rejected (remote has new commits):
```bash
git pull --rebase origin main
# Resolve conflicts if any
git push origin main
```

### 4. Verify

```bash
git status
git log --oneline -3 origin/main
```

Success criteria:
- `git status` shows: "Your branch is up-to-date with 'origin/main'"
- No local commits pending push

## Guidelines

- This sub-skill ONLY pushes to the monorepo remote
- Use `/mg-publish` for subtree operations
- If conflicts occur during rebase, guide user through resolution
- For "push subtrees" requests, redirect to `/mg-publish`
