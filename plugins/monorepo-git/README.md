# Monorepo Git Plugin

Git operations for monorepos with subtree management. Separates daily development (high velocity commit/push) from curated subtree publishing.

## Philosophy

The monorepo is the source of truth. Changes flow outward:
- Daily work: commit and push to monorepo frequently
- Publishing: push to subtrees deliberately, with curated batches of work

## Commands

### Daily development (high velocity)

| Command | Purpose |
|---------|---------|
| `/mg-commit` | Analyze changes and create logical commits |
| `/mg-push` | Push to monorepo remote only |
| `/mg-status` | Quick working tree status |

### Subtree publishing (curated)

| Command | Purpose |
|---------|---------|
| `/mg-subtree-status` | Show divergence for all subtrees |
| `/mg-publish` | Interactive selection of subtrees to publish |
| `/mg-subtree` | CRUD operations (add, list, pull, move, remove) |

### Project lifecycle

| Command | Purpose |
|---------|---------|
| `/mg-graduate` | Move project from lab to production with subtree setup |

## Workflow

### Daily workflow

```
/mg-commit    # Create logical commits
/mg-push      # Push to monorepo (fast, no subtree overhead)
```

### Publishing workflow (when ready to share)

```
/mg-subtree-status    # See what's pending for each subtree
/mg-publish           # Pick which subtrees to publish
```

## Configuration

Create `.monorepo-git.yaml` in your repo root (optional):

```yaml
# Subtree detection
subtree_remote_prefix: "remote-"
default_branch: "main"

# Directory structure for graduate workflow
directories:
  lab: "path/to/lab"
  public: "path/to/public"
  private: "path/to/private"
```

Without config, the plugin uses sensible defaults:
- Subtrees detected by `remote-*` pattern
- Branch defaults to `main`
- Graduate prompts for paths

## Subtree conventions

Subtree remotes should follow the `remote-*` naming pattern:

```bash
git remote add remote-project-name https://github.com/user/project-name.git
```

The plugin auto-detects these remotes and maps them to directories based on git history.

## Requirements

- Git with subtree support (standard in modern Git)
- GitHub CLI (`gh`) for graduate workflow
