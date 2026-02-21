#!/usr/bin/env bash
#
# setup-labels.sh - Ensure gh-tasks labels exist in the repo
#
# Idempotently creates/updates the label schema used by the
# gh-tasks pipeline (status, priority, size).
#
# Usage:
#   setup-labels.sh              # Create/update all labels
#   setup-labels.sh --dry-run    # Show what would change
#   setup-labels.sh --delete     # Remove gh-tasks labels
#
set -euo pipefail
export GH_PAGER=""

DRY_RUN=false
DELETE_MODE=false

# ── Label schema ──────────────────────────────────────────────
# Format: "name|color|description"

STATUS_LABELS=(
  "status-plan|7B61FF|Needs planning before implementation"
  "status-implement|0075CA|Has plan, ready for implementation"
  "status-review|E4A221|Has draft PR, needs review"
  "status-blocked|D73A4A|Waiting on external dependency"
)

PRIORITY_LABELS=(
  "priority-p1|B60205|Urgent - do today"
  "priority-p2|D93F0B|High - do this week"
  "priority-p3|FBCA04|Medium - do this cycle"
  "priority-p4|0E8A16|Low - backlog"
)

SIZE_LABELS=(
  "size-xs|C5DEF5|Extra small - < 30 min"
  "size-s|BFD4F2|Small - 1-2 hours"
  "size-m|A2CBEE|Medium - half day"
  "size-l|7DB8DA|Large - full day"
  "size-xl|5FA4CE|Extra large - multi-day"
)

AGENT_LABELS=(
  "agent-plan|0E8A16|Agent should plan this issue"
  "agent-implement|1D76DB|Agent should implement this issue"
  "agent-review|5319E7|Agent should review this PR"
  "agent-merge-ready|B60205|Review passed, ready for human merge"
)

ALL_LABELS=("${STATUS_LABELS[@]}" "${PRIORITY_LABELS[@]}" "${SIZE_LABELS[@]}" "${AGENT_LABELS[@]}")

# ── Functions ─────────────────────────────────────────────────

ensure_label() {
  local spec="$1"
  local name color description
  IFS='|' read -r name color description <<< "$spec"

  # Check if label exists
  local existing
  existing=$(gh label list --search "$name" --json name,color,description --limit 100 2>/dev/null || echo "[]")

  # Exact match (search is fuzzy, so filter precisely)
  local match
  match=$(echo "$existing" | jq -r --arg n "$name" '.[] | select(.name == $n)')

  if [ -z "$match" ]; then
    # Label does not exist - create it
    if [ "$DRY_RUN" = true ]; then
      echo "  [create] $name ($color) - $description"
    else
      if gh label create "$name" --color "$color" --description "$description" 2>/dev/null; then
        echo "  [created] $name"
      else
        echo "  [error] Failed to create $name" >&2
        return 1
      fi
    fi
  else
    # Label exists - check if update needed
    local current_color current_desc
    current_color=$(echo "$match" | jq -r '.color' | tr '[:upper:]' '[:lower:]')
    current_desc=$(echo "$match" | jq -r '.description // ""')
    color_lower=$(echo "$color" | tr '[:upper:]' '[:lower:]')

    if [ "$current_color" != "$color_lower" ] || [ "$current_desc" != "$description" ]; then
      if [ "$DRY_RUN" = true ]; then
        echo "  [update] $name ($current_color → $color) - $description"
      else
        if gh label edit "$name" --color "$color" --description "$description" 2>/dev/null; then
          echo "  [updated] $name"
        else
          echo "  [error] Failed to update $name" >&2
          return 1
        fi
      fi
    else
      echo "  [ok] $name"
    fi
  fi
}

delete_label() {
  local spec="$1"
  local name
  IFS='|' read -r name _ _ <<< "$spec"

  # Check if label exists
  local existing
  existing=$(gh label list --search "$name" --json name --limit 100 2>/dev/null || echo "[]")
  local match
  match=$(echo "$existing" | jq -r --arg n "$name" '.[] | select(.name == $n) | .name')

  if [ -n "$match" ]; then
    if [ "$DRY_RUN" = true ]; then
      echo "  [delete] $name"
    else
      if gh label delete "$name" --yes 2>/dev/null; then
        echo "  [deleted] $name"
      else
        echo "  [error] Failed to delete $name" >&2
        return 1
      fi
    fi
  else
    echo "  [skip] $name (not found)"
  fi
}

show_summary() {
  echo ""
  echo "=== Label setup complete ==="
  echo ""
  echo "Label groups:"
  echo "  Status:   status-plan, status-implement, status-review, status-blocked"
  echo "  Priority: priority-p1 (urgent) → priority-p4 (backlog)"
  echo "  Size:     size-xs (< 30 min) → size-xl (multi-day)"
  echo "  Agent:    agent-plan, agent-implement, agent-review, agent-merge-ready"
  echo ""
  echo "Total: ${#ALL_LABELS[@]} labels"
}

# ── Main ──────────────────────────────────────────────────────

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --delete)
      DELETE_MODE=true
      shift
      ;;
    --help|-h)
      echo "setup-labels.sh - Ensure gh-tasks labels exist in the repo"
      echo ""
      echo "Usage:"
      echo "  $0              Create/update all labels"
      echo "  $0 --dry-run    Show what would change"
      echo "  $0 --delete     Remove gh-tasks labels"
      echo ""
      echo "Labels managed: status-*, priority-*, size-*, agent-*"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

repo=$(gh repo view --json nameWithOwner -q '.nameWithOwner' 2>/dev/null || echo "unknown")
echo "Repository: $repo"
[ "$DRY_RUN" = true ] && echo "(dry run - no changes will be made)"
echo ""

if [ "$DELETE_MODE" = true ]; then
  echo "Removing gh-tasks labels..."
  echo ""
  for spec in "${ALL_LABELS[@]}"; do
    delete_label "$spec"
  done
else
  echo "Status labels"
  echo "─────────────"
  for spec in "${STATUS_LABELS[@]}"; do
    ensure_label "$spec"
  done
  echo ""

  echo "Priority labels"
  echo "───────────────"
  for spec in "${PRIORITY_LABELS[@]}"; do
    ensure_label "$spec"
  done
  echo ""

  echo "Size labels"
  echo "───────────"
  for spec in "${SIZE_LABELS[@]}"; do
    ensure_label "$spec"
  done
  echo ""

  echo "Agent labels"
  echo "────────────"
  for spec in "${AGENT_LABELS[@]}"; do
    ensure_label "$spec"
  done

  show_summary
fi
