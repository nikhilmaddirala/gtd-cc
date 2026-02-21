---
description: Check subtree sync status, diagnose remote configuration, and guide setup
---

# subtrees-status

## Overview

Diagnose the health of subtree remotes and their sync status. Uses convention-over-configuration: every directory in `40-code/41-subtrees/` is a subtree, with remote name `remote-<dirname>`.

The status script answers one question per subtree: is it in sync or not? It does not determine directionality (pull vs push) -- that requires AI judgment in the sync sub-skill.


## Process

### Step 1: Run the status script

```bash
scripts/subtrees-status.sh
```

If the output shows missing remotes (`⚠ No git remote`), re-run with `--setup` to get the setup commands:
```bash
scripts/subtrees-status.sh --setup
```

Example output:
```
PROJECT            REMOTE                    STATUS
───────            ──────                    ──────
asai-youtube       remote-asai-youtube       ✓ Synced
carnatic-abc       remote-carnatic-abc       ✓ Synced
<project-name>     remote-<project-name>     ✗ 11 files differ
gtd-cc             remote-gtd-cc             ✗ 3 files differ
foo                (not configured)          ⚠ No git remote
```

### Step 2: Act on the results

- `✓ Synced` - nothing to do
- `✗ N files differ` - use the sync sub-skill to resolve
- `⚠ No git remote` - remote not configured on this machine; set up with the commands below
- `✗ Fetch failed` - remote configured but not reachable; check auth/network/repo existence

### Step 3: Fix missing remotes

Git remotes are local configuration (stored in `.git/config`), not part of the repo. They must be re-added after cloning on a new machine. The `--setup` flag prints the exact commands needed.

To set up manually:

```bash
# Create the GitHub repo (if it doesn't exist)
gh repo create <project> --private --description "description"

# Add the git remote
git remote add remote-<project> https://github.com/<owner>/<project>.git

# Initial push (use sync sub-skill after setup)
```


## Why `git diff` for sync detection

Subtree split rewrites commits into new SHAs, so the monorepo and remotes never share a common ancestor. `git log A..B` range comparisons don't work (they produce inflated counts like "13,238 commits" for repos that are actually in sync). Instead the script uses `git diff HEAD:<prefix> remote/branch` to compare file trees directly.


## Guidelines

- The filesystem is the source of truth: `ls 41-subtrees/` = list of subtrees
- Remote naming convention: `remote-<dirname>`
- Use `git diff HEAD:<prefix> remote/branch` for sync detection (not `git log` ranges)
- Distinguish between "remote not configured" (setup issue on this machine) and "fetch failed" (auth/network/repo issue)
- Offer to run setup commands with user confirmation
