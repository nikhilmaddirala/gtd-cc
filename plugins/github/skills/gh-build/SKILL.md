---
name: gh-build
description: GitHub workflow automation skill for code implementation and building.
---

# GitHub Build Skill

## Overview

This skill provides comprehensive guidance for GitHub build workflows including code implementation in isolated development environments. It serves as the authoritative source for all GitHub build operations. Use this skill when implementing approved plans in isolated development environments, creating worktrees, writing code and running tests, or creating draft pull requests ready for review.

## Workflows

Use the appropriate workflow from the `workflows/` directory:

- **build-new.md** - Implements approved plans from scratch by creating worktrees, writing code, running tests, and creating draft PRs ready for review
- **build-iterate.md** - Updates existing PRs by addressing review feedback and change requests

## Guidelines

Follow these general guidelines when executing any workflow in this skill:

- **Single Source of Truth**: This skill and its workflow files contain all procedural knowledge for GitHub build operations.
- **Isolated Development**: Always work in dedicated worktrees for isolated development environments.
- **Quality First**: All code must pass tests, linting, and build verification before creating or updating PRs.
- **Merge Conflict Prevention**: Always rebase on main before creating or updating PRs to ensure zero merge conflicts:
  1. Fetch latest from main: `git fetch origin main`
  2. Rebase your work: `git rebase origin/main`
  3. If conflicts arise, resolve them immediately and verify tests still pass
  4. Force-push if needed after rebase: `git push --force-with-lease`
  5. Verify PR shows as mergeable in GitHub before finishing
- **Conventional Commits**: Use imperative mood with format: `<type>(<scope>): <description>` (e.g., `feat(auth): add login form`)
- **Repository Conventions**: Adapt to existing code style, architecture patterns, and naming conventions.
- **Security Awareness**: Review code for security vulnerabilities (XSS, injection, etc.) before submitting.
- **When this skill is referenced by a command or agent**: Read the workflow file, follow the process steps exactly as written, reference guidelines and success criteria to ensure quality.
- **Common References**: See `../_common/guidelines.md` for shared hygiene and `../_common/labels.md` for lifecycle labels expected by ops/review.

### Common Requirements (Both Workflows)

- **Work autonomously**: No human interaction during implementation
- **Document thoroughly**: Clear commit messages and PR descriptions with context
- **Handle errors gracefully**: Update labels and provide clear error information when blockers occur
- **Worktree management**: Use the pattern `worktrees/issue-<number>-<slug>` and clean up after merging

## Additional Information

### Error Handling

If workflows encounter blocking issues:
- Document the problem clearly in PR comments or issue comments
- For technical issues: Suggest alternative approaches or request clarification
- For merge conflicts: Rebase on main; if unresolvable, document resolution strategy
- For test failures: Fix issues or document known limitations with mitigation plans
- For worktree issues: Clean up worktree and branch, update issue label to "blocked"

### Dependencies

- **Planning Completed**: Implementation depends on having an approved implementation plan (for build-new)
- **Repository Setup**: Repository must have proper worktree structure and branch protection
- **Development Environment**: Build requires isolated development environments
- **Code Review Standards**: Review depends on established quality guidelines and requirements
