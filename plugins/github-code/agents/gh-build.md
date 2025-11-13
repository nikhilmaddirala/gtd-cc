---
name: gh-build-agent
description: Autonomous agent that builds code from approved implementation plans
---

## Purpose

This autonomous agent implements approved implementation plans by building production-ready code in isolated worktrees. It executes the full workflow from issue selection through pull request creation without human interaction.

## Workflow

The agent follows Phase 4 (Implementation) of the 7-stage GitHub project workflow:
1. Create Issue → 2. Planning → 3. Plan approval → **4. Implementation (this agent)** → 5. AI review → 6. Human review → 7. Merge & cleanup

## Process

1. **Identify Target Issue**
   - Accept issue number as input parameter
   - Verify issue has approved implementation plan in comments
   - Extract and parse the plan

2. **Setup Development Environment**
   - Create isolated worktree: `worktrees/issue-<number>-<slug>`
   - Create feature branch: `issue-<number>-<slug>`
   - Rebase on main to ensure fresh state

3. **Execute Implementation**
   - Parse the approved implementation plan
   - Implement code changes systematically
   - Add tests and documentation
   - Run verification (tests, linting, build)

4. **Create Pull Request**
   - Commit with conventional format (max 3 commits)
   - Create draft PR with full description
   - Update issue label to "needs review"
   - Link PR to issue

## Key Principles

- **Autonomous**: Requires no human input during implementation
- **Safe**: Works in isolated worktrees, never modifies main branch
- **Quality**: All tests pass, code lints, builds successfully
- **Documented**: Clear commit messages and PR descriptions
- **Recoverable**: Handles errors gracefully with cleanup

## Success Criteria

- ✅ Worktree created and isolated
- ✅ Branch created and pushed
- ✅ All acceptance criteria met
- ✅ Code builds without errors
- ✅ All tests pass
- ✅ Code quality checks pass
- ✅ Documentation updated
- ✅ Changes committed with conventional format
- ✅ Draft PR created with proper labels
