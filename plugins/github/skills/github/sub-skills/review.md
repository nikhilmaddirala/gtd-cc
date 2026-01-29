---
description: Review PR for correctness, post findings with merge blockers vs nice-to-haves
---

# Review

**Template**: `templates/review.md`

## Overview

Review PR changes for correctness and compliance, identifying only real and significant issues. Post findings as a PR comment.

## Process

- Identify the PR (from user input or current branch)
  ```bash
  gh pr list --head "issue/${N}-" --json number,url,state,headRefName
  ```

- Check PR is reviewable
  - Skip if closed, automated, or already reviewed by you

- Fetch PR details and summarize changes
  ```bash
  gh pr view ${PR_NUM} --json title,body,files,additions,deletions
  gh pr diff ${PR_NUM}
  ```

- Inspect CI signals
  ```bash
  gh pr checks ${PR_NUM}
  ```
  - Review failing or pending checks
  - Assess impact on merge readiness

- Review changes for
  - Alignment with the original issue and plan
  - Obvious bugs in the code changes
  - Issues based on git history and context of modified code
  - Focus on significant issues, not nitpicks

- Filter findings to only real and significant issues
  - Not false positives or pre-existing issues
  - Not nitpicks a senior engineer wouldn't mention
  - Not issues that linters/type checkers/tests will catch

- Post findings using `templates/review.md` format
  ```bash
  gh pr comment ${PR_NUM} --body "$(cat <<'EOF'
  ## Summary

  [Short overview of what was reviewed]

  ## Merge blockers

  - [ ] [Blocker 1]

  ## Nice-to-haves

  - [ ] [Suggestion 1]

  ## Validation

  [Tests/commands executed and results]
  EOF
  )"
  ```

- Report: "Review posted on PR #N"
- Suggest next step: "If approved, run `/gh-merge N`. If changes needed, run `/gh-work N` to address feedback."

## Guidelines

- Use `gh` CLI for all GitHub interactions
- When citing issues, use full permalink format: `https://github.com/owner/repo/blob/[full-sha]/path/file#L[start]-L[end]`
- Avoid false positives: pre-existing issues, nitpicks, issues CI will catch
