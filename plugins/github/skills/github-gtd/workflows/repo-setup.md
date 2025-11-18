---
description: Set up essential GitHub workflow infrastructure including labels and worktree directory
---

## Overview

Configure GitHub repositories for the 7-stage issue-driven development workflow by creating workflow labels and setting up isolated development environments.

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

**Goal**: Set up essential GitHub workflow infrastructure in the current repository, enabling the 7-stage issue-driven development workflow.

**Role**: You are Stage 0 (Repository Initialization) in the workflow:
**0. Repository initialization** ← (You are here) → 1. Create Issue → 2. Planning → ... → 7. Merge & cleanup

### Process

1. **Verify Repository Context**
   - Confirm this is a git repository with GitHub remote
   - Verify GitHub authentication is active

2. **Set Up Workflow Labels**
   Create labels for workflow state tracking. These are required for all subsequent workflow stages:

   **Workflow state labels:**
   ```bash
   gh label create "needs planning" --description "Requires implementation plan" --color "FEF2C0"
   gh label create "needs plan approval" --description "Human must review approach" --color "FBCA04"
   gh label create "needs implementation" --description "Ready for coding" --color "0E8A16"
   gh label create "in review" --description "Code under review" --color "1D76DB"
   gh label create "ready for approval" --description "Awaiting human approval" --color "5319E7"
   gh label create "approved for merge" --description "Ready to merge" --color "0E8A16"
   gh label create "blocked" --description "Work stopped, needs intervention" --color "D93F0B"
   ```

   **Issue type labels (optional but recommended):**
   ```bash
   gh label create "feature" --description "New functionality" --color "A2EEEF"
   gh label create "bug" --description "Defect or unexpected behavior" --color "D73A4A"
   gh label create "docs" --description "Documentation changes" --color "0075CA"
   gh label create "refactor" --description "Code improvements without behavior change" --color "FBCA04"
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
