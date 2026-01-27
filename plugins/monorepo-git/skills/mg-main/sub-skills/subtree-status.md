---
description: Show sync status between monorepo and all subtree remotes
---

# Subtree Status

## Overview

This sub-skill shows the sync status for all subtree remotes. It displays pending (local) and incoming (remote) commit counts to help users understand what needs to be published or pulled.

## Context

User wants to see which subtrees are in sync, which have pending changes, and which need to pull from upstream.

## Process

### 1. Detect subtree remotes

```bash
git remote -v | grep "remote-"
```

List all remotes matching the subtree pattern (default: `remote-*`).

### 2. Map remotes to directories

For each subtree remote, find its directory:

```bash
# Search commit history for subtree directory mapping
git log --all --grep="git-subtree-dir:" --pretty=format:"%s" | grep "remote-name"
```

### 3. Check sync status for each subtree

For each subtree:

```bash
# Fetch latest from remote
git fetch remote-name

# Count pending commits (local changes not in remote)
git log --oneline remote-name/main..HEAD -- path/to/directory/ | wc -l

# Count incoming commits (remote changes not in local)
git log --oneline HEAD..remote-name/main | wc -l
```

### 4. Present status table

```
Subtree Sync Status
===================

Subtree          | Directory              | Pending | Incoming | Status
-----------------|------------------------|---------|----------|----------------
project-a        | path/to/project-a      | 5       | 0        | Ready to publish
project-b        | path/to/project-b      | 12      | 3        | Pull first
project-c        | path/to/project-c      | 0       | 0        | Synced
config-repo      | path/to/config         | 0       | 2        | Pull available

Legend:
  Pending  = Local commits not yet pushed to subtree remote
  Incoming = Remote commits not yet pulled into monorepo
```

### 5. Action prompts

Based on status, suggest next actions:

- **Ready to publish**: Has pending commits, no incoming
  > "Run `/mg-publish` to publish changes"

- **Pull first**: Has both pending and incoming
  > "Run `/mg-subtree pull <name>` before publishing"

- **Synced**: No pending, no incoming
  > "No action needed"

- **Pull available**: No pending, has incoming
  > "Run `/mg-subtree pull <name>` to sync upstream changes"

## Guidelines

- Always fetch before checking status to get accurate counts
- Show directory paths to help user understand the mapping
- If a remote can't be fetched (network/auth issue), show error but continue with others
- Keep table format concise and scannable
