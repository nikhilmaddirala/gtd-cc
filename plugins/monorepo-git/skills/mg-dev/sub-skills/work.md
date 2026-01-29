---
description: Read issue context and implement the plan in the feature worktree
---

# Work

## Overview

Read the linked GitHub issue and comments and implement the plan. 


## Context

User has a feature worktree with a plan ready. They want to implement the task.


## Process

- Fetch the relevant Github issue. The user may have specified the issue number or description. Else you can try to search the issue matching the branch number.
- Fetch the issue. Read full issue and all comments to understand the goal and plan
   ```bash
   gh issue view ${ISSUE_NUM} --json number,title,body,comments
   ```
- Implement the plan
- Use `commit.md` to commit logical chunks and create a draft pull request.
- Verification: All plan items implemented and committed


## Guidelines

- Commit frequently in logical chunks
- Keep commits focused and conventional


