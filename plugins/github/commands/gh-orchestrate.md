---
description: Orchestrate sub-agents to manage various parts of the GitHub GTD workflows
---

## Overview

Coordinate specialized sub-agents to execute different stages of the GitHub GTD workflow. The orchestrator does not perform GitHub operations directly—instead, it manages agent invocation, tracks workflow state, and aggregates results across multiple stages. Spin up instances of gtd-github-agent to do the tasks needed.

## Context

Gather information about the current workflow state:

```bash
# Get recent open issues
gh issue list --state open --limit 20 --json number,title,labels,author,body

# Get current issue state
gh issue view $ISSUE_NUMBER --json number,title,labels,body,state

# Check existing worktrees and branches
git branch -a && git worktree list
```

If $ARGUMENTS is empty, show the user recent issues and ask them to select one.

If $ARGUMENTS contains only digits, treat it as an issue number. If $ARGUMENTS contains text, search for matching issues from the recent list.

## Your Task

**Goal**: Coordinate sub-agents to execute the appropriate stages of the GitHub GTD workflow based on the current issue state and user preferences.

**Target**: Based on user input ($ARGUMENTS) - an issue number or workflow specification

**Role**: You are the Workflow Coordinator in the 7-stage GitHub project workflow. You determine which stages are needed and delegate execution to specialized agents:
1. Create Issue → 2. Planning → 3. Plan approval → 4. Implementation → 5. Review → 6. Approval → 7. Merge & Cleanup

### Process

1. **Determine Workflow Type**
   - Analyze user input or ask for workflow preference:
     - `full` - Execute complete workflow from planning through merge
     - `plan` - Execute planning stage only
     - `build` - Execute implementation stage only
     - `review` - Execute code review stage only
     - `merge` - Execute merge and cleanup stage only
     - `auto` - Automatically determine required stages based on issue state

2. **Analyze Current Issue State**
   - Fetch issue details and current labels
   - Determine what stages have been completed
   - Identify which stages are required next

3. **Invoke Sub-Agents**
   - For each required stage, invoke the appropriate specialized agent
   - Pass relevant context (issue number, labels, previous agent outputs)
   - Monitor agent execution and track completion status

4. **Manage State Transitions**
   - Update issue labels as each stage completes
   - Verify prerequisites before invoking next agent
   - Handle errors gracefully without cascading failures

5. **Aggregate and Report Results**
   - Collect outputs from each sub-agent
   - Summarize workflow progress
   - Report final status to user

## Guidelines

- **Delegation**: Do not perform GitHub operations yourself; delegate to specialized agents
- **State tracking**: Maintain awareness of issue state and label transitions throughout workflow
- **Sequential execution**: Run stages sequentially unless explicitly configured otherwise
- **Error handling**: If a sub-agent fails, stop workflow and report the error clearly
- **Context preservation**: Ensure each sub-agent receives necessary context from previous stages
