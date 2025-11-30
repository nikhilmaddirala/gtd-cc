---
description: Autonomously implement approved plans or address review feedback in isolated worktrees
---

## Overview

Build production-ready code from approved implementation plans or address review feedback in isolated development environments, creating pull requests ready for review.

## Context

Start by gathering recent issues and PRs to identify what to build:

```bash
# Get recent open issues with implementation label
gh issue list --state open --limit 20 --json number,title,labels,author,body

# Get recent PRs that may need updates
gh pr list --state open --limit 20 --json number,title,labels,headRefName,body
```

Issue/PR to work on will be provided as context when invoking this skill.

Once you have identified the target (issue or PR), gather repository information:

```bash
# Get current repository state
echo "Repository: $(git remote get-url origin)"
echo "Current branch: $(git branch --show-current)"
echo "Worktrees: $(git worktree list)"
echo "Recent commits: $(git log --oneline -5)"

# Find issues ready for implementation
echo "Looking for issues with 'status-planning-done' label..."
gh issue list --state open --label "status-planning-done" --limit 5 --json number,title,labels,body

# Check existing worktrees and branches
echo "Existing worktrees:"
ls -la worktrees/ 2>/dev/null || echo "No worktrees directory"
echo "Feature branches:"
git branch -r | grep -E "issue-[0-9]+" || echo "No feature branches found"

# Verify repository is clean before starting
if [ -n "$(git status --porcelain)" ]; then
  echo "WARNING: Repository has uncommitted changes"
  git status --short
fi
```

## Your Task

**Goal**: Autonomously implement approved plans or address review feedback by building production-ready code in isolated worktrees that is ready to merge without conflicts.

**Target**: Provided as context when invoking this skill - can be either:
1. An issue with "status-planning-done" label (new implementation from an approved plan)
2. A PR with open review comments (addressing feedback on existing work)

**Role**: You are Phase 4 (Implementation) in the 7-stage GitHub project workflow:
1. Create Issue → 2. Planning → 3. Plan approval → **4. Implementation** ← (You are here) → 5. AI review → 6. Human review → 7. Merge & cleanup

### Process

#### Path A: New Implementation (Issue with "status-planning-done" label)

1. **Verify Target Issue**
   - Confirm issue has "status-planning-done" label
   - IMPORTANT: Get all the issue comments and extract approved implementation plan from issue comments

2. **Setup Development Environment**
   - Create worktree and branch (if not already exists):
      - `worktrees/issue-<number>-<slug>`
      - `issue-<number>-<slug>`
   - CRITICAL: You MUST work in a dedicated worktree for this task.
   - Rebase on main branch to ensure clean history

3. **Execute Implementation Plan**
   - Parse approved plan from issue comments
   - Implement code changes systematically
   - Add comprehensive tests and documentation
   - Run tests, linting, and build verification
   - Ensure code meets repository standards

4. **Create Pull Request**
   - Rebase on main to eliminate any merge conflicts before creating PR
   - Commit changes with conventional format (max 3 commits)
   - Create draft PR with detailed description and link to issue

#### Path B: Address Review Feedback (PR with open comments)

1. **Verify Target PR**
   - Confirm PR exists and has open review comments or requested changes
   - Extract review feedback and requirements from PR comments
   - Identify the linked issue (if any)

2. **Setup Development Environment**
   - Switch to existing worktree if available, or create new one
   - Fetch latest changes from main branch
   - **CRITICAL**: Rebase PR branch on latest main to ensure no merge conflicts exist
   - Verify worktree is clean and ready for changes

3. **Address Review Feedback**
   - Parse all review comments and change requests
   - Implement requested changes systematically
   - Run tests, linting, and build verification
   - Ensure all feedback is addressed

4. **Update Pull Request**
   - Rebase again on main to guarantee zero merge conflicts
   - Commit changes with conventional format (focused on specific feedback)
   - Push updates to existing PR (do not create new PR)
   - Update PR description if needed to reflect changes made


### Common Requirements (Both Paths)

- **Work autonomously**: No human interaction during implementation
- **Follow repository conventions**: Adapt to existing code style and architecture
- **Ensure quality**: All tests pass, code lints, builds successfully
- **Use isolated environments**: Always work in dedicated worktrees
- **Document thoroughly**: Clear commit messages and PR descriptions
- **Prevent merge conflicts**: Always rebase on main before creating/updating PR
- **Handle errors gracefully**: Update labels and provide clear error information when blockers occur:
  - Technical issues: Document problems and suggest alternatives in PR comments
  - Missing context: Request clarification through PR comments on the original issue
  - Architecture conflicts: Propose solutions and create follow-up issues
  - Test failures: Fix issues or document known limitations with mitigation plans
  - Merge conflicts: Rebase on main; if unresolvable conflicts exist, document in PR with mitigation strategy
  - Worktree issues: Clean up worktree and branch, update issue label to "blocked"

### Merge Conflict Prevention Strategy

**Before creating or updating any PR:**
1. Fetch latest from main: `git fetch origin main`
2. Rebase your work: `git rebase origin/main`
3. If conflicts arise, resolve them immediately and verify tests still pass
4. Force-push if needed after rebase: `git push --force-with-lease`
5. Verify PR shows as mergeable in GitHub before finishing

This ensures the PR is always ready to merge without human intervention.

## Success Criteria & Output

Your work is complete when all criteria are met. End with a summary:

### For New Implementation (Path A):
- ✅ Worktree created: `worktrees/issue-<number>-<slug>`
- ✅ Branch created and pushed: `issue-<number>-<slug>`
- ✅ All acceptance criteria from the plan are met
- ✅ Code builds successfully without errors
- ✅ All tests pass (unit, integration, existing regression tests)
- ✅ Code quality checks pass (linting, formatting, security scans)
- ✅ Documentation is updated and accurate
- ✅ Changes committed with conventional format
- ✅ PR created with "needs review" label and linked to issue
- ✅ PR rebased on main with zero merge conflicts

### For Review Feedback (Path B):
- ✅ All review comments addressed
- ✅ Requested changes implemented
- ✅ Code builds successfully without errors
- ✅ All tests pass
- ✅ Code quality checks pass
- ✅ Changes committed and pushed to existing PR
- ✅ PR rebased on main with zero merge conflicts
- ✅ PR is mergeable and ready for approval
