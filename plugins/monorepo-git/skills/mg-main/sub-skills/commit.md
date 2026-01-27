---
description: Analyze changes and create logical commits with conventional format
---

# Commit

## Overview

This sub-skill analyzes repository changes and creates logical commits using conventional commit format. It groups changes by git subtree and by feature/fix/topic rather than just by directory.

## Context

User wants to commit changes. This may be a single change or multiple unrelated changes that should be separate commits.

## Process

### 1. Check status

```bash
git status
git diff --stat
git log -5 --oneline
```

### 2. Group changes logically

Grouping guidelines:
- CRITICAL: Subtrees should be in separate commits; e.g. we should not mix dragonix/ changes and gtd-cc/ changes in a single commit.
- Group related changes together (same feature/fix/topic)
- Split unrelated changes within the same directory
- Aim for logical, atomic commits

Present plan BEFORE executing:
1. Analyze changes (read files, check diffs)
2. Show YOUR recommended commit grouping with:
   - Commit message (using conventional format)
   - List of files in that commit
3. Ask: "Does this grouping look good? (y/n)"
4. ONLY AFTER approval, execute git add and git commit

Do NOT run any git add or git commit commands before getting user approval.

### 3. Commit with conventional format

For each logical group:

```bash
git add <files-or-directory>
git commit -m "type(scope): description"
```

Types: feat, fix, docs, style, refactor, test, chore
Scope: Directory or project name
Examples:
- `feat(my-project): add user authentication`
- `fix(config): resolve memory leak`
- `docs: update installation guidelines`

### 4. Verify

```bash
git status
```

Success criteria:
- No staged changes
- No unstaged modifications
- No untracked files that should be committed
- Output shows: "nothing to commit, working tree clean"

If uncommitted changes remain, return to step 2 and group remaining changes.

### 5. Offer push

After committing, ask user:
> "Run `/mg-push` to push these changes?" (y/n)

If yes, run the push sub-skill.

## Guidelines

- Always get user approval before committing
- If pre-commit hook fails, fix issues and create NEW commit (never amend)
- If staged unrelated changes, use `git reset` to unstage, then stage correct files
- Consolidate related changes into fewer commits
