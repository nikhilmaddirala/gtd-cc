---
name: gh-manage
description: Single entrypoint for triage and orchestration across plan/build/review/merge
---

# Manage (Triage + Orchestrate)

## Overview

Use this command as the human-facing entrypoint. It loads the `gh-manage` skill to triage vague asks, set labels, and orchestrate to the correct downstream agent.

## Context

User provides a free-form request or an issue/PR number via $ARGUMENTS. If missing, recent issues will be shown for selection.

## Process

1) Load the `gh-manage` skill.  
2) If the request is vague, run the `triage` workflow to clarify, set lifecycle labels, and create/update an issue if needed.  
3) Run the `orchestrate` workflow to package context (issue/PR numbers, labels, plan link, CI status, prior-stage notes) and dispatch to the correct agent:
   - Planning → `gh-plan-agent`
   - Build/implementation → `gh-build-agent`
   - Review/approval/merge → `gh-review-agent` (including merge workflow)
4) Report back with routing decision, labels set, and next steps.
