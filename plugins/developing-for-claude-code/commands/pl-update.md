---
name: pl-update
description: Add new components or update existing plugin structure
---

# Update existing plugin

## Overview

This command guides you through adding new components (commands, agents, workflows) or updating existing structure in an established Claude Code plugin. It ensures all additions follow gtd-cc architectural patterns and are properly registered.

## Context

You provide:
- Plugin name (must be an existing plugin)
- Component type to add (command, agent, workflow, or skill)
- Component name and description
- Any workflow dependencies

The command validates the plugin structure and ensures manifest consistency.

## Process

Follow the plugin-development-gtd skill and execute the update-existing-plugin workflow exactly as written. The workflow will:

- Validate plugin exists and has proper structure
- Determine component type and requirements
- Create new component files using templates
- Update plugin manifest registration
- Validate manifest syntax and completeness
- Test the new component locally
