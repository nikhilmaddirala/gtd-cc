---
name: doc-init
description: Initialize documentation structure for new or existing projects
---

# doc-init

## Overview

This command guides users through docs-management interactively. CRITICAL: You MUST use docs-management for this task.


## Context

If the user has provided any additional context, pass that into the skill invocation. Here is the context provided by the user: $ARGUMENTS


## Process

- Load docs-management (or its initialize.md sub-skill if targeting a specific procedure); you MUST do this first.
- Parse the user input and understand how it relates to the skill.
- Interactively guide the user through the skill step by step, collecting inputs and executing each step with confirmation.
