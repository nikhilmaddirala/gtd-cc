#!/usr/bin/env bash
#
# tasks-status.sh - Diagnose monorepo workflow health
#
# Validates the airtight tracking invariant:
#   issue ↔ worktree ↔ branch ↔ draft PR
#
# Usage:
#   tasks-status.sh              # Full diagnostic
#   tasks-status.sh --json       # Machine-readable output
#
set -euo pipefail
export GH_PAGER=""

MONOREPO_DIR=~/repos/monorepo
WORKTREES_DIR="$MONOREPO_DIR/.worktrees"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Tracking arrays for anomalies
declare -a ANOMALIES=()
declare -a HEALTHY=()

# Extract issue number from worktree/branch name
extract_issue_number() {
  local name="$1"
  echo "$name" | grep -oE 'issue-[0-9]+' | head -1 | sed 's/issue-//'
}

check_worktree_health() {
  local wt_path="$1"
  local name
  name=$(basename "$wt_path")
  local issue_num
  issue_num=$(extract_issue_number "$name")

  local status="healthy"
  local issues_found=()

  # Get branch name
  local branch
  branch=$(cd "$wt_path" && git branch --show-current 2>/dev/null || echo "")

  # Check 1: Can we extract an issue number?
  if [ -z "$issue_num" ]; then
    status="anomaly"
    issues_found+=("no issue number in name")
  else
    # Check 2: Does the issue exist and is it open?
    local issue_state
    issue_state=$(gh issue view "$issue_num" --json state --jq '.state' 2>/dev/null || echo "NOT_FOUND")

    if [ "$issue_state" = "NOT_FOUND" ]; then
      status="anomaly"
      issues_found+=("issue #$issue_num not found")
    elif [ "$issue_state" = "CLOSED" ]; then
      status="stale"
      issues_found+=("issue #$issue_num is closed")
    fi
  fi

  # Check 3: Does a PR exist for this branch?
  local pr_info=""
  local pr_state=""
  if [ -n "$branch" ]; then
    local pr_json
    pr_json=$(gh pr list --head "$branch" --json number,state,isDraft --limit 1 2>/dev/null || echo "[]")
    if [ "$pr_json" = "[]" ]; then
      status="incomplete"
      issues_found+=("no PR for branch")
    else
      local pr_num
      pr_num=$(echo "$pr_json" | jq -r '.[0].number // empty')
      local is_draft
      is_draft=$(echo "$pr_json" | jq -r '.[0].isDraft // false')
      pr_state=$(echo "$pr_json" | jq -r '.[0].state // empty')

      if [ "$pr_state" = "MERGED" ]; then
        status="stale"
        issues_found+=("PR #$pr_num is merged")
      elif [ "$pr_state" = "CLOSED" ]; then
        status="stale"
        issues_found+=("PR #$pr_num is closed")
      else
        if [ "$is_draft" = "true" ]; then
          pr_info="PR #$pr_num (draft)"
        else
          pr_info="PR #$pr_num (ready)"
        fi
      fi
    fi
  fi

  # Build result
  local result=""
  if [ "$status" = "healthy" ]; then
    result="${GREEN}✓${NC} $name"
    [ -n "$issue_num" ] && result="$result → #$issue_num"
    [ -n "$pr_info" ] && result="$result → $pr_info"
    HEALTHY+=("$result")
  else
    result="${RED}✗${NC} $name"
    [ -n "$issue_num" ] && result="$result → #$issue_num"
    [ -n "$pr_info" ] && result="$result → $pr_info"
    result="$result\n   ${YELLOW}Issues:${NC} ${issues_found[*]}"
    ANOMALIES+=("$result")
  fi
}

check_orphan_prs() {
  # Find PRs that don't have local worktrees
  local prs_json
  prs_json=$(gh pr list --state open --json number,headRefName,isDraft --limit 20 2>/dev/null || echo "[]")

  if [ "$prs_json" = "[]" ]; then
    return
  fi

  echo "$prs_json" | jq -c '.[]' | while read -r pr; do
    local pr_num
    pr_num=$(echo "$pr" | jq -r '.number')
    local branch
    branch=$(echo "$pr" | jq -r '.headRefName')
    local is_draft
    is_draft=$(echo "$pr" | jq -r '.isDraft')

    # Check if worktree exists for this branch
    local has_worktree=false
    if [ -d "$WORKTREES_DIR" ]; then
      for wt in "$WORKTREES_DIR"/*; do
        [ -d "$wt" ] || continue
        local wt_branch
        wt_branch=$(cd "$wt" && git branch --show-current 2>/dev/null || echo "")
        if [ "$wt_branch" = "$branch" ]; then
          has_worktree=true
          break
        fi
      done
    fi

    if [ "$has_worktree" = false ]; then
      local pr_type="ready"
      [ "$is_draft" = "true" ] && pr_type="draft"
      echo "orphan_pr:$pr_num:$branch:$pr_type"
    fi
  done
}

show_diagnostic() {
  echo ""
  echo "═══════════════════════════════════════════════════════════════"
  echo "              MONOREPO TASK STATUS"
  echo "═══════════════════════════════════════════════════════════════"
  echo ""

  # Section 1: Check worktrees
  echo "WORKTREE HEALTH"
  echo "───────────────"

  if [ ! -d "$WORKTREES_DIR" ] || [ -z "$(ls -A "$WORKTREES_DIR" 2>/dev/null)" ]; then
    echo "(no active worktrees)"
  else
    for wt in "$WORKTREES_DIR"/*; do
      [ -d "$wt" ] || continue
      check_worktree_health "$wt"
    done

    # Print healthy first
    for item in "${HEALTHY[@]:-}"; do
      [ -n "$item" ] && echo -e "$item"
    done

    # Then anomalies
    for item in "${ANOMALIES[@]:-}"; do
      [ -n "$item" ] && echo -e "$item"
    done
  fi
  echo ""

  # Section 2: Check for orphan PRs
  echo "ORPHAN PRs (no local worktree)"
  echo "──────────────────────────────"

  local orphans
  orphans=$(check_orphan_prs)

  if [ -z "$orphans" ]; then
    echo "(none)"
  else
    echo "$orphans" | while IFS=: read -r type pr_num branch pr_state; do
      if [ "$type" = "orphan_pr" ]; then
        echo -e "${YELLOW}⚠${NC} PR #$pr_num ($pr_state) on branch: $branch"
        echo "   Fix: ./scripts/work.sh --resume $branch"
      fi
    done
  fi
  echo ""

  # Section 3: Actionable issues (what can I do next?)
  echo "NEXT ACTIONS"
  echo "────────────"

  local has_actions=false

  # Issues needing planning (status-plan)
  local plan_issues
  plan_issues=$(gh issue list --state open --label "status-plan" --json number,title --jq '.[] | "#\(.number) \(.title)"' 2>/dev/null || echo "")
  if [ -n "$plan_issues" ]; then
    echo -e "${YELLOW}Needs planning:${NC}"
    echo "$plan_issues" | while read -r issue; do
      local num
      num=$(echo "$issue" | grep -oE '#[0-9]+')
      echo "  $issue"
      echo "    → /mg-plan ${num#\#}"
    done
    has_actions=true
  fi

  # Issues ready for implementation (status-implement, no worktree)
  local impl_issues
  impl_issues=$(gh issue list --state open --label "status-implement" --json number,title --jq '.[] | "\(.number)|\(.title)"' 2>/dev/null || echo "")
  if [ -n "$impl_issues" ]; then
    echo "$impl_issues" | while read -r line; do
      local num title
      num=$(echo "$line" | cut -d'|' -f1)
      title=$(echo "$line" | cut -d'|' -f2)

      # Check if worktree already exists for this issue
      local has_wt=false
      if [ -d "$WORKTREES_DIR" ]; then
        for wt in "$WORKTREES_DIR"/issue-"$num"-*; do
          [ -d "$wt" ] && has_wt=true && break
        done
      fi

      if [ "$has_wt" = false ]; then
        echo -e "${GREEN}Ready to implement:${NC}"
        echo "  #$num $title"
        echo "    → /mg-work $num"
      fi
    done
    has_actions=true
  fi

  # Issues in review (status-review)
  local review_issues
  review_issues=$(gh issue list --state open --label "status-review" --json number,title --jq '.[] | "#\(.number) \(.title)"' 2>/dev/null || echo "")
  if [ -n "$review_issues" ]; then
    echo -e "${BLUE}Ready for review:${NC}"
    echo "$review_issues" | while read -r issue; do
      local num
      num=$(echo "$issue" | grep -oE '#[0-9]+')
      echo "  $issue"
      echo "    → /mg-review ${num#\#}"
    done
    has_actions=true
  fi

  # Active worktrees to continue
  if [ -d "$WORKTREES_DIR" ] && [ -n "$(ls -A "$WORKTREES_DIR" 2>/dev/null)" ]; then
    echo -e "${NC}Continue working:${NC}"
    for wt in "$WORKTREES_DIR"/*; do
      [ -d "$wt" ] || continue
      local name
      name=$(basename "$wt")
      local issue_num
      issue_num=$(extract_issue_number "$name")
      echo "  cd $WORKTREES_DIR/$name"
      [ -n "$issue_num" ] && echo "    → issue #$issue_num"
    done
    has_actions=true
  fi

  if [ "$has_actions" = false ]; then
    echo "(no pending actions)"
    echo "  → /mg-new \"description\" to start something new"
  fi
  echo ""

  # Section 4: Resolution summary (for anomalies)
  local total_anomalies=${#ANOMALIES[@]}
  local orphan_count
  orphan_count=$(echo "$orphans" | grep -c "orphan_pr" 2>/dev/null || echo "0")

  if [ "$total_anomalies" -gt 0 ] || [ "$orphan_count" -gt 0 ]; then
    echo "ANOMALIES"
    echo "─────────"
    [ "$total_anomalies" -gt 0 ] && echo -e "${YELLOW}• $total_anomalies worktree(s) need attention${NC}"
    [ "$orphan_count" -gt 0 ] && echo -e "${YELLOW}• $orphan_count orphan PR(s) without local worktrees${NC}"
    echo ""
    echo "Run /mg-tasks-status for guided resolution"
    echo ""
  fi
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --json)
      # TODO: JSON output mode
      shift
      ;;
    --help|-h)
      echo "tasks-status.sh - Diagnose monorepo workflow health"
      echo ""
      echo "Validates: issue ↔ worktree ↔ branch ↔ draft PR"
      echo ""
      echo "Usage:"
      echo "  $0              Full diagnostic"
      echo "  $0 --json       Machine-readable output"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

show_diagnostic
