---
name: mg-commit
description: Analyze changes and create logical commits with conventional format
---

# Commit Changes

## Overview

This command guides you through committing changes interactively.

CRITICAL: You MUST use the monorepo-git skill (commit sub-skill) for this task.

## Context

If the user has provided any additional context, pass that into the skill invocation: $ARGUMENTS

## Process

1. Load the monorepo-git skill's `commit` sub-skill
2. Execute the commit workflow:
   - Check status and analyze changes
   - Group changes logically
   - Present commit plan for approval
   - Execute commits after approval
3. Offer to push when done
