---
description: Executes final merge operations and cleanup
---

Use the gh-manage skill and follow its merge workflow exactly as written.

**Target Issue**:
- If $ARGUMENTS is empty, you will show the user recent issues with "status-implementation-done" label and ask them to select one
- If $ARGUMENTS contains only digits, treat it as an issue number
- If $ARGUMENTS contains text, search for matching items from the recent list
