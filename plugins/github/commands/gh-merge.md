---
name: gh-merge
description: Merge PR via GitHub and cleanup the worktree
---

# Merge task

- Use the github skill and its merge sub-skill to merge the PR and cleanup. CRITICAL: you MUST invoke the github skill.
- If the user has provided any additional context, pass that into the skill invocation. Here is the context provided by the user: $ARGUMENTS
