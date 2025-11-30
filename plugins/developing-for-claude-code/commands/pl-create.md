---
name: pl-create
description: Create new plugin with proper structure and marketplace registration
---

# Create new plugin

## Overview

This command guides you through creating a new Claude Code plugin with proper architectural structure, marketplace registration, and all required components (skills, commands, agents, workflows).

## Context

You provide:
- Plugin name and description
- Plugin type and purpose
- Initial components to include (skills, commands, agents)

The command validates plugin naming conventions and ensures the plugin follows gtd-cc architectural patterns.

## Process

Follow the plugin-development-gtd skill and execute the create-new-plugin workflow exactly as written. The workflow will:

- Validate plugin name and structure
- Create plugin directories with proper hierarchy
- Initialize plugin manifest
- Create initial skill with workflows
- Register commands and agents
- Validate all components
- Test locally
