---
description: Sync worktrees from remote branches across all machines
---

# worktree-sync

## Overview

Sync all worktrees from remote branches. This ensures every worktree that exists on GitHub also exists locally, enabling seamless work across multiple machines.

Git-sync automatically runs this every 2 minutes via systemd/launchd, but you can trigger it manually when:
- Setting up a new machine
- Recovering worktrees after cleanup
- Immediately seeing all active branches without waiting for the timer


## Process

1. Run the sync command:
   ```bash
   monorepo-worktree-sync
   ```

2. The command will:
   - Fetch all remote branches
   - Create local worktrees for any branches that don't exist locally
   - Skip branches that already have worktrees
   - Report how many were created vs skipped

3. List synced worktrees:
   ```bash
   ls ~/.worktrees/
   ```


## Relationship to automatic sync

The `monorepo-worktree-sync` command is exposed as a package by the Nix module. Both manual usage and the automatic service call the same binary:

**Automatic service** (runs every 2 minutes)
- systemd service: `git-sync-worktrees.service` (Linux)
- launchd agent: `git-sync-worktrees` (macOS)
- Calls: `monorepo-worktree-sync`
- Automatically keeps worktrees in sync across all machines

**Manual usage**
- Run: `monorepo-worktree-sync`
- Same binary as the automatic service
- Use when you need immediate results
- Useful for new machines or after `git worktree prune`

Both use identical logic: fetch remote branches, create missing worktrees.


## Guidelines

- Automatic sync runs every 2 minutes via git-sync-worktrees service
- Worktrees are named `<sanitized-branch-name>-<commit-hash>` for uniqueness
- All branches except `main`, `HEAD`, and `origin-HEAD` are synced
- Branch names are sanitized: lowercase, hyphens replace slashes/special chars
