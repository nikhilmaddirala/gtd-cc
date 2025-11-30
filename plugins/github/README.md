# GitHub Workflow Plugin

Commands and agents for issue-driven GitHub work. One entrypoint (`gh-manage`) routes everything else. See `skills/README.md` for skill layout and `_common` standards.

## How to use

- Start here: `gh-manage <request>` (or `gh-manage-agent` for autonomous). It will triage, label, and dispatch to plan/build/review/merge.
- Need a specific stage?
  - Planning: `gh-plan <issue>`
  - Build/iterate: `gh-build <issue>`
  - Review/approval/merge: `gh-review <issue>` or `gh-merge <issue>`
  - Repo/issue/commit hygiene: `gh-repo`, `gh-issue`, `gh-commit`
- Human checkpoints stay in GitHub UI; labels track state and trigger the next agent.

## Commands (interactive)
- `gh-manage` — triage + orchestrate (primary entry; use this instead of gh-orchestrate)
- `gh-plan`, `gh-build`, `gh-review`, `gh-merge` — plan → implement → review/merge
- `gh-issue`, `gh-repo`, `gh-commit`, `gh-approve-plan`, `gh-approve` — ops/support

## Agents (autonomous)
- `gh-manage-agent` — manager/dispatcher (triage + orchestrate)
- `gh-plan-agent`, `gh-build-agent`, `gh-review-agent`, `gh-merge-agent`
- Ops helpers: `gh-repo-setup-agent`, `gh-issue-creation-agent`, `gh-issue-management-agent`, `gh-commit-agent`

## Lifecycle labels (see `_common/labels.md`)
- `status-planning-todo` → `status-planning-review` → `status-planning-done`
- `status-implementation-in-progress` → `status-implementation-done`
- `status-review-in-progress` → `status-review-changes-requested` / `status-review-approved`
- `status-merged`, `blocked`

## Stages (at a glance)
1) Intake/triage: clarify, label, create/update issue; capture context for next stage.  
2) Plan: research, write plan comment, update labels.  
3) Build: worktree/branch, implement, tests, draft PR, set review-ready labels.  
4) Review/approval: code review and optional human approval; set approval/changes labels.  
5) Merge/cleanup: squash merge, close issue/PR, delete branch/worktree; mark as merged.

## Quick patterns
- Always enter via `gh-manage` when unsure; it will find or create the issue and route correctly.
- Commands are interactive (ask/confirm); agents run end-to-end; both rely on skills as single source of truth.
- Keep labels in sync; `_common/labels.md` defines the lifecycle used by manager and orchestration.
