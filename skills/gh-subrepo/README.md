# gh-subrepo

## Overview

- Stateful bidirectional sync with `git-subrepo`
- Project graduation from lab to production
- Subrepo setup and health diagnostics

## Why this skill exists

The current monorepo workflow has active writers on both sides:

- monorepo subdirectory edits by the owner
- standalone repo edits by collaborators

`git-subrepo` provides explicit per-subdir sync state and commit-aware pull/push workflows, so the process does not rely on file-level direction heuristics.

The custom `scripts/subrepo-status.sh` helper is optional. It provides a single monorepo-wide table that combines managed and unmanaged projects, but the authoritative command remains `git subrepo status`.

## Roadmap

- Pilot on one subtree and validate operational flow
- Add more robust status reporting after pilot
- Migrate graduate and sync automation from rsync-based logic to subrepo-first logic
