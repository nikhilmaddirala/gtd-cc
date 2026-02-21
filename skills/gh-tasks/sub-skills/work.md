---
description: Ensure worktree + draft PR exist, implement the plan, commit changes, push branch
---

# work

## Overview

Ensure a worktree and draft PR exist for an issue, then implement the changes. The script is idempotent: it converges to the correct state regardless of what already exists (worktree, branch, PR). Safe to call whether starting fresh, resuming, or returning after review feedback.


## Process

1. Ensure worktree and draft PR exist (delegate to script):
   ```bash
   # Works for both fresh starts and resumes
   scripts/work.sh <issue-number>
   ```
   The script checks what already exists and only creates what's missing:
   - No worktree → creates branch, worktree, pushes, creates draft PR
   - Worktree exists → reports it and continues
   - Branch on remote but no local worktree → recreates worktree from remote
   - PR already exists → shows it instead of creating a duplicate

   For orphan PR recovery (branch name known, issue number unknown):
   ```bash
   scripts/work.sh --resume <branch>
   ```

   Skip this step if already inside the worktree (continuation mode).

3. Gather implementation context (script fetches title only, not the full body):
   ```bash
   # Fetch issue body with plan
   gh issue view <N> --json number,title,body

   # If returning after review, read feedback
   gh pr view <PR_NUM> --json comments
   ```
   - Parse the plan section below `---` separator in issue body (if present)
   - If review feedback exists, identify the requested changes

4. Implement the changes:
   - Read the plan section (or review feedback) to understand what to build
   - Work inside the worktree directory
   - Commit in logical chunks using conventional format

5. Push updates and post progress to issue:
   ```bash
   git push origin $(git branch --show-current)
   ```
   After each push, post an issue comment summarizing progress:
   ```bash
   gh issue comment <N> --body "### Update: <brief description>
   - Completed: ...
   - Blockers: ... (if any)
   - Decisions: ... (if any)
   - Plan changes: ... (if any)"
   ```
   The first push (when draft PR is created) should note "Draft PR opened: #X".

6. If the plan changes during implementation:
   - Edit the issue body to reflect the updated plan (keep it as the single source of truth)
   - Note the change in the issue comment for that push

7. Squash-rebase onto main to ensure the PR is mergeable:
   ```bash
   scripts/rebase.sh
   git push --force-with-lease
   ```
   The script squashes all feature commits into one before rebasing, avoiding the conflict minefield of replaying git-sync noise commits individually.
   - If a conflict arises, resolve it (only one round) and `git add -A && git rebase --continue`
   - Verify mergeability after push: `gh api repos/{owner}/{repo}/pulls/<PR_NUM> --jq '.mergeable_state'`

8. Report: "Draft PR updated. Progress posted to issue #N."

9. Suggest next step: "Run `review` sub-skill to review the PR"


## Guidelines

- Requires an existing issue -- use `new` sub-skill first to create one
- Commit frequently in logical chunks with conventional format
- PR body MUST include "Closes #N" for auto-close on merge (the script handles this for new PRs)
- If PR already exists (returning after feedback), just push updates
- Branch naming: `issue-<number>-<slug>` (slug = lowercase, hyphens, max 30 chars)
