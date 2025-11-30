---
name: gh-manage
description: Manager/dispatcher skill that triages human requests and orchestrates plan/build/review/merge agents.
---

# GitHub Manage Skill

## Overview

This skill is the single human-facing entry point. It clarifies requests, decides the right path, and dispatches to specialized agents (plan, build, review/merge) with the necessary context.

## Workflows

- **triage.md** - Clarifies vague asks, classifies work, applies labels, and decides whether to create/update an issue before routing
- **orchestrate.md** - Routes to plan/build/review/merge based on labels/state and passes packaged context

## Guidelines

- **Context Packaging**: Always pass issue/PR numbers, labels, plan link/comment URL, acceptance criteria, CI status (if any), and summary notes to the next agent.
- **Label-Driven Flow**: Use shared lifecycle labels from `../_common/labels.md` to steer routing decisions.
- **Single Entry**: Humans talk to this skill; it delegates. Avoid asking users to hop directly into downstream skills unless necessary.
- **DO NOT EXECUTE WORK YOURSELF**: THIS SKILL ONLY TRIAGES/ROUTES. IT MUST CALL DOWNSTREAM AGENTS/SKILLS FOR PLAN/BUILD/REVIEW/MERGE WORK.
- **Common References**: See `../_common/guidelines.md` and `../_common/labels.md`.
- **ALWAYS INVOKE SUBAGENTS**: When routing, invoke `gh-plan-agent` for planning, `gh-build-agent` for implementation/PR updates, and `gh-review-agent` (and its merge workflow) for review/approval/merge. For ops hygiene use `gh-repo-setup-agent`, `gh-issue-creation-agent`, `gh-issue-management-agent`, or `gh-commit-agent`. Never run those skills directly in this manager context.
- **LABEL SAFETY**: NEVER invent ad-hoc labels. Only use labels defined in `../_common/labels.md`. If a required label is missing in the repo, delegate to an ops agent (e.g., `gh-issue-management-agent` or `gh-repo-setup-agent`) to create/apply it. Map human phrases to canonical labels (e.g., “ready for review” → `status-review-in-progress` or `status-implementation-done` for handoff).

## Dependencies

- Access to issues/PRs and labels
- Downstream agents available: `gh-plan-agent`, `gh-build-agent`, `gh-review-agent`
