---
name: mg-repo-setup
description: Initialize GitHub labels for issue-driven workflow (one-time setup)
---

# Repository Setup

## Overview

One-time setup to create the standard labels required for the monorepo-git issue-driven workflow.


## Process

1. Verify GitHub CLI is authenticated
   ```bash
   gh auth status
   ```

2. Check current labels
   ```bash
   gh label list
   ```

3. Create missing labels (idempotent - skips existing)
   ```bash
   # Status labels
   gh label create "status-todo" --description "New issue, needs planning" --color "d4c5f9" 2>/dev/null || echo "status-todo exists"
   gh label create "status-planning" --description "Plan in progress" --color "c5def5" 2>/dev/null || echo "status-planning exists"
   gh label create "status-doing" --description "Implementation in progress" --color "fbca04" 2>/dev/null || echo "status-doing exists"
   gh label create "status-review" --description "PR created, under review" --color "f9d0c4" 2>/dev/null || echo "status-review exists"
   gh label create "status-done" --description "Merged and closed" --color "0e8a16" 2>/dev/null || echo "status-done exists"

   # Priority labels
   gh label create "priority-p1" --description "Urgent, do first" --color "d73a4a" 2>/dev/null || echo "priority-p1 exists"
   gh label create "priority-p2" --description "High priority" --color "ff7b00" 2>/dev/null || echo "priority-p2 exists"
   gh label create "priority-p3" --description "Medium priority" --color "fbca04" 2>/dev/null || echo "priority-p3 exists"
   gh label create "priority-p4" --description "Low priority, backlog" --color "c2e0c6" 2>/dev/null || echo "priority-p4 exists"

   # Size labels
   gh label create "size-xs" --description "Extra small, < 1 hour" --color "bfd4f2" 2>/dev/null || echo "size-xs exists"
   gh label create "size-s" --description "Small, 1-4 hours" --color "c2e0c6" 2>/dev/null || echo "size-s exists"
   gh label create "size-m" --description "Medium, 1-2 days" --color "fbca04" 2>/dev/null || echo "size-m exists"
   gh label create "size-l" --description "Large, 3-5 days" --color "f9d0c4" 2>/dev/null || echo "size-l exists"
   gh label create "size-xl" --description "Extra large, 1+ week" --color "d73a4a" 2>/dev/null || echo "size-xl exists"
   ```

4. Verify labels were created
   ```bash
   gh label list | grep -E "^(status-|priority-|size-)"
   ```


## Output

Report which labels were created vs already existed:

```
Repository setup complete!

Labels created:
- status-todo
- status-planning
- ...

Labels already existed:
- priority-p1
- ...

Ready to use /mg-main-task to create issues.
```
