---
name: mg-main-list
description: List GitHub Issues by status, project, or priority
---

# List Tasks

## Overview

This command lists tasks from GitHub Issues.

CRITICAL: You MUST use the mg-main skill's `task` sub-skill for this task.


## Context

If the user has provided any additional context (filters), pass that into the skill invocation: $ARGUMENTS


## Process

1. Load the mg-main skill's `task` sub-skill
2. List issues using: `gh issue list --label "status-todo" --json number,title,labels`
3. Display table: #, title, status, priority
