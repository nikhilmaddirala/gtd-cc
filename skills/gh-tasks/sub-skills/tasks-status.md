---
description: Show workflow status - PRs, issues, worktrees - and guide next actions
---

# tasks-status

## Overview

Gather all active work items (PRs, issues, worktrees) and analyze the state to guide next actions. The goal is to answer: "What's going on and what should I do next?"


## Process

1. Run diagnostic (delegate to script):
   ```bash
   scripts/tasks-status.sh
   ```
   The script outputs four sections:
   - Worktree health -- each worktree classified as healthy, anomaly, stale, or incomplete, with issue and PR cross-references
   - Orphan PRs -- open PRs without local worktrees, with resume commands
   - Next actions -- issues grouped by status label (needs-planning, ready-to-implement, ready-for-review) with suggested commands
   - Anomaly summary -- count of items needing attention

2. Interpret and contextualize:
   - Parse the script output sections
   - Relate findings to the user's current question or context
   - Prioritize: anomalies first, then actionable items, then informational

3. Present findings:
   - Lead with overall health assessment (all clean, or N items need attention)
   - Show the script's data organized by urgency
   - For anomalies, explain what happened and what the options are

4. Recommend and offer fixes:
   - For each anomaly, suggest the specific sub-skill or command to resolve it:
     - Stale worktree (issue closed): "Remove with `git worktree remove`?"
     - Orphan PR: "Resume with `work --resume <branch>` or close with `gh pr close`?"
     - Issue needs planning: "Run `plan` sub-skill"
     - Issue ready to implement: "Run `work` sub-skill"
     - PR ready for review: "Run `review` sub-skill"
   - If everything is healthy: suggest starting something new with `new` sub-skill
   - Get user confirmation before taking any destructive action


## Guidelines

- Always gather fresh data -- don't rely on cached state
- Present data first, then analysis, then recommendations
- Be specific about which sub-skill to run next
- If a PR/branch doesn't follow `issue-N-*` naming, note it's outside the managed workflow
- Offer to fix anomalies only with user confirmation
