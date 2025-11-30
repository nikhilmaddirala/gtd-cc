---
description: Autonomous agent that builds code from approved implementation plans or addresses review feedback
---

Use the gh-build skill and follow its build workflow exactly as written.

**Target Issue/PR**:
- If $ARGUMENTS is empty, you will show the user recent issues and PRs and ask them to select one
- If $ARGUMENTS contains only digits, treat it as an issue or PR number
- If $ARGUMENTS contains text, search for matching items from the recent list
