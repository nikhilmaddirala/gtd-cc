# Monorepo Git Plugin

## Overview

- Git operations for monorepo workflows
- Conventional commits with logical grouping
- Subtree management: CRUD, sync status, curated publishing
- Project graduation: lab to production with GitHub repo setup

## User guide

### Quick start

```bash
/plugin install monorepo-git@gtd-cc
```

### Commands

| Command | Purpose |
|---------|---------|
| `/mg-commit` | Analyze changes, create logical commits, optionally push |
| `/mg-subtree` | Subtree operations: add, list, pull, move, remove, status, publish |
| `/mg-graduate` | Graduate project from lab to production |

### Examples

Commit changes:
```
/mg-commit
→ analyzes changes, groups by subtree/topic
→ presents plan for approval
→ commits and offers to push
```

Subtree operations:
```
/mg-subtree list
/mg-subtree add https://github.com/user/repo path/to/dir
/mg-subtree pull project-name
/mg-subtree status
/mg-subtree publish
```

Graduate project:
```
/mg-graduate my-project
→ creates GitHub repo
→ moves to production directory
→ sets up subtree sync
```

### Configuration

Create `.monorepo-git.yaml` in repo root:

```yaml
subtree_remote_prefix: "remote-"
default_branch: "main"

subtrees:
  remote-project-a:
    prefix: "path/to/project-a"

directories:
  lab: "40-code/43-lab"
  public: "40-code/41-public"
  private: "40-code/42-private"
```

## Developer guide

### Directory map

```
monorepo-git/
├── .claude-plugin/plugin.json
├── commands/
│   ├── mg-commit.md
│   ├── mg-subtree.md
│   └── mg-graduate.md
├── skills/
│   └── monorepo-git/
│       ├── SKILL.md
│       ├── sub-skills/
│       │   ├── commit.md
│       │   ├── subtree.md
│       │   └── graduate.md
│       └── resources/
│           └── templates/
│               └── config.example.yaml
└── README.md
```

### Architecture

- 1 skill (`monorepo-git`) with 3 sub-skills
- 3 thin wrapper commands that invoke the skill
- All domain logic lives in sub-skills; commands are routing only

### Requirements

- Git with subtree and worktree support
- GitHub CLI (`gh`) authenticated with repo access
