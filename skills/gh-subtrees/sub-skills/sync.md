---
description: Sync subtree between monorepo and standalone GitHub repo with clean commit history
---

# sync

## Overview

Bidirectional sync between monorepo and standalone GitHub repos. The sync process uses rsync to copy the monorepo subtree into a worktree checked out from the remote, then the AI writes clean commit messages based on the diff and monorepo history. It also handles pulling remote-side changes back into the monorepo.

No `git subtree split` is used. Instead:
- Context comes from `git log` on the monorepo subtree path
- Push uses `rsync` to copy the subtree into a worktree checked out from the remote
- The AI writes clean commit messages based on the diff and monorepo history

Critical ordering: always push first, pull second. Writing files to main can trigger git-sync; do not write files to main while a sync worktree exists.


## Process

### Step 0: Preflight checks

Before any sync decisions, ensure the workspace is safe.

```bash
PREFIX=40-code/41-subtrees/<name>
REMOTE=remote-<name>

# Must run from monorepo root on main
git branch --show-current

# Never leave staged changes on main (git-sync expects clean index)
git diff --cached --quiet || {
  echo "Staged changes detected. Unstage first."; exit 1;
}

# Do not mix unrelated local edits in the subtree path
git diff --quiet -- "$PREFIX" || {
  echo "Uncommitted local edits under $PREFIX. Resolve first."; exit 1;
}
```

### Step 1: Context gathering and snapshot

Before any sync decisions, build a full picture of the subtree's state.

```bash
PREFIX=40-code/41-subtrees/<name>
REMOTE=remote-<name>

# Fetch remote
git fetch "$REMOTE"

# Detect default branch from fetched refs first
if git symbolic-ref -q --short "refs/remotes/$REMOTE/HEAD" >/dev/null; then
  BRANCH=$(git symbolic-ref --short "refs/remotes/$REMOTE/HEAD" | sed "s#^$REMOTE/##")
elif git rev-parse --verify "$REMOTE/main" &>/dev/null; then
  BRANCH=main
elif git rev-parse --verify "$REMOTE/master" &>/dev/null; then
  BRANCH=master
else
  BRANCH=main
fi

# 1. What's different between monorepo and remote?
git diff --name-status -M -C "HEAD:$PREFIX" "$REMOTE/$BRANCH"

# 2. Monorepo history for this subtree (recent changes with diffs)
git log --oneline -p -- "$PREFIX"
```

Read the diff and history to understand:
- What files were added, modified, or deleted in the monorepo and roughly why
- Whether files absent from monorepo were intentionally deleted vs never existed there
- How to group and describe changes for clean commit messages later

The `--name-status` output gives status codes:
- `D` = exists in monorepo path, absent in remote path
- `A` = exists in remote path, absent in monorepo path
- `M` = exists on both sides, content differs
- `R`/`C` = rename/copy detected by Git; treat as path-level changes and classify both old and new paths

### Step 2: Classify changes by direction

For each status, determine which side is the source of truth.

Create four lists:
- `PUSH_ADD_OR_UPDATE`: apply monorepo content to remote
- `PUSH_DELETE`: delete path on remote
- `PULL_ADD_OR_UPDATE`: copy remote content into monorepo
- `PULL_DELETE`: delete path in monorepo

Use this decision table:

```bash
# helpers: epoch timestamp of latest path change on each side
MONO_TS=$(git log -1 --format=%ct -- "$PREFIX/<path>" || true)
REMOTE_TS=$(git log -1 --format=%ct "$REMOTE/$BRANCH" -- "<path>" || true)

# explicit deletion checks
MONO_DEL_TS=$(git log --diff-filter=D -1 --format=%ct -- "$PREFIX/<path>" || true)
REMOTE_DEL_TS=$(git log --diff-filter=D -1 --format=%ct "$REMOTE/$BRANCH" -- "<path>" || true)
```

- `A` (remote-only path)
  - monorepo has explicit deletion newer than remote path change -> `PUSH_DELETE`
  - otherwise -> `PULL_ADD_OR_UPDATE`

- `D` (monorepo-only path)
  - remote has explicit deletion newer than monorepo path change -> `PULL_DELETE`
  - otherwise -> `PUSH_ADD_OR_UPDATE`

- `M` (both exist, differ)
  - `MONO_TS > REMOTE_TS` -> `PUSH_ADD_OR_UPDATE`
  - `REMOTE_TS > MONO_TS` -> `PULL_ADD_OR_UPDATE`
  - equal/missing timestamps -> ambiguous, ask user

- `R`/`C`
  - classify old/new paths independently using the same rules

If classification is ambiguous for any path, stop and ask the user with a concise path list and proposed default.

If both push and pull lists are empty, sync is complete.

### Step 3: Push (monorepo -> remote)

Skip this step if both push lists are empty.

Create a worktree from the remote HEAD:

```bash
STAMP=$(date +%Y%m%d-%H%M)
SYNC_BRANCH=sync-<name>-$STAMP
WT=.worktrees/$SYNC_BRANCH
git worktree add "$WT" -b "$SYNC_BRANCH" "$REMOTE/$BRANCH"
```

Build an exclude file from all pull-list paths so rsync does not overwrite remote-newer paths.

Rsync the monorepo subtree into the worktree:

```bash
EXCLUDES_FILE=$(mktemp)
# write one pattern per line into $EXCLUDES_FILE from pull lists

rsync -a --delete --exclude='.git' --exclude-from="$EXCLUDES_FILE" \
  "$PREFIX/" "$WT/"
```

Use directory-level patterns (trailing slash) only when the full directory is remote-owned. Use file-level patterns for individual files.

Stage and review:

```bash
git -C "$WT" add -A
git -C "$WT" diff --cached --stat   # Summary of changes
git -C "$WT" diff --cached           # Full diff for commit message context
```

Verify the staged diff only contains push-list changes. If pull-list paths appear, fix excludes and restage before committing.

Write a clean commit message using:
- The staged diff (what changed)
- The monorepo git log from Step 0 (why it changed)
- Group related changes if the diff is large
- Only describe monorepo changes; do not mention remote-side changes

Get user approval, then push. Default is direct push to the remote default branch. If the user requested a PR (for example: `sync gtd-cc --pr`), push to a separate branch and open a PR.

Direct push (default):

```bash
git -C "$WT" push "$REMOTE" "$SYNC_BRANCH:$BRANCH"
```

PR flow (when user requests it):

```bash
# Push sync branch as its own remote branch
git -C "$WT" push "$REMOTE" "$SYNC_BRANCH:$SYNC_BRANCH"

# Extract repo slug from remote URL for gh CLI
REPO_URL=$(git remote get-url "$REMOTE")
REPO_SLUG=$(echo "$REPO_URL" | sed 's|.*github.com/||; s|\.git$||')

# Create PR
gh pr create --repo "$REPO_SLUG" --head "$SYNC_BRANCH" --base "$BRANCH" --title "..." --body "..."
```

Clean up the worktree immediately after push:

Direct push cleanup:

```bash
git worktree remove "$WT"
git branch -D "$SYNC_BRANCH"
```

PR cleanup (keep branch until merged):

```bash
git worktree remove "$WT"
```

### Step 4: Pull (remote -> monorepo)

Only after the push worktree is fully removed. Skip if both pull lists are empty.

For `PULL_ADD_OR_UPDATE`, copy from a temporary remote worktree using rsync (preserves mode and symlinks better than shell redirection).

```bash
PULL_WT=.worktrees/pull-<name>-$(date +%Y%m%d-%H%M)
git worktree add --detach "$PULL_WT" "$REMOTE/$BRANCH"

# for each path in PULL_ADD_OR_UPDATE
mkdir -p "$PREFIX/$(dirname <path>)"
rsync -a "$PULL_WT/<path>" "$PREFIX/<path>"

# for each path in PULL_DELETE
rm -rf "$PREFIX/<path>"

git worktree remove "$PULL_WT"
```

Git-sync will pick up the new/updated files on main automatically.

### Step 5: Verify

```bash
scripts/subtrees-status.sh
```

If Step 4 wrote files to main, status may still show differences until those changes are committed. Re-run verification after git-sync commit (or after a manual commit).


## Guidelines

- NEVER `cd` into the worktree; always use `git -C "$WT"` (avoids fatal cwd errors on cleanup)
- NEVER write files to main while a sync worktree exists
- NEVER leave staged changes on main
- Use worktrees so main stays checked out
- Get user approval before pushing
- One clean commit per sync is fine; multiple commits only if changes are clearly separable
- Treat `A/D/M/R/C` as direction-analysis inputs; do not assume monorepo is always newer
