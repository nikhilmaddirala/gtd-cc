---
description: Reviews AI-generated implementation plans and provides approval or feedback
---

Use the gh-manage skill and follow its approval workflow exactly as written.

**Target Issue**:
- If $ARGUMENTS is empty, you will show the user recent issues with "status-planning-review" label and ask them to select one
- If $ARGUMENTS contains only digits, treat it as an issue number
- If $ARGUMENTS contains text, search for matching issues from the recent list
