# Monorepo Git Plugin

## Overview

- Task-driven development with worktree isolation
- Two skills strictly separated by context: mg-main and mg-dev
- Subtree publishing for distributing to external repos

**Replaces**: `github`, `pm`, and `obsidian-gtd` plugins (will be deprecated).


## User guide

### Quick start

```bash
/plugin install monorepo-git@gtd-cc
```

### Workflow

```
mg-main skill                              mg-dev skill
─────────────                              ────────────

1. Create task
   /mg-main-task "Add dark mode"
   → 30-para/tasks/task-042.md

2. Start (plan + create worktree)
   /mg-main-start 042
   → explores codebase
   → creates plan
   → creates .worktrees/task-042/

                                           3. Work (implement)
                                              /mg-dev-work
                                              → reads task + plan
                                              → implements
                                              → commits along the way

                                           4. Finish (create PR)
                                              /mg-dev-finish
                                              → push branch
                                              → create pull request

5. Merge + cleanup
   /mg-main-merge 042
   → merges branch to main
   → removes worktree
   → marks task done

6. Push + Publish
   /mg-push
   /mg-publish
```

### Commands

**Task workflow (mg-main)**

| Command | Purpose |
|---------|---------|
| `/mg-main-task` | Create, list, or update tasks |
| `/mg-main-list` | List tasks with filters |
| `/mg-main-start <id>` | Plan + create worktree |
| `/mg-main-merge <id>` | Merge branch + cleanup |

**Development (mg-dev)**

| Command | Purpose |
|---------|---------|
| `/mg-dev-work` | Implement the plan |
| `/mg-dev-finish` | Push + create PR |

**Git operations**

| Command | Purpose |
|---------|---------|
| `/mg-commit` | Create conventional commits |
| `/mg-push` | Push to remote |
| `/mg-status` | Show status |

**Subtree publishing**

| Command | Purpose |
|---------|---------|
| `/mg-subtree-status` | Check divergence |
| `/mg-publish` | Publish to subtrees |
| `/mg-subtree` | Subtree CRUD |
| `/mg-graduate` | Lab → production |


## Developer guide

### Directory map

```
monorepo-git/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── mg-main-task.md
│   ├── mg-main-list.md
│   ├── mg-main-start.md
│   ├── mg-main-merge.md
│   ├── mg-dev-work.md
│   ├── mg-dev-finish.md
│   └── ... (existing git/subtree commands)
├── skills/
│   ├── mg-main/               # mg-main skill
│   │   ├── SKILL.md
│   │   └── sub-skills/
│   │       ├── task.md
│   │       ├── start.md
│   │       ├── merge.md
│   │       └── ... (existing)
│   └── mg-dev/                # mg-dev skill
│       ├── SKILL.md
│       └── sub-skills/
│           ├── work.md
│           ├── finish.md
│           ├── commit.md
│           └── status.md
├── agents/
│   └── mg-publish-agent.md
└── README.md
```

### Skills

**mg-main** (main worktree): Task management, git operations, subtree publishing

| Sub-skill | Type | Purpose |
|-----------|------|---------|
| `task.md` | atomic | Task CRUD + list |
| `start.md` | orchestrating | Plan + create worktree |
| `merge.md` | orchestrating | Merge branch + cleanup |
| `status.md` | atomic | Repo overview |
| `commit.md` | atomic | Commit with warning |
| `push.md` | atomic | Push to remote |
| `publish.md` | orchestrating | Subtree publishing |
| `subtree-*.md` | atomic | Subtree operations |
| `graduate.md` | orchestrating | Lab → production |

**mg-dev** (feature worktree): Implementation and finishing

| Sub-skill | Type | Purpose |
|-----------|------|---------|
| `work.md` | orchestrating | Implement the plan |
| `finish.md` | orchestrating | Push + create PR |
| `commit.md` | atomic | Normal commits |
| `status.md` | atomic | Branch diff + task info |

### Contributing

- **Task workflow**: Improve task.md, start.md, merge.md
- **Dev workflow**: Improve work.md, finish.md
- **Templates**: Add task file templates


## Roadmap

- [x] Phase 1: mg-main skill (task.md, start.md, merge.md)
- [x] Phase 2: mg-dev skill (work.md, finish.md, commit.md, status.md)
- [ ] Phase 3: Deprecate github, pm, obsidian-gtd plugins
- [ ] Phase 4: Context-aware routing (auto-detect worktree)


## References

- [Git worktrees](https://git-scm.com/docs/git-worktree)
- [Git subtree](https://git-scm.com/book/en/v2/Git-Tools-Advanced-Merging#_subtree_merge)
- [Conventional commits](https://www.conventionalcommits.org/)


## Appendix

### Configuration

Create `.monorepo-git.yaml` in repo root:

```yaml
subtree_remote_prefix: "remote-"
default_branch: "main"

directories:
  lab: "40-code/43-lab"
  public: "40-code/41-public"
  private: "40-code/42-private"
  tasks: "30-para/tasks"

worktree:
  directory: ".worktrees"
  branch_prefix: "task/"
```

### Requirements

- Git with subtree and worktree support
- GitHub CLI (`gh`) for PR creation and graduate workflow
