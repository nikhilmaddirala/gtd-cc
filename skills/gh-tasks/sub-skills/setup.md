---
description: Bootstrap repo labels and configuration for the gh-tasks pipeline
---

# setup

## Overview

Ensure the current repository has the labels and configuration needed by the gh-tasks pipeline. Delegates to `scripts/setup-labels.sh` for the happy path, and handles edge cases (conflicting labels, partial failures, repos with existing label schemes) with AI reasoning.


## Process

1. Run the setup script to sync labels:
   ```bash
   # Preview what would change
   scripts/setup-labels.sh --dry-run

   # Apply changes
   scripts/setup-labels.sh
   ```

2. If the script reports errors, diagnose the issue:
   - **Permission errors**: user may not have write access to the repo
   - **Name conflicts**: repo may have existing labels that collide (e.g., a `blocked` label vs `status-blocked`)
   - **API rate limits**: back off and retry
   - **Partial failures**: re-run the script (it's idempotent)

3. For label conflicts, ask the user how to resolve:
   - Rename the existing label to match the gh-tasks schema
   - Keep both and adjust the gh-tasks label name
   - Delete the conflicting label (with confirmation)

4. Verify setup:
   ```bash
   gh label list --json name,color,description | jq '[.[] | select(.name | startswith("status-") or startswith("priority-") or startswith("size-"))]'
   ```

5. Report what was created/updated/skipped.


## Removing labels

To remove all gh-tasks labels from a repo:
```bash
scripts/setup-labels.sh --delete
```

Confirm with the user before running this, especially if issues already reference these labels.


## Guidelines

- Always run `--dry-run` first and show the user what will change
- The script is idempotent: safe to run multiple times
- Label colors and descriptions are updated if they drift from the schema
- Never delete labels without explicit user confirmation
- If the repo has an existing label scheme, discuss with the user before overwriting
