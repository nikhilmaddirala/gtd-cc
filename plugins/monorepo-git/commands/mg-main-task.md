---
name: mg-main-task
description: Create, list, or update tasks as GitHub Issues
---

# Task Management

## Overview

This command manages tasks stored as GitHub Issues with standard labels.

CRITICAL: You MUST use the mg-main skill's `task` sub-skill for this task.


## Context

If the user has provided any additional context, pass that into the skill invocation: $ARGUMENTS


## Process

1. Load the mg-main skill's `task` sub-skill
2. Determine operation from user input:
   - No args or "list" → list issues by status
   - Description text → create new issue
   - Issue number → show or update issue
3. Execute the appropriate operation
