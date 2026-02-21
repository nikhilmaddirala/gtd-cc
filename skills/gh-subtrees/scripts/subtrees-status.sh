#!/usr/bin/env bash
#
# subtrees-status.sh - Diagnose subtree remote configuration and sync status
#
# Convention: every directory in 40-code/41-subtrees/ is a subtree.
# Remote name: remote-<dirname>
#
# Checks three layers for each subtree:
#   1. Git remote configured?
#   2. Remote reachable? (parallel fetch)
#   3. In sync?
#
# Usage:
#   subtrees-status.sh              # Full diagnostic
#   subtrees-status.sh --setup      # Include setup commands for missing remotes
#
set -euo pipefail
export GH_PAGER=""

MONOREPO_DIR=$(git rev-parse --show-toplevel)
SUBTREES_DIR="$MONOREPO_DIR/40-code/41-subtrees"
CONFIG_FILE="$MONOREPO_DIR/40-code/41-subtrees.yaml"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

# Look up remote URL from 41-subtrees.yaml
get_configured_url() {
  local project="$1"
  if [ -f "$CONFIG_FILE" ]; then
    grep -E "^  ${project}:" "$CONFIG_FILE" | sed 's/^[^:]*: *//' | tr -d '"' | head -1
  fi
}

# Detect default branch from already-fetched remote refs (no network call)
get_default_branch() {
  local remote="$1"
  if git rev-parse --verify "$remote/main" &>/dev/null; then
    echo "main"
  elif git rev-parse --verify "$remote/master" &>/dev/null; then
    echo "master"
  else
    echo "main"
  fi
}

show_diagnostic() {
  local show_setup="${1:-false}"

  cd "$MONOREPO_DIR"

  echo ""
  echo "═══════════════════════════════════════════════════════════════"
  echo "              SUBTREE STATUS"
  echo "═══════════════════════════════════════════════════════════════"
  echo ""

  if [ ! -d "$SUBTREES_DIR" ]; then
    echo "(no 41-subtrees/ directory found)"
    exit 0
  fi

  # Discover subtrees from filesystem
  local subtrees=()
  for dir in "$SUBTREES_DIR"/*/; do
    [ -d "$dir" ] || continue
    subtrees+=("$(basename "$dir")")
  done

  if [ ${#subtrees[@]} -eq 0 ]; then
    echo "(no projects in 41-subtrees/)"
    exit 0
  fi

  # Separate configured vs missing remotes
  declare -a configured_projects=()
  declare -a missing_remotes=()

  for project in "${subtrees[@]}"; do
    local remote="remote-$project"
    if git remote get-url "$remote" &>/dev/null; then
      configured_projects+=("$project")
    else
      missing_remotes+=("$project")
    fi
  done

  # Parallel fetch all configured remotes at once
  declare -A fetch_failed=()
  if [ ${#configured_projects[@]} -gt 0 ]; then
    local pids=()
    local tmpdir
    tmpdir=$(mktemp -d)

    for project in "${configured_projects[@]}"; do
      local remote="remote-$project"
      ( git fetch "$remote" 2>"$tmpdir/$project.err" && touch "$tmpdir/$project.ok" ) &
      pids+=($!)
    done

    # Wait for all fetches
    for pid in "${pids[@]}"; do
      wait "$pid" 2>/dev/null || true
    done

    # Check which fetches failed
    for project in "${configured_projects[@]}"; do
      if [ ! -f "$tmpdir/$project.ok" ]; then
        fetch_failed["$project"]=1
      fi
    done

    rm -rf "$tmpdir"
  fi

  # Display results
  declare -a unreachable_remotes=()
  declare -a needs_sync=()

  printf "%-25s %-40s %s\n" "PROJECT" "REMOTE" "STATUS"
  printf "%-25s %-40s %s\n" "───────" "──────" "──────"

  for project in "${subtrees[@]}"; do
    local remote="remote-$project"
    local prefix="40-code/41-subtrees/$project"

    # Layer 1: Git remote configured?
    if [[ " ${missing_remotes[*]} " == *" $project "* ]]; then
      echo -e "$(printf "%-25s" "$project") $(printf "%-40s" "(not configured)") ${YELLOW}⚠ No git remote${NC}"
      continue
    fi

    # Layer 2: Fetch succeeded?
    if [ "${fetch_failed[$project]+_}" ]; then
      local remote_url
      remote_url=$(git remote get-url "$remote" 2>/dev/null || echo "")
      echo -e "$(printf "%-25s" "$project") $(printf "%-40s" "$remote") ${RED}✗ Fetch failed${NC}"
      unreachable_remotes+=("$project|$remote_url")
      continue
    fi

    # Layer 3: Content comparison (in sync or not?)
    local branch
    branch=$(get_default_branch "$remote")
    local diff_count
    diff_count=$(git diff --name-only "HEAD:$prefix" "$remote/$branch" 2>/dev/null | wc -l | tr -d ' ')

    if [ "$diff_count" -eq 0 ]; then
      echo -e "$(printf "%-25s" "$project") $(printf "%-40s" "$remote") ${GREEN}✓ Synced${NC}"
    else
      echo -e "$(printf "%-25s" "$project") $(printf "%-40s" "$remote") ${YELLOW}✗ $diff_count files differ${NC}"
      needs_sync+=("$project|$diff_count files differ")
    fi
  done

  echo ""

  # Show fixes/setup guidance
  local has_issues=false

  if [ ${#missing_remotes[@]} -gt 0 ]; then
    has_issues=true
    echo "MISSING REMOTES"
    echo "───────────────"
    echo "Git remotes are local config (not cloned) - they need to be added per machine."
    echo ""

    for project in "${missing_remotes[@]}"; do
      local configured_url
      configured_url=$(get_configured_url "$project")

      echo -e "  ${YELLOW}$project${NC}"

      if [ "$show_setup" = "true" ]; then
        if [ -n "$configured_url" ]; then
          echo "    git remote add remote-$project $configured_url"
        else
          echo "    (no URL in 41-subtrees.yaml - add it first, then:)"
          echo "    git remote add remote-$project <url>"
        fi
        echo ""
      else
        echo "    Run with --setup to see setup commands"
      fi
    done
    echo ""
  fi

  if [ ${#unreachable_remotes[@]} -gt 0 ]; then
    has_issues=true
    echo "UNREACHABLE REMOTES"
    echo "───────────────────"
    echo ""

    for entry in "${unreachable_remotes[@]}"; do
      local project url
      project=$(echo "$entry" | cut -d'|' -f1)
      url=$(echo "$entry" | cut -d'|' -f2)

      echo -e "  ${RED}$project${NC} → $url"
      echo "    Possible causes:"
      echo "    - Repo doesn't exist → gh repo create $project"
      echo "    - Auth issue → gh auth status"
      echo "    - URL wrong → git remote set-url remote-$project <correct-url>"
      echo ""
    done
  fi

  if [ ${#needs_sync[@]} -gt 0 ]; then
    echo "NEEDS SYNC"
    echo "──────────"
    for entry in "${needs_sync[@]}"; do
      local project info
      project=$(echo "$entry" | cut -d'|' -f1)
      info=$(echo "$entry" | cut -d'|' -f2-)
      echo -e "  $project  $info"
    done
    echo ""
  fi

  if [ "$has_issues" = false ] && [ ${#needs_sync[@]} -eq 0 ]; then
    echo -e "${GREEN}All subtrees healthy.${NC}"
    echo ""
  fi
}

# Parse arguments
show_setup=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --setup|-s)
      show_setup=true
      shift
      ;;
    --help|-h)
      echo "subtrees-status.sh - Diagnose subtree remote configuration and sync status"
      echo ""
      echo "Convention: every directory in 40-code/41-subtrees/ is a subtree"
      echo "Remote name: remote-<dirname>"
      echo ""
      echo "Usage:"
      echo "  $0              Full diagnostic"
      echo "  $0 --setup      Include setup commands for missing remotes"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

show_diagnostic "$show_setup"
