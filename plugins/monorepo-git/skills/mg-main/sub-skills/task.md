---
description: Task CRUD and listing using GitHub Issues
---

# Task

## Overview

Create, list, and manage tasks stored as GitHub Issues with standard labels.


## Context

User wants to create a new task or view existing tasks from the main worktree.


## Process

1. Determine operation (create, list, view, or update)

2. For create:
   ```bash
   gh issue create \
     --title "Task title here" \
     --body "$(cat <<'EOF'
   ## Goal

   Describe what needs to be done.

   ## Context

   Any relevant background information.
   EOF
   )" \
     --label "status-todo,priority-p3"
   ```
   - Extract issue number from output
   - Report: "Created issue #N"

3. For list:
   ```bash
   # List open issues with status labels
   gh issue list --label "status-todo" --json number,title,labels --jq '.[] | "#\(.number)\t\(.title)"'
   gh issue list --label "status-doing" --json number,title,labels --jq '.[] | "#\(.number)\t\(.title)"'
   gh issue list --label "status-planning" --json number,title,labels --jq '.[] | "#\(.number)\t\(.title)"'
   ```
   - Display table: #, title, status, priority

4. For view (single issue):
   ```bash
   gh issue view N --json number,title,body,labels,comments
   ```
   - Display issue details with any plan comments

5. For update:
   ```bash
   # Change priority
   gh issue edit N --remove-label "priority-p3" --add-label "priority-p1"

   # Change status
   gh issue edit N --remove-label "status-todo" --add-label "status-doing"

   # Add comment
   gh issue comment N --body "Update: ..."
   ```

6. Verification: Issue created, listed, or updated


## Guidelines

- Default labels for new issues: `status-todo`, `priority-p3`
- User can override priority: "create urgent task" → `priority-p1`
- Size labels added during planning, not at creation
- When listing, group by status (todo, planning, doing)
- Issue numbers are the primary identifier (no zero-padding needed)


## Examples

Create task:
```
User: "create task: add dark mode support"
→ gh issue create --title "Add dark mode support" --label "status-todo,priority-p3"
→ "Created issue #42"
```

Create urgent task:
```
User: "urgent: login fails on mobile"
→ gh issue create --title "Login fails on mobile" --label "status-todo,priority-p1"
```

List tasks:
```
User: "list tasks" or "show my tasks"
→ Display table of open issues grouped by status
```

View task:
```
User: "show task 42"
→ gh issue view 42 --json ...
→ Display issue details
```
