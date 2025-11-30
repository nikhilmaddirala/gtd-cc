---
description: Address review feedback on existing pull requests
---

## Overview

Update existing pull requests by addressing review feedback and change requests in isolated development environments.

## Context

Start by gathering recent pull requests to identify the PR to update:

```bash
# Get recent open PRs with review comments
gh pr list --state open --limit 20 --json number,title,labels,reviewDecision,body

# Check existing worktrees and branches
echo "Existing worktrees:"
ls -la worktrees/ 2>/dev/null || echo "No worktrees directory"

# Verify repository is clean before starting
if [ -n "$(git status --porcelain)" ]; then
  echo "WARNING: Repository has uncommitted changes"
  git status --short
fi
```

PR to work on will be provided as context when invoking this workflow.

## Your Task

**Goal**: Autonomously address review feedback on open pull requests by implementing requested changes that are ready to merge without conflicts.

**PR to update**: Provided as context when invoking this workflow - must have open review comments or requested changes

**Role**: Implementation revision stage of the GitHub workflow

### Process

1. **Verify Target PR**
   - Confirm PR exists and has open review comments or requested changes
   - Extract all review feedback and requirements from PR comments
   - Identify the linked issue (if any)
   - Understand the scope and priority of requested changes

2. **Setup Development Environment**
   - Switch to existing worktree for this PR if available, otherwise create one
   - Fetch latest changes from main: `git fetch origin main`
   - Rebase PR branch on main to ensure no merge conflicts: `git rebase origin/main`
   - Verify worktree is clean and ready for changes

3. **Address Review Feedback**
   - Parse all review comments and change requests
   - Implement requested changes systematically
   - Run tests, linting, and build verification
   - Ensure all feedback is fully addressed

4. **Update Pull Request**
   - Apply merge conflict prevention (see SKILL.md guidelines)
   - Commit changes with conventional format focused on specific feedback
   - Push updates to existing PR (never create a new PR)
   - Add comment summarizing which feedback items were addressed

## Guidelines

Refer to the common guidelines in SKILL.md:
- Merge conflict prevention strategy
- Conventional commit format
- Worktree management patterns
- Common requirements for all build workflows

## Success Criteria

- ✅ All review comments understood and documented
- ✅ All requested changes implemented
- ✅ Code builds successfully without errors
- ✅ All tests pass (unit, integration, regression)
- ✅ Code quality checks pass (linting, formatting, security)
- ✅ Changes committed and pushed to existing PR
- ✅ PR rebased on main with zero merge conflicts
- ✅ PR is mergeable and ready for approval
- ✅ PR comment summarizes addressed feedback
- ✅ Review-ready labels applied for handoff (see `../../_common/labels.md`)
