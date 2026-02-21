---
description: Move project from lab to subtrees and initialize git-subrepo tracking
---

# graduate

## Overview

Graduate a project from `40-code/42-lab/` to `40-code/41-subtrees/`, create the GitHub repo, then initialize the project as a `git-subrepo` managed subdir.

## Process

### Step 1: Gather info

Get from user:

- project name (directory in `40-code/42-lab/`)
- visibility (`--public` or `--private`)
- optional owner/org

Validate source exists:

```bash
ls 40-code/42-lab/<project>
```

### Step 2: Create GitHub repo

```bash
gh repo create <project> --public|--private --description "..." [--owner <owner>]
```

### Step 3: Move and commit

```bash
git mv 40-code/42-lab/<project> 40-code/41-subtrees/<project>
git commit -m "feat(<project>): graduate to subtrees"
```

### Step 4: Register remote

```bash
git remote add remote-<project> <repo-url>.git
```

Also add or update the URL in `40-code/41-subtrees.yaml` under `remotes:`.

### Step 5: Initialize subrepo tracking

```bash
SUBDIR=40-code/41-subtrees/<project>
git subrepo init "$SUBDIR" -r <repo-url> -b main
```

Commit the new `.gitrepo` file if not already committed.

### Step 6: Initial push

```bash
git subrepo push "$SUBDIR"
```

Use PR-based push flow if requested by user policy.

### Step 7: Verify

```bash
git subrepo status "$SUBDIR"
scripts/subrepo-status.sh
gh repo view <project> --web
```

Present to user:

- new path in `41-subtrees/`
- GitHub URL
- remote name
- that future updates should use the `sync` sub-skill

## Guidelines

- Commit the move before subrepo initialization
- Keep remote naming convention as `remote-<project>`
- Do not mix old rsync-sync steps with subrepo-managed projects
