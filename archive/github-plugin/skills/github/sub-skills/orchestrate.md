---
description: Automated pipeline from main. Creates issue, plans, spins up worktree, launches subagent for implementation. Never modifies main directly.
---

# Orchestrate

## Overview

End-to-end automated pipeline that runs from the main worktree. Creates an issue, researches and plans, sets up an isolated worktree, then launches a subagent inside that worktree to implement. The orchestrator never makes code changes in main — all modifications happen inside the dedicated worktree.

## Prerequisites

- MUST be run from the main worktree (not from `.worktrees/*`)
- Verify before proceeding:
  ```bash
  CURRENT_DIR=$(pwd)
  if [[ "$CURRENT_DIR" == *".worktrees"* ]]; then
    echo "ERROR: orchestrate must run from the main worktree, not from a feature worktree"
    exit 1
  fi
  ```

## Process

### Stage 1: create issue (from main)

- Execute the `new` sub-skill process
  - Create issue using `templates/issue.md` format
  - Apply labels: `status-plan`, appropriate priority
- Capture the issue number `N`

### Stage 2: plan (from main)

- Execute the `plan` sub-skill process
  - Load the issue
  - Research the codebase, analyze options
  - Append plan to issue body using `templates/plan.md` format
  - Update status: `status-plan` → `status-implement`
- Create the worktree
  ```bash
  SLUG=$(echo "issue-title" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | cut -c1-30)
  git branch issue/${N}-${SLUG} main
  git worktree add .worktrees/issue-${N} issue/${N}-${SLUG}
  ```

### Stage 3: implement (via subagent in worktree)

- Launch a subagent with its working directory set to the worktree
  - The subagent's task: execute the `work` sub-skill for issue `N`
  - The subagent works inside `.worktrees/issue-${N}` and MUST NOT cd out of it
  - The subagent reads the plan from the issue body and implements it
  - The subagent commits, pushes, and creates a draft PR

- Subagent instructions:
  ```
  You are working in a feature worktree at .worktrees/issue-${N}.
  Your task: implement the plan for issue #${N}.

  Steps:
  1. Read the issue: gh issue view ${N} --json number,title,body
  2. The plan is in the issue body below the --- separator
  3. Rebase on main: git fetch origin main && git rebase origin/main
  4. Implement the plan, committing in logical chunks with conventional format
  5. Push: git push -u origin $(git branch --show-current)
  6. Create draft PR using templates/implementation.md format with "Closes #${N}" in body
  7. Update status: gh issue edit ${N} --remove-label "status-implement" --add-label "status-review"

  CRITICAL: Do not modify files outside this worktree. Do not cd to the main worktree.
  ```

- Wait for subagent to complete

### Stage 4: report (from main)

- Verify the PR was created
  ```bash
  gh pr list --head "issue/${N}-" --json number,url
  ```
- Report: "Issue #N created, planned, and implemented. Draft PR ready for review."
- Suggest next step: "Run `/gh-review N` to review the PR"

## Guidelines

- NEVER make code changes in the main worktree — orchestrate is a coordinator, not an implementer
- All code modifications happen inside `.worktrees/issue-{N}` via the subagent
- The orchestrator stays in main throughout; only the subagent works in the worktree
- If the subagent fails, report the failure and leave the worktree intact for manual intervention
- The worktree directory is `.worktrees/issue-{N}` (alongside human-managed worktrees in the same location)
