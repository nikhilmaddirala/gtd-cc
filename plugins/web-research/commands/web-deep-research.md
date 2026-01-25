---
name: web-deep-research
description: Perform comprehensive multi-step research on a complex topic, breaking it into subtopics, searching iteratively, and producing a cited report.
---

# Deep research

## Overview

This command guides users through deep-research interactively. CRITICAL: You MUST use deep-research skill for this task.


## Context

If the user has provided any additional context, pass that into the skill invocation. Here is the context provided by the user: $ARGUMENTS


## Process

- Load deep-research skill; you MUST do this first.
- Parse the user input and understand how it relates to the skill.
- Interactively guide the user through the skill step by step, collecting inputs and executing each step with confirmation.
- For the research planning step, present the proposed subtopics to the user for approval before executing searches.
