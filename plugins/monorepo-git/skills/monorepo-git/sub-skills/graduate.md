---
description: Move a project from lab to production with GitHub repo and subtree setup
---

# Graduate

## Overview

This sub-skill graduates a project from a development/lab directory to production and sets up subtree synchronization with a new GitHub repository.

## Context

User has a project ready for production. They want to:
1. Create a GitHub repository
2. Move the project to a production directory
3. Set up subtree sync for ongoing development

## Process

### 1. Gather project information

Ask user for:
- **Source directory**: Where the project currently lives
- **Target directory**: Where to move it (public or private production path)
- **GitHub repo name**: Name for the new repository
- **Visibility**: public or private

If a config file (`.monorepo-git.yaml`) exists with `directories` defined, suggest those paths. Otherwise, ask user to provide paths explicitly.

### 2. Create GitHub repository

For public projects:
```bash
gh repo create repo-name --public --description "Project description"
```

For private projects:
```bash
gh repo create repo-name --private --description "Project description"
```

Note the repository URL for later.

### 3. Move to production directory

```bash
mv source/path/project-name target/path/project-name
```

### 4. Commit to monorepo

CRITICAL: Commit the move before setting up subtree.

```bash
git add -A
git commit -m "feat(project-name): graduate project to production"
```

### 5. Add subtree remote

```bash
git remote add remote-projectname https://github.com/username/repo-name.git
```

Follow the `remote-*` naming convention for auto-detection.

### 6. Initialize remote (push)

Since the remote is empty, push to initialize:

```bash
git subtree push --prefix=target/path/project-name remote-projectname main
```

### 7. Verify

```bash
# Check directory exists
ls -la target/path/project-name/

# Check remote added
git remote -v | grep remote-projectname

# Check GitHub has the code
gh repo view username/repo-name --web
```

Success criteria:
- Project exists in target directory
- Files committed to monorepo
- Remote configured for subtree
- Code pushed to GitHub repository
- No files remain in source directory

## Guidelines

### Special cases

**Repo already exists on GitHub:**
- If empty: Proceed as normal
- If has commits: Skip `gh repo create`. After adding remote, use `git subtree add` instead of push:
  ```bash
  git subtree add --prefix=target/path/project-name remote-projectname main --squash
  ```

**Push rejected (non-fast-forward):**
- Remote has existing history
- Solution: `git fetch remote-name`, then `git subtree pull --squash`, resolve conflicts, then push

### Undo graduation

If you need to cancel:
```bash
# Undo the monorepo commit
git reset HEAD~1

# Move back to source
mv target/path/project-name source/path/project-name

# Remove remote
git remote remove remote-projectname
```

### Configuration

If `.monorepo-git.yaml` exists with directories defined:
```yaml
directories:
  lab: "path/to/lab"
  public: "path/to/public"
  private: "path/to/private"
```

Use these as defaults when prompting user for paths.
