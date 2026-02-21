---
description: Research codebase, analyze options, create implementation plan, append to issue body
---

# plan

**Template**: `templates/plan.md`

## Overview

Research the codebase, analyze options, and create an implementation plan before starting work. The plan is appended to the issue body as the single source of truth. This phase is optional but recommended for complex work.


## Process

1. Load the issue:
   ```bash
   gh issue view N --json number,title,body,labels
   ```

2. Requirement analysis:
   - Problem/goal: what exactly needs to be done and why
   - Acceptance criteria: how will we know this is complete
   - Scope: what's in scope vs out of scope
   - Constraints: technical, time, or resource constraints
   - Dependencies: related issues or prerequisites

3. Codebase research:
   - Explore existing architecture and patterns
   - Identify files to create/modify
   - Check for similar implementations to follow
   - Use Glob/Grep/Read tools to understand the code

4. Identify affected subtrees:
   - Check if modified paths fall under any `.monorepo-git.yaml` subtree prefixes
   - Note which remotes will need publishing after merge
   - Consider cross-subtree dependencies

5. Options analysis (if multiple approaches exist):
   - Compare alternatives with tradeoffs
   - Consider maintainability and scalability
   - Document recommendation with rationale

6. Technical feasibility:
   - Evaluate complexity and risks
   - Identify potential blockers
   - Plan testing approach

7. Append plan to issue body using `templates/plan.md` format:
   ```bash
   EXISTING_BODY=$(gh issue view N --json body --jq '.body')
   gh issue edit N --body "${EXISTING_BODY}

   ---

   ## Plan

   ### Summary

   [1-2 sentences on goal and approach]

   ### Technical approach

   [Key decisions and rationale]

   ### Files to create/modify

   - \`path/to/file\` - description of change

   ### Affected subtrees

   - [remote-name] - [description of impact]

   ### Implementation steps

   1. [Step 1]
   2. [Step 2]
   3. [Step 3]

   ### Testing

   [How to verify the changes work]"
   ```

8. Optionally update status label (if using labels):
   ```bash
   gh issue edit N --remove-label "status-plan" --add-label "status-implement"
   ```

9. Report: "Plan added to issue #N. Ready for implementation."

10. Suggest next step: "Run `start-work --issue N` or `/mg-start-work --issue N` to create worktree"


## Guidelines

- Always create plan before starting work on complex tasks
- Append plan to issue body (not as a comment) so it stays as the single source of truth
- Do NOT create worktree in this phase - that's the start-work sub-skill's job
- Pay special attention to subtree impacts - changes to `41-subtrees/` will need publishing
- If the task is simple (single file, obvious change), skip planning and go straight to start-work


## When to use

Use this sub-skill when:
- The task touches multiple files or directories
- There are multiple valid approaches
- The task affects published subtrees
- You want to document the approach before implementing
- The issue description is vague and needs clarification

Skip this sub-skill when:
- The task is a simple bug fix or typo
- The change is isolated to a single file
- The approach is obvious from the issue description
