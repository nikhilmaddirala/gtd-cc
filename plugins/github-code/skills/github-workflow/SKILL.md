# GitHub Workflow Skill

## Overview

This skill provides foundation knowledge and utilities for working with GitHub repositories, issues, pull requests, and workflows using the GitHub CLI (`gh` command).

## Core Capabilities

### Issue Management
- Creating and updating issues
- Searching and filtering issues by labels, state, and content
- Parsing issue details, comments, and linked PRs
- Managing issue labels and assignments

### Pull Request Workflow
- Creating pull requests with descriptions and linked issues
- Reviewing and managing PR approvals
- Handling merge conflicts and merge strategies
- Squashing, rebasing, and conventional commits

### Repository Operations
- Managing branches (creation, deletion, listing)
- Working with worktrees for isolated development
- Checking repository status and remotes
- Managing GitHub workflows and actions

### Code Review
- Retrieving PR reviews and comments
- Parsing code suggestions and feedback
- Tracking review status and requirements

## Key Tools

- `gh issue` - Issue management
- `gh pr` - Pull request operations
- `gh repo` - Repository information
- `git worktree` - Isolated development environments
- `git branch` - Branch management

## Common Patterns

### Finding Issues
```bash
# List open issues with specific label
gh issue list --state open --label "needs-implementation" --json number,title,body

# Search issues by content
gh issue list --search "keyword" --json number,title
```

### Creating and Updating PRs
```bash
# Create PR with linked issue
gh pr create --title "PR Title" --body "Description" --issue <number>

# Check PR status
gh pr view <number> --json status,reviewDecision
```

### Working with Worktrees
```bash
# Create isolated development environment
git worktree add worktrees/feature-branch feature-branch-name

# Clean up after completion
git worktree remove worktrees/feature-branch
```

## Integration Points

This skill integrates with:
- **gh-build agent**: Uses issue management and PR creation
- **gh-merge agent**: Handles final merge operations
- **gh-maintenance agent**: Monitors repository health
- **Implementation skill**: Coordinates code changes with GitHub workflows
