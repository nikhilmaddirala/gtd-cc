#!/usr/bin/env bash
#
# rebase.sh - Smart squash-rebase onto main
#
# Squashes all feature branch commits into one, then rebases that single
# commit onto origin/main. This avoids the "conflict minefield" that happens
# when rebasing many git-sync noise commits one by one.
#
# Usage:
#   rebase.sh                    # Run from inside a worktree
#   rebase.sh <worktree-path>    # Run from anywhere
#
set -euo pipefail

# Determine working directory
if [ -n "${1:-}" ] && [ -d "$1" ]; then
  cd "$1"
elif [ -n "${1:-}" ]; then
  echo "Error: Directory not found: $1"
  exit 1
fi

# Verify we're on a feature branch, not main
branch=$(git branch --show-current 2>/dev/null || echo "")
if [ -z "$branch" ]; then
  echo "Error: Not on a branch (detached HEAD or mid-rebase?)"
  echo ""
  echo "If a previous rebase was interrupted:"
  echo "  git rebase --abort"
  exit 1
fi

if [ "$branch" = "main" ]; then
  echo "Error: Cannot rebase main onto itself"
  exit 1
fi

# Fetch latest main
echo "Fetching origin/main..."
git fetch origin main

# Check if we're already up to date
behind=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")
if [ "$behind" = "0" ]; then
  echo "Already up to date with origin/main."
  exit 0
fi

# Find the merge base (where this branch diverged from main)
merge_base=$(git merge-base HEAD origin/main)
ahead=$(git rev-list --count "$merge_base"..HEAD)

echo "Branch: $branch"
echo "  $ahead commit(s) ahead of merge-base"
echo "  $behind commit(s) behind origin/main"

if [ "$ahead" = "0" ]; then
  echo "No commits to rebase. Fast-forwarding..."
  git rebase origin/main
  echo ""
  echo "Rebase complete. Push with:"
  echo "  git push --force-with-lease"
  exit 0
fi

# Commit any uncommitted changes first
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Committing uncommitted changes..."
  git add -A
  git commit -m "chore: save uncommitted changes before rebase"
  ahead=$((ahead + 1))
fi

# Squash all feature commits into one
echo ""
echo "Squashing $ahead commit(s) into one..."
git reset --soft "$merge_base"
git commit -m "squash: all feature work on $branch (squashed from $ahead commits)"

# Rebase the single commit onto main
echo "Rebasing single commit onto origin/main..."
if ! git rebase origin/main; then
  echo ""
  echo "Conflict detected during rebase."
  echo "Resolve conflicts, then:"
  echo "  git add -A && git rebase --continue"
  echo "  git push --force-with-lease"
  exit 1
fi

echo ""
echo "Rebase successful."
echo "  git push --force-with-lease"
