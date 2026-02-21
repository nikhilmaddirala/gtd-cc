# gh-tasks

## Overview

- Issue-driven development with worktree isolation
- 5-stage linear pipeline with human gates between stages
- Automatic sync via git-sync (main branch + worktrees)

## User guide

### Quick start

This skill is installed in the monorepo at `.claude/skills/gh-tasks/`.

Create labels in your repo (one-time setup): the Label schema section below contains `gh label create` commands for all status labels.

### Pipeline

```
new → plan → work → review → merge
```

Each sub-skill updates the issue status and suggests the next step.

Use `tasks-status` to diagnose workflow health and find broken tracking loops.

### Sub-skills

| Sub-skill | Purpose | Status change |
|-----------|---------|---------------|
| new | Create issue | → `status-plan` |
| plan | Plan + append to issue | `status-plan` → `status-implement` |
| work | Create worktree + draft PR | `status-implement` → `status-review` |
| review | Review PR | stays `status-review` |
| merge | Merge + cleanup | `status-review` → (closed) |
| tasks-status | Diagnose tracking loops | (no change) |
| orchestrate | Automated end-to-end | `status-plan` → `status-review` |

### Workflow example

```
1. gh-tasks "new" → "Add dark mode support"
   → creates issue #42 with status-plan

2. gh-tasks "plan 42"
   → explores codebase, appends plan to issue body
   → changes label to status-implement

3. gh-tasks "work 42"
   → creates .worktrees/issue-42-add-dark-mode/
   → creates draft PR linked to issue
   → changes label to status-review

4. gh-tasks "review 42"
   → reviews PR changes
   → posts findings (merge blockers vs nice-to-haves)

5. gh-tasks "merge 42"
   → merges PR (squash), cleans up worktree
   → issue auto-closes via "Closes #42" in PR
```

### Label schema

**Status** (required):
- `status-plan` - Needs planning
- `status-implement` - Has plan, ready for implementation
- `status-review` - Has draft PR, needs review
- `status-blocked` - Waiting on external dependency

**Priority** (optional):
- `priority-p1` (urgent) through `priority-p4` (low)

**Size** (optional):
- `size-xs`, `size-s`, `size-m`, `size-l`, `size-xl`

One-time setup commands:

```bash
# Status labels
gh label create "status-plan" --color "fbca04" --description "Needs planning"
gh label create "status-implement" --color "0e8a16" --description "Has plan, ready for implementation"
gh label create "status-review" --color "1d76db" --description "Has draft PR, needs review"
gh label create "status-blocked" --color "b60205" --description "Waiting on external dependency"

# Priority labels (optional)
gh label create "priority-p1" --color "b60205" --description "Urgent"
gh label create "priority-p2" --color "d93f0b" --description "High"
gh label create "priority-p3" --color "fbca04" --description "Medium"
gh label create "priority-p4" --color "0e8a16" --description "Low"

# Size labels (optional)
gh label create "size-xs" --color "c5def5" --description "Extra small (< 1 hour)"
gh label create "size-s" --color "c5def5" --description "Small (1-4 hours)"
gh label create "size-m" --color "c5def5" --description "Medium (1-2 days)"
gh label create "size-l" --color "c5def5" --description "Large (3-5 days)"
gh label create "size-xl" --color "c5def5" --description "Extra large (> 1 week)"
```

## Developer guide

### Directory map

```
.claude/skills/gh-tasks/
├── SKILL.md                    # Main skill coordinator
├── README.md                   # This file
├── scripts/
│   ├── work.sh                 # Create worktree + draft PR
│   ├── merge.sh                # Merge PR + cleanup
│   ├── rebase.sh               # Squash-rebase onto main
│   └── tasks-status.sh         # Workflow diagnostic
├── sub-skills/
│   ├── new.md                  # Create issue
│   ├── plan.md                 # Research + plan
│   ├── work.md                 # Implement
│   ├── review.md               # Review PR
│   ├── merge.md                # Merge + cleanup
│   ├── rebase.md               # Squash-rebase onto main
│   ├── tasks-status.md         # Diagnose tracking loops
│   └── orchestrate.md          # Automated pipeline
└── templates/
    ├── issue.md                # Issue body format
    ├── plan.md                 # Plan format
    └── review.md               # Review comment format
```

### Architecture

- Scripts for deterministic pipelines (work, merge, tasks-status)
- Templates consumed by sub-skills for consistent output formatting
- Script-first sub-skills delegate mechanics to scripts, then add AI interpretation
- Skill-first sub-skills (new, plan, review) use inline CLI directly

### Key invariant

Airtight tracking: `issue ↔ worktree ↔ branch ↔ draft PR`

The `tasks-status` sub-skill validates this invariant and offers guided resolution when something is out of sync.

### Documentation conventions

The skill uses two separate threads for different purposes:

| Location | Purpose | Content |
|----------|---------|---------|
| Issue body | Single source of truth for intent | Goal, context, acceptance criteria, implementation plan |
| Issue comments | Work journal | Progress updates, blockers, decisions, scope changes |
| PR body | Link mechanism | `Closes #N` only |
| PR comments | Code conversation | Review findings, author responses, follow-up reviews |

Key principles:
- Issue body stays accurate: if the plan changes during implementation, edit the body to reflect current reality
- Issue comments capture the narrative: post an update each time you push to the draft PR
- PR comments stay focused on code quality, not scope/requirements
- If a review finding requires a scope change, post that decision to an issue comment, not the PR thread

### Sync mechanism

- Main branch: home-manager `services.git-sync` (every 2 min)
- Worktrees: custom systemd timer with `git-sync` (every 2 min)
- Config: `dragonix/modules/home/cloud-storage/git-sync.nix`

Squash merge strategy means auto-commits in feature branches are acceptable.

### Sync safety guardrails

- Use path-scoped sync by default for follow-up updates (only sync paths explicitly requested by the user)
- Maintain a persistent remote-owned path list per subtree so pull/push direction is deterministic across runs
- Require a preflight manifest before push that groups paths as push, pull, and ignored
- Block suspicious recursive path patterns and warn on absolute symlinks before commit/push
- Use `gh ... --body-file` or single-quoted heredocs for comments to avoid shell interpolation issues

## Roadmap

- [x] Empty commit for PR creation (`work.sh`)
- [x] Worktree sync via systemd timer
- [x] Task tool for orchestration
- [x] Hybrid scripts approach
- [x] Status diagnostic with anomaly detection
- [ ] Auto-update labels during pipeline transitions
- [ ] Quick-capture new issues without detailed scoping (defer to planning stage)
- [ ] Cross-machine worktree sync via manifest file — `work.sh` writes/removes branch names to `.worktrees-manifest` on main, git-sync propagates it, worktree sync script reads it and auto-creates/prunes worktrees (avoids brittle `gh` API calls at sync time)
- [ ] Add subtree sync policy file for remote-owned path exclusions and default direction rules
- [ ] Add path allowlist mode for "small follow-up" PR updates
- [ ] Add pre-push safety checks for recursive path explosions and absolute symlink targets
- [ ] Add dry-run sync manifest output (push/pull/ignored) and require confirmation before push
