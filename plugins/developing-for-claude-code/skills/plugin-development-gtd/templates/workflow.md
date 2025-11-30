---
description: TLDR description of workflow and when to use it.
---

# Workflow name

## Overview

This workflow accomplishes [specific goal] and should be used when [specific conditions or use cases]. Commands and agents should reference this workflow directly and follow the process exactly as written.


## Context

- This section describes the context and prerequisites needed to run this workflow and how this context will be provided.
- Example: User will provide plugin name and feature description; workflow will validate plugin.json exists and has required structure.


## Process

- This section describes the process that needs to be followed by this workflow in a clear and structured manner.
- Example: Step 1: Validate plugin structure and manifest; Step 2: Create component files; Step 3: Update plugin.json registration; Step 4: Test locally.


## Guidelines

- This section describes general guidelines that need to be followed when executing this workflow.
- Example: Always validate JSON manifests before modification; use absolute paths; preserve git hygiene; provide clear error messages.


## Final review 

- This section describes the final review that must be performed at the end of the workflow to verify that everything is completed and the desired end state has been achieved.
- Example: Verify plugin.json is valid; all required files created; component properly registered; local test succeeds.
