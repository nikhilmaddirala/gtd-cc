---
name: gh-orchestrate
description: Orchestrates GitHub workflow stages autonomously
---

# Workflow Orchestration

## Overview

This command orchestrates multiple GitHub workflow stages by delegating to the appropriate agents. It serves as a coordinator for complex multi-stage workflows.

## Context

User provides issue number and optional workflow type via $ARGUMENTS. If not provided, recent issues will be shown for selection.

## Process

Parse $ARGUMENTS to determine the issue number and workflow type:
- If empty: Show recent open issues and ask user to select one and choose workflow type
- If numeric: Treat as issue number, ask for workflow type (plan, build, review, merge, or auto)
- If text: Parse for issue number and workflow keywords

Based on the workflow type selected:
- **plan**: Invoke gh-plan-agent for planning
- **build**: Invoke gh-build-agent for implementation
- **review**: Invoke gh-review-agent for code review
- **merge**: Invoke gh-merge-agent for merge and cleanup
- **auto**: Analyze issue state and invoke appropriate agent(s) in sequence

For multi-stage requests, orchestrate agents in the correct sequence.

