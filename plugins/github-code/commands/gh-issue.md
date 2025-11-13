---
description: Create issue
---

## Context: Repository State

```bash
# Available issue labels
gh label list

# Issue templates (if any)
ls -la .github/ISSUE_TEMPLATE/ 2>/dev/null || echo "No issue templates found"

# Recent issues for style reference
gh issue list --limit 5 --state all

# Current project boards
gh project list 2>/dev/null || echo "No project boards found"
```

## Your Task

**Goal**: Create a well-documented GitHub issue following repository conventions.

**User's initial request**: $ARGUMENTS

### Process

1. **Understand the request**
   - Chat iteratively with the user to clarify details
   - Determine issue type (feature, bug, docs, refactor, or other)
   - Understand scope, constraints, and dependencies

2. **Check for issue templates**
   - If `.github/ISSUE_TEMPLATE/` exists, offer available templates to user
   - Allow user to choose a template or create custom issue
   - If no templates, use structured format below

3. **Gather complete information**
   Ask about:
   - **Problem/Goal**: What needs to be done and why?
   - **Context**: Any relevant background, links, or constraints
   - **Acceptance Criteria**: How will we know it's complete?
   - **Dependencies**: Related issues, blockers, or prerequisites
   - **Scope**: What's in scope vs. out of scope (if applicable)

4. **Structure the issue**
   Use this format (adapt based on templates or repo conventions):
   ```markdown
   ## Problem/Goal
   [Clear description of what needs to be done and why]

   ## Context
   [Relevant background, constraints, related work]

   ## Acceptance Criteria
   - [ ] [Specific, testable criterion]
   - [ ] [Another criterion]

   ## Additional Notes
   [Dependencies, scope boundaries, open questions]
   ```

5. **Apply labels (if available)**
   - Check `gh label list` output to see what labels exist
   - Suggest relevant labels based on issue type and content
   - Common patterns: type labels (feature, bug, docs) and status labels
   - If user has custom labels or no labels, that's fine - labels are optional

6. **Create the issue**
   - Use `gh issue create` with:
     - Clear, descriptive title
     - Well-structured body following template/format
     - Labels (if user wants them and they exist)
   - Link to project board if configured
   - Return issue URL and number

### Guidelines

- Ensure the issue contains sufficient detail that someone could implement it
- Ask clarifying questions when user input is vague or incomplete
- Follow existing repository conventions (check recent issues for style)
- If multiple approaches exist, note them briefly for consideration
- Keep issue focused and actionable
- Adapt format to match repository patterns (some repos prefer different structures)
