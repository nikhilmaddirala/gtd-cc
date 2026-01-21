---
name: mg-graduate
description: Graduate a project from lab to production with GitHub repo and subtree setup
---

# Graduate Project

## Overview

This command graduates a project from a development/lab directory to production, creating a GitHub repository and setting up subtree synchronization.

CRITICAL: You MUST use the monorepo-git skill (graduate sub-skill) for this task.

## Context

If the user has provided project name or paths, pass that into the skill invocation: $ARGUMENTS

## Process

1. Load the monorepo-git skill's `graduate` sub-skill
2. Execute the graduation workflow:
   - Gather project information (source, target, visibility)
   - Create GitHub repository
   - Move project to production directory
   - Commit to monorepo
   - Set up subtree remote
   - Push to initialize remote
   - Verify completion
