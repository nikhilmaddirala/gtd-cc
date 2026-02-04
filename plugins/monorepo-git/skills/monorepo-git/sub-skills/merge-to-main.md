---
description: Merge dev branch to main with clean, subtree-separated commits and optional publishing
---

# Merge to main

## Overview

Merge changes from dev branch to main, creating separate commits per subtree with meaningful messages, then optionally publish affected subtrees to their remotes.

## Context

The monorepo uses a git-sync workflow where daily work happens on `dev` with frequent auto-commits. When ready to release, dev is merged to main with the messy sync commits cleaned up and split by subtree.

## Process

### Setup worktree

Create a temporary worktree for main to avoid disrupting dev:

```bash
git worktree add tmp/main main
cd tmp/main
git fetch origin
git pull origin main
```

### Stage changes

Merge dev changes without committing:

```bash
git merge --squash dev --no-commit
```

This stages all changes from dev since the last merge. If no changes exist, report this and exit early.

### Analyze changes by subtree

Read `.monorepo-git.yaml` to get subtree mappings:

```yaml
subtrees:
  remote-gtd-cc:
    prefix: "40-code/41-public/gtd-cc"
  remote-dragonix:
    prefix: "40-code/42-private/dragonix"
  # ...
```

For each subtree prefix, check for changes:

```bash
git diff --cached --stat -- <prefix>/
```

Group changes into:
- **Subtree changes**: One group per subtree that has changes
- **Non-subtree changes**: Everything else (monorepo infrastructure, docs, knowledge notes) grouped into ONE commit

### Present commit plan

Show the user what will be committed:

```
## Commit plan

### 1. feat(gtd-cc): add claude code CLI guidance
Files: 1 changed
- plugins/random/skills/ai-agent-clis/sub-skills/claude-code-cli.md

### 2. feat(dragonix): add git-sync, omniwm, refactor keyboard modules
Files: 54 changed
- modules/home/cloud-storage/git-sync.nix (new)
- modules/home/programs/omniwm.nix (new)
- modules/home/keyboard/* (refactored into subdirs)
- ...

### 3. chore: monorepo infrastructure and docs
Files: 12 changed
- README.md - git-sync workflow documentation
- justfile - restructured commands for autocomplete
- AGENTS.md - updated guidance
- .gitignore - added tmp/
- 40-code/43-lab/monorepo-scripts/worktree.sh (new)
- 30-para/* - knowledge notes

Does this look good? (yes/no/edit)
```

Guidelines for commit messages:
- Analyze actual file changes to determine type (feat, fix, docs, chore, refactor)
- Summarize the purpose, not just "update X"
- Each subtree MUST be in its own commit
- Non-subtree changes go in ONE commit with detailed description

### Create commits

After user approval, unstage all and commit each group:

```bash
git reset HEAD
```

For each subtree with changes:
```bash
git add <subtree-prefix>/
git commit -m "type(scope): summary

Detailed description of changes.

Co-Authored-By: Claude <noreply@anthropic.com>"
```

For non-subtree changes (single commit):
```bash
git add .
git commit -m "chore: monorepo infrastructure and docs

- README.md: git-sync workflow documentation
- justfile: restructured commands for autocomplete
- worktree.sh: feature branch management with draft PRs
- .gitignore: added tmp/ for temporary worktrees
- 30-para/*: knowledge notes

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Push main

```bash
git push origin main
```

### Publish subtrees

For each subtree that had changes, offer to publish:

```
## Subtrees ready to publish

| Subtree | Remote | Prefix | Status |
|---------|--------|--------|--------|
| gtd-cc | remote-gtd-cc | 40-code/41-public/gtd-cc | Ready |
| dragonix | remote-dragonix | 40-code/42-private/dragonix | Ready |

Publish all? (yes/no/select)
```

Check if remote exists:
```bash
git remote -v | grep remote-<name>
```

If remote not configured, offer to add it based on GitHub username pattern:
```bash
git remote add remote-<name> git@github.com:<user>/<name>.git
```

Publish each selected subtree:
```bash
git subtree push --prefix=<path> remote-<name> main
```

### Cleanup

Return to monorepo root and remove the temporary worktree:

```bash
cd ~/repos/monorepo
git worktree remove tmp/main
```

## Guidelines

- CRITICAL: Each subtree MUST be committed separately (never mix subtree directories)
- Non-subtree changes are grouped into a SINGLE commit with detailed description
- Always get user approval before committing
- Always get user approval before publishing to subtree remotes
- Use intelligent commit messages based on actual changes
- If a subtree remote is not configured, ask user if they want to add it
- Handle merge conflicts by stopping and asking user for guidance
- If no changes exist between dev and main, report this and exit early
