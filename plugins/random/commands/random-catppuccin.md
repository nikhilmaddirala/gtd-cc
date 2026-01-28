---
name: random-catppuccin
description: Agent skill for creating and validating Catppuccin theme ports
---

# Catppuccin port creation

## Overview

This command guides users through creating Catppuccin theme ports. CRITICAL: You MUST use the catppuccin-port-creation skill for this task.


## Context

If the user has provided any additional context, pass that into the skill invocation. Here is the context provided by the user: $ARGUMENTS


## Process

- Load the catppuccin-port-creation skill; you MUST do this first.
- Parse the user input and identify the target application for theming.
- Interactively guide the user through the port creation workflow: target analysis, theme generation, validation, and submission preparation.
