---
name: gh-manage
description: GitHub workflow automation skill for repository management, operations, and workflow coordination.
---

# GitHub Manage Skill

## Overview

This skill provides comprehensive guidance for GitHub repository management workflows including repository setup, issue creation, plan approval, code review, human approval, git operations, merge processes, and cleanup activities. It serves as the authoritative source for all GitHub management operations. Use this skill when setting up new repositories for issue-driven development, creating well-structured issues from user requirements, reviewing implementation approaches, performing code reviews, conducting approval processes, managing git commits, or executing merge and cleanup operations.

## Workflows

Use the appropriate workflow from the `workflows/` directory:

- **repo-setup.md** - Sets up essential GitHub workflow infrastructure including workflow labels, issue templates, PR templates, branch protection rules, and worktree directory structure
- **issue-creation.md** - Transforms user requirements into well-documented GitHub issues with clear problem statements, acceptance criteria, and appropriate labels
- **approve-plan.md** - Guides humans through reviewing AI-generated implementation plans with decision framework for approval or revision requests
- **review.md** - Performs code reviews focusing on compliance with requirements, bugs, and architectural alignment
- **human-approval.md** - Guides humans through local testing, code review, and approval decision-making for implementations ready for merge
- **commit.md** - Creates well-structured git commits with conventional commit format
- **merge.md** - Executes final merge operations including squash-merging PR to main, closing issues, deleting branches, and removing worktrees

## Guidelines

Follow these general guidelines when executing any workflow in this skill:

- **Single Source of Truth**: This skill and its workflow files contain all procedural knowledge for GitHub management operations.
- **Repository Foundation**: Management workflows emphasize proper repository setup and infrastructure before other operations.
- **Git Best Practices**: All git operations follow conventional commit standards and branch management practices with format `<type>(<scope>): <description>`
- **Clean Operations**: Merge and cleanup workflows focus on maintaining repository hygiene and organization.
- **When this skill is referenced by a command or agent**: Read the workflow file, follow the process steps exactly as written, reference guidelines and success criteria to ensure quality.

## Error Handling

If workflows encounter blocking issues:
- Document the problem clearly in repository documentation
- Update issue label to indicate blocking status
- Suggest alternative approaches or ask for clarification
- Resume when blocker is resolved

## Dependencies

- **Repository Access**: Management workflows require appropriate repository permissions
- **Git Configuration**: Proper git configuration required for commit and merge operations
- **Team Coordination**: Repository setup often requires team consensus and configuration

## Reference Files

All workflow details are contained in individual `.md` files in the `workflows/` directory. Each file provides complete procedural guidance for its specific workflow.
