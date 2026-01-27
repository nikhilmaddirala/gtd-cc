---
description: Label schema for GitHub Issues workflow
---

# Labels

## Overview

Standard labels used by the monorepo-git plugin for issue-driven development.


## Status labels

Track issue lifecycle through the workflow.

| Label | Description | Color |
|-------|-------------|-------|
| `status-todo` | New issue, needs planning | `#d4c5f9` (lavender) |
| `status-planning` | Plan in progress | `#c5def5` (light blue) |
| `status-doing` | Implementation in progress | `#fbca04` (yellow) |
| `status-review` | PR created, under review | `#f9d0c4` (peach) |
| `status-done` | Merged and closed | `#0e8a16` (green) |


## Priority labels

Indicate urgency for triage.

| Label | Description | Color |
|-------|-------------|-------|
| `priority-p1` | Urgent, do first | `#d73a4a` (red) |
| `priority-p2` | High priority | `#ff7b00` (orange) |
| `priority-p3` | Medium priority | `#fbca04` (yellow) |
| `priority-p4` | Low priority, backlog | `#c2e0c6` (light green) |


## Size labels

T-shirt sizing for effort estimation.

| Label | Description | Color |
|-------|-------------|-------|
| `size-xs` | Extra small, < 1 hour | `#bfd4f2` (light blue) |
| `size-s` | Small, 1-4 hours | `#c2e0c6` (light green) |
| `size-m` | Medium, 1-2 days | `#fbca04` (yellow) |
| `size-l` | Large, 3-5 days | `#f9d0c4` (peach) |
| `size-xl` | Extra large, 1+ week | `#d73a4a` (red) |


## gh CLI commands

Create all labels in a repository:

```bash
# Status labels
gh label create "status-todo" --description "New issue, needs planning" --color "d4c5f9"
gh label create "status-planning" --description "Plan in progress" --color "c5def5"
gh label create "status-doing" --description "Implementation in progress" --color "fbca04"
gh label create "status-review" --description "PR created, under review" --color "f9d0c4"
gh label create "status-done" --description "Merged and closed" --color "0e8a16"

# Priority labels
gh label create "priority-p1" --description "Urgent, do first" --color "d73a4a"
gh label create "priority-p2" --description "High priority" --color "ff7b00"
gh label create "priority-p3" --description "Medium priority" --color "fbca04"
gh label create "priority-p4" --description "Low priority, backlog" --color "c2e0c6"

# Size labels
gh label create "size-xs" --description "Extra small, < 1 hour" --color "bfd4f2"
gh label create "size-s" --description "Small, 1-4 hours" --color "c2e0c6"
gh label create "size-m" --description "Medium, 1-2 days" --color "fbca04"
gh label create "size-l" --description "Large, 3-5 days" --color "f9d0c4"
gh label create "size-xl" --description "Extra large, 1+ week" --color "d73a4a"
```


## Workflow transitions

```
status-todo → status-planning → status-doing → status-review → status-done
     ↑              ↓                ↓              ↓
     └──────────────┴────────────────┴──────────────┘
                  (can go back if blocked)
```

Transitions:
- **todo → planning**: When `/mg-main-start N` begins planning
- **planning → doing**: When plan is approved and worktree is created
- **doing → review**: When `/mg-dev-finish` creates a PR
- **review → done**: When PR is merged (auto via "Closes #N")


## Defaults

New issues get:
- `status-todo` (always)
- `priority-p3` (unless specified: "urgent" → p1, "low priority" → p4)
- No size label (added during planning when effort is estimated)
