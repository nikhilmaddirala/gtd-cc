---
description: Review AI's implementation plan and approve or request revisions
---

## Overview

Help the human review AI-generated implementation plans and make informed decisions to approve or request revisions.

## Context

Gather the issue details to understand the plan:

```bash
# Get recent issues needing plan approval
gh issue list --state open --label "needs plan approval" --limit 10 --json number,title,labels,author
```

If $ARGUMENTS is empty, show the user recent issues with "needs plan approval" label and ask them to select one.

If $ARGUMENTS contains only digits, treat it as an issue number. If $ARGUMENTS contains text, search for matching issues from the recent list.

Once you have identified the issue number, gather the plan details:

```bash
# Get issue details including all comments
gh issue view ISSUE_NUMBER --json title,body,labels,comments,number

# Check for implementation plan in comments (usually starts with "## Implementation Plan")
gh issue view ISSUE_NUMBER --comments | grep -A 50 "## Implementation Plan" || echo "No implementation plan found"

# Get repository context
git log --oneline -n 5
git branch -a
```

## Your Task

**Goal**: Help the human review AI's implementation plan and make an informed decision to approve or request revisions.

**Issue to review**: Based on user input ($ARGUMENTS) or selection from recent issues

**Role**: You are Stage 3 (Plan Approval - Conditional) in the workflow:
1. Create Issue → 2. Planning → **3. Plan approval** ← (You are here) → 4. Implementation → ... → 7. Merge & cleanup

**Note**: This stage only occurs when AI requests human input on the approach. For straightforward plans, AI auto-approves and skips this stage.

### Process

1. **Verify Issue Status**
   - Confirm issue has "needs plan approval" label
   - Extract the implementation plan from comments
   - Identify why AI requested human approval (stated in plan comments)

2. **Present Plan Summary**
   Display the implementation plan in a clear, readable format:
   - Summary of the approach
   - Technical approach and rationale
   - Files to create/modify
   - Implementation steps
   - Options considered (if applicable) with AI's recommendation
   - Why AI requested human approval

3. **Help Human Evaluate**
   Guide the user through key questions:
   - Does the approach make sense for the requirements?
   - Are there any missing considerations or edge cases?
   - Do you agree with the recommended option (if multiple approaches were presented)?
   - Are the implementation steps clear enough for autonomous execution?
   - Do you have concerns about the approach?

4. **Interactive Decision**
   Ask the user what they want to do:

   **Option A: Approve the plan**
   - Update issue label from "needs plan approval" to "needs implementation"
   - Add comment confirming approval
   - Optionally add any additional guidance or constraints

   **Option B: Request revisions**
   - Update issue label from "needs plan approval" back to "needs planning"
   - Add comment with specific feedback on what needs to change
   - Explain what concerns need to be addressed

   **Option C: Ask questions first**
   - Help user formulate questions for the AI
   - Add comment with questions
   - Keep "needs plan approval" label until questions are answered

5. **Execute Decision**
   Depending on user's choice:

   **For approval:**
   ```bash
   # Add approval comment
   gh issue comment ISSUE_NUMBER --body "Plan approved. Proceeding to implementation."

   # Update label
   gh issue edit ISSUE_NUMBER --remove-label "needs plan approval" --add-label "needs implementation"
   ```

   **For revision request:**
   ```bash
   # Add revision feedback
   gh issue comment ISSUE_NUMBER --body "Requesting plan revisions:

   [User's specific feedback]

   Please address these concerns and update the plan."

   # Update label
   gh issue edit ISSUE_NUMBER --remove-label "needs plan approval" --add-label "needs planning"
   ```

   **For questions:**
   ```bash
   # Add questions comment
   gh issue comment ISSUE_NUMBER --body "Questions about the plan:

   [User's questions]

   Please clarify these points."

   # Label stays "needs plan approval"
   ```

### Guidelines

- **Human judgment required**: This is a human decision point, not autonomous
- **Clear presentation**: Make the plan easy to understand and evaluate
- **Ask guiding questions**: Help user think through important considerations
- **Capture reasoning**: When user approves or requests revisions, document their reasoning
- **Respectful of AI analysis**: Present AI's reasoning fairly while supporting human decision
- **Efficient workflow**: Make it easy to approve good plans quickly while ensuring careful review of complex ones

## Success Criteria

Your work is complete when:
- ✅ Implementation plan presented clearly to user
- ✅ User has made an informed decision (approve, revise, or ask questions)
- ✅ Issue label updated appropriately:
  - "needs implementation" if approved
  - "needs planning" if revisions requested
  - "needs plan approval" if questions asked (unchanged)
- ✅ Comment added to issue documenting the decision
- ✅ User understands next steps

## Next Steps

**After approval** ("needs implementation" label):
- User can run `/gh-build <issue-number>` to start implementation
- Or wait for autonomous build agent to pick it up

**After revision request** ("needs planning" label):
- User can run `/gh-plan <issue-number>` to revise the plan
- Or wait for autonomous planning agent to pick it up

**After questions** ("needs plan approval" label - unchanged):
- User can run `/gh-plan <issue-number>` to have AI address questions
- Or manually review AI's response when it answers the questions
