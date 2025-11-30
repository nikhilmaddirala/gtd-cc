---
name: gh-build
description: Builds code from approved implementation plans or addresses review feedback
---

# Build Implementation

## Overview

This command guides you through code implementation in isolated development environments using the gh-build skill. Build production-ready code from approved plans or address review feedback.

## Context

User will provide issue or PR number via $ARGUMENTS. If not provided, recent issues with "status-planning-done" label and open PRs will be shown for selection.

## Process

Load the gh-build skill and follow the appropriate workflow based on your target:

**If building from an approved plan (issue with "status-planning-done" label):**
- Follow the `build-new` workflow to implement the plan from scratch

**If addressing review feedback (PR with open comments):**
- Follow the `build-iterate` workflow to update the existing PR

Both workflows operate in isolated worktrees, run tests and quality checks, and ensure the PR is ready for review or approval.
