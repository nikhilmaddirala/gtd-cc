---
description: Automated end-to-end pipeline from main. Creates issue, plans, spins up worktree, launches subagent for implementation.
---

# orchestrate

## Overview

End-to-end automated pipeline that runs from the main worktree. Creates an issue, researches and plans, sets up an isolated worktree, then launches a subagent inside that worktree to implement. The orchestrator never makes code changes in main — all modifications happen inside the dedicated worktree.


## Prerequisites

- MUST be run from the main worktree (not from `.worktrees/*`)
- Verify before proceeding:
  ```bash
  CURRENT_DIR=$(pwd)
  if [[ "$CURRENT_DIR" == *".worktrees"* ]]; then
    echo "ERROR: orchestrate must run from the main worktree, not from a feature worktree"
    exit 1
  fi
  ```


## Process

### Stage 1: create issue (from main)

Create a GitHub issue for the task:
```bash
gh issue create --title "Task title" --body "$(cat <<'EOF'
## Goal

[What needs to be done and why]

## Context

[Relevant background]

## Acceptance criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
EOF
)"
```

Capture the issue number `N` from the output.


### Stage 2: plan (from main)

Execute the `plan` sub-skill process:
- Load the issue: `gh issue view N --json number,title,body`
- Research the codebase using Glob/Grep/Read tools
- Identify affected subtrees by checking paths against `.monorepo-git.yaml`
- Analyze options if multiple approaches exist
- Append plan to issue body using `templates/plan.md` format


### Stage 3: create worktree (from main)

Use the work script to create the worktree:
```bash
scripts/work.sh N
```

This creates:
- Branch: `issue-N-<slug>`
- Worktree: `.worktrees/issue-N-<slug>`
- Draft PR linked to the issue


### Stage 4: implement (via Task tool)

Use the Task tool to launch an agent for implementation. The orchestrator decides the appropriate task configuration based on the work to be done.

Key considerations for the task:
- Set working directory to the worktree (`.worktrees/issue-N-<slug>`)
- The task should read the plan from the issue body
- The task should commit and push changes
- The task should not modify files outside its worktree

Example Task tool usage:
```
Task(
  description="Implement issue N",
  prompt="Implement the plan for issue #N in worktree .worktrees/issue-N-slug. Read the issue for the plan, implement it, commit with conventional format, and push.",
  subagent_type="general-purpose"
)
```

The orchestrator has flexibility to adjust the task prompt and parameters based on:
- Complexity of the work
- Whether to run in background
- How much context to provide

Wait for task to complete (or monitor if running in background).


### Stage 5: report (from main)

Verify the PR was created/updated:
```bash
gh pr list --head "issue-N-" --json number,url,state
```

Report: "Issue #N created, planned, and implemented. Draft PR ready for review."

Suggest next steps:
- "Run `review` sub-skill to review the PR"
- "Run `merge` sub-skill to merge when ready"


## Guidelines

- NEVER make code changes in the main worktree — orchestrate is a coordinator, not an implementer
- All code modifications happen inside `.worktrees/issue-N-<slug>` via the subagent
- The orchestrator stays in main throughout; only the subagent works in the worktree
- If the subagent fails, report the failure and leave the worktree intact for manual intervention
- Check subtree impacts during planning to note which remotes will need publishing after merge


## When to use

Use orchestrate when:
- You want fully automated end-to-end task completion
- The task is well-defined and can be planned programmatically
- You trust the AI to implement without step-by-step guidance

Use manual workflow (plan → start-work → implement → review → finish-work) when:
- You want to review each stage before proceeding
- The task is complex or ambiguous
- You want fine-grained control over the implementation
