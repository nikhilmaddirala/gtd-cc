---
name: monorepo-git
description: This skill should be used when the user asks to "commit my changes", "push changes", "git status", "publish subtrees", "subtree status", or any git operations in a monorepo with subtrees. Handles intelligent commits, monorepo pushes, and curated subtree publishing.
---

# Monorepo Git

## Overview

This skill manages git operations for monorepos with subtree awareness. It separates daily development (high velocity) from subtree publishing (curated).

The monorepo is always the source of truth. Changes flow outward: commit to monorepo first, publish to subtrees when ready.

## Context

User wants to perform git operations in a monorepo. This may be:
- Daily operations: commit, push (monorepo only), status
- Subtree publishing: check divergence, publish to selected subtrees
- Subtree management: add, list, pull, move, remove subtrees
- Project lifecycle: graduate projects from lab to production

## Sub-skills

CRITICAL: Load the appropriate sub-skill from `sub-skills/` based on user intent.

### Daily development

- **commit.md**: Analyze changes and create logical commits
  - Triggers: "commit", "commit my changes", "save changes"
  - After success, prompt user about pushing

- **push.md**: Push to monorepo remote only (no subtree logic)
  - Triggers: "push", "push changes", "push to monorepo"
  - If uncommitted changes exist, suggest commit first

- **status.md**: Quick working tree status
  - Triggers: "status", "git status", "what's changed"
  - For subtree status, suggest `/mg-subtree-status`

### Subtree publishing

- **publish.md**: Curated push to selected subtrees
  - Triggers: "publish", "publish subtrees", "push to subtrees"
  - Shows interactive selection with pending commit counts
  - User chooses which subtrees to publish

- **subtree-status.md**: Show divergence for all subtrees
  - Triggers: "subtree status", "what needs publishing", "check subtrees"
  - Shows table with pending/incoming counts per subtree

- **subtree-manage.md**: CRUD operations for subtrees
  - Triggers: "add subtree", "list subtrees", "pull subtree", "move subtree", "remove subtree"
  - Routes internally to create/read/update/delete sections

### Project lifecycle

- **graduate.md**: Move project from lab to production with subtree setup
  - Triggers: "graduate project", "move to public", "move to production"
  - Creates GitHub repo, moves directory, sets up subtree remote

## Process

1. Determine user intent from their request
2. Load the appropriate sub-skill
3. Execute sub-skill process

## Resources

- **sub-skills/**: Individual operation workflows
- **resources/templates/config.example.yaml**: Configuration template

## Guidelines

- NEVER perform destructive git operations (`git reset --hard`, `git push --force`) without explicit user request
- NEVER assume user changes should be discarded
- Daily workflow (commit/push/status) NEVER touches subtrees
- Use conventional commit format: `type(scope): description`
- For "commit and push" requests, run commit then push sequentially

## Appendix

### Configuration

The skill reads `.monorepo-git.yaml` from repo root if present:

```yaml
subtree_remote_prefix: "remote-"  # Default
default_branch: "main"            # Default
directories:                      # For graduate workflow
  lab: "path/to/lab"
  public: "path/to/public"
  private: "path/to/private"
```

### Subtree detection

Subtree remotes are detected by pattern matching on `git remote -v`:
- Pattern: `remote-*` (configurable via `subtree_remote_prefix`)
- Example: `remote-project-a` corresponds to a subtree

Directory mapping is determined from git history by searching for `git-subtree-dir:` patterns in commit messages.

### Conventional commits

Format: `type(scope): description`

Types: feat, fix, docs, style, refactor, test, chore

Scope: Directory or project name (e.g., `feat(project-a):`, `chore(config):`)
