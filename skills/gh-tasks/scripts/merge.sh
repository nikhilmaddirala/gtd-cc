#!/usr/bin/env bash
#
# merge.sh - Merge PR and cleanup worktree/branch
#
# Usage:
#   merge.sh <pr-number>
#
set -euo pipefail
export GH_PAGER=""

MONOREPO_DIR=~/repos/monorepo
WORKTREES_DIR=$MONOREPO_DIR/.worktrees

cd "$MONOREPO_DIR"

# Parse arguments
if [ $# -eq 0 ] || ! [[ "$1" =~ ^[0-9]+$ ]]; then
  echo "merge.sh - Merge PR and cleanup worktree/branch"
  echo ""
  echo "Usage:"
  echo "  $0 <pr-number>"
  exit 1
fi

pr_num="$1"
branch=$(gh pr view "$pr_num" --json headRefName -q '.headRefName')

echo "Merging PR #${pr_num} (branch: $branch)..."

# Stop any background sync
pkill -f "git-sync.*$branch" 2>/dev/null || true

# Check if we're in the worktree - need to exit first
current_dir=$(pwd)
if [[ "$current_dir" == *"$branch"* ]]; then
  echo "Currently in worktree, switching to main..."
  cd "$MONOREPO_DIR"
fi

# Push any final changes from worktree
if [ -d "$WORKTREES_DIR/$branch" ]; then
  echo "Pushing final changes from worktree..."
  (
    cd "$WORKTREES_DIR/$branch"
    git add -A
    git commit -m "chore: final changes before merge" 2>/dev/null || true
    git push origin "$branch" 2>/dev/null || true
  )
fi

# Convert draft to ready if needed
is_draft=$(gh pr view "$pr_num" --json isDraft -q '.isDraft')
if [ "$is_draft" = "true" ]; then
  echo "Converting draft PR to ready..."
  gh pr ready "$pr_num"
fi

# Check CI status
echo "Checking CI status..."
gh pr checks "$pr_num" 2>/dev/null || echo "  (no checks configured)"

# Pre-flight mergeability check (before any destructive operations)
echo "Checking mergeability..."
for attempt in 1 2 3; do
  merge_state=$(gh api "repos/{owner}/{repo}/pulls/$pr_num" --jq '.mergeable_state')
  if [ "$merge_state" != "unknown" ]; then
    break
  fi
  echo "  Mergeability unknown, waiting... (attempt $attempt/3)"
  sleep 3
done

if [ "$merge_state" = "dirty" ]; then
  echo ""
  echo "PR has merge conflicts (mergeable_state: dirty)"

  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

  if [ -d "$WORKTREES_DIR/$branch" ]; then
    echo "Running squash-rebase to resolve..."
    echo ""
    if "$SCRIPT_DIR/rebase.sh" "$WORKTREES_DIR/$branch"; then
      echo ""
      echo "Pushing rebased branch..."
      (cd "$WORKTREES_DIR/$branch" && git push --force-with-lease)
      echo "Waiting for GitHub to recalculate mergeability..."
      sleep 5
      merge_state=$(gh api "repos/{owner}/{repo}/pulls/$pr_num" --jq '.mergeable_state')
      if [ "$merge_state" = "dirty" ]; then
        echo ""
        echo "ERROR: Still not mergeable after rebase (mergeable_state: $merge_state)"
        echo "Resolve conflicts manually in: $WORKTREES_DIR/$branch"
        exit 1
      fi
      echo "Mergeability resolved: $merge_state"
    else
      echo ""
      echo "ERROR: Squash-rebase failed (likely conflict)."
      echo "Resolve conflicts in the worktree, then retry merge:"
      echo ""
      echo "  cd $WORKTREES_DIR/$branch"
      echo "  git add -A && git rebase --continue"
      echo "  git push --force-with-lease"
      exit 1
    fi
  else
    echo "ERROR: No local worktree found for branch: $branch"
    echo "Recreate worktree first:"
    echo "  scripts/work.sh --resume $branch"
    exit 1
  fi
fi

if [ "$merge_state" = "blocked" ]; then
  echo ""
  echo "ERROR: PR is blocked (required checks or reviews missing)"
  exit 1
fi

# Merge with squash (before cleanup so worktree survives on failure)
echo ""
echo "Merging..."
gh pr merge "$pr_num" --squash --delete-branch

# --- Post-merge cleanup (best-effort) ---
set +e

# Remove worktree after successful merge
if [ -d "$WORKTREES_DIR/$branch" ]; then
  echo "Removing worktree..."
  git worktree remove "$WORKTREES_DIR/$branch" --force
fi

# Delete local branch
git branch -D "$branch" 2>/dev/null || true

echo ""
echo "Updating main branch..."
git checkout main 2>/dev/null
# Commit any git-sync changes so pull doesn't fail
git add -A && git commit -m "chore: sync before merge pull" 2>/dev/null
git pull origin main
git fetch --prune origin 2>/dev/null

# Extract issue number and verify closure
issue_num=$(echo "$branch" | grep -oE 'issue-[0-9]+' | sed 's/issue-//')
if [ -n "$issue_num" ]; then
  echo ""
  echo "Verifying issue #${issue_num}..."
  issue_state=$(gh issue view "$issue_num" --json state -q '.state')
  if [ "$issue_state" = "CLOSED" ]; then
    echo "  Issue #${issue_num}: CLOSED ✓"
  else
    echo "  Issue #${issue_num}: $issue_state (expected CLOSED)"
    echo "  Closing manually..."
    gh issue close "$issue_num"
  fi
fi

echo ""
echo "=== Merge complete ==="
echo "PR:       #${pr_num} MERGED"
echo "Branch:   $branch DELETED"
echo "Worktree: REMOVED"
[ -n "${issue_num:-}" ] && echo "Issue:    #${issue_num} CLOSED"
echo ""
echo "Next: Run subtrees-status to check for subtrees to publish"
