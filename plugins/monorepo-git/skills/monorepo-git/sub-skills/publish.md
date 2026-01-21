---
description: Curated push to selected subtrees with interactive selection
---

# Publish

## Overview

This sub-skill provides curated subtree publishing. It shows which subtrees have pending changes and lets the user choose which to publish. This is a deliberate operation for sharing batched work with external repos.

## Context

User wants to push changes to subtree remotes. Unlike daily monorepo pushes, this is a curated operation where the user selects which subtrees to sync.

## Process

### 1. Pre-publish check

```bash
git status
```

If uncommitted changes exist: Stop and suggest user commit first.

If local is behind origin: Suggest push monorepo first with `/mg-push`.

### 2. Detect subtree remotes

```bash
git remote -v | grep "remote-"
```

Identify all subtree remotes (pattern: `remote-*` or configured prefix).

### 3. Check pending changes per subtree

For each subtree remote, find its directory and check pending commits:

```bash
# Find directory from git history
git log --all --grep="git-subtree-dir:" --pretty=format:"%s" | grep -E "remote-name"

# Check pending commits for that directory
git log --oneline remote-name/main..HEAD -- path/to/directory/
```

### 4. Present interactive selection

Display subtrees with pending changes:

```
Subtrees with pending changes:

  [1] project-a (5 commits)
      - feat: add user templates
      - fix: resolve auth issue
      - docs: update readme

  [2] project-b (12 commits)
      - refactor: reorganize modules
      - feat: add new feature
      - ...and 10 more

  [3] project-c (2 commits)
      - chore: update config
      - docs: add examples

Which to publish? (1,2,3,all,none):
```

Wait for user selection.

### 5. Publish selected subtrees

For each selected subtree:

```bash
# Check for incoming changes first
git fetch remote-name
git log --oneline HEAD..remote-name/main -- path/to/directory/
```

If remote has new commits, ask user:
> "Remote has new commits. Pull first? (y/n)"

If yes:
```bash
git subtree pull --prefix=path/to/directory remote-name main --squash
```

Then push:
```bash
git subtree push --prefix=path/to/directory remote-name main
```

IMPORTANT: Use ONLY `git subtree push`. Never use `git subtree split` + `git push`.

If push fails with "creates a split": No changes for this subtree, skip it.

### 6. Summary

After publishing, show results:

```
Published:
  - project-a (5 commits) - success
  - project-b (12 commits) - success

Skipped:
  - project-c - no changes
```

## Guidelines

- Always show pending commit count and summaries before publishing
- Let user choose which subtrees to publish (don't auto-publish all)
- Handle conflicts gracefully with pull-first option
- Use `--squash` on pulls to keep history clean
- If no subtrees have changes, inform user and exit
