# Monorepo Git Plugin

Git operations for monorepos with subtree management. Integrates task management with worktree-based development for clean, focused work.

## Philosophy

The monorepo is the source of truth. This plugin unifies three concerns:

- **What** you're working on → Tasks (PARA-based task management)
- **Where** you're working → Worktrees (isolated workspaces per task)
- **How** changes flow → Subtrees (curated publishing to external repos)

Key principles:
- Main worktree stays clean (no WIP, no mixed changes)
- Each task gets its own worktree (isolation by default)
- Subtree publishing is deliberate (batch when ready)

## Worktree context model

Operations are context-aware based on which worktree you're in:

### Main worktree operations

These run from the main worktree and manage the overall repo:

| Sub-skill | Command | Purpose |
|-----------|---------|---------|
| `status.md` | `/mg-status` | Overall repo status |
| `push.md` | `/mg-push` | Push monorepo to remote |
| `subtree-status.md` | `/mg-subtree-status` | Check all subtree divergence |
| `publish.md` | `/mg-publish` | Publish to selected subtrees |
| `subtree-manage.md` | `/mg-subtree` | Subtree CRUD operations |
| `graduate.md` | `/mg-graduate` | Move project lab → production |
| `worktree-start.md` | `/mg-wt-start` | Create worktree for task [planned] |
| `worktree-manage.md` | `/mg-wt-list` | List all active worktrees [planned] |
| `worktree-manage.md` | `/mg-wt-clean` | Remove stale worktrees [planned] |
| `task-manage.md` | `/mg-task` | Task CRUD operations [planned] |
| `task-manage.md` | `/mg-task-list` | List tasks by status/project [planned] |

### Feature worktree operations

These run from within a feature worktree and operate on that branch:

| Sub-skill | Command | Purpose |
|-----------|---------|---------|
| `commit.md` | `/mg-commit` | Commit changes in current worktree |
| `worktree-finish.md` | `/mg-wt-finish` | Complete work, merge, cleanup [planned] |
| `task-update.md` | `/mg-task-done` | Mark current task as done [planned] |

### Context-aware operations

These adapt behavior based on current worktree:

| Sub-skill | Behavior |
|-----------|----------|
| `status.md` | Main: repo overview / Feature: branch status + diff summary |
| `commit.md` | Main: warns about direct commits / Feature: normal commit flow |

## Task management integration [planned]

Tasks are stored as markdown files with YAML frontmatter (PARA method), enabling:

- Obsidian GUI management via TaskNotes plugin
- Terminal/Claude management via this plugin
- Git-tracked task history

### Task-worktree lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                    TASK-DRIVEN DEVELOPMENT                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Task exists (status: todo)                                   │
│     └── 30-para/tasks/task-042-add-dark-mode.md                  │
│                                                                  │
│  2. Start work: /mg-wt-start task-042                            │
│     ├── Creates worktree: .worktrees/task-042/                   │
│     ├── Creates branch: task/042-add-dark-mode                   │
│     └── Updates task status: todo → doing                        │
│                                                                  │
│  3. Work in worktree (isolated from main)                        │
│     └── All changes scoped to this task                          │
│                                                                  │
│  4. Finish: /mg-wt-finish                                        │
│     ├── Reviews all changes                                      │
│     ├── Creates clean commit(s)                                  │
│     ├── Merges to main (or creates PR)                           │
│     ├── Removes worktree + branch                                │
│     └── Updates task status: doing → done                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Task file format

```yaml
---
global-type: task
task-status: doing              # todo | doing | done
task-priority: p2               # p1 | p2 | p3 | p4
para-projects:
  - "[[project-name]]"
code-path: 40-code/43-lab/project
git-branch: task/042-add-dark-mode      # [planned] auto-populated
git-worktree: .worktrees/task-042       # [planned] auto-populated
---

# Add dark mode support

## Goal
...
```

## Commands

### Task management [planned]

| Command | Purpose | Context |
|---------|---------|---------|
| `/mg-task` | Create, read, update tasks | main |
| `/mg-task-list` | List tasks by status/project/priority | main |
| `/mg-task-done` | Mark current task complete | feature |

### Worktree workflow [planned]

| Command | Purpose | Context |
|---------|---------|---------|
| `/mg-wt-start` | Create worktree for task | main |
| `/mg-wt-list` | List active worktrees | main |
| `/mg-wt-switch` | Switch to different worktree | any |
| `/mg-wt-finish` | Complete work, merge, cleanup | feature |
| `/mg-wt-clean` | Remove stale worktrees | main |

### Daily development

| Command | Purpose | Context |
|---------|---------|---------|
| `/mg-commit` | Create logical commits | feature (preferred) or main |
| `/mg-push` | Push to monorepo remote | main |
| `/mg-status` | Working tree status | any |

### Subtree publishing

| Command | Purpose | Context |
|---------|---------|---------|
| `/mg-subtree-status` | Show divergence for all subtrees | main |
| `/mg-publish` | Interactive subtree selection | main |
| `/mg-subtree` | CRUD operations | main |

### Project lifecycle

| Command | Purpose | Context |
|---------|---------|---------|
| `/mg-graduate` | Move project lab → production with subtree | main |

## Workflows

### Task-driven workflow (recommended) [planned]

For any non-trivial work, use task + worktree isolation:

```bash
# 1. Create or find task
/mg-task create "Add dark mode support" --project gtd-cc --priority p2

# 2. Start isolated work
/mg-wt-start task-042       # Creates worktree, marks task as "doing"

# 3. Work freely in isolated worktree
# ... make changes, no need to worry about mixing with other work ...

# 4. Complete and merge
/mg-wt-finish               # Reviews, commits, merges, marks "done"

# 5. Push and publish
/mg-push                    # Push monorepo
/mg-publish                 # Publish to subtrees if applicable
```

### Quick fix workflow

For trivial fixes, work directly on main (traditional flow):

```bash
/mg-status    # Check current state
/mg-commit    # Create logical commits
/mg-push      # Push to monorepo
```

### Publishing workflow

When ready to share changes with subtree repos:

```bash
/mg-subtree-status    # See what's pending
/mg-publish           # Pick which subtrees to publish
```

## Configuration

Create `.monorepo-git.yaml` in your repo root (optional):

```yaml
# Subtree detection
subtree_remote_prefix: "remote-"
default_branch: "main"

# Directory structure
directories:
  lab: "40-code/43-lab"
  public: "40-code/41-public"
  private: "40-code/42-private"
  tasks: "30-para/tasks"            # [planned] PARA tasks directory
  projects: "30-para/31-projects"   # [planned] PARA projects directory

# Worktree settings [planned]
worktree:
  directory: ".worktrees"
  branch_prefix: "task/"
  cleanup_after_merge: true
  warn_on_main_commit: true         # Warn when committing directly to main

# Task settings [planned]
task:
  auto_create_worktree: true        # Auto-create worktree when starting task
  auto_update_status: true          # Auto-update task status on worktree events
  link_git_metadata: true           # Add git-branch/git-worktree to task frontmatter
```

## Subtree conventions

Subtree remotes follow the `remote-*` naming pattern:

```bash
git remote add remote-project-name https://github.com/user/project-name.git
```

The plugin auto-detects these remotes and maps them to directories.

## Requirements

- Git with subtree and worktree support (standard in modern Git)
- GitHub CLI (`gh`) for graduate workflow and issue integration
- PARA task structure in `30-para/tasks/` for task management [planned]

## Roadmap

### Phase 1: Core worktree workflow (next)

Focus: Basic worktree isolation without task integration

- `/mg-wt-start` - Create worktree + branch
  - Accept task ID, GitHub issue number, or description
  - Auto-generate branch name
  - Create worktree in `.worktrees/`
- `/mg-wt-finish` - Complete work and merge
  - Review changes, create commits
  - Merge to main (or PR)
  - Clean up worktree + branch
- `/mg-wt-list` - Show active worktrees
- Context detection in `commit.md` and `status.md`

### Phase 2: Task management integration

Focus: Connect PARA tasks with worktrees

- `/mg-task` - Task CRUD operations
- `/mg-task-list` - Query tasks
- `/mg-task-done` - Mark task complete
- Auto-update task status on worktree lifecycle events
- Add `git-branch` and `git-worktree` fields to task frontmatter

### Phase 3: Worktree management

- `/mg-wt-switch` - Change active worktree
- `/mg-wt-clean` - Remove stale worktrees
- Session start hook: remind about open worktrees
- Stale worktree detection

### Phase 4: Advanced integration

- PR creation flow from `/mg-wt-finish --pr`
- GitHub issue ↔ task ↔ worktree linking
- Time tracking per task/worktree
- Multi-project task handling

## Plugin structure

```
monorepo-git/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── commands/
│   ├── mg-commit.md
│   ├── mg-push.md
│   ├── mg-status.md
│   ├── mg-publish.md
│   ├── mg-subtree-status.md
│   ├── mg-subtree.md
│   ├── mg-graduate.md
│   ├── mg-wt-start.md           [planned - phase 1]
│   ├── mg-wt-list.md            [planned - phase 1]
│   ├── mg-wt-finish.md          [planned - phase 1]
│   ├── mg-wt-switch.md          [planned - phase 3]
│   ├── mg-wt-clean.md           [planned - phase 3]
│   ├── mg-task.md               [planned - phase 2]
│   ├── mg-task-list.md          [planned - phase 2]
│   └── mg-task-done.md          [planned - phase 2]
├── agents/
│   └── mg-publish-agent.md
└── skills/
    └── monorepo-git/
        ├── SKILL.md
        ├── resources/
        │   ├── templates/
        │   └── task-schema.md   [planned - phase 2]
        └── sub-skills/
            │
            │  # Main worktree sub-skills
            ├── status.md
            ├── push.md
            ├── subtree-status.md
            ├── publish.md
            ├── subtree-manage.md
            ├── graduate.md
            ├── worktree-start.md    [planned - phase 1]
            ├── worktree-manage.md   [planned - phase 1]
            ├── task-manage.md       [planned - phase 2]
            │
            │  # Feature worktree sub-skills
            ├── commit.md
            ├── worktree-finish.md   [planned - phase 1]
            └── task-update.md       [planned - phase 2]
```
