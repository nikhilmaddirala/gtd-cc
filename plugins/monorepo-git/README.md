# Monorepo Git Plugin

## Overview

- Issue-driven development with worktree isolation
- Tasks stored as GitHub Issues with standard labels
- Two skills strictly separated by context: mg-main and mg-dev
- Subtree publishing for distributing to external repos

**Replaces**: `github`, `pm`, and `obsidian-gtd` plugins (will be deprecated).


## User guide

### Quick start

```bash
/plugin install monorepo-git@gtd-cc
/mg-repo-setup  # One-time: create labels in your repo
```

### Workflow

```
mg-main skill                              mg-dev skill
─────────────                              ────────────

1. Create issue
   /mg-main-task "Add dark mode"
   → GitHub Issue #42

2. Start (plan + create worktree)
   /mg-main-start 42
   → explores codebase
   → posts plan as issue comment
   → creates .worktrees/issue-42/

                                           3. Work (implement)
                                              /mg-dev-work
                                              → reads issue + plan
                                              → implements
                                              → commits along the way

                                           4. Finish (create PR)
                                              /mg-dev-finish
                                              → push branch
                                              → create PR with "Closes #42"
                                              → updates issue to status-review

5. Merge + cleanup
   /mg-main-merge 42
   → merges PR via GitHub
   → removes worktree
   → issue auto-closes

6. Push + Publish
   /mg-push
   /mg-publish
```

### Commands

**Issue workflow (mg-main)**

| Command | Purpose |
|---------|---------|
| `/mg-repo-setup` | One-time: create labels |
| `/mg-main-task` | Create, list, or update issues |
| `/mg-main-list` | List issues with filters |
| `/mg-main-start <N>` | Plan + create worktree |
| `/mg-main-merge <N>` | Merge PR + cleanup |

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
│   ├── mg-repo-setup.md      # NEW: Initialize labels
│   ├── mg-main-task.md
│   ├── mg-main-list.md
│   ├── mg-main-start.md
│   ├── mg-main-merge.md
│   ├── mg-dev-work.md
│   ├── mg-dev-finish.md
│   └── ... (existing git/subtree commands)
├── skills/
│   ├── _common/
│   │   └── labels.md         # NEW: Label schema
│   ├── mg-main/
│   │   ├── SKILL.md
│   │   └── sub-skills/
│   │       ├── task.md       # GitHub Issues CRUD
│   │       ├── start.md      # Plan + worktree
│   │       ├── merge.md      # PR merge + cleanup
│   │       └── ... (existing)
│   └── mg-dev/
│       ├── SKILL.md
│       └── sub-skills/
│           ├── work.md       # Issue-based context
│           ├── finish.md     # PR with "Closes #N"
│           ├── commit.md
│           └── status.md
├── agents/
│   └── mg-publish-agent.md
└── README.md
```

### Label schema

Issues use standard labels for workflow tracking:

**Status labels**
- `status-todo` - New issue, needs planning
- `status-planning` - Plan in progress
- `status-doing` - Implementation in progress
- `status-review` - PR created, under review
- `status-done` - Merged and closed

**Priority labels**
- `priority-p1` - Urgent
- `priority-p2` - High
- `priority-p3` - Medium (default)
- `priority-p4` - Low

**Size labels** (t-shirt sizing)
- `size-xs` - Extra small, < 1 hour
- `size-s` - Small, 1-4 hours
- `size-m` - Medium, 1-2 days
- `size-l` - Large, 3-5 days
- `size-xl` - Extra large, 1+ week

### Skills

**mg-main** (main worktree): Issue management, git operations, subtree publishing

| Sub-skill | Type | Purpose |
|-----------|------|---------|
| `task.md` | atomic | Issue CRUD via `gh issue` |
| `start.md` | orchestrating | Plan + create worktree |
| `merge.md` | orchestrating | Merge PR + cleanup |
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
| `status.md` | atomic | Branch diff + issue info |

### Contributing

- **Issue workflow**: Improve task.md, start.md, merge.md
- **Dev workflow**: Improve work.md, finish.md
- **Labels**: Update _common/labels.md


## Roadmap

- [x] Phase 1: mg-main skill (task.md, start.md, merge.md)
- [x] Phase 2: mg-dev skill (work.md, finish.md, commit.md, status.md)
- [x] Phase 3: Migrate to GitHub Issues
- [ ] Phase 4: Context-aware routing (auto-detect worktree)


## References

- [Git worktrees](https://git-scm.com/docs/git-worktree)
- [Git subtree](https://git-scm.com/book/en/v2/Git-Tools-Advanced-Merging#_subtree_merge)
- [Conventional commits](https://www.conventionalcommits.org/)
- [GitHub CLI](https://cli.github.com/manual/)


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

worktree:
  directory: ".worktrees"
  branch_prefix: "issue/"
```

### Requirements

- Git with subtree and worktree support
- GitHub CLI (`gh`) authenticated with repo access
