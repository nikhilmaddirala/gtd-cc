---
name: github
description: Issue-driven development with worktree isolation. 5-stage pipeline (new, plan, work, review, merge) with human gates between stages. Use when creating tasks, planning, implementing, reviewing, or merging.
---

# github

## Overview

Linear pipeline for issue-driven development. Each stage updates the issue status and suggests the next command, requiring human approval to proceed.

```
/gh-new → /gh-plan → /gh-work → /gh-review → /gh-merge
```

## Context

User wants to manage the lifecycle of a development task from issue creation through merge. Tasks are GitHub Issues with standard labels for status tracking.

## Sub-skills

Load the appropriate sub-skill from `sub-skills/` based on user intent.

- **new.md**: Create a GitHub Issue with status and priority labels
  - Triggers: "new task", "create issue", "add task"
  - Status: → `status-plan`

- **plan.md**: Explore codebase, post plan as issue comment, create worktree
  - Triggers: "plan task", "start planning", "plan issue N"
  - Status: `status-plan` → `status-implement`

- **work.md**: Implement plan, commit, push, create draft PR
  - Triggers: "work on task", "implement", "build"
  - Status: `status-implement` → `status-review`

- **review.md**: Review PR for correctness, post findings
  - Triggers: "review PR", "review task", "check PR"
  - Status: `status-review` → `status-merge`

- **merge.md**: Merge PR, cleanup worktree
  - Triggers: "merge", "merge task", "finish"
  - Status: `status-merge` → `status-done`

## Process

- Determine which pipeline stage the user wants
- Load the appropriate sub-skill
- Execute sub-skill process
- Sub-skill updates status and suggests next command

## Guidelines

- Each sub-skill MUST update the issue status label on completion
- Each sub-skill MUST suggest the next pipeline command at the end
- Use conventional commit format: `type(scope): description`
- Worktree directory: `.worktrees/issue-{N}`
- Branch naming: `issue/{N}-{slug}`
- PR body MUST include "Closes #N" for auto-close on merge

## Resources

- **templates/**: Issue, plan, implementation, review (one per pipeline stage)

## Appendix

### Label schema

**Status labels**

| Label | Description | Color |
|-------|-------------|-------|
| `status-plan` | New issue, needs planning | `#d4c5f9` (lavender) |
| `status-implement` | Plan approved, ready for implementation | `#c5def5` (light blue) |
| `status-review` | PR created, needs review | `#f9d0c4` (peach) |
| `status-merge` | Review approved, ready to merge | `#fbca04` (yellow) |
| `status-done` | Merged and closed | `#0e8a16` (green) |

**Priority labels**

| Label | Description | Color |
|-------|-------------|-------|
| `priority-p1` | Urgent, do first | `#d73a4a` (red) |
| `priority-p2` | High priority | `#ff7b00` (orange) |
| `priority-p3` | Medium priority | `#fbca04` (yellow) |
| `priority-p4` | Low priority, backlog | `#c2e0c6` (light green) |

**Size labels**

| Label | Description | Color |
|-------|-------------|-------|
| `size-xs` | Extra small, < 1 hour | `#bfd4f2` (light blue) |
| `size-s` | Small, 1-4 hours | `#c2e0c6` (light green) |
| `size-m` | Medium, 1-2 days | `#fbca04` (yellow) |
| `size-l` | Large, 3-5 days | `#f9d0c4` (peach) |
| `size-xl` | Extra large, 1+ week | `#d73a4a` (red) |

### Create all labels

```bash
gh label create "status-plan" --description "New issue, needs planning" --color "d4c5f9"
gh label create "status-implement" --description "Plan approved, ready for implementation" --color "c5def5"
gh label create "status-review" --description "PR created, needs review" --color "f9d0c4"
gh label create "status-merge" --description "Review approved, ready to merge" --color "fbca04"
gh label create "status-done" --description "Merged and closed" --color "0e8a16"
gh label create "priority-p1" --description "Urgent, do first" --color "d73a4a"
gh label create "priority-p2" --description "High priority" --color "ff7b00"
gh label create "priority-p3" --description "Medium priority" --color "fbca04"
gh label create "priority-p4" --description "Low priority, backlog" --color "c2e0c6"
gh label create "size-xs" --description "Extra small, < 1 hour" --color "bfd4f2"
gh label create "size-s" --description "Small, 1-4 hours" --color "c2e0c6"
gh label create "size-m" --description "Medium, 1-2 days" --color "fbca04"
gh label create "size-l" --description "Large, 3-5 days" --color "f9d0c4"
gh label create "size-xl" --description "Extra large, 1+ week" --color "d73a4a"
```
