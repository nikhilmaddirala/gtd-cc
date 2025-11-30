---
name: gh-manage
description: GitHub workflow automation skill for repository management, operations, and workflow coordination.
---

# GitHub Manage Skill

This skill provides comprehensive guidance for GitHub repository management workflows including repository setup, issue creation, plan approval, code review, human approval, git operations, merge processes, and cleanup activities. It serves as the authoritative source for all GitHub management operations.

## About This Skill

The GitHub Manage skill is designed to facilitate repository setup and management workflows. It encompasses repository initialization, workflow labels and templates, issue creation, plan approval, code review, human approval, git commit operations, final merge processes, and cleanup activities. This skill consolidates procedural knowledge, best practices, and detailed workflow instructions used across interactive commands and autonomous agents.

### When to Use This Skill

This skill should be used when:
- Setting up a new repository for issue-driven development
- Creating well-structured GitHub issues from user requirements
- Reviewing and approving implementation approaches generated during planning
- Performing code reviews for quality, security, and completeness
- Conducting human approval processes including local testing and final review
- Managing git commit operations with conventional commit format
- Executing final merge operations and cleanup
- Managing branch protection and worktree directory structure
- Performing repository maintenance and cleanup tasks

## Available Workflows

This skill provides detailed guidance for the following workflows:

- **Repository Setup** - Sets up essential GitHub workflow infrastructure including workflow labels, issue templates, PR templates, branch protection rules, and worktree directory structure
- **Issue Creation** - Transform user requirements into well-documented GitHub issues with clear problem statements, acceptance criteria, context, and appropriate labels
- **Plan Approval** - Guides humans through reviewing AI-generated implementation plans with decision framework for approval, revision requests, or questions
- **Code Review** - Performs code reviews focusing on compliance with requirements, README guidelines, significant bugs, and architectural alignment
- **Human Approval** - Guides humans through local testing, code review, and approval decision-making for implementations ready for merge
- **Git Commits** - Creates well-structured git commits with conventional commit format, describing changes with clear intent
- **Merge & Cleanup** - Executes final merge operations including squash-merges PR to main, closes issue, deletes branch, and removes worktree

## Individual Workflow Guides

Each workflow provides detailed procedural instructions in its respective markdown file:

### Repository Setup
**File**: `workflows/repo-setup.md`

Sets up essential GitHub workflow infrastructure in the current repository, including workflow labels, issue templates, PR templates, branch protection rules, and worktree directory structure.

**Use this when**: Setting up a new repository for the first time

### Issue Creation
**File**: `workflows/issue-creation.md`

Transforms user requirements into well-documented GitHub issues with clear problem statements, acceptance criteria, context, and appropriate labels.

**Use this when**: Creating new issues to track work

### Plan Approval
**File**: `workflows/approve-plan.md`

Guides humans through reviewing AI-generated implementation plans. Provides decision framework for approval, revision requests, or questions.

**Use this when**: Human needs to review an implementation plan (only triggered when AI requests approval)

### Code Review
**File**: `workflows/review.md`

Performs code reviews focusing on compliance with requirements, README guidelines, significant bugs, and architectural alignment. Filters for real issues only.

**Use this when**: Reviewing a pull request for quality and correctness

### Human Approval
**File**: `workflows/human-approval.md`

Guides humans through local testing, code review, and approval decision-making for implementations ready for merge.

**Use this when**: Human needs to test and approve an implementation

### Git Commits
**File**: `workflows/commit.md`

Creates well-structured git commits with conventional commit format, describing changes with clear intent.

**Use this when**: Committing changes to the repository

### Merge & Cleanup
**File**: `workflows/merge.md`

Executes final merge operations: squash-merges PR to main, closes issue, deletes branch, and removes worktree.

**Use this when**: Merging an approved implementation to main

## How to Use This Skill

When this skill is referenced by a command or agent:

1. **Read the workflow file** for the appropriate workflow (see list above)
2. **Follow the process steps** as written in the workflow
3. **Reference guidelines and success criteria** to ensure quality
4. **Execute the operations** (usually bash/git/gh commands embedded in workflow)

## Key Principles

**Single Source of Truth**: This skill and its workflow files contain all procedural knowledge for GitHub management operations. Commands reference this skill rather than containing inline instructions.

**Repository Foundation**: Management workflows emphasize proper repository setup and infrastructure before other operations.

**Clean Operations**: Merge and cleanup workflows focus on maintaining repository hygiene and organization.

**Git Best Practices**: All git operations follow conventional commit standards and branch management practices.

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
