#!/usr/bin/env bash
#
# work.sh - Ensure worktree + draft PR exist for an issue
#
# Idempotent: converges to the correct state regardless of what
# already exists (worktree, branch, PR). Safe to run multiple times.
#
# Usage:
#   work.sh <issue-number>           # Create or resume worktree + PR
#   work.sh --resume <branch>        # Resume by branch name (orphan PR recovery)
#
set -euo pipefail
export GH_PAGER=""

MONOREPO_DIR=~/repos/monorepo
WORKTREES_DIR=$MONOREPO_DIR/.worktrees

slugify() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-' | cut -c1-30
}

# ── Ensure worktree + PR for issue ────────────────────────────
# Checks what already exists and only creates what's missing.
ensure_worktree_for_issue() {
  local issue_number="$1"

  cd "$MONOREPO_DIR"
  git fetch origin

  echo "Fetching issue #${issue_number}..."
  local title
  title=$(gh issue view "$issue_number" --json title -q '.title')

  if [ -z "$title" ]; then
    echo "Error: Issue #${issue_number} not found"
    exit 1
  fi

  local slug
  slug=$(slugify "$title")
  local branch="issue-${issue_number}-${slug}"

  # ── Step 1: Ensure worktree exists ──

  local worktree_created=false

  if [ -d "$WORKTREES_DIR/$branch" ]; then
    echo "Worktree exists: .worktrees/$branch"
  elif git show-ref --verify --quiet "refs/remotes/origin/$branch" 2>/dev/null; then
    echo "Branch exists on remote, recreating worktree..."
    git worktree add "$WORKTREES_DIR/$branch" "$branch" 2>/dev/null || \
      git worktree add "$WORKTREES_DIR/$branch" -b "$branch" "origin/$branch"
    worktree_created=true
  else
    echo "Creating worktree and branch: $branch"
    git worktree add "$WORKTREES_DIR/$branch" -b "$branch" main
    worktree_created=true
  fi

  # ── Step 2: Ensure branch is pushed ──

  cd "$WORKTREES_DIR/$branch"

  if ! git show-ref --verify --quiet "refs/remotes/origin/$branch" 2>/dev/null; then
    # Branch not on remote yet — push it
    # Need at least one commit ahead of main for PR creation
    local ahead
    ahead=$(git rev-list --count main..HEAD 2>/dev/null || echo "0")
    if [ "$ahead" = "0" ]; then
      git commit --allow-empty -m "chore: initialize branch for issue #${issue_number}"
    fi
    git push -u origin "$branch"
    echo "Pushed branch to remote"
  else
    # Ensure tracking is set up
    git branch --set-upstream-to="origin/$branch" "$branch" 2>/dev/null || true
  fi

  # ── Step 3: Ensure draft PR exists ──

  local pr_json
  pr_json=$(gh pr list --head "$branch" --json number,url,isDraft,state --limit 1 2>/dev/null || echo "[]")

  local pr_url=""

  if [ "$pr_json" != "[]" ]; then
    pr_url=$(echo "$pr_json" | jq -r '.[0].url')
    local pr_num
    pr_num=$(echo "$pr_json" | jq -r '.[0].number')
    local pr_state
    pr_state=$(echo "$pr_json" | jq -r '.[0].state')
    echo "PR exists: #$pr_num ($pr_state)"
  else
    echo "Creating draft PR linked to issue #${issue_number}..."
    pr_url=$(gh pr create --draft \
      --title "WIP: $title" \
      --body "## Summary

Implements #${issue_number}

## Changes

- [Describe changes here]

## Testing

- [How to test]

---
Closes #${issue_number}
" | tail -1)
    echo "Created draft PR"
  fi

  # ── Report ──

  local repo_name
  repo_name=$(gh repo view --json nameWithOwner -q '.nameWithOwner' 2>/dev/null || echo "unknown")

  echo ""
  if [ "$worktree_created" = true ]; then
    echo "=== Work started ==="
  else
    echo "=== Resuming work ==="
  fi
  echo "Issue:    https://github.com/${repo_name}/issues/${issue_number}"
  [ -n "$pr_url" ] && echo "PR:       $pr_url"
  echo "Worktree: $WORKTREES_DIR/$branch"
  echo ""
  echo "Next: cd $WORKTREES_DIR/$branch"
}

# ── Resume by branch name (orphan PR recovery) ───────────────
resume_by_branch() {
  local branch="$1"

  cd "$MONOREPO_DIR"
  git fetch origin

  if [ -d "$WORKTREES_DIR/$branch" ]; then
    echo "Worktree exists: .worktrees/$branch"
  elif git show-ref --verify --quiet "refs/remotes/origin/$branch" 2>/dev/null; then
    echo "Recreating worktree from remote..."
    git worktree add "$WORKTREES_DIR/$branch" "$branch" 2>/dev/null || \
      git worktree add "$WORKTREES_DIR/$branch" -b "$branch" "origin/$branch"
  else
    echo "Error: Branch $branch not found locally or on remote"
    exit 1
  fi

  echo ""
  echo "Existing PR:"
  gh pr view "$branch" --json url,title,isDraft 2>/dev/null || echo "  No PR found"

  echo ""
  echo "=== Resuming work ==="
  echo "Worktree: $WORKTREES_DIR/$branch"
  echo ""
  echo "Next: cd $WORKTREES_DIR/$branch"
}


# ── Parse arguments ───────────────────────────────────────────
case "${1:-}" in
  --resume)
    [ -z "${2:-}" ] && { echo "Usage: $0 --resume <branch>"; exit 1; }
    resume_by_branch "$2"
    ;;
  --help|-h|"")
    echo "work.sh - Ensure worktree + draft PR exist for an issue"
    echo ""
    echo "Usage:"
    echo "  $0 <issue-number>          Create or resume worktree + PR"
    echo "  $0 --resume <branch>       Resume by branch name (orphan PR recovery)"
    echo ""
    echo "Idempotent: safe to run multiple times. Only creates what's missing."
    echo ""
    echo "Note: Issue must exist first. Use 'new' sub-skill to create one."
    ;;
  *)
    if [[ "$1" =~ ^[0-9]+$ ]]; then
      ensure_worktree_for_issue "$1"
    else
      echo "Error: Expected issue number, got '$1'"
      echo "Usage: $0 <issue-number>"
      exit 1
    fi
    ;;
esac
