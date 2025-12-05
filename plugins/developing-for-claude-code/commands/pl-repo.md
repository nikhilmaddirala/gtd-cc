---
name: pl-repo
description: Create repository-specific .claude/ automation following gtd-cc patterns
---

# Create repository plugin

## Overview

This command guides you through creating repository-specific `.claude/` automation that follows gtd-cc architectural patterns and integrates with existing repository workflows. CRITICAL: You MUST use the plugin-development-gtd skill for this task.

## Context

User will provide repository type, automation scope, and workflow patterns. The command validates repository structure and ensures proper integration with existing development workflows without requiring full plugin installation.

## Process

Load plugin-development-gtd skill first. Interactively guide the user through this skill and create-repo-plugin workflow step by step, collecting inputs and executing each step with confirmation.