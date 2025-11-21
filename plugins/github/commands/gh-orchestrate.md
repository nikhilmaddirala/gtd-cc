---
description: Orchestrate sub-agents to manage various parts of the GitHub GTD workflows
---

## Your task

You are the workflow coordinator. Parse $ARGUMENTS to determine the issue number and workflow type, then invoke the gtd-github-agent with appropriate instructions. If the user's request spans multiple stages or issues, you will determine how to call multiple instances of the subagent in sequence or parallel.

## Parsing $ARGUMENTS

- If empty: show recent open issues and ask the user to select one
- If numeric: treat as issue number, ask user for workflow type (or default to `auto`)
- If text: parse for issue number and workflow type keywords (full, plan, build, review, merge, auto)

## Invoking the agent

Call the gtd-github-agent with instructions specifying:

- **Issue number** - the GitHub issue to work with
- **Workflow type** - the stage(s) to execute:
  - `plan` - planning stage only
  - `build` - implementation stage only
  - `review` - code review stage only
  - `merge` - merge and cleanup stage only

The agent will analyze the issue state and execute the requested workflow autonomously.

