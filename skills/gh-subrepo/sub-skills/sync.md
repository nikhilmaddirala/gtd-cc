---
description: Sync an existing subrepo between monorepo subdir and standalone GitHub repository
---

# sync

## Overview

Use `git-subrepo` commands for bidirectional sync:

- pull collaborator changes from standalone repo into monorepo subdir
- push local monorepo subdir changes back upstream

This replaces custom file-level reconciliation with commit-aware sync state.

## Process

### Step 0: Preflight checks

```bash
SUBDIR=40-code/41-subtrees/<name>

git branch --show-current
git diff --cached --quiet || { echo "Staged changes detected on main"; exit 1; }
test -f "$SUBDIR/.gitrepo" || { echo "$SUBDIR is not initialized as subrepo"; exit 1; }

# Clean up any leftover artifacts from previous operations
git subrepo clean "$SUBDIR" --force 2>/dev/null || true
```

If there are uncommitted edits in the subdir, either commit first or confirm that the sync should include them.

### Step 1: Inspect status

```bash
git subrepo status --fetch "$SUBDIR"
```

Check if `Upstream Ref` differs from `Pulled Commit` — this indicates remote changes you need to pull.

### Step 2: Handle mixed commits (if present)

If you have local commits that touch both the subrepo AND other files in the monorepo, ask the user:

- "Do you want clean history in the standalone repo? (y/n)"

If yes, use the worktree cleanup pattern documented in `references/manual-workflow.md` under "Clean Push with Mixed Commits (Worktree Pattern)". This creates clean, focused commits for the standalone repository.

If no, proceed with normal push — the standalone repo will have the mixed commit history including unrelated files and commit messages.

### Step 3: Pull first

Always pull before push so collaborator changes are integrated first.

```bash
git subrepo pull "$SUBDIR"
```

If pull reports conflicts, resolve them using normal git conflict flow:

```bash
git status                      # See conflicts
edit conflicted files           # Fix them
git add resolved files          # Stage them
git subrepo commit "$SUBDIR"    # Complete the pull
```

See `references/manual-workflow.md` "Pulling Remote Changes" section for full details.

### Step 4: Push second

If local commits exist after pull and the user wants them upstream:

```bash
git subrepo push "$SUBDIR"
```

Get user approval before push.

### Step 5: Clean up artifacts

```bash
git subrepo clean "$SUBDIR" --force
```

### Step 6: Verify

```bash
git subrepo status "$SUBDIR"
scripts/subrepo-status.sh
```

If operating on monorepo `main`, remember git-sync may add follow-up auto-commits shortly after changes are written.

## Guidelines

- Prefer `git subrepo pull` then `git subrepo push` for regular sync
- Avoid custom timestamp heuristics for direction decisions
- Keep monorepo main index unstaged
- Use PR-based upstream flow if user asks for reviewable sync changes
