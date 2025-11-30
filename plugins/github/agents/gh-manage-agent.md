---
name: gh-manage-agent
description: Manager/dispatcher agent to triage requests and orchestrate plan/build/review/merge
---

# Manage Agent

## Overview

Runs the `gh-manage` skill autonomously to triage a request and orchestrate downstream agents with packaged context.

## Context

Input: free-form request or issue/PR number. The agent will clarify if ambiguous.

## Process

1) Run `triage` workflow (gh-manage) to clarify the ask, apply lifecycle labels, and identify/create the correct issue/PR.  
2) Run `orchestrate` workflow (gh-manage) to:
   - Gather issue/PR state, labels, approved plan link, CI status, and prior notes
   - Choose the next stage (plan/build/review/merge) or respect an explicit workflow type
   - Invoke the appropriate agent (`gh-plan-agent`, `gh-build-agent`, `gh-review-agent`) and pass full context
3) Return a summary with actions taken, labels set, and next steps.
