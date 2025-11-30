---
description: Implement approved plans by creating code in isolated worktrees
---

## Overview

Build production-ready code from approved implementation plans in isolated development environments, creating pull requests ready for review.

**Goal**: Autonomously implement approved plans by creating production-ready code in isolated worktrees that is ready to merge without conflicts.

## Context

Issue to work on will be provided as context when invoking this workflow. The issue may be specified by issue number or by description. Start by gathering recent issues to identify the issue to build:

```bash
# Find issues ready for implementation
echo "Looking for issues with 'status-planning-done' label..."
gh issue list --state open --label "status-planning-done" --limit 10 --json number,title,labels,body

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


## Process

1. **Verify Target Issue**
   - Confirm issue has "status-planning-done" label
   - Get all issue comments and extract the approved implementation plan
   - Verify the plan has clear implementation steps, files to modify/create, and acceptance criteria

2. **Setup Development Environment**
   - Create worktree and branch (if not already exists):
     - `worktrees/issue-<number>-<slug>`
     - `issue-<number>-<slug>` (branch name)
   - CRITICAL: Work in the dedicated worktree, not main
   - Rebase on main to ensure clean history: `git rebase origin/main`

3. **Execute Implementation Plan**
   - Follow the approved plan steps systematically
   - Implement code changes, add tests, update documentation
   - Run tests, linting, and build verification
   - Ensure all acceptance criteria from the plan are met

4. **Create Pull Request**
   - Apply merge conflict prevention (see SKILL.md guidelines)
   - Commit changes with conventional format (max 3 commits)
   - Create draft PR with detailed description linking to issue
   - PR description should summarize the implementation approach

## Guidelines

Refer to the common guidelines in SKILL.md:
- Merge conflict prevention strategy
- Conventional commit format
- Worktree management patterns
- Common requirements for all build workflows

## Success Criteria

- ✅ Issue has "status-planning-done" label
- ✅ Worktree created: `worktrees/issue-<number>-<slug>`
- ✅ Branch created and pushed: `issue-<number>-<slug>`
- ✅ All acceptance criteria from plan are met
- ✅ Code builds successfully without errors
- ✅ All tests pass (unit, integration, regression)
- ✅ Code quality checks pass (linting, formatting, security)
- ✅ Documentation is updated and accurate
- ✅ Changes committed with conventional format
- ✅ PR created with link to issue
- ✅ PR rebased on main with zero merge conflicts
