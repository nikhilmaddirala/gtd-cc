---
description: Clarify vague requests, classify work, label appropriately, and route to plan/build/review via orchestrator
allowed_tools:
  - Bash(gh issue:*)
  - Bash(gh search:*)
---

## Overview

Serve as the intake manager when a human provides a vague or mixed request. Clarify the ask, map it to the correct issue or create one, set lifecycle labels, and decide whether to proceed to planning, building, or reviewing.

**DO NOT EXECUTE PLAN/BUILD/REVIEW/MERGE WORK. THIS WORKFLOW ONLY CLARIFIES AND ROUTES TO THE APPROPRIATE AGENT.**

When routing, explicitly hand off to: `gh-plan-agent` (planning), `gh-build-agent` (implementation/PR updates), or `gh-review-agent` (review/approval/merge). Do not run those skills directly here.

## Context

Inputs expected:
- Free-form request from human (may or may not include issue/PR number)
- Repository to operate in

## Process

1. **Clarify the Ask**
   - Summarize the request back to the human; ask for missing essentials (goal, scope, constraints, deadlines).
   - Identify whether this is a feature/change, bug, support question, or review/approval request.

2. **Check for Existing Work**
   - Search existing issues/PRs by keywords to avoid duplicates.
   - If a relevant issue/PR exists, gather its number, labels, and status.

3. **Decide Routing Path**
   - No clear issue and ask is actionable → create or update an issue with `gh-ops/workflows/issue-creation.md`.
   - Ops hygiene (repo setup/labels/templates/protection, issue lifecycle, commit help) → route to ops agents (`gh-repo-setup-agent`, `gh-issue-creation-agent`, `gh-issue-management-agent`, `gh-commit-agent`).
   - Issue exists but needs scoping → route to planning (`gh-plan-agent`).
   - Issue has approved plan and needs implementation → route to build (`gh-build-agent`).
   - PR open and needs review/approval/merge → route to review (`gh-review-agent` workflows).

4. **Label and Record Context**
   - Apply lifecycle labels from `../../_common/labels.md` based on the chosen path; do not invent new labels.
   - If required labels are missing in the repo, delegate to ops (`gh-issue-management-agent` or `gh-repo-setup-agent`) to create/apply them.
   - Add a short triage note/comment capturing: summary, routing decision, next agent, and any open questions.

5. **Handoff**
   - Pass to the orchestrator workflow with: issue/PR numbers, labels, any plan link, acceptance criteria, and triage notes.
   - If information is still missing, document blockers and request specifics from the human.

## Success Criteria

- ✅ Request is summarized and clarified with missing info identified or resolved
- ✅ Existing work checked to prevent duplicates
- ✅ Issue/PR identified or created as needed
- ✅ Lifecycle labels set per `../../_common/labels.md`
- ✅ Routing decision made (plan/build/review) and documented in a comment/note
- ✅ Context packaged for orchestrator/next agent (issue/PR numbers, labels, plan link, acceptance criteria, triage notes)
