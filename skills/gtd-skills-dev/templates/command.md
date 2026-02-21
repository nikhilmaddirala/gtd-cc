---
name: command-name
description: Brief description of what this command does
---

# [Command name]

## Overview

This command guides users through [skill-name] interactively. CRITICAL: You MUST use [skill-name] for this task.


## Context

If the user has provided any additional context, pass that into the skill invocation. Here is the context provided by the user: $ARGUMENTS


## Process

- Load [skill-name] (or its [sub-skill-name] sub-skill if targeting a specific procedure); you MUST do this first.
- Parse the user input and understand how it relates to the skill.
- Interactively guide the user through the skill step by step, collecting inputs and executing each step with confirmation.
