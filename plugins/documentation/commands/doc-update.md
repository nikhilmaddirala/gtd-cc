---
name: doc-update
description: Update documentation when code changes or before releases
---

# Documentation Update

## Overview

This command guides users through the docs-management skill's update.md workflow interactively. CRITICAL: You MUST use the docs-management skill for this task.

## Context

User may provide scope (single, multiple, or all) and type (minor or refactor) parameters. This command should parse these parameters and guide users through appropriate documentation update process.

## Process

- Load the docs-management skill and its update.md workflow; you MUST do this first.
- Parse the user input to understand scope and type parameters:
  - scope: single (individual documents), multiple (across layers), or all (entire documentation)
  - type: minor (references and key info) or refactor (restructure content)
- Interactively guide the user through the docs-management's update.md workflow step by step:
  1. If no parameters provided, ask about the update scope and type needed
  2. Identify which documentation layers need updating
  3. Guide through updating individual documents (scope=single) or multiple layers (scope=multiple/all)
  4. Help with minor updates (type=minor) or major restructuring (type=refactor)
  5. Ensure consistency across documentation layers
  6. Verify all links and references remain valid
- Collect inputs and execute each step with confirmation.