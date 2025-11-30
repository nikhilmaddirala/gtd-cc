---
description: Orchestrate GitHub workflow stages autonomously by delegating to appropriate agents
allowed_tools:
  - Bash(gh issue:*)
  - Bash(gh pr:*)
  - Bash(git:*)
---

## Overview

Orchestrate multiple GitHub workflow stages by analyzing issue state and delegating execution to the appropriate agents (plan → build → review/merge). This workflow coordinates multi-stage flows, determines which agent to invoke, and passes the necessary context.

**DO NOT EXECUTE ANY PLAN/BUILD/REVIEW/MERGE WORK DIRECTLY. THIS WORKFLOW ONLY PACKAGES CONTEXT AND CALLS THE APPROPRIATE AGENT.**

## Context

Workflow orchestration receives:
- Issue number (required) or empty (will show recent issues for selection)
- Workflow type preference (optional): plan, build, review, merge, or auto
- Current issue state including labels, assigned PR, and completion status
- Agent availability and capabilities
- Link to approved plan (if exists) and any build/review summary comments

## Your Task

**Goal**: Determine appropriate workflow stage(s), package the right context, and invoke the correct agent(s) in sequence.

**MANDATORY ROUTING RULE**: ALWAYS DELEGATE. For planning use `gh-plan-agent`; for build/implementation use `gh-build-agent`; for review/approval/merge use `gh-review-agent` (including its merge workflow). DO NOT run those skills directly in this manager.

**Process**:

1. Parse input to determine issue number and workflow type
   - If empty: Fetch recent open issues and present for user selection
   - If numeric: Treat as issue number and ask for workflow type
   - If text: Parse for issue number and workflow keywords

2. Fetch issue details to understand current state
   - Issue status and labels (see `../../_common/labels.md`)
   - Associated PR if any exists
   - Implementation plan status and link
   - Completion requirements and existing comments

3. Determine appropriate workflow stage(s)
   - If workflow type specified: Use that directly
   - If "auto" mode: Analyze issue state and determine next logical stage
     - Repo/issue/commit hygiene requests → route to ops agents directly (e.g., `gh-repo-setup-agent`, `gh-issue-creation-agent`, `gh-issue-management-agent`, `gh-commit-agent`)
     - New/unstarted issue → Planning stage (`gh-plan-agent`)
     - Planned issue ready for implementation → Build stage (`gh-build-agent`)
     - PR open for review → Review stage (`gh-review-agent` for review/human-approval as needed)
     - Approved PR ready to merge → Merge stage (`gh-review-agent` merge workflow)
   - For multi-stage workflows: Execute agents in correct sequence with proper handoff

4. Invoke appropriate agent(s) with packaged context
   - Always pass: issue number, PR number (if any), labels, plan link/comment URL, and any summary notes from previous stage
   - For build: include approved plan link and acceptance criteria
   - For review: include PR number, CI status, and build notes
   - For merge: include PR number, approval signals, and cleanup targets
   - **Never perform implementation/review/merge steps here—always delegate to the appropriate agent.**

5. Maintain workflow continuity
   - Update labels to reflect stage transitions (see `../../_common/labels.md`); do not invent labels
   - If a needed label is missing, delegate to an ops agent (`gh-issue-management-agent`/`gh-repo-setup-agent`) to create/apply it
   - Allow human review/approval between stages when requested
   - Persist key links/comments in the issue for the next agent

6. Return orchestration completion summary
   - Which stages were executed
   - Final issue state
   - Next recommended action if any

## Guidelines

- Use `gh` to interact with GitHub for issue and PR information
- Parse issue labels to understand workflow state (see `../../_common/labels.md`)
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
