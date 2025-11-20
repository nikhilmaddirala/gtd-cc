---
description: Create a lightweight GitHub issue to capture user requests
---

## Overview

Quickly capture user requests as GitHub issues with basic categorization. All detailed planning and scoping will be handled by the planning workflow.

## Context

Repository state:
```bash
# Available issue labels
gh label list

# Issue templates (if any)
ls -la .github/ISSUE_TEMPLATE/ 2>/dev/null || echo "No issue templates found"
```

## Your Task

**Goal**: Create a lightweight GitHub issue that captures the user's request.

**User's initial request**: $ARGUMENTS

**Role**: You are Stage 1 (Issue Creation) in the 7-stage workflow:
1. Create Issue → 2. Planning → 3. Plan approval → 4. Implementation → 5. Review → 6. Approval → 7. Merge

### Process

1. **Quick clarification**
   - Get a clear problem statement from the user
   - Determine basic issue type (feature, bug, docs, refactor, or other)
   - Keep clarification minimal - just enough to understand the request

2. **Check for issue templates**
   - If `.github/ISSUE_TEMPLATE/` exists, offer available templates to user
   - Allow user to choose a template or create custom issue
   - If no templates, use lightweight format below

3. **Basic issue structure**
   Use this lightweight format (adapt based on templates or repo conventions):
   ```markdown
   ## Request
   [User's request or problem statement in their own words]

   ## Basic Information
   - **Type**: [feature/bug/docs/refactor/other]
   - **Additional context**: [Any immediate context provided by user]
   ```

4. **Apply basic labels (if available)**
   - Check `gh label list` output to see what labels exist
   - Apply `status-planning-todo` label if available
   - Apply basic type label based on issue type (type-feature, type-bug, type-docs, type-refactor, etc.)

5. **Create the issue**
   - Use `gh issue create` with:
     - Clear title based on user request
     - Lightweight body with request and basic info
     - `status-planning-todo` label (if available)
   - Return issue URL and number

## Guidelines

- **Focus on capture**: Your job is to capture the request, not plan it
- **Minimal clarification**: Only ask what's needed to understand the request
- **No scoping**: Don't ask about scope, dependencies, or implementation approaches
- **No feasibility assessment**: Don't evaluate if/how something should be implemented
- **Fast turnaround**: The goal is quick issue creation without extensive discussion
- **Apply `status-planning-todo` label**: This signals the next stage should handle detailed analysis

## Success Criteria

- ✅ Issue title clearly captures the user's request
- ✅ Issue body contains the user's request and basic categorization
- ✅ Issue has `needs planning` label applied (if available)
- ✅ Issue is created quickly without extensive planning discussion
- ✅ Issue URL and number are shared with user
