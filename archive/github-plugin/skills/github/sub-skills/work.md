---
description: Implement the plan, commit changes, push branch, create draft PR
---

# Work

**Template**: `templates/implementation.md`

## Overview

Read the issue and plan, implement the changes, commit, push, and create a draft PR. This sub-skill handles both initial implementation and addressing review feedback.

## Process

- Determine issue number (from user input or branch name)
  ```bash
  BRANCH=$(git branch --show-current)
  ISSUE_NUM=$(echo $BRANCH | sed 's|issue/\([0-9]*\)-.*|\1|')
  ```

- Fetch issue and plan (plan is in the issue body below the `---` separator)
  ```bash
  gh issue view ${ISSUE_NUM} --json number,title,body
  ```

- Rebase on latest main
  ```bash
  git fetch origin main && git rebase origin/main
  ```

- Implement the plan
  - Read the plan section in the issue body for implementation steps
  - If returning after review feedback, read PR comments for requested changes
  - Commit in logical chunks using conventional format

- Push branch
  ```bash
  git push -u origin $(git branch --show-current)
  ```

- Create draft PR (or update existing) using `templates/implementation.md` format
  ```bash
  EXISTING_PR=$(gh pr list --head "$(git branch --show-current)" --json number --jq '.[0].number')

  if [ -z "$EXISTING_PR" ]; then
    ISSUE_TITLE=$(gh issue view ${ISSUE_NUM} --json title --jq '.title')
    gh pr create \
      --draft \
      --title "feat: ${ISSUE_TITLE}" \
      --body "$(cat <<EOF
  ## Summary

  Implements #${ISSUE_NUM}

  ## Changes

  - [Key change 1]
  - [Key change 2]

  ## Testing

  - [How to test these changes]

  ---
  Closes #${ISSUE_NUM}
  EOF
  )"
  else
    echo "PR #${EXISTING_PR} already exists, pushed updates"
  fi
  ```

- Update issue status
  ```bash
  gh issue edit ${ISSUE_NUM} --remove-label "status-implement" --add-label "status-review"
  ```

- Report: "Draft PR created (or updated). Issue #N moved to status-review."
- Suggest next step: "Run `/gh-review N` to review the PR"

## Guidelines

- Always rebase on main before starting work
- Commit frequently in logical chunks with conventional format
- PR body MUST include "Closes #N" for auto-close on merge
- Always create at least a draft PR
- If PR already exists (returning after feedback), just push updates
