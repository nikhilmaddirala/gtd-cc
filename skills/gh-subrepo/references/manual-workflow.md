# Git Subrepo Workflow

This document describes the complete workflow for working with git-subrepo in your monorepo.

## Core Concepts

Git-subrepo creates a bidirectional sync between a monorepo subdirectory and a standalone GitHub repository. Unlike git-submodule, the content lives directly in your working tree as normal files.

Key files:
- `.gitrepo` — Metadata file tracking the upstream commit, remote, and branch
- Content in the subdirectory — Normal files that you edit directly

## The Workflow

### Phase 1: Making Local Changes

Edit files directly in the subrepo directory:

```bash
# Edit files in 40-code/415-subrepos/petaluma-ai-github-io/
# Use any editor — these are normal files
```

Commit to your monorepo:

```bash
git add 40-code/415-subrepos/petaluma-ai-github-io/
git commit -m "describe your changes"
```

**Important:** This commits to your monorepo's main branch. The `.gitrepo` file is NOT updated yet — your changes are local only.

### Phase 2: Checking Status

To see if there are changes on the remote (collaborator commits):

```bash
git subrepo status --fetch 40-code/415-subrepos/petaluma-ai-github-io
```

**Understanding the output:**
- If `Upstream Ref` and `Pulled Commit` match = You're up to date
- If they differ = Collaborator has made changes you haven't pulled yet
- The `Fetch Ref` shows the latest commit on the remote

**Example output when remote has changes:**
```
Git subrepo '40-code/415-subrepos/petaluma-ai-github-io':
  Remote URL:      https://github.com/petaluma-ai/petaluma-ai.github.io.git
  Upstream Ref:    615d113ee           # Latest remote
  Tracking Branch: main
  Pulled Commit:   ed63efff1           # What you have
  Pull Parent:     8f78acc39
  Refs:
    Fetch Ref:     615d113ee (refs/subrepo/.../fetch)
```

### Phase 3: Pulling Remote Changes

When collaborators have made changes:

```bash
git subrepo pull 40-code/415-subrepos/petaluma-ai-github-io
```

**What happens:**
1. Fetches latest from remote
2. Creates a branch of your local subrepo commits
3. Merges remote changes with your local changes
4. Squashes the result into a single commit on your main branch
5. Updates the `.gitrepo` file

**If there are conflicts:**

```bash
# Resolve conflicts normally
git status                      # See conflicts
edit conflicted files           # Fix them
git add resolved files          # Stage them
git subrepo commit 40-code/415-subrepos/petaluma-ai-github-io   # Complete the pull
```

### Phase 4: Pushing Your Changes Upstream

When you want to publish your local changes to the standalone repository:

```bash
git subrepo push 40-code/415-subrepos/petaluma-ai-github-io
```

**What happens:**
1. Takes the properly merged branch from a successful pull
2. Pushes individual commits (not squashed) to the remote repository
3. Updates `.gitrepo` if you use `--update` flag

**Important:** Before pushing, you MUST have pulled first if there are remote changes.

## Command Reference

| Action | Command |
|--------|---------|
| Make changes | Edit files, `git commit` normally |
| Clean artifacts | `git subrepo clean <dir> --force` |
| Check status | `git subrepo status <dir>` |
| Fetch remote | `git subrepo fetch <dir>` |
| Pull changes | `git subrepo pull <dir>` |
| Push changes | `git subrepo push <dir>` |
| Clean all artifacts | `git subrepo clean --all --force` |

## Common Issues

### "Can't pull subrepo. Unstaged changes" error

Git-subrepo requires a clean working tree to run `pull`, even if your changes are unrelated to the subrepo. This is because Git's worktree mechanism (used internally by subrepo) requires it.

**Solution:** Stash your changes temporarily:

```bash
git stash push -m "Temporary stash for subrepo pull"
git subrepo pull 40-code/415-subrepos/petaluma-ai-github-io
git stash pop
```

### Mixed commits (subrepo + other files in same commit)

If a commit in your monorepo touches both the subrepo directory AND other files, git-subrepo will extract the entire commit when you run `pull` or `push`. The non-subrepo changes get included in the extracted branch.

**This is a problem because:**
- When pushing, those unrelated changes would be pushed to the standalone repository
- The standalone repo would contain files/changes that don't belong there

**Solutions:**

1. **Best practice:** Keep subrepo changes in separate commits from other changes.

2. **If you already have mixed commits:** Use interactive rebase to split them:

```bash
# Start an interactive rebase for the affected commits
git rebase -i HEAD~N

# Mark the mixed commit as 'edit' instead of 'pick'
# When rebase stops, reset only the subrepo files:
git reset HEAD^
git add 40-code/415-subrepos/petaluma-ai-github-io/
git commit -m "subrepo changes only"

# Then commit the remaining files:
git add .
git commit -m "other changes"

# Continue the rebase
git rebase --continue
```

3. **To check if you have mixed commits:**

```bash
git log --oneline --stat <subrepo-dir> | grep -A5 "commit"
```

### "worktree already exists" error

This happens when a previous subrepo command left a temporary worktree.

**Solution:** Run `git subrepo clean <dir> --force` before the command that failed.

### Quick status check

The basic `git subrepo status` (without flags) only shows metadata from `.gitrepo` and doesn't fetch latest from remote.

**Solution:** Use `git subrepo status --fetch <dir>` to see current state including remote changes.

### Need to undo a pull

If a pull goes wrong or you want to retry:

```bash
# Reset the merge commit
git reset --hard HEAD~1

# Clean up artifacts
git subrepo clean <dir> --force
```

## Clean Push with Mixed Commits (Worktree Pattern)

When you have mixed commits that touch both the subrepo and other files, use a separate worktree to prepare clean changes for the standalone repo. This keeps your main working directory untouched.

### When to use this

- Your monorepo commits mix subrepo changes with other files
- You want clean commit messages in the standalone repository
- You want to squash multiple subrepo changes into a focused commit

### Step-by-step workflow

**1. Pull remote changes first**

```bash
# Stash any unstaged changes in main
git stash push -m "Temporary stash for subrepo work"

# Pull to get the merged branch with all changes
git subrepo pull 40-code/415-subrepos/petaluma-ai-github-io

# Restore your stashed changes
git stash pop
```

**2. Create a worktree for cleanup**

```bash
# Create a temporary worktree at the merged branch
git worktree add /tmp/subrepo-worktree refs/subrepo/40-code/415-subrepos/petaluma-ai-github-io/pull

# Navigate to the worktree
cd /tmp/subrepo-worktree
```

**3. Clean up the commits**

```bash
# Interactive rebase to clean up commit history
# Squash related commits, rewrite messages, drop non-subrepo changes
git rebase -i HEAD~N  # where N is the number of commits to review

# In the editor:
# - squash related commits into one
# - reword commit messages to be subrepo-specific
# - drop commits that don't actually change subrepo content
```

**4. Reset to root (optional, for single clean commit)**

If you want a single squashed commit instead of multiple:

```bash
# Find the root of your changes (the remote parent)
git log --oneline | grep "subrepo pull\|git subrepo" | head -1

# Reset to that point, keeping all changes staged
git reset --soft <remote-parent-commit>

# Create one clean commit
git commit -m "Update website: concise description of changes"
```

**5. Push from the cleaned branch**

```bash
# Push the cleaned-up branch
git subrepo push 40-code/415-subrepos/petaluma-ai-github-io
```

**6. Clean up the worktree**

```bash
# Return to main repo
cd /Users/nikhilmaddirala/repos/monorepo

# Remove the temporary worktree
git worktree remove /tmp/subrepo-worktree

# Clean up subrepo artifacts
git subrepo clean 40-code/415-subrepos/petaluma-ai-github-io --force
```

### Example: Complete clean push session

```bash
# In your main monorepo directory
git stash push -m "WIP"
git subrepo pull 40-code/415-subrepos/petaluma-ai-github-io
git stash pop

# Create worktree for cleanup
git worktree add /tmp/petaluma-work refs/subrepo/40-code/415-subrepos/petaluma-ai-github-io/pull
cd /tmp/petaluma-work

# Review and clean up (example: 5 commits back)
git rebase -i HEAD~5
# Squash 3 website commits into one with message "Update homepage hero section"
# Drop 2 commits that only touched dragonix config

# Or reset everything to one clean commit
git reset --soft $(git log --oneline --grep="git subrepo" | head -1 | awk '{print $1}')
git commit -m "Update website: homepage hero and pricing sections"

# Push the cleaned changes
git subrepo push 40-code/415-subrepos/petaluma-ai-github-io

# Back in main repo, clean up
cd -
git worktree remove /tmp/petaluma-work
git subrepo clean 40-code/415-subrepos/petaluma-ai-github-io --force
```

### Advantages of worktree pattern

- **Isolation:** Your main working directory stays untouched
- **Safety:** You can experiment with rebase/squash without affecting main branch
- **Flexibility:** Can keep the worktree around for multiple push attempts
- **Clean history:** Standalone repo gets focused, well-organized commits

### Tips for good commit messages in standalone repo

- Focus on WHAT changed in the website, not HOW or WHY
- Keep it concise: "Update homepage hero section" not "Merge branch feature/new-hero"
- If squashing multiple changes, use a summary: "Update website: hero, pricing, and team sections"
- Avoid monorepo-specific references (ticket numbers, internal jira, etc.)

## Typical Session

Start of work:

```bash
# Check for remote changes
git subrepo status --fetch 40-code/415-subrepos/petaluma-ai-github-io

# If Upstream Ref differs from Pulled Commit, pull them
git subrepo pull 40-code/415-subrepos/petaluma-ai-github-io
```

Make your changes:

```bash
# Edit files
git add 40-code/415-subrepos/petaluma-ai-github-io/
git commit -m "your changes"
```

Push your changes:

```bash
# First check/pull again if collaborator pushed meanwhile
git subrepo status --fetch 40-code/415-subrepos/petaluma-ai-github-io
git subrepo pull 40-code/415-subrepos/petaluma-ai-github-io

# Then push your changes
git subrepo push 40-code/415-subrepos/petaluma-ai-github-io
```
