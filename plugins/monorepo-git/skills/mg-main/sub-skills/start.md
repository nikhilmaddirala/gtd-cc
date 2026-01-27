---
description: Plan an issue and create an isolated worktree for implementation
---

# Start

## Overview

Prepares an issue for implementation: explores codebase, creates plan, sets up worktree.


## Context

User has an issue number and wants to start working on it. Issue must exist in GitHub.


## Process

1. Load issue
   ```bash
   gh issue view N --json number,title,body,labels
   ```
   - Extract title for branch slug
   - Extract body for context (goal, requirements)

2. Update status to planning
   ```bash
   gh issue edit N --remove-label "status-todo" --add-label "status-planning"
   ```

3. Explore and plan
   - Read relevant code based on issue description
   - Identify files to modify
   - Create implementation plan

4. Post plan as issue comment
   ```bash
   gh issue comment N --body "$(cat <<'EOF'
   ## Plan

   **Goal**: Brief statement

   **Files to modify**:
   - path/to/file.ts - change X
   - path/to/other.ts - add Y

   **Steps**:
   1. First step
   2. Second step
   3. Third step

   **Testing**:
   - How to verify the changes work
   EOF
   )"
   ```

5. Update status to doing
   ```bash
   gh issue edit N --remove-label "status-planning" --add-label "status-doing"
   ```

6. Create worktree
   ```bash
   # Generate slug from title (kebab-case, max 30 chars)
   SLUG=$(echo "issue-title-here" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | cut -c1-30)

   git branch issue/${N}-${SLUG} main
   git worktree add .worktrees/issue-${N} issue/${N}-${SLUG}
   ```

7. Verification: Worktree created and user prompted to cd into it


## Guidelines

- Always create plan before worktree
- Post plan as comment so it's visible in GitHub
- Worktree directory: `.worktrees/issue-{N}`
- Branch naming: `issue/{N}-{slug}`
- Slug is kebab-case from first 30 chars of title


## Example

```
User: "/mg-main-start 42"

1. gh issue view 42 → "Add dark mode support"
2. gh issue edit 42 --add-label "status-planning"
3. [Agent explores codebase, identifies theme.ts, App.tsx]
4. gh issue comment 42 --body "## Plan ..."
5. gh issue edit 42 --add-label "status-doing"
6. git worktree add .worktrees/issue-42 issue/42-add-dark-mode-support

Output:
"Worktree created at .worktrees/issue-42
Branch: issue/42-add-dark-mode-support

To start implementation:
  cd .worktrees/issue-42
  /mg-dev-work"
```
