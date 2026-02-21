---
description: Move project from lab to subtrees with GitHub repo and subtree setup
---

# graduate

## Overview

Graduate a project from `42-lab/` (experiments) to `41-subtrees/` (production). Create a GitHub repository, register the subtree remote, and initialize it using the sync workflow.


## Process

### Step 1: Gather info

Get from user:
- Project name (directory in `42-lab/`)
- GitHub visibility (`--public` or `--private`)

Optional:
- GitHub owner/org (if not default account)

Validate the source exists:
```bash
ls 40-code/42-lab/<project>
```

### Step 2: Create GitHub repo

```bash
gh repo create <project> --public|--private --description "..." [--owner <owner>]
```

### Step 3: Move and commit

Move the directory, then commit. The commit MUST happen before subtree setup.

```bash
git mv 40-code/42-lab/<project> 40-code/41-subtrees/<project>
git commit -m "feat(<project>): graduate to subtrees"
```

### Step 4: Register subtree remote

```bash
git remote add remote-<project> <repo-url>.git
```

Also record/update the remote URL in `40-code/41-subtrees.yaml` under `remotes:`.

### Step 5: Initialize remote content via sync

Do not use `git subtree push`.

Use the `sync` sub-skill to perform the initial push from monorepo to standalone repo:

```bash
# Run the sync workflow for the new project
# Expected result: push list contains project files, pull list is empty
```

If the user prefers PR-based initialization, use the sync PR flow instead of direct push.

### Step 6: Verify

```bash
gh repo view <project> --web
git remote get-url remote-<project>
scripts/subtrees-status.sh
```

Present to user: new location, GitHub URL, remote name, and that future updates run through the `sync` sub-skill.


## Guidelines

- CRITICAL: Commit the move BEFORE setting up the subtree remote
- Follow `remote-<project>` naming convention
- Do not use `git subtree push` in this workflow
- If the GitHub repo already has meaningful commits, run `sync` with direction analysis and user confirmation before first push
