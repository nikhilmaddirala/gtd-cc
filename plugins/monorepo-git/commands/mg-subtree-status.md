---
name: mg-subtree-status
description: Show sync status between monorepo and all subtree remotes
---

# Subtree Status

## Overview

This command shows the sync status for all subtree remotes, including pending and incoming commit counts.

CRITICAL: You MUST use the monorepo-git skill (subtree-status sub-skill) for this task.

## Context

If the user has provided any additional context, pass that into the skill invocation: $ARGUMENTS

## Process

1. Load the monorepo-git skill's `subtree-status` sub-skill
2. Execute the status workflow:
   - Detect all subtree remotes
   - Check pending/incoming commits for each
   - Display status table
   - Suggest next actions per subtree
