---
description: Review PR for correctness, post findings with merge blockers vs nice-to-haves
---

# review

**Template**: `templates/review.md`

## Overview

Review PR changes for correctness and compliance before merging. Identifies only real and significant issues, distinguishing merge blockers from nice-to-haves. Posts findings as a PR comment.


## Process

1. Identify the PR:
   ```bash
   # From PR number
   gh pr view <PR_NUM> --json number,title,state,isDraft

   # From branch name
   gh pr list --head "<branch>" --json number,url,state,headRefName
   ```
   - If PR is closed or merged: skip with message
   - If already reviewed: check if new commits since last review

2. Fetch PR details and diff:
   ```bash
   gh pr view <PR_NUM> --json title,body,files,additions,deletions,headRefName
   gh pr diff <PR_NUM>
   gh pr checks <PR_NUM>
   ```

3. Locate the worktree for the PR branch:
   ```bash
   scripts/tasks-status.sh
   ```
   Find the worktree path matching the PR's `headRefName`. When reading full file content beyond the diff, use that worktree path instead of the current directory (which is typically `main`).

4. Fetch the linked issue for alignment checking:
   ```bash
   # Extract issue number from PR body ("Closes #N")
   gh issue view <ISSUE_NUM> --json body
   ```
   - Parse the plan section below `---` separator to understand intended changes

5. Analyze changes:
   - Alignment with the original issue and plan (if plan exists in issue body)
   - Obvious bugs or logic errors
   - Issues based on git history and context
   - Focus on significant issues, not nitpicks

6. Filter findings to only real and significant issues:
   - Not false positives or pre-existing issues
   - Not nitpicks a senior engineer wouldn't mention
   - Not issues that linters/type checkers/tests will catch

7. Post findings using `templates/review.md` format:
   ```bash
   gh pr comment <PR_NUM> --body "<review content>"
   ```

8. Report: "Review posted on PR #N"

9. Suggest next step:
   - If approved: "Run `merge` sub-skill to merge"
   - If changes needed: "Address feedback in worktree, then request re-review"


## Guidelines

- Use `gh` CLI for all GitHub interactions
- When citing issues, use full permalink format with commit SHA
- Avoid false positives: pre-existing issues, nitpicks, issues CI will catch
- Consider backward compatibility for published code
- Keep PR comments focused on code quality, not scope/requirements
- If a review finding requires a scope or plan change, the author should post that decision to an issue comment (not debate it in the PR thread), then update the issue body if the plan changes
