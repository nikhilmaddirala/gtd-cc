---
name: mg-push
description: Push commits to monorepo remote (does not touch subtrees)
---

# Push to Monorepo

## Overview

This command pushes commits to the monorepo remote only. For subtree publishing, use `/mg-publish`.

CRITICAL: You MUST use the monorepo-git skill (push sub-skill) for this task.

## Context

If the user has provided any additional context, pass that into the skill invocation: $ARGUMENTS

## Process

1. Load the monorepo-git skill's `push` sub-skill
2. Execute the push workflow:
   - Check for uncommitted changes
   - Push to monorepo origin
   - Handle conflicts if rejected
   - Verify success
