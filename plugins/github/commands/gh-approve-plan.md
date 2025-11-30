---
name: gh-approve-plan
description: Reviews AI-generated implementation plans and provides approval or feedback
---

# Plan Approval

## Overview

This command guides you through reviewing and approving implementation plans using the gh-manage skill. CRITICAL: You MUST use the gh-manage skill for this task.

## Context

User will provide an issue number via $ARGUMENTS. If not provided, recent issues with "status-planning-review" label will be shown for selection.

## Process

Load the gh-manage skill first. Follow its `approve-plan` workflow exactly as written to review the AI-generated implementation plan and provide approval, revision requests, or feedback. The workflow provides a decision framework for your approval.
