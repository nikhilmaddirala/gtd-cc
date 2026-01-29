---
description: Move project from lab to production with GitHub repo and subtree setup
---

# Graduate

## Overview

Graduate a project from a development/lab directory to production, creating a GitHub repository and setting up subtree synchronization.

## Process

- Gather project information
  - Source directory (where project lives now)
  - Target directory (production path)
  - GitHub repo name and visibility (public/private)
  - Read `.monorepo-git.yaml` `directories` for path suggestions

- Create GitHub repository
  ```bash
  gh repo create repo-name --public --description "Project description"
  ```

- Move to production directory
  ```bash
  mv source/path/project target/path/project
  ```

- Commit to monorepo (CRITICAL: commit before subtree setup)
  ```bash
  git add -A
  git commit -m "feat(project): graduate to production"
  ```

- Add subtree remote
  ```bash
  git remote add remote-project https://github.com/user/repo.git
  ```

- Push to initialize remote
  ```bash
  git subtree push --prefix=target/path/project remote-project main
  ```

- Verify
  ```bash
  ls -la target/path/project/
  git remote -v | grep remote-project
  gh repo view user/repo --web
  ```

## Guidelines

- Follow `remote-*` naming convention
- If repo already exists with commits, use `git subtree add --squash` instead of push
- Push rejected (non-fast-forward): fetch, pull with `--squash`, resolve conflicts, then push
