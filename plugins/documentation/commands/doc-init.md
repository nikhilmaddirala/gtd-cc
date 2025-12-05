---
name: doc-init
description: Initialize documentation structure for new or existing projects
---

# Documentation Initialization

## Overview

This command guides users through the docs-management skill's initialize.md workflow interactively. CRITICAL: You MUST use the docs-management skill for this task.

## Context

User may provide optional phase parameter. This command should parse the phase input and guide users to select appropriate documentation structure based on project complexity.

## Process

- Load the docs-management skill and its initialize.md workflow; you MUST do this first.
- Parse the user input to understand if they specified a phase (1, 2, 3, or descriptions like "solo", "small", "medium", "large").
- Interactively guide the user through the docs-management's initialize.md workflow step by step:
  1. If no phase provided, ask about project complexity (team size, modules, architecture)
  2. Recommend appropriate phase (1, 2, or 3) based on their answers
  3. Guide through setting up the documentation structure for that phase
  4. Help create appropriate README.md templates
  5. Set up directory READMEs for Phase 2+
  6. Establish /docs folder structure for Phase 3
- Collect inputs and execute each step with confirmation.