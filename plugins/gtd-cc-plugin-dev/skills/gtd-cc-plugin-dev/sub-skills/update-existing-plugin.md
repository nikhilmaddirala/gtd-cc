---
description: Add components to existing plugin by wrapping official plugin-dev skill and applying gtd-cc patterns
---

# Update existing plugin

## Overview

This sub-skill adds new components (commands, agents, skills) to an existing gtd-cc plugin. It wraps the official plugin-dev skill to assess current state and validate, then applies gtd-cc patterns to add components.

CRITICAL: You MUST use the official plugin-dev skill for validation and mechanics. Let plugin-dev handle its own internal routing.


## Context

User wants to add new components to an existing plugin. They specify what component type (command, agent, skill) and its purpose.


## Process

1. Validate current plugin state
   - Use the official plugin-dev skill to assess current structure
   - Identify what components already exist
   - Confirm plugin follows gtd-cc patterns

2. Gather new component specifications
   - Component type (command, agent, skill, sub-skill)
   - Name and purpose
   - Which skill it should reference (for commands/agents)

3. Create new component
   - Use appropriate template from `../templates/`
   - For commands: thin wrapper referencing skill
   - For agents: thin wrapper referencing skill
   - For skills: full skill structure with sub-skills if needed

4. Update plugin manifest
   - Add new component to plugin.json
   - Bump minor version number (e.g., 1.0.0 → 1.1.0) - required for plugin cache to refresh

5. Re-validate
   - Use the official plugin-dev skill to confirm updates are correct

6. Verification: Confirm new component follows gtd-cc thin wrapper pattern


## Guidelines

- Always validate before and after updates
- New commands/agents must be thin wrappers
- All logic belongs in skills, not commands/agents
- Use templates from `../templates/` directory
