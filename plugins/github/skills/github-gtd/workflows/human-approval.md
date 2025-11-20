---
description: Review implementation, test locally, and approve for merge
---

## Overview

Guide humans through local testing, code review, and approval decision-making for implementations ready for merge.

## Context

Start by gathering issues and PRs ready for approval:

```bash
# Get issues ready for human approval
gh issue list --state open --label "status-implementation-review" --limit 10 --json number,title,labels,author

# Get corresponding PRs
gh pr list --state open --limit 20 --json number,title,labels,headRefName,state,isDraft
```

If $ARGUMENTS is empty, show the user recent issues with "status-implementation-review" label and ask them to select one.

If $ARGUMENTS contains only digits, treat it as an issue number. If $ARGUMENTS contains text, search for matching items from the recent list.

Once you have identified the issue, gather PR and implementation details:

```bash
# Get issue details
gh issue view ISSUE_NUMBER --json title,body,labels,comments,number

# Find linked PR
gh pr list --search "linked:ISSUE_NUMBER" --json number,title,headRefName,url,state

# Get PR details and review comments
gh pr view PR_NUMBER --json title,body,state,isDraft,reviews,comments,headRefName

# Get PR diff summary
gh pr diff PR_NUMBER --name-status

# Check worktree location
echo "Worktrees:"
git worktree list | grep "issue-ISSUE_NUMBER" || echo "No worktree found for this issue"

# Check tests and build status
gh pr checks PR_NUMBER
```

## Your Task

**Goal**: Help the human review, test, and approve the implementation for merging.

**Issue to approve**: Based on user input ($ARGUMENTS) or selection from recent issues

**Role**: You are Stage 6 (Human Approval) in the workflow:
1. Create Issue → ... → 5. Code review → **6. Human approval** ← (You are here) → 7. Merge & cleanup

### Process

1. **Verify Issue and PR Status**
   - Confirm issue has "status-implementation-review" label
   - Confirm linked PR exists and is ready for review (not draft)
   - Check that AI code review is complete
   - Verify all checks/tests are passing

2. **Present Implementation Summary**
   Display key information for the user:
   - What the issue was trying to accomplish
   - Summary of changes made (from PR description)
   - Files modified/created (high-level overview)
   - Test results and code review feedback
   - Any concerns or notes from AI review

3. **Guide Local Testing**
   Help the user test the implementation locally:

   **Option A: Use existing worktree**
   ```bash
   # If worktree exists
   echo "Navigate to worktree:"
   echo "cd worktrees/issue-ISSUE_NUMBER-<slug>"
   echo ""
   echo "Run tests:"
   echo "npm test"  # or appropriate test command for the project
   echo ""
   echo "Try the feature manually"
   ```

   **Option B: Check out PR branch**
   ```bash
   # If no worktree, check out the PR branch
   echo "Check out the PR branch:"
   echo "gh pr checkout PR_NUMBER"
   echo ""
   echo "Run tests:"
   echo "npm test"  # or appropriate test command
   echo ""
   echo "Try the feature manually"
   ```

   Ask user to verify:
   - All acceptance criteria from the issue are met
   - The implementation works as expected
   - No unexpected side effects or regressions
   - Code quality meets their standards

4. **Review Code Quality**
   Guide the user through code review:
   - Show PR diff with `gh pr diff PR_NUMBER`
   - Highlight any AI review comments
   - Ask if code follows repository conventions
   - Check if documentation is adequate

5. **Interactive Decision**
   Ask the user what they want to do:

   **Option A: Approve for merge**
   - Approve the PR in GitHub
   - Update issue label from "status-implementation-review" to "status-implementation-done"
   - Optionally add approval comment

   **Option B: Request changes**
   - Add review comments specifying what needs to change
   - Update issue label from "status-implementation-review" back to "status-implementation-todo"
   - Tag the implementation for revision

   **Option C: Ask questions or need more time**
   - Help user add questions as PR comments
   - Keep "status-implementation-review" label until ready to decide

6. **Execute Decision**
   Depending on user's choice:

   **For approval:**
   ```bash
   # Approve the PR
   gh pr review PR_NUMBER --approve --body "[Optional approval message]"

   # Update issue label
   gh issue edit ISSUE_NUMBER --remove-label "status-implementation-review" --add-label "status-implementation-done"

   # Optionally add comment
   gh issue comment ISSUE_NUMBER --body "Implementation approved. Ready to merge."
   ```

   **For requesting changes:**
   ```bash
   # Request changes on PR (user should specify what needs to change)
   gh pr review PR_NUMBER --request-changes --body "[Specific feedback on what needs to change]"

   # Update issue label
   gh issue edit ISSUE_NUMBER --remove-label "status-implementation-review" --add-label "status-implementation-todo"

   # Add comment to issue
   gh issue comment ISSUE_NUMBER --body "Changes requested. See PR for details."
   ```

   **For questions/more time:**
   ```bash
   # Add questions as PR comment
   gh pr comment PR_NUMBER --body "[User's questions or notes]"

   # Label stays "status-implementation-review"
   ```

### Guidelines

- **Human judgment required**: This is a human decision point, not autonomous
- **Thorough testing encouraged**: Guide user to actually test the implementation, not just review code
- **Clear navigation**: Make it easy for user to find and test the code
- **Capture feedback**: When requesting changes, ensure specific actionable feedback is provided
- **Efficient workflow**: Make it easy to approve good implementations quickly
- **Trust but verify**: AI review is helpful, but human should validate critical functionality

## Success Criteria

Your work is complete when:
- ✅ User has tested the implementation locally
- ✅ User has reviewed the code changes
- ✅ User has made an informed decision (approve, request changes, or ask questions)
- ✅ PR approved in GitHub (if approved)
- ✅ Issue label updated appropriately:
  - "status-implementation-done" if approved
  - "status-implementation-todo" if changes requested
  - "status-implementation-review" if questions asked (unchanged)
- ✅ Comments added documenting the decision
- ✅ User understands next steps

## Next Steps

**After approval** ("status-implementation-done" label):
- User can run `/gh-merge <issue-number>` to merge and clean up
- Or wait for autonomous merge agent to handle it

**After requesting changes** ("status-implementation-todo" label):
- Implementation team (or AI) addresses feedback
- Returns to "status-implementation-review" when changes are made

**After questions** ("status-implementation-review" label - unchanged):
- Wait for questions to be answered
- Then complete the approval process
