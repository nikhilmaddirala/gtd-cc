---
name: doc-update
description: Update documentation when code changes or before releases
---

# Documentation Update

## Overview

This command guides users through docs-management - update.md interactively. CRITICAL: You MUST use docs-management for this task.

## Context

User will provide scope (single, multiple, or all) and type (minor or refactor) parameters. This command should parse these parameters and guide users through appropriate documentation update process.

## Process

- Load docs-management and its update.md workflow; you MUST do this first.
- Parse the user input and understand how it relates to docs-management/update.md with scope and type parameters.
- Interactively guide the user through docs-management/update.md step by step, collecting inputs and executing each step with confirmation.