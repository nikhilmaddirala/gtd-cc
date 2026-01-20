---
description: Create new gtd-cc marketplace plugin by wrapping official plugin-dev skill and applying gtd-cc patterns
---

# Create new plugin

## Overview

This sub-skill creates a new plugin for the gtd-cc marketplace. It wraps the official plugin-dev skill for mechanics and applies gtd-cc architectural patterns on top.

CRITICAL: You MUST use the official plugin-dev skill for the mechanical aspects of plugin creation. Let plugin-dev handle its own internal routing.


## Context

User provides plugin name, description, and functionality requirements. This sub-skill will guide them through plugin-dev creation then apply gtd-cc patterns.


## Process

1. Gather plugin specifications from user
   - Plugin name (kebab-case)
   - Brief description
   - Initial commands/agents needed

2. Invoke plugin-dev for mechanics
   - Use the official plugin-dev skill
   - Let plugin-dev handle directory structure, manifests, and its own routing

3. Apply gtd-cc patterns
   - Restructure commands as thin wrappers using `../templates/command.md`
   - Restructure agents as thin wrappers using `../templates/agent.md`
   - Ensure skills follow `../templates/skill.md` structure
   - Apply gtd-cc naming conventions (plugin prefix: gh-*, doc-*, etc.)

4. Register in gtd-cc marketplace
   - Add plugin to `.claude-plugin/marketplace.json`

5. Verification: Confirm plugin follows gtd-cc thin wrapper architecture


## Guidelines

- Let plugin-dev handle all file creation mechanics
- Focus on applying gtd-cc patterns after plugin-dev completes
- Use templates from `../templates/` directory
- Follow gtd-cc naming conventions
