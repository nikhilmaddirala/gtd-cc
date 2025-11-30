---
description: Guides humans through local testing and final approval process
---

Use the gh-manage skill and follow its approval workflow exactly as written.

**Target Issue/PR**:
- If $ARGUMENTS is empty, you will show the user recent issues with "status-implementation-review" label and ask them to select one
- If $ARGUMENTS contains only digits, treat it as an issue or PR number
- If $ARGUMENTS contains text, search for matching items from the recent list
