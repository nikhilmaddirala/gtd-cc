---
name: mg-status
description: Show quick working tree status for the monorepo
---

# Git Status

## Overview

This command shows a quick status of the working tree. For subtree sync status, use `/mg-subtree-status`.

CRITICAL: You MUST use the monorepo-git skill (status sub-skill) for this task.

## Context

If the user has provided any additional context, pass that into the skill invocation: $ARGUMENTS

## Process

1. Load the monorepo-git skill's `status` sub-skill
2. Execute the status workflow:
   - Show basic git status
   - Summarize changed files
   - Suggest next action (commit/push)
