---
name: gtd-cc-plugin-dev
description: Apply gtd-cc architectural patterns when developing Claude Code plugins. Use when creating or updating plugins for the gtd-cc marketplace.
---

# gtd-cc Plugin Development

## Overview

This skill applies gtd-cc architectural patterns to Claude Code plugin development. It wraps the official plugin-dev toolkit, which handles mechanics (creating files, manifests, validation). This skill adds the gtd-cc layer: thin wrappers, centralization, and marketplace conventions.

CRITICAL: You MUST use the official plugin-dev toolkit for plugin mechanics. This skill provides patterns and templates on top of plugin-dev.


## Context

User wants to create or update a plugin for the gtd-cc marketplace. They may have already used plugin-dev to create a base structure, or they may be starting fresh.


## Prerequisites

This skill requires the official plugin-dev skill to be installed. Before proceeding with any sub-skill:

1. Check if the plugin-dev skill is available (look for `plugin-dev:` prefixed skills in your available tools)
2. If plugin-dev is NOT available, stop and tell the user:
   ```
   This skill requires the official plugin-dev toolkit. Please install it first:
   /plugin install plugin-dev@claude-code-plugins

   Then retry your command.
   ```
3. Only proceed when plugin-dev is confirmed available


## Sub-skills

CRITICAL: Load the appropriate sub-skill from `sub-skills/` when routing is needed. Each sub-skill wraps the official plugin-dev skill (let plugin-dev handle its own internal routing).

- **create-new-plugin.md**: Create new gtd-cc marketplace plugin
- **create-new-skill.md**: Create skill with gtd-cc patterns
- **update-existing-plugin.md**: Add components to existing plugin
- **validate-existing-plugins.md**: Validate gtd-cc patterns
- **create-repo-plugin.md**: Create repository-specific `.claude/` automation


## Process

1. Determine what the user needs (new plugin, new skill, validation, etc.)
2. Load the appropriate sub-skill
3. Follow sub-skill process, which will invoke plugin-dev for mechanics and apply gtd-cc patterns


## Resources

- **templates/**: gtd-cc templates for skills, commands, agents, READMEs


## Guidelines

- Use plugin-dev for mechanics, this skill for patterns
- Commands and agents are thin wrappers - all logic lives in skills
- Apply templates from `templates/` directory
- Follow gtd-cc naming: plugin prefix pattern (gh-*, doc-*, ob-*)


## Appendix

### gtd-cc architecture

The core principle is centralization: all domain logic lives in skills. Commands and agents are thin wrappers that invoke skills with context.

```
Human → Command → Skill
Claude Code → Agent → Skill
                ↓
            Sub-skills (if needed)
```

Why this matters:
- Update logic once in skill, all commands/agents inherit changes
- Skills are testable and documentable
- Codebase is predictable - same pattern everywhere

### gtd-cc naming conventions

Plugin prefix pattern - all component names are prefixed with the plugin abbreviation:
- Plugin: `github` → Components: `gh-*`
- Plugin: `documentation` → Components: `doc-*`
- Plugin: `obsidian` → Components: `ob-*`

### gtd-cc marketplace registration

```bash
# Add plugin to marketplace manifest
jq --arg name "$PLUGIN_NAME" \
   --arg path "plugins/$PLUGIN_NAME" \
   '.plugins += [{name: $name, path: $path}]' \
   .claude-plugin/marketplace.json > tmp.json && mv tmp.json .claude-plugin/marketplace.json
```
