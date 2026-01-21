# pm - Worktree Project Management

## Overview

- Local-first task tracking using markdown files with YAML frontmatter
- Isolated development via git worktrees - one branch/worktree per task
- Designed for AI agent workflows - tasks can be assigned to humans or agents


## User guide

### Quick start

```bash
/plugin install pm@gtd-cc
```

### Configuration

Requires a monorepo structure with:
- Main worktree at `~/repos/monorepo/monorepo-main/`
- Task directory at `30-para/35-tasks/`
- Parent directory `~/repos/monorepo/` for task worktrees

### Usage

```bash
# === In main worktree (monorepo-main/) ===

# Create a new task (inbox)
/pm-task "Add dark mode support"

# List tasks
/pm-list --status inbox
/pm-list --assignee claude

# Start working on a task (creates worktree)
/pm-start 001
# Output: Worktree created at ~/repos/monorepo/monorepo-task-001-add-dark-mode
# Then: cd ~/repos/monorepo/monorepo-task-001-add-dark-mode

# === In feature worktree (monorepo-task-001-*/) ===

# Create implementation plan
/pm-plan

# Execute the plan
/pm-execute

# === Back in main worktree ===

# Merge completed work
/pm-merge 001

# Clean up worktree
/pm-cleanup 001
```


## Developer guide

### Directory map

```
pm/
├── skills/
│   ├── pm-main/
│   │   ├── SKILL.md           # Skill for main worktree operations
│   │   └── sub-skills/        # task-create, task-list, worktree-*
│   └── pm-worktree/
│       ├── SKILL.md           # Skill for feature worktree operations
│       └── sub-skills/        # task-plan, task-execute, task-assign, etc.
├── commands/                  # Thin wrapper commands
└── README.md
```

### Contributing

- **Features:** New commands or sub-skills
- **Bug fixes:** Edge cases in worktree handling
- **Documentation:** README and skill improvements


## Roadmap

- [x] Initial plugin structure
- [ ] Core skill with sub-skills
- [ ] Task CRUD commands (pm-task, pm-list, pm-status)
- [ ] Worktree commands (pm-start, pm-done)
- [ ] Agent for autonomous task execution


## Appendix

### Skills

Two skills, organized by execution context:

**pm-main** (runs in main worktree `monorepo-main/`)
- **task-create.md**: Create new task file (status=inbox, current-assignee=user)
- **task-list.md**: Query tasks with filters for status, priority, current-assignee
- **worktree-start.md**: Create branch and worktree, user switches to it
- **worktree-merge.md**: Merge feature branch to main (direct or PR)
- **worktree-cleanup.md**: Remove worktree and delete branch after merge

**pm-worktree** (runs in feature worktrees `monorepo-task-*/`)
- **task-plan.md**: Create/update implementation plan, assign back to user for review
- **task-execute.md**: Implement plan, assign back to user for review
- **task-assign.md**: Hand off between user↔claude, update current-assignee
- **task-transition.md**: Move between stages (planning→execution, execution→done)
- **task-block.md**: Mark task blocked with reason, or unblock and resume
- **task-commit.md**: Commit current work with conventional commit message

### Task lifecycle

```
[inbox] ──triage──▶ [planning] ◀──loop──▶ [execution] ──approve──▶ [done]
                         │                     │
                         └───▶ [blocked] ◀─────┘
```

| Stage | Status | Assignee cycles | What happens |
|-------|--------|-----------------|--------------|
| Inbox | `inbox` | user | Capture and triage task |
| Planning | `planning` | user ↔ claude | Create plan, review, iterate until approved |
| Execution | `execution` | user ↔ claude | Execute plan, review deliverables, iterate until approved |
| Blocked | `blocked` | user or external | Unblock and return to previous stage |
| Done | `done` | - | Task complete |

**Assignee values:**
- `user`: Human needs to act (review, approve, provide input)
- `claude`: Claude Code needs to act (plan, implement, update)
- `external`: Waiting on something outside this system

### Task file schema

Location: `30-para/35-tasks/TASK-<id>-<slug>.md`

```yaml
---
# Core identification
type: task
task-id: "001"
title: "Clear task title"

# Status and assignment
status: inbox                        # inbox | planning | execution | blocked | done
task-owner: user                     # Who owns this task overall
current-assignee: user               # Whose turn (user | claude | external)

# Worktree tracking
task-branch: task/001-setup-pm
task-worktree: monorepo-task-001-setup-pm

# Metadata
priority: p2                         # p1 (urgent+important) | p2 | p3 | p4
created: 2026-01-20
modified: 2026-01-20
deadline:                            # Optional

# Blocking (only when status=blocked)
blocked-from:                        # planning | execution (stage interrupted)
blocked-reason:                      # Why it's blocked
---
```

**Priority definitions (Eisenhower matrix):**
- `p1`: Urgent + Important (do immediately)
- `p2`: Not urgent + Important (schedule time)
- `p3`: Urgent + Not important (delegate or do quickly)
- `p4`: Neither (defer or drop)

### Naming conventions

| Element | Pattern | Example |
|---------|---------|---------|
| Task ID | 3-digit zero-padded | `001`, `042` |
| Task file | `TASK-<id>-<slug>.md` | `TASK-001-setup-pm.md` |
| Branch | `task/<id>-<slug>` | `task/001-setup-pm` |
| Worktree | `monorepo-task-<id>-<slug>` | `monorepo-task-001-setup-pm` |

### Worktree architecture (proposal)

#### Directory structure

```
~/repos/monorepo/                        # Container directory
├── monorepo.git/                        # Bare repo (optional, or use main as primary)
├── monorepo-main/                       # Main worktree (main branch)
│   └── 30-para/35-tasks/                # Task files (source of truth on main)
├── monorepo-task-001-setup-pm/          # Feature worktree (task/001-setup-pm branch)
│   └── 30-para/35-tasks/                # Task files (branch's copy)
└── monorepo-task-002-add-feature/       # Feature worktree
```

#### Task file lifecycle

Task files travel with branches:

1. **Inbox** (main): Task created with status=inbox, committed to main
2. **Planning** (main→worktree): User triages, assigns to Claude Code. Worktree created when planning begins.
3. **Planning loop** (worktree): Claude Code plans → user reviews → iterate. All updates committed to feature branch.
4. **Execution loop** (worktree): Claude Code executes → user reviews → iterate. Code + task updates committed together.
5. **Done** (worktree→main): Task approved, branch merged, worktree cleaned up. Main gets final task state.

Each worktree has its own view of task files reflecting that branch's state.

#### Sub-skills by execution context

**pm-main** (CWD: `monorepo-main/`)

| Sub-skill | Behavior |
|-----------|----------|
| `task-create` | Creates task file (inbox), commits to main |
| `task-list` | Lists tasks visible in main branch |
| `worktree-start` | Creates feature branch + worktree, outputs path |
| `worktree-merge` | Merges feature branch to main (direct or via PR) |
| `worktree-cleanup` | Removes worktree directory, deletes branch |

**pm-worktree** (CWD: `monorepo-task-*/`)

| Sub-skill | Behavior |
|-----------|----------|
| `task-plan` | Creates/updates plan in task file, assigns to user |
| `task-execute` | Implements plan, creates deliverables, assigns to user |
| `task-assign` | Updates current-assignee, commits |
| `task-transition` | Moves between stages, commits |
| `task-block` | Sets/clears blocked status with reason |
| `task-commit` | Commits work with conventional message |

#### Detection logic

Skills detect context via git commands:

```bash
# Current worktree root
git rev-parse --show-toplevel

# List all worktrees (find main)
git worktree list

# Current branch
git branch --show-current

# Is this main branch?
[[ $(git branch --show-current) == "main" ]]
```

Skills can derive:
- Whether running in main vs feature worktree
- Path to main worktree (for cross-worktree operations)
- Task ID from branch name (`task/001-slug` → `001`)

#### Merge workflow

Merges always happen from main worktree. The flow:

1. Work completes in feature worktree, task status=execution, current-assignee=user
2. User reviews and approves deliverables
3. User switches to main: `cd ~/repos/monorepo/monorepo-main`
4. User runs merge: `/pm-merge 001` (or PR if needed)
5. User runs cleanup: `/pm-cleanup 001`

**Merge strategies:**

| Scenario | Strategy |
|----------|----------|
| Small task, single dev | Direct merge: `git merge task/001-slug` |
| Larger task, needs review | PR via `gh pr create`, merge via GitHub UI |
| Subtree-affected code | Always PR (human review required) |

**After merge (cleanup):**
```bash
# From main worktree
git worktree remove ../monorepo-task-001-slug
git branch -d task/001-slug
# Update task file: status=done
```

#### Design decisions

**1. Bare repo vs main worktree as canonical?**

Suggestion: **Main worktree is sufficient.** Bare repos add complexity without much benefit here. The main worktree serves as source of truth; feature worktrees branch from it.

```
~/repos/monorepo/
├── monorepo-main/              # Primary worktree (not bare)
├── monorepo-task-001-*/        # Feature worktrees
└── monorepo-task-002-*/
```

**2. When should worktree be created?**

Suggestion: **At planning start.** Inbox stage is just capture/triage - no code involved. Once user assigns to Claude Code for planning, create the worktree because:
- Claude Code needs to explore codebase during planning
- Plan commits should be on the feature branch
- Keeps main clean (only has inbox tasks, not in-progress work)

Workflow:
- `task-create` → creates task in main (inbox)
- User triages, runs `worktree-start 001` → creates worktree, transitions to planning
- All subsequent work happens in worktree

**3. How to handle user↔Claude Code handoffs?**

Suggestion: **Auto-commit when Claude Code hands back to user.** This preserves work and creates clear checkpoints. The commit message indicates the handoff:

```bash
# When Claude Code finishes and assigns back to user
git commit -m "planning: draft plan ready for review

current-assignee: user"
```

User can review, then either approve (transition) or request changes (assign back to Claude Code).

**4. Should worktree-done auto-detect merge strategy?**

Suggestion: **Default to PR, allow override for small changes.** Safety first:
- PR by default (human review before merge)
- `--direct` flag for small/confident changes
- Always PR if touching subtree paths (`40-code/41-public/*`)

## Appendix: CCPM Integration Strategy (Proposal)

We plan to pivot the `pm` plugin to wrap the [automazeio/ccpm](https://github.com/automazeio/ccpm) methodology. `ccpm` is a mature "Spec-Driven Development" system for Claude Code that uses GitHub Issues and Worktrees.

The `pm` plugin will **not** rewrite `ccpm`'s core logic. Instead, it will be a wrapper that adapts `ccpm` for our monorepo environment.

### 1. Functional Modifications

Our wrapper modifies `ccpm` behavior in three specific ways:

#### A. The "Fast Track" (Workflow Modification)
**Problem:** `ccpm` enforces `PRD -> Epic -> Issue -> Code`. Overkill for small fixes.
**Wrapper Solution:**
- Introduces `/pm-task "Title" --fast`.
- Directly creates a GitHub Issue and spins up the worktree, bypassing PRD/Epic generation.
- **Benefit:** Same isolation/tracking, zero admin overhead for small tasks.

#### B. Environment Synchronization (Context Injection)
**Problem:**
1.  **Untracked Files:** New worktrees miss local config (`.env`, `settings.local.json`) not in git.
2.  **Stale Knowledge:** A long-running feature branch has an outdated `30-para/` folder. The agent misses notes added to `main` recently.
**Wrapper Solution:**
- **Secrets:** Automatically symlinks `.env` and local config from root to the worktree.
- **Live Knowledge:** Optionally symlinks the "Live" `30-para` folder from the main root, ensuring the agent always references the absolute latest knowledge base, regardless of branch age.

#### C. Automated Cleanup (Lifecycle Modification)
**Problem:** `ccpm` focuses on *starting* work, leaving cleanup (deleting branches/dirs) to the user.
**Wrapper Solution:**
- Introduces `/pm-finish <id>`.
- Verifies PR merge status.
- Destructively cleans up the local environment (removes worktree folder, deletes branch).
- **Benefit:** Keeps the developer's machine clean.

#### D. 3-Way Sync (Data Modification)
**Problem:** `ccpm` uses GitHub Issues as the source of truth, but users often prefer planning in local Markdown (Obsidian).
**Wrapper Solution:**
- Establishes a sync loop: **Obsidian (PRD.md) ↔ Wrapper ↔ GitHub Issues**.
- **Flow:**
    1.  User drafts `PRD.md` in Obsidian.
    2.  `/pm-sync` pushes this to a GitHub Issue (or updates it).
    3.  Agent works and updates the Issue status/comments.
    4.  Wrapper pulls these updates back into `PRD.md` in Obsidian.
- **Benefit:** Best of both worlds—Local-first planning interface with Cloud-native execution tracking.

### 2. Integration Architecture

The plugin acts as a command-line adapter:

| Layer | Component | Responsibility |
| :--- | :--- | :--- |
| **Interface** | `pm` Plugin | CLI commands (`/pm-start`, `/pm-finish`), Monorepo config, Symlinking logic. |
| **Core Engine** | `ccpm` (Vendored) | Planning logic, GitHub API interaction, PRD/Spec generation templates. |
| **Infrastructure** | Git / GitHub | Worktrees, Branches, Issues, PRs. |

### 3. Migration Plan

1.  **Vendor `ccpm`:** Clone/copy the relevant `ccpm` context and commands into `pm/vendor/`.
2.  **Wrap Commands:** Create `pm-*` commands that internally call `ccpm` logic but add our pre/post hooks.
3.  **Deprecate Markdown:** Move away from local task files (current `pm` design) to GitHub Issues (`ccpm` design) as the source of truth.