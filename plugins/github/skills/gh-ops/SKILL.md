---
name: gh-ops
description: GitHub workflow automation skill for intake, governance, repo hygiene, orchestration, and commit assistance for human-made changes.
---

# GitHub Ops Skill

## Overview

This skill governs repository hygiene and git support for human-made changes on main. Use this skill to set up repositories, create and manage issues, and help humans commit existing work.

## Workflows

Use the appropriate workflow from the `workflows/` directory:

- **repo-setup.md** - Sets up labels, templates, protections, and worktree structure for issue-driven development
- **issue-creation.md** - Transforms requests into well-documented GitHub issues with clear scope and labels
- **issue-management.md** - Manages lifecycle labels, links, and status throughout the development flow
- **commit.md** - Helps humans commit already-made changes on main using conventional commits and safe hygiene

## Guidelines

Follow these general guidelines when executing any workflow in this skill:

- **Single Source of Truth**: This skill and its workflow files contain procedural knowledge for ops/governance.
- **Governance First**: Ensure labels, templates, and protections exist before routing work.
- **Conventional Commits**: Follow `<type>(<scope>): <description>` when assisting humans with commits.
- **Common References**: See `../_common/guidelines.md` and `../_common/labels.md` for shared standards.

## Error Handling

If workflows encounter blocking issues:
- Document the problem clearly on the issue
- Update issue label to indicate blocking status
- Suggest alternative approaches or ask for clarification
- Resume when blocker is resolved

## Dependencies

- **Repository Access**: Ops workflows require appropriate repository permissions
- **Git Configuration**: Proper git configuration required for commit assistance
- **Team Coordination**: Repository setup often requires team consensus and configuration
