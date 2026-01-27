---
description: Read issue context and implement the plan in the feature worktree
---

# Work

## Overview

Read the linked GitHub issue and implement the plan posted during `/mg-main-start`.


## Context

User has a feature worktree with a plan ready. They want to implement the task.


## Process

1. Extract issue number from branch
   ```bash
   BRANCH=$(git branch --show-current)
   ISSUE_NUM=$(echo $BRANCH | sed 's|issue/\([0-9]*\)-.*|\1|')
   echo "Working on issue #${ISSUE_NUM}"
   ```

2. Fetch issue context
   ```bash
   gh issue view ${ISSUE_NUM} --json number,title,body,comments
   ```
   - Extract goal from issue body
   - Find plan in comments (look for "## Plan" heading)

3. Display context to user
   - Issue title and goal
   - Plan steps
   - Files to modify

4. Implement the plan
   - Make changes as specified in the plan
   - Use `commit.md` to commit logical chunks

5. Verification: All plan items implemented and committed


## Guidelines

- Follow the plan created during `/mg-main-start`
- Plan is in the issue comments, not the issue body
- Commit frequently in logical chunks
- Keep commits focused and conventional
- If plan is unclear, post a comment asking for clarification


## Example

```
User: "/mg-dev-work"

1. Branch: issue/42-add-dark-mode-support → Issue #42
2. gh issue view 42 --json ... →
   - Title: "Add dark mode support"
   - Body: "## Goal\nAdd toggle for dark/light theme..."
   - Comments: [{ body: "## Plan\n**Files to modify**:\n- theme.ts..." }]
3. Display:
   "Issue #42: Add dark mode support

   Plan:
   1. Add theme context in theme.ts
   2. Create toggle component
   3. Update App.tsx to wrap with provider

   Ready to implement."
4. [Agent implements changes, commits along the way]
```
