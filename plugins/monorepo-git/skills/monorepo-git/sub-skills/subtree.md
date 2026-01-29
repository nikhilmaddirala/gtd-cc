---
description: Subtree CRUD, sync status, and curated publishing
---

# Subtree

## Overview

Manage Git subtrees: add, list, pull, move, remove, check sync status, and publish changes to subtree remotes.

## Process

Route based on user intent:

### Add subtree

- Gather: GitHub repo URL, target directory, remote name (`remote-<name>`)
  ```bash
  git remote add remote-name https://github.com/user/repo.git
  git subtree add --prefix=path/to/directory remote-name main --squash
  ```

### List subtrees

- Detect remotes and map to directories
  ```bash
  git remote -v | grep "remote-"
  ```
- Read `.monorepo-git.yaml` for mappings, or fall back to git history:
  ```bash
  git log --all --grep="git-subtree-dir:" --pretty=format:"%B" | grep "git-subtree-dir:" | sort -u
  ```

### Pull changes

```bash
git fetch remote-name main
git subtree pull --prefix=path/to/directory remote-name main --squash
```

### Move subtree

```bash
git mv path/to/old path/to/new
git commit -m "chore(name): move from old-path to new-path"
```

### Remove subtree

- Create backup, require explicit "yes" confirmation
  ```bash
  cp -r path/to/directory /tmp/subtree-backup-$(date +%Y%m%d-%H%M%S)
  git rm -r path/to/directory/
  git remote remove remote-name
  git commit -m "chore(name): remove subtree"
  ```

### Check sync status

For each subtree remote:
```bash
git fetch remote-name
git log --oneline remote-name/main..HEAD -- path/to/directory/ | wc -l   # pending
git log --oneline HEAD..remote-name/main | wc -l                          # incoming
```

Present as table with status (Synced / Ready to publish / Pull first / Pull available).

### Publish to subtrees

- Pre-check: no uncommitted changes, monorepo pushed
- Show subtrees with pending changes
- Let user select which to publish
- For each selected:
  ```bash
  git fetch remote-name
  git subtree push --prefix=path/to/directory remote-name main
  ```
  If remote has new commits, offer to pull first with `--squash`.

## Guidelines

- CRITICAL: Always resolve directory prefix from `.monorepo-git.yaml` or git history. Never guess.
- NEVER use `git push remote-name main` for subtrees — always use `git subtree push --prefix=<dir>`
- Always use `--squash` on pulls
- Let user choose which subtrees to publish (don't auto-publish all)
- If prefix cannot be resolved, STOP and ask the user
