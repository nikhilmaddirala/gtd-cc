---
description: Sets up labels, templates, and branch protection for workflow management
---

## Context: Repository State

```bash
# Check current repository
echo "Repository: $(git remote get-url origin 2>/dev/null || echo 'Not a git repository')"
echo "Current branch: $(git branch --show-current 2>/dev/null || echo 'No branch')"

# Check GitHub authentication
gh auth status

# Check existing labels
echo -e "\n=== Existing Labels ==="
gh label list

# Check existing issue templates
echo -e "\n=== Issue Templates ==="
ls -la .github/ISSUE_TEMPLATE/ 2>/dev/null || echo "No issue templates found"

# Check existing PR template
echo -e "\n=== Pull Request Template ==="
test -f .github/pull_request_template.md && echo "PR template exists" || echo "No PR template found"

# Check branch protection rules
echo -e "\n=== Branch Protection ==="
gh api repos/:owner/:repo/branches/$(git branch --show-current)/protection 2>/dev/null || echo "No branch protection configured"
```

## Your Task

**Goal**: Set up GitHub workflow infrastructure in the current repository, enabling the 7-stage issue-driven development workflow.

**Role**: You are Stage 0 (Repository Initialization) in the workflow:
**0. Repository initialization** ← (You are here) → 1. Create Issue → 2. Planning → ... → 7. Merge & cleanup

### Process

1. **Verify Repository Context**
   - Confirm this is a git repository with GitHub remote
   - Check if workflow infrastructure already exists
   - Ask user if they want to overwrite existing labels/templates

2. **Set Up Workflow Labels**
   Create labels for workflow state tracking (if they don't already exist):

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

   **Issue type labels:**
   ```bash
   gh label create "feature" --description "New functionality" --color "A2EEEF"
   gh label create "bug" --description "Defect or unexpected behavior" --color "D73A4A"
   gh label create "docs" --description "Documentation changes" --color "0075CA"
   gh label create "refactor" --description "Code improvements without behavior change" --color "FBCA04"
   ```

3. **Create Issue Templates**
   Create standardized issue templates in `.github/ISSUE_TEMPLATE/`:

   **feature_request.yml** - For new features:
   ```yaml
   name: Feature Request
   description: Propose a new feature or enhancement
   labels: ["feature", "needs planning"]
   body:
     - type: markdown
       attributes:
         value: |
           ## Problem/Goal
     - type: textarea
       id: problem
       attributes:
         label: What needs to be done and why?
         description: Clear description of the feature and its purpose
       validations:
         required: true
     - type: markdown
       attributes:
         value: |
           ## Context
     - type: textarea
       id: context
       attributes:
         label: Background and constraints
         description: Relevant background, links, or constraints
     - type: markdown
       attributes:
         value: |
           ## Acceptance Criteria
     - type: textarea
       id: acceptance
       attributes:
         label: How will we know it's complete?
         description: Specific, testable criteria (use checkboxes)
         value: |
           - [ ]
       validations:
         required: true
   ```

   **bug_report.yml** - For bugs:
   ```yaml
   name: Bug Report
   description: Report a defect or unexpected behavior
   labels: ["bug", "needs planning"]
   body:
     - type: markdown
       attributes:
         value: |
           ## Problem
     - type: textarea
       id: problem
       attributes:
         label: What is happening?
         description: Clear description of the bug
       validations:
         required: true
     - type: markdown
       attributes:
         value: |
           ## Expected Behavior
     - type: textarea
       id: expected
       attributes:
         label: What should happen instead?
       validations:
         required: true
     - type: markdown
       attributes:
         value: |
           ## Steps to Reproduce
     - type: textarea
       id: steps
       attributes:
         label: How can we reproduce this?
         value: |
           1.
           2.
           3.
     - type: markdown
       attributes:
         value: |
           ## Additional Context
     - type: textarea
       id: context
       attributes:
         label: Environment, logs, screenshots, etc.
   ```

4. **Create Pull Request Template**
   Create `.github/pull_request_template.md`:
   ```markdown
   ## Summary

   Closes #

   <!-- Brief description of what this PR does -->

   ## Changes

   -

   ## Test Plan

   - [ ] Tests pass locally
   - [ ] Code follows repository conventions
   - [ ] Documentation updated (if needed)

   ## Checklist

   - [ ] All acceptance criteria from the issue are met
   - [ ] Tests added/updated as appropriate
   - [ ] No merge conflicts with main
   ```

5. **Configure Branch Protection** (for main branch)
   Ask user if they want to enable branch protection with these settings:
   - Require pull request reviews before merging
   - Require status checks to pass before merging
   - Require branches to be up to date before merging
   - Do not allow force pushes
   - Do not allow deletions

   ```bash
   # Example branch protection (requires GitHub API)
   gh api -X PUT repos/:owner/:repo/branches/main/protection \
     --field required_status_checks='{"strict":true,"contexts":[]}' \
     --field enforce_admins=true \
     --field required_pull_request_reviews='{"required_approving_review_count":1}' \
     --field restrictions=null
   ```

6. **Create Worktree Directory**
   Set up directory structure for isolated development:
   ```bash
   mkdir -p worktrees
   echo "worktrees/" >> .gitignore
   ```

7. **Summary**
   Provide a summary of what was configured:
   - Labels created/updated
   - Templates created
   - Branch protection configured (or not)
   - Next steps for the user

### Guidelines

- **Non-destructive**: Don't overwrite existing labels unless user confirms
- **Customizable**: Ask about branch protection settings rather than forcing defaults
- **Repository-specific**: Adapt to existing repository conventions when possible
- **Clear output**: Summarize what was done and what the user can do next
- **Error handling**: If not in a git repo or GitHub remote missing, guide user to set up first

## Success Criteria

Your work is complete when:
- ✅ All workflow labels exist in the repository
- ✅ Issue templates created in `.github/ISSUE_TEMPLATE/`
- ✅ PR template created at `.github/pull_request_template.md`
- ✅ Branch protection configured (if user requested)
- ✅ Worktree directory structure set up
- ✅ Summary provided to user with next steps

## Next Steps for User

After running `/gh-repo`, users can:
1. Create their first issue with `/gh-issue "description"`
2. Or manually create an issue in GitHub using the new templates
3. Start the workflow with `/gh-plan <issue-number>`
