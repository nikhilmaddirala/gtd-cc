---
name: gh-review
description: GitHub workflow automation skill for code review, human approval guidance, and merge/cleanup.
---

# GitHub Review Skill

## Overview

Use this skill when a PR is ready for review, approval, and merge. It focuses on correctness, alignment to the approved plan and issue, and clean handoff into main with cleanup.

## Workflows

Use the appropriate workflow from the `workflows/` directory:

- **review-pr.md** - Performs code reviews focusing on correctness, requirements alignment, and significant bugs
- **human-approval.md** - Guides humans through local testing and approval decision-making when human sign-off is required
- **merge.md** - Executes final merge operations including squash-merge, issue closure, branch deletion, and worktree cleanup

## Guidelines

- **Single Source of Truth**: This skill and its workflow files contain all procedural knowledge for GitHub review/approval/merge operations.
- **Context First**: Always pull the issue, approved plan link, PR number, labels, and CI status before acting.
- **Handoff Ready**: Expect build agents to provide a summary comment; if missing, gather context before review.
- **Common References**: See `../_common/guidelines.md`, `../_common/labels.md`, and templates under `../_common/templates/`.

## Dependencies

- **Repository Access**: Requires PR read/comment/review permissions
- **CI Signals**: Uses CI status to inform review/merge readiness
- **Issue Context**: Relies on issue link and approved plan (if available) for correctness checks
