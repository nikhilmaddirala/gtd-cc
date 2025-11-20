---
description: Develop detailed implementation plans with options analysis for GitHub issues
---

## Overview

Research the codebase, analyze options, and create implementation plans ready for autonomous execution.

## Context

Gather recent issues to identify the issue to plan:

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

**Goal**: Develop a focused implementation plan ready for autonomous execution.

**Issue to plan**: Based on user input ($ARGUMENTS) or selection from recent issues

**Role**: You are Stage 2 (Planning) in the 7-stage workflow:
1. Create Issue → **2. Planning** ← (You are here) → 3. Plan approval → 4. Implementation → 5. Review → 6. Approval → 7. Merge

### Process

1. **Understand the Issue**
   - Read and summarize the requirement from the lightweight issue
   - Ask clarifying questions if the request is ambiguous or incomplete
   - Define the problem statement and goals clearly

2. **Detailed Requirement Analysis**
   Gather and clarify:
   - **Problem/Goal**: What exactly needs to be done and why it matters
   - **Acceptance Criteria**: How will we know this is complete and successful
   - **Context**: Relevant background, constraints, related work, or links
   - **Dependencies**: Related issues, blockers, or prerequisites
   - **Scope**: What's definitively in scope vs. out of scope
   - **Constraints**: Technical, time, or resource constraints

3. **Research Codebase**
   - Explore existing architecture and patterns that could be reused
   - Understand naming and structural conventions
   - Check for similar implementations that can inform the approach
   - Identify areas where the change will impact existing code

4. **Repository Convention Analysis**
   - Analyze recent issues and pull requests for style patterns
   - Check existing documentation for guidelines and standards
   - Understand testing conventions and requirements
   - Identify any repository-specific processes or standards

5. **Research External Options (If Applicable)**
   - If multiple significant approaches exist, compare alternatives
   - Document key tradeoffs and implementation considerations
   - Consider third-party libraries, frameworks, or tools
   - Evaluate long-term maintainability and scalability implications

6. **Technical Feasibility Assessment**
   - Evaluate implementation complexity and estimated effort
   - Identify potential risks or blockers
   - Consider testing requirements and validation approaches
   - Assess if the implementation approach is technically sound

7. **Develop Implementation Approach**
   - Define the technical approach and rationale
   - List specific files to create/modify
   - Outline detailed implementation sequence
   - Consider integration points and impacts on existing functionality
   - Plan for testing, documentation, and validation

8. **Post Plan**
   - Create plan comment with structured format (see below)
   - Update issue label from "needs planning" to "needs plan approval"

### Guidelines

- **Comprehensive analysis**: Since issue creation is now lightweight, you must conduct thorough requirement gathering, scoping, and analysis.

- **Research before deciding**: Understand the codebase architecture, patterns, conventions, and options. This prevents wasted implementation effort.

- **Detail for autonomous execution**: The gh-build agent will execute this plan independently. Be specific enough to avoid ambiguity.

- **Follow repository conventions**: Research and adapt to existing code style, architecture patterns, testing standards, and documentation requirements.

- **Ask clarifying questions**: Get alignment early on requirements, scope, dependencies, and technical approach if the issue is ambiguous or complex.

- **Consider all aspects**: Analyze technical feasibility, risks, testing requirements, documentation needs, and integration impacts.

- **Repository context gathering**: Analyze recent issues, pull requests, and documentation to understand project standards and processes.

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
- Update the issue label from "status-planning-todo" to "status-planning-review"

## Success Criteria

- ✅ Issue requirement thoroughly understood with detailed clarification completed
- ✅ Comprehensive scope and boundary analysis completed (in scope vs. out of scope)
- ✅ Dependencies, constraints, and acceptance criteria clearly defined
- ✅ Repository conventions researched and understood (patterns, standards, processes)
- ✅ Codebase research completed (architecture, patterns, conventions, similar implementations)
- ✅ Technical feasibility assessed (complexity, risks, blockers, testing requirements)
- ✅ Options analyzed and documented (if multiple approaches exist)
- ✅ Implementation plan posted on issue with required structure:
  - Summary, Technical Approach, Files to Create/Modify, Implementation Steps, Options (if applicable)
- ✅ Plan is detailed enough for autonomous execution by gh-build agent
- ✅ Issue label updated from "status-planning-todo" to "status-planning-review"
