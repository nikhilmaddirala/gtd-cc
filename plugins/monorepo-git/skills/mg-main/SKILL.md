---
name: mg-main
description: Main worktree skill for issue management, git operations, and subtree publishing. Use when in main worktree (not .worktrees/*). Triggers on "create task", "list tasks", "start task", "commit", "push", "status", "publish subtrees".
---

# mg-main

## Overview

Main worktree skill. Handles issue management via GitHub Issues, git operations, and subtree publishing. For feature worktrees, see `mg-dev` skill.

## Context

User is in the main worktree and wants to:
- Issue management: create, list, start working on issues
- Daily git: commit, push, status
- Subtree publishing: check divergence, publish to selected subtrees
- Project lifecycle: graduate projects from lab to production

## Sub-skills

CRITICAL: Load the appropriate sub-skill from `sub-skills/` based on user intent.

### Issue management

- **task.md**: Create, list, update issues via GitHub
  - Triggers: "create task", "new task", "list tasks", "show tasks"
  - Uses: `gh issue create`, `gh issue list`, `gh issue edit`

- **start.md**: Plan issue and create worktree
  - Triggers: "start task", "work on issue", "begin issue 42"
  - Posts plan as issue comment, creates `.worktrees/issue-{N}`

- **merge.md**: Merge PR and cleanup worktree
  - Triggers: "merge task", "finish issue 42", "merge and cleanup"
  - Uses: `gh pr merge --squash`, auto-closes issue via "Closes #N"

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
- **_common/labels.md**: GitHub label definitions
- **resources/templates/config.example.yaml**: Configuration template

## Guidelines

- NEVER perform destructive git operations (`git reset --hard`, `git push --force`) without explicit user request
- NEVER assume user changes should be discarded
- Daily workflow (commit/push/status) NEVER touches subtrees
- Use conventional commit format: `type(scope): description`
- For "commit and push" requests, run commit then push sequentially

## Appendix

### Label schema

Issues use standard labels for workflow tracking:
- Status: `status-todo`, `status-planning`, `status-doing`, `status-review`, `status-done`
- Priority: `priority-p1` through `priority-p4`
- Size: `size-xs`, `size-s`, `size-m`, `size-l`, `size-xl` (t-shirt sizing)

Run `/mg-repo-setup` to create labels in a new repository.

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
