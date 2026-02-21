---
description: Create a GitHub Issue for focused work
---

# new

**Template**: `templates/issue.md`

## Overview

Create a new task as a GitHub Issue. The issue body follows the issue template structure with goal, context, and acceptance criteria.


## Process

1. Create issue using `templates/issue.md` format:
   ```bash
   gh issue create \
     --title "Task title here" \
     --body "$(cat <<'EOF'
   ## Goal

   [What needs to be done and why]

   ## Context

   [Relevant background, constraints, dependencies]

   ## Acceptance criteria

   - [ ] [Criterion 1]
   - [ ] [Criterion 2]
   EOF
   )"
   ```

2. Extract issue number from output

3. Report: "Created issue #N"

4. Suggest next steps:
   - For complex work: "Run `plan` sub-skill to research and design approach"
   - For simple work: "Run `work` sub-skill to start implementation"


## Guidelines

- Keep issue title concise and action-oriented
- Goal section explains the "what" and "why"
- Context provides background needed to understand the task
- Acceptance criteria should be specific and testable
- Note affected areas if you know which directories/subtrees will be modified
