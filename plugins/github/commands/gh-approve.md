---
name: gh-approve
description: Guides humans through local testing and final approval process
---

# Implementation Approval

## Overview

This command guides you through testing and approving implementations using the gh-manage skill. CRITICAL: You MUST use the gh-manage skill for this task.

## Context

User will provide an issue number or PR number via $ARGUMENTS. If not provided, recent issues with "status-implementation-review" label will be shown for selection.

## Process

Load the gh-manage skill first. Follow its `human-approval` workflow exactly as written to guide you through local testing, code review, and making an approval decision for the implementation ready to merge.
