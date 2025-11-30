---
description: Orchestrate GitHub workflow stages autonomously by delegating to appropriate agents
allowed_tools:
  - Bash(gh issue:*)
  - Bash(gh pr:*)
  - Bash(git:*)
---

## Overview

Orchestrate multiple GitHub workflow stages by analyzing issue state and delegating execution to the appropriate agents. This workflow coordinates complex multi-stage workflows, determining which agent should be invoked based on issue status and user preferences.

## Context

Workflow orchestration receives:
- Issue number (required) or empty (will show recent issues for selection)
- Workflow type preference (optional): plan, build, review, merge, or auto
- Current issue state including labels, assigned PR, and completion status
- Agent availability and capabilities

## Your Task

**Goal**: Determine appropriate workflow stage(s) and invoke the correct agent(s) in sequence.

**Process**:

1. Parse input to determine issue number and workflow type
   - If empty: Fetch recent open issues and present for user selection
   - If numeric: Treat as issue number and ask for workflow type
   - If text: Parse for issue number and workflow keywords

2. Fetch issue details to understand current state
   - Issue status and labels
   - Associated PR if any exists
   - Implementation plan status
   - Completion requirements

3. Determine appropriate workflow stage(s)
   - If workflow type specified: Use that directly
   - If "auto" mode: Analyze issue state and determine next logical stage
     - New/unstarted issue → Planning stage
     - Planned issue ready for implementation → Build stage
     - PR open for review → Review stage
     - Approved PR ready to merge → Merge stage
   - For multi-stage workflows: Execute agents in correct sequence with proper handoff

4. Invoke appropriate agent(s)
   - Pass issue number and context to agent
   - Maintain workflow continuity between stages
   - Allow user to review/approve between stages for multi-stage workflows

5. Return orchestration completion summary
   - Which stages were executed
   - Final issue state
   - Next recommended action if any

## Guidelines

- Use `gh` to interact with GitHub for issue and PR information
- Parse issue labels to understand workflow state (e.g., "plan::approved", "implementation::in-progress")
- Handle multi-stage workflows by executing agents sequentially with context passing
- For "auto" mode, intelligently determine next stage based on issue state
- Gracefully handle missing or closed issues
- Provide clear feedback about which agent(s) will be invoked and why

## Success Criteria

- ✅ Issue number identified or selected from recent issues
- ✅ Workflow type determined (explicit or inferred from issue state)
- ✅ Appropriate agent(s) identified for workflow stage(s)
- ✅ Agent(s) invoked with correct context and issue information
- ✅ Multi-stage workflows execute agents in proper sequence
- ✅ Orchestration summary provided showing completed stages and next steps
- ✅ Issue state reflects completed workflow stages
