---
description: Develop detailed implementation plans with options analysis for GitHub issues
---

## Overview

Research the codebase, analyze options, and create implementation plans ready for autonomous execution.

**Goal**: Develop a focused implementation plan ready for autonomous execution.

## Context

Issue to work on will be provided as context when invoking this skill. The issue may be specified by issue number or by description. Gather recent issues to identify the issue to plan:

```bash
# Get recent open issues
gh issue list --state open --limit 20 --json number,title,labels,author
```


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


## Process

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

8. **Post Plan as Issue Comment**
   - Create a plan comment using the template structure from SKILL.md
   - Include Summary, Technical Approach, Files to Create/Modify, Implementation Steps, and Options (if applicable)
   - Update issue label from "status-planning-todo" to "status-planning-review"

### Guidelines

Refer to the guidelines in SKILL.md:
- Research-First Approach
- Comprehensive Analysis
- Detail for Autonomous Execution
- Follow Repository Conventions
- Options Analysis
- Repository Context Gathering

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
