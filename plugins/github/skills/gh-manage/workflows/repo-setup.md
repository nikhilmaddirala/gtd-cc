---
description: Set up essential GitHub workflow infrastructure including labels and worktree directory
---

## Overview

Configure GitHub repositories for issue-driven development by creating workflow labels and setting up isolated development environments.

## Context

```bash
# Check current repository
echo "Repository: $(git remote get-url origin 2>/dev/null || echo 'Not a git repository')"
echo "Current branch: $(git branch --show-current 2>/dev/null || echo 'No branch')"

# Check GitHub authentication
gh auth status

# Check existing workflow labels
echo -e "\n=== Workflow Labels ===\"
gh label list | grep -E "needs planning|needs plan approval|needs implementation|in review|ready for approval|approved for merge|blocked"
```

## Your Task

**Goal**: Set up essential GitHub workflow infrastructure in the current repository to enable issue-driven development workflows.

**Role**: Repository initialization stage of the GitHub workflow

### Process

1. **Verify Repository Context**
   - Confirm this is a git repository with GitHub remote
   - Verify GitHub authentication is active

2. **Set Up Workflow Labels**
   Create labels for workflow state tracking. These are required for all subsequent workflow stages:

   **Status labels (track issue progress through planning and implementation):**
   ```bash
   gh label create "status-planning-todo" --description "Requires implementation plan" --color "FEF2C0"
   gh label create "status-planning-review" --description "Plan is under review" --color "FBCA04"
   gh label create "status-planning-done" --description "Planning completed, ready for implementation" --color "C2E0C6"
   gh label create "status-implementation-todo" --description "Ready for coding" --color "0E8A16"
   gh label create "status-implementation-review" --description "Implementation under review" --color "1D76DB"
   gh label create "status-implementation-done" --description "Implementation completed, ready to merge" --color "6F42C1"
   gh label create "blocked" --description "Work stopped, needs intervention" --color "D93F0B"
   ```

   **Type labels (categorize issue - optional but recommended):**
   ```bash
   gh label create "type-feature" --description "New functionality" --color "A2EEEF"
   gh label create "type-bug" --description "Defect or unexpected behavior" --color "D73A4A"
   gh label create "type-docs" --description "Documentation changes" --color "0075CA"
   gh label create "type-refactor" --description "Code improvements without behavior change" --color "FBCA04"
   ```

3. **Create Worktree Directory**
   Set up directory structure for isolated development. Required for `gh-build` and `gh-merge`:
   ```bash
   mkdir -p worktrees
   echo "worktrees/" >> .gitignore
   ```

4. **Summary**
   Provide a summary of what was configured:
   - Labels created/updated
   - Worktree directory structure set up
   - Next steps for the user

### Guidelines

- **Minimal and focused**: Only set up what's essential for workflow automation
- **Non-destructive**: Don't overwrite existing labels unless user confirms
- **Repository-specific**: Adapt to existing repository conventions when possible
- **Clear output**: Summarize what was done and what the user can do next
- **Error handling**: If not in a git repo or GitHub remote missing, guide user to set up first

## Success Criteria

Your work is complete when:
- ✅ All workflow state labels exist in the repository
- ✅ Worktree directory structure set up with `.gitignore` entry
- ✅ Summary provided to user with next steps

## Next Steps for User

After running `/gh-repo`, users can:
1. Create their first issue with `/gh-issue "description"`
2. Start the workflow with `/gh-plan <issue-number>`
