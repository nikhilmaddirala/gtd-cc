---
description: Check subrepo setup and sync health for projects in 40-code/41-subtrees/
---

# subrepo-status

## Overview

Diagnose whether projects in `40-code/41-subtrees/` are subrepo-managed and whether they appear healthy.

## Process

### Step 1: Run native status command

```bash
git subrepo status --all --fetch
```

Use native `git subrepo status` as the primary source of truth. The `--fetch` flag fetches latest from remote and shows whether local is behind upstream by comparing `Upstream Ref` with `Pulled Commit`.

### Step 2: Optional quick check

```bash
scripts/subrepo-status.sh
```

The script is a thin wrapper that runs `git subrepo status --all --fetch` with a header. Use it when you want the status output formatted for monorepo projects.

### Step 3: Handle common outcomes

- managed and clean: no action needed
- managed and diverged: run the sync sub-skill
- unmanaged project: use graduate sub-skill or run `git subrepo init`
- git-subrepo missing: install or enable it first

### Step 4: Optional detailed view

```bash
git subrepo status --all --verbose
```

Use this when you need extra context about local and upstream commits.

## Guidelines

- Treat `git subrepo status` as the source of truth for managed projects
- Keep compatibility with existing `remote-<project>` naming when adding remotes
- Offer to run next-step sync commands after showing status
