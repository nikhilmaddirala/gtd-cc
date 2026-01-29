---
description: Create a GitHub Issue with status and priority labels
---

# New

**Template**: `templates/issue.md`

## Overview

Create a new task as a GitHub Issue with default labels. The issue body follows the issue template structure.

## Process

- Create issue using `templates/issue.md` format
  ```bash
  gh issue create \
    --title "Task title here" \
    --body "$(cat <<'EOF'
  ## Goal

  [What needs to be done and why]

  ## Context

  [Relevant background, constraints, dependencies]

  ## Acceptance criteria

  - [ ] [Criterion 1]
  - [ ] [Criterion 2]
  EOF
  )" \
    --label "status-plan,priority-p3"
  ```
- Extract issue number from output
- If user specified urgency, adjust priority label accordingly ("urgent" → `priority-p1`, "low priority" → `priority-p4`)
- Report: "Created issue #N"
- Suggest next step: "Run `/gh-plan N` to start planning"

## Guidelines

- Default labels: `status-plan`, `priority-p3`
- Size labels are added during planning, not at creation
