---
description: CRUD operations for managing Git subtrees (add, list, pull, move, remove)
---

# Subtree Manage

## Overview

This sub-skill provides comprehensive CRUD operations for managing Git subtrees. Subtrees enable selective directory synchronization with external GitHub repositories while keeping the monorepo as the source of truth.

## Context

User wants to manage subtrees: add new ones, list existing ones, pull changes, move directories, or remove subtrees.

## Process

Route to the appropriate operation section based on user intent:
- "add subtree" -> Create: Add subtree
- "list subtrees" -> Read: List subtrees
- "pull subtree" -> Update: Pull changes
- "move subtree" -> Update: Move directory
- "remove subtree" -> Delete: Remove subtree

---

## Create: Add subtree

Add an existing GitHub repository as a subtree to the monorepo.

### Process

1. Gather information from user:
   - GitHub repository URL
   - Target directory path in monorepo
   - Remote name (suggest: `remote-<project-name>`)

2. Add remote

```bash
git remote add remote-name https://github.com/user/repo.git
```

3. Add subtree

```bash
git subtree add --prefix=path/to/directory remote-name main --squash
```

If directory already exists:
```bash
mv existing-directory /tmp/backup-$(date +%Y%m%d)
git subtree add --prefix=path/to/directory remote-name main --squash
```

4. Verify

```bash
git remote -v | grep remote-name
ls -la path/to/directory/
git log --oneline -1
```

### Guidelines

- Use `--squash` to keep history clean
- Follow `remote-*` naming convention for auto-detection
- If wrong branch, replace `main` with actual branch name

---

## Read: List subtrees

Display all subtree remotes with directory mappings and sync status.

### Process

1. Detect subtree remotes

```bash
git remote -v | grep "remote-"
```

2. Map to directories

Read `.monorepo-git.yaml` from repo root for `subtrees:` mappings (preferred). If no config, fall back to git history:

```bash
# Extract from commit BODY (%B, not %s) — git-subtree-dir is in the body
git log --all --grep="git-subtree-dir:" --pretty=format:"%B" | grep "git-subtree-dir:" | sort -u
```

3. Present as table

```
Remote Name          | Directory                | URL
---------------------|--------------------------|---------------------------
remote-project-a     | path/to/project-a        | github.com/user/project-a
remote-project-b     | path/to/project-b        | github.com/user/project-b
```

### Guidelines

- If no subtrees found, inform user
- For full sync status, suggest `/mg-subtree-status`

---

## Update: Pull changes

Fetch and merge latest changes from subtree remote into monorepo.

### Process

1. Identify subtree (from user or list available)

2. Fetch and check for changes

```bash
git fetch remote-name main
git log --oneline HEAD..remote-name/main -- path/to/directory/
```

If no changes, inform user subtree is up to date.

3. Pull changes

```bash
git subtree pull --prefix=path/to/directory remote-name main --squash
```

4. Resolve conflicts if any

```bash
git status
# Edit conflicted files
git add <resolved-files>
git commit -m "chore(subtree-name): merge upstream changes"
```

5. Verify

```bash
git log --oneline -1
git status
```

### Guidelines

- Always use `--squash` for clean history
- Guide user through conflict resolution if needed

---

## Update: Move directory

Relocate a subtree to a different directory path.

### Process

1. Check for uncommitted changes

```bash
git status path/to/old-directory/
```

Commit or stash changes first if any.

2. Move directory

```bash
git mv path/to/old-directory path/to/new-directory
```

3. Commit move

```bash
git commit -m "chore(subtree-name): move from old-path to new-path"
```

4. Verify subtree still works

```bash
git subtree push --prefix=path/to/new-directory remote-name main --dry-run
```

### Guidelines

- Use `git mv` to preserve history
- Test with `--dry-run` before actual push

---

## Delete: Remove subtree

Completely remove a subtree from the monorepo.

### Process

1. SAFETY: Create backup

```bash
BACKUP_DIR="/tmp/subtree-backup-$(date +%Y%m%d-%H%M%S)"
cp -r path/to/directory "$BACKUP_DIR"
echo "Backup created at: $BACKUP_DIR"
```

2. SAFETY: Confirm with user

> "This will permanently remove the subtree 'name' from the monorepo. A backup has been created at $BACKUP_DIR. Continue? (yes/no)"

Only proceed if user confirms with "yes".

3. Remove directory

```bash
git rm -r path/to/directory/
```

4. Remove remote

```bash
git remote remove remote-name
```

5. Commit removal

```bash
git commit -m "chore(subtree-name): remove subtree from monorepo"
```

6. Verify

```bash
git remote -v | grep remote-name  # Should be empty
ls path/to/  # Directory should be gone
git status
```

### Guidelines

- Always create backup before deletion
- Require explicit "yes" confirmation
- Inform user of backup location for recovery

---

## Appendix

### Common mistakes

Using git push instead of git subtree push:
```bash
# WRONG:
git push remote-name main

# CORRECT:
git subtree push --prefix=path/to/directory remote-name main
```

Forgetting --squash flag:
```bash
# WRONG:
git subtree pull --prefix=path/to/directory remote-name main

# CORRECT:
git subtree pull --prefix=path/to/directory remote-name main --squash
```

### Troubleshooting

- **Subtree push fails "creates a split"**: No changes to push, skip it
- **Merge conflicts**: Use Update: Pull section for resolution
- **Remote not found**: Check spelling, re-add with `git remote add`
- **Auth failures**: Verify SSH key or use HTTPS with token
