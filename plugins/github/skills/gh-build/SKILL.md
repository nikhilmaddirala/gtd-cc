---
name: gh-build
description: GitHub workflow automation skill for code implementation and building.
---

# GitHub Build Skill

This skill provides comprehensive guidance for GitHub build workflows including code implementation in isolated development environments. It serves as the authoritative source for all GitHub build operations.

## About This Skill

The GitHub Build skill is designed to facilitate structured build workflows. It encompasses code implementation in isolated environments, creating worktrees, writing code, running tests, and creating draft pull requests ready for review. This skill consolidates procedural knowledge, best practices, and detailed workflow instructions used across interactive commands and autonomous agents.

### When to Use This Skill

This skill should be used when:
- Implementing approved plans in isolated development environments
- Creating worktrees for isolated development
- Writing code and running tests
- Creating draft pull requests ready for review

## Available Workflows

This skill provides detailed guidance for the following workflows:

- **Build/Implement** - Autonomously implements approved plans by creating worktrees, writing code, running tests, and creating draft PRs ready for review

## Individual Workflow Guides

Each workflow provides detailed procedural instructions in its respective markdown file:

### Build/Implement
**File**: `workflows/build.md`

Autonomously implements approved plans by creating worktrees, writing code, running tests, and creating draft PRs ready for review.

**Use this when**: Building code from an approved implementation plan

## How to Use This Skill

When this skill is referenced by a command or agent:

1. **Read the workflow file** for the appropriate workflow (see list above)
2. **Follow the process steps** as written in the workflow
3. **Reference guidelines and success criteria** to ensure quality
4. **Execute the operations** (usually bash/git/gh commands embedded in workflow)

## Key Principles

**Single Source of Truth**: This skill and its workflow files contain all procedural knowledge for GitHub build operations. Commands reference this skill rather than containing inline instructions.

**Isolated Development**: Implementation workflows emphasize using worktrees for isolated development environments.

**Quality First**: Code review and commit workflows focus on maintaining quality standards and compliance.

**Security Awareness**: Build workflows include security considerations and best practices.

## Error Handling

If workflows encounter blocking issues:
- Document the problem clearly in PR comments or build documentation
- Update issue label to indicate blocking status
- Suggest alternative approaches or ask for clarification
- Resume when blocker is resolved

## Dependencies

- **Planning Completed**: Implementation depends on having an approved implementation plan
- **Repository Setup**: Repository must have proper worktree structure and branch protection
- **Development Environment**: Build requires isolated development environments
- **Code Review Standards**: Review depends on established quality guidelines and requirements

## Reference Files

All workflow details are contained in individual `.md` files in the `workflows/` directory. Each file provides complete procedural guidance for its specific workflow.
