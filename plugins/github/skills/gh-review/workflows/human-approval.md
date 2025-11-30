---
description: Guide humans through local testing, verification, and approval decisions before merge
---

## Overview

Support humans in validating a PR locally and deciding whether to approve or request changes.

## Context

Inputs expected:
- PR number (and linked issue number)
- Approved implementation plan link (if available)
- Current labels and CI status

## Process

1. **Gather Context**
   - Fetch PR details, linked issue, CI status, and existing review feedback.
   - Read the approved plan link if present.
2. **Prep Local Validation**
   - Pull latest branch; ensure dependencies and setup instructions are known.
   - If instructions are missing, note the gap and request them from the build agent.
3. **Validate**
   - Run tests/builds listed in the plan/PR description.
   - Perform targeted checks on areas touched (per diff summary).
   - Confirm acceptance criteria from the issue/plan.
4. **Decision**
   - If all checks pass: run through `../../_common/templates/approval-checklist.md`, add approval signal, and update labels to `status-review-approved` (or repo equivalent).
   - If issues found: document blockers, request changes, and set label to `status-review-changes-requested`.
5. **Handoff to Merge**
   - When approved, hand PR number/issue/labels and any validation notes to the merge workflow.

## Guidelines

- Keep feedback concise and action-oriented.
- Reference specific commits/lines when noting issues.
- Use shared labels from `../../_common/labels.md` for state updates.
- If local validation cannot be run, document what was skipped and why.
