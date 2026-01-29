---
description: Explore codebase, create implementation plan, update issue body, create worktree
---

# Plan

**Template**: `templates/plan.md`

## Overview

Research the codebase, analyze options, create an implementation plan, append it to the issue body, and set up a worktree for implementation.

## Process

- Load issue
  ```bash
  gh issue view N --json number,title,body,labels
  ```

- Update status
  ```bash
  gh issue edit N --remove-label "status-plan" --add-label "status-implement"
  ```

- Requirement analysis
  - Problem/goal: what exactly needs to be done and why
  - Acceptance criteria: how will we know this is complete
  - Scope: what's in scope vs out of scope
  - Constraints: technical, time, or resource constraints
  - Dependencies: related issues or prerequisites

- Codebase research
  - Explore existing architecture and patterns
  - Identify files to modify and impact areas
  - Check for similar implementations

- Options analysis (if multiple approaches exist)
  - Compare alternatives with tradeoffs
  - Consider maintainability and scalability
  - Document recommendation with rationale

- Technical feasibility
  - Evaluate complexity and risks
  - Identify potential blockers
  - Plan testing approach

- Append plan to issue body using `templates/plan.md` format
  - Read the existing issue body
  - Append a `---` separator followed by the plan section
  ```bash
  EXISTING_BODY=$(gh issue view N --json body --jq '.body')
  gh issue edit N --body "${EXISTING_BODY}

  ---

  ## Plan

  ### Summary

  [1-2 sentences on goal and approach]

  ### Technical approach

  [Key decisions and rationale]

  ### Files to create/modify

  - \`path/to/file\` - description of change

  ### Implementation steps

  1. [Step 1]
  2. [Step 2]
  3. [Step 3]

  ### Testing

  [How to verify the changes work]"
  ```

- Create worktree
  ```bash
  SLUG=$(echo "issue-title" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | cut -c1-30)
  git branch issue/${N}-${SLUG} main
  git worktree add .worktrees/issue-${N} issue/${N}-${SLUG}
  ```

- Report: "Plan added to issue #N. Worktree created at `.worktrees/issue-N`"
- Suggest next step: "Review the plan on the issue, then run `/gh-work N` when ready"

## Guidelines

- Always create plan before worktree
- Append plan to issue body (not as a comment) so it stays as the single source of truth
- Worktree directory: `.worktrees/issue-{N}`
- Branch naming: `issue/{N}-{slug}` (kebab-case, max 30 chars)
