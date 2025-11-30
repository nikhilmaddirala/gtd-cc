---
description: Analyze issues and apply appropriate labels and comments
---

## Overview

Manage issue lifecycle by analyzing current state and taking appropriate actions to move issues through the workflow.

## Context

Issue to work on will be provided as context when invoking this skill.

```bash
# Get issue details
gh issue view $ISSUE_NUMBER --json title,body,labels,comments,number,author

# Get linked PR if it exists
gh pr list --search "$ISSUE_NUMBER" --json number,title,headRefName,url,state

# Check current worktree
git worktree list | grep "issue-$ISSUE_NUMBER" || echo "No worktree found"
```

## Your Task

**Goal**: Analyze the issue and take appropriate action to move it forward in the workflow.

**Issue to manage**: Provided as context when invoking this skill.

### Process

1. **Analyze Issue State**
   - Identify current labels and status
   - Check for implementation plans in comments
   - Look for linked PRs
   - Review any outstanding questions or blockers

2. **Determine Next Action**
   Based on the current state, take one of these actions:

   **Planning needed** (no implementation plan):
   ```bash
   gh issue edit $ISSUE_NUMBER --add-label "status-planning-todo"
   gh issue comment $ISSUE_NUMBER --body "This issue needs implementation planning. Adding planning label to begin stage 2."
   ```

   **Plan ready for review** (implementation plan exists but not approved):
   ```bash
   gh issue edit $ISSUE_NUMBER --remove-label "status-planning-todo" --add-label "status-planning-review"
   gh issue comment $ISSUE_NUMBER --body "Implementation plan ready for review. See the plan in issue comments."
   ```

   **Implementation needed** (plan approved, no PR):
   ```bash
   gh issue edit $ISSUE_NUMBER --remove-label "status-planning-done" --add-label "status-implementation-todo"
   gh issue comment $ISSUE_NUMBER --body "Plan approved. Ready for implementation (stage 4)."
   ```

   **Implementation ready for review** (PR exists and needs review):
   ```bash
   gh issue edit $ISSUE_NUMBER --remove-label "status-implementation-todo" --add-label "status-implementation-review"
   gh issue comment $ISSUE_NUMBER --body "Implementation complete and ready for code review (stage 5)."
   ```

   **Implementation approved** (PR reviewed and approved):
   ```bash
   gh issue edit $ISSUE_NUMBER --remove-label "status-implementation-review" --add-label "status-implementation-done"
   gh issue comment $ISSUE_NUMBER --body "Implementation approved and ready for merge (stage 7)."
   ```

   **Blocked or needs clarification**:
   ```bash
   gh issue edit $ISSUE_NUMBER --add-label "blocked"
   gh issue comment $ISSUE_NUMBER --body "This issue is blocked and needs human intervention before proceeding."
   ```

3. **Add Contextual Comments**
   - Summarize what action was taken and why
   - Reference the relevant workflow stage
   - Note any dependencies or blockers
   - Suggest next steps if applicable

## Guidelines

- **State-based decisions**: Use existing labels to determine current workflow stage
- **Clear transitions**: Always update from current state to appropriate next state
- **Helpful comments**: Explain what happened and what comes next
- **Progress forward**: Always aim to move issues toward completion
- **Human awareness**: Flag issues that need human judgment or intervention

## Success Criteria

Your work is complete when:
- ✅ Issue analyzed for current state and needs
- ✅ Appropriate label(s) applied based on workflow stage
- ✅ Informative comment added explaining the action taken
- ✅ Issue is clearly positioned for next workflow step
- ✅ No ambiguous or unclear state remains