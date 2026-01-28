---
name: random-secrets
description: Manage secrets with 1Password CLI, Infisical, and other tools for development and automation workflows
---

# Secrets management

## Overview

This command guides users through secrets management using 1Password CLI or Infisical. CRITICAL: You MUST use the secrets-management skill for this task.


## Context

If the user has provided any additional context, pass that into the skill invocation. Here is the context provided by the user: $ARGUMENTS


## Process

- Load the secrets-management skill; you MUST do this first.
- Parse the user input and understand what secrets operation is needed (1Password op read/run/inject, Infisical project setup, machine identity creation, runtime fetching).
- Interactively guide the user through the appropriate secrets management workflows.
