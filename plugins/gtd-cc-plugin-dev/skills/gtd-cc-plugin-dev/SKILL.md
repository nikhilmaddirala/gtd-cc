---
name: gtd-cc-plugin-dev
description: Apply gtd-cc architectural patterns when developing Claude Code plugins. Use when creating or updating plugins for the gtd-cc marketplace.
---

# gtd-cc plugin development

## Overview

This skill applies gtd-cc architectural patterns to Claude Code plugin development. It wraps the official plugin-dev plugin, which handles mechanics (creating files, manifests, validation). This skill adds the gtd-cc layer: thin wrappers, centralization, and marketplace conventions.


## Context

User wants to create or update a plugin for the gtd-cc marketplace. They may have already used plugin-dev to create a base structure, or they may be starting fresh.


## Prerequisites

This skill requires the official plugin-dev plugin to be installed. Before proceeding with any sub-skill:

- Check if plugin-dev is enabled via `claude plugin list`
- If plugin-dev is NOT available, stop and tell the user:
  ```
  This skill requires the official plugin-dev toolkit. Please install it first:
  claude plugin install plugin-dev@claude-plugins-official

  Then retry your command.
  ```
- Only proceed when plugin-dev is confirmed available



## Sub-skills

Load the appropriate sub-skill from `sub-skills/` when routing is needed.

- **create.md**: Create new plugin (marketplace or repo-local)
- **update.md**: Add components or skills to existing plugin
- **validate.md**: Validate plugins follow gtd-cc patterns
- **refactor.md**: Refactor plugin to follow gtd-cc patterns


## Process

- Determine what the user needs (new plugin, new component, validation, refactoring)
- Load the appropriate sub-skill
- Follow sub-skill process, which invokes plugin-dev for mechanics and applies gtd-cc patterns


## CRITICAL Guidelines

- Always use the official plugin-dev skill for plugin mechanics (file creation, manifests, validation, directory structure). Let plugin-dev handle its own internal routing. This skill only adds gtd-cc patterns on top.
- Always run the validate sub-skill after create, update, or refactor operations. Validate can also be invoked standalone.
- For any plugin changes, bump minor version in plugin.json (e.g., 1.0.0 → 1.1.0) - required for plugin cache to refresh
- Keep each skill file as short as possible focusing only on what is essential. No boilerplate or common knowledge.


## Resources

- **templates/**: gtd-cc templates for skills, commands, agents, READMEs


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

### Applying gtd-cc patterns to components

After plugin-dev creates the mechanical structure, apply these patterns:
- Restructure commands as thin wrappers using `templates/command.md`
- Restructure agents as thin wrappers using `templates/agent.md`
- Ensure skills follow `templates/SKILL.md` structure
- Apply naming conventions: plugin prefix pattern (e.g., `github` → `gh-*`, `documentation` → `doc-*`)

### gtd-cc marketplace registration

```bash
jq --arg name "$PLUGIN_NAME" \
   --arg path "plugins/$PLUGIN_NAME" \
   '.plugins += [{name: $name, path: $path}]' \
   .claude-plugin/marketplace.json > tmp.json && mv tmp.json .claude-plugin/marketplace.json
```
