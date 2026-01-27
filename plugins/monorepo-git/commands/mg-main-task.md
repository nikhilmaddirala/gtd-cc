---
name: mg-main-task
description: Create, list, or update tasks in the PARA task directory
---

# Task Management

## Overview

This command manages tasks stored in `30-para/tasks/`.

CRITICAL: You MUST use the mg-main skill's `task` sub-skill for this task.


## Context

If the user has provided any additional context, pass that into the skill invocation: $ARGUMENTS


## Process

1. Load the mg-main skill's `task` sub-skill
2. Determine operation from user input:
   - No args or "list" → list tasks
   - Description text → create new task
   - Task ID → show or update task
3. Execute the appropriate operation
