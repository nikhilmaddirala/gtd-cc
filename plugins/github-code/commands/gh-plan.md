---
description: Develop detailed implementation plans with options analysis for GitHub issues
---

## Context

Start by gathering recent issues to identify the issue to plan:

```bash
# Get recent open issues
gh issue list --state open --limit 20 --json number,title,labels,author
```

If $ARGUMENTS is empty, show the user the recent issues and ask them to select one.

If $ARGUMENTS contains only digits, treat it as an issue number. If $ARGUMENTS contains text, search for matching issues from the recent list.

Once you have identified the issue number, gather repository information:

```bash
# Get issue details
gh issue view ISSUE_NUMBER --json title,body,labels,number,state

# Check current branches and worktrees
git branch -a && git worktree list

# Get recent commits to understand repo conventions
git log --oneline -n 10

# Check for existing worktrees related to this issue
ls -la worktrees/ 2>/dev/null || echo "No worktrees directory"

# Get repository structure overview
find . -maxdepth 2 -type f -name "*.md" | head -20
```

## Your Task

**Goal**: Develop a focused implementation plan ready for autonomous execution by the gh-build agent.

**Issue to plan**: Based on user input ($ARGUMENTS) or selection from recent issues

### Process

1. **Understand the Issue**
   - Read and summarize the requirement
   - Ask clarifying questions if ambiguous

2. **Research Codebase**
   - Explore existing architecture and patterns that could be reused
   - Understand naming and structural conventions

3. **Research External Options (If Applicable)**
   - If multiple significant approaches exist, compare alternatives
   - Document key tradeoffs

4. **Develop Implementation Approach**
   - Define the technical approach and rationale
   - List files to create/modify
   - Outline implementation sequence

5. **Post Plan**
   - Create plan comment with structured format (see below)
   - Update issue label from "needs planning" to "needs plan approval"

### Guidelines

- **Research before deciding**: Understand the codebase and options. This prevents wasted implementation effort.

- **Detail for autonomous execution**: The gh-build agent will execute this plan independently. Be specific enough to avoid ambiguity.

- **Follow repository conventions**: Adapt to existing code style and architecture patterns.

- **Ask clarifying questions**: Get alignment early if the issue is ambiguous or complex.

## Plan Structure (Post as Issue Comment)

When you've completed the planning process, post a comment on the issue with this structure:

```markdown
## Implementation Plan

### Summary
[1-2 sentence overview of the approach]

### Technical Approach
[How the feature will be implemented and key rationale]

### Files to Create/Modify
- `file/path/one.ts` - Description of changes
- `new-file.ts` - Description of new code

### Implementation Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]
...

### Options (if applicable)
**Option 1: [Name]** - [Description and tradeoffs]
**Option 2: [Name]** - [Description and tradeoffs]
**Recommended: Option [X]** - [Why]
```

After posting the plan:
- Update the issue label from "needs planning" to "needs plan approval"
