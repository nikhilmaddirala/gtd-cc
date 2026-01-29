---
name: monorepo-git
description: Git operations for monorepo workflows. Conventional commits, subtree publishing (CRUD + status + publish), and project graduation (lab to production). Use when committing, managing subtrees, or graduating projects.
---

# monorepo-git

## Overview

Git operations for monorepo workflows. Three sub-skills for daily git, subtree management, and project lifecycle.

## Context

User wants to perform git operations in a monorepo: commit changes, manage subtree remotes, check sync status, publish to subtrees, or graduate projects from lab to production.

## Sub-skills

Load the appropriate sub-skill from `sub-skills/` based on user intent.

- **commit.md**: Analyze changes, create logical commits, optionally push
  - Triggers: "commit", "push", "commit and push"

- **subtree.md**: CRUD, sync status, and curated publishing for subtrees
  - Triggers: "add subtree", "list subtrees", "pull subtree", "subtree status", "publish"

- **graduate.md**: Move project from lab to production with GitHub repo and subtree setup
  - Triggers: "graduate project", "move to production"

## Process

- Determine user intent
- Load the appropriate sub-skill
- Execute sub-skill process

## Guidelines

- Use conventional commit format: `type(scope): description`
- Subtrees use `remote-*` naming convention for auto-detection
- NEVER use `git push remote-name main` for subtrees — always use `git subtree push --prefix=<dir> remote-name main`
- Directory mappings come from `.monorepo-git.yaml` (preferred) or git history fallback
- Always get user approval before committing or publishing

## Appendix

### Configuration

Read `.monorepo-git.yaml` from repo root if present:

```yaml
subtree_remote_prefix: "remote-"
default_branch: "main"

subtrees:
  remote-project-a:
    prefix: "path/to/project-a"

directories:
  lab: "path/to/lab"
  public: "path/to/public"
  private: "path/to/private"
```
