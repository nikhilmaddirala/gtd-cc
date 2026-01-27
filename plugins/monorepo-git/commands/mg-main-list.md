---
name: mg-main-list
description: List tasks by status, project, or priority
---

# List Tasks

## Overview

This command lists tasks from `30-para/tasks/`.

CRITICAL: You MUST use the mg-main skill's `task` sub-skill for this task.


## Context

If the user has provided any additional context (filters), pass that into the skill invocation: $ARGUMENTS


## Process

1. Load the mg-main skill's `task` sub-skill
2. List tasks, applying any filters from arguments
3. Display table: ID, title, status, priority
