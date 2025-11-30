---
name: gh-merge
description: Executes final merge operations and cleanup
---

# Merge and Cleanup

## Overview

This command executes final merge operations and cleanup using the gh-manage skill. CRITICAL: You MUST use the gh-manage skill for this task.

## Context

User will provide an issue number via $ARGUMENTS. If not provided, recent issues with "status-implementation-done" label will be shown for selection.

## Process

Load the gh-manage skill first. Follow its `merge` workflow exactly as written to squash-merge the PR to main, close the issue and PR, delete the branch, remove the worktree, and complete cleanup activities.
