# GitHub Plugin

## Overview

- Issue-driven development with worktree isolation
- 5-stage linear pipeline with human gates between stages
- Tasks stored as GitHub Issues with standard labels

## User guide

### Quick start

```bash
/plugin install github@gtd-cc
```

Create labels in your repo (one-time setup): the SKILL.md appendix contains `gh label create` commands for all status, priority, and size labels.

### Pipeline

```
/gh-new → /gh-plan → /gh-work → /gh-review → /gh-merge
```

Each command updates the issue status and suggests the next step.

### Commands

| Command | Purpose | Status change |
|---------|---------|---------------|
| `/gh-new` | Create issue | → `status-plan` |
| `/gh-plan` | Plan + create worktree | `status-plan` → `status-implement` |
| `/gh-work` | Implement + draft PR | `status-implement` → `status-review` |
| `/gh-review` | Review PR | stays `status-review` |
| `/gh-merge` | Merge + cleanup | `status-review` → `status-done` |

### Workflow example

```
1. /gh-new "Add dark mode support"
   → creates issue #42 with status-plan

2. /gh-plan 42
   → explores codebase, posts plan as issue comment
   → creates .worktrees/issue-42/
   → "Review the plan, then run /gh-work 42"

3. /gh-work 42
   → rebases on main, implements plan
   → commits, pushes, creates draft PR
   → "Run /gh-review 42"

4. /gh-review 42
   → reviews PR changes
   → posts findings (merge blockers vs nice-to-haves)
   → "If approved, run /gh-merge 42"

5. /gh-merge 42
   → merges PR, cleans up worktree
   → issue auto-closes
```

### Label schema

**Status**: `status-plan`, `status-implement`, `status-review`, `status-merge`, `status-done`

**Priority**: `priority-p1` (urgent) through `priority-p4` (low)

**Size**: `size-xs` through `size-xl` (t-shirt sizing)

## Developer guide

### Directory map

```
github/
├── .claude-plugin/plugin.json
├── commands/
│   ├── gh-new.md
│   ├── gh-plan.md
│   ├── gh-work.md
│   ├── gh-review.md
│   └── gh-merge.md
├── skills/
│   └── github/
│       ├── SKILL.md
│       ├── sub-skills/
│       │   ├── new.md
│       │   ├── plan.md
│       │   ├── work.md
│       │   ├── review.md
│       │   └── merge.md
│       └── templates/
│           ├── issue.md
│           ├── plan.md
│           ├── implementation.md
│           └── review.md
└── README.md
```

### Architecture

- 1 skill (`github`) with 5 sub-skills mapping to pipeline stages
- 5 thin wrapper commands that invoke the skill
- Templates consumed by sub-skills for consistent output formatting
- All domain logic lives in sub-skills; commands are routing only

### Contributing

- Pipeline logic: edit sub-skills in `skills/github/sub-skills/`
- Output formats: edit stage templates in `skills/github/templates/`
- Label schema: defined in `SKILL.md` appendix
