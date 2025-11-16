---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

- The user has made some changes to this git repository and needs help committing those changes.
- Your task is to understand the git context and commit all uncommitted changes descriptive commit messages.
- Usually a single commit should suffice for all the user's changes, but in some cases it makes more sense to break it up into multiple commits. No more than 2 or 3 commits at most.
- The end result is that all uncommitted changes should be committed.
