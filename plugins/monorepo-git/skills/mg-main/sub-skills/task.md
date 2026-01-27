---
description: Task CRUD and listing for PARA-based task management
---

# Task

## Overview

Create, list, and manage tasks stored as markdown files in `30-para/tasks/`.


## Context

User wants to create a new task or view existing tasks from the main worktree.


## Process

1. Determine operation (create, list, or update)

2. For create:
   - Generate task ID (next available number, zero-padded 3 digits)
   - Create file: `30-para/tasks/task-{id}-{slug}.md`
   - Populate frontmatter and goal section

3. For list:
   ```bash
   ls -1 30-para/tasks/task-*.md
   ```
   - Parse frontmatter, display table: ID, title, status, priority

4. Verification: Task file created or list displayed


## Guidelines

- Task IDs are zero-padded 3 digits (001, 042, 123)
- Slugs are kebab-case from title
- Status: todo | doing | done
- Priority: p1 | p2 | p3 | p4
