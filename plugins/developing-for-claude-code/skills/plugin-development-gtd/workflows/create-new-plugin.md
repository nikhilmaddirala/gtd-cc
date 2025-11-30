---
description: Create new plugin with proper structure and marketplace registration
---

# Create New Plugin Workflow

## Overview

This workflow creates a brand new plugin in the gtd-cc marketplace with complete directory structure, manifests, initial components, and marketplace registration. Commands and agents should reference this workflow directly and follow the process exactly as written.

## Context

User provides plugin specifications including name, description, and basic functionality requirements. This workflow validates the plugin name doesn't conflict with existing plugins and gathers necessary context before creation.

## Guidelines

Follow these general guidelines when executing this workflow:

- Always validate plugin names for uniqueness before creating directory structure
- Use absolute paths for all file operations to avoid ambiguity
- Validate all JSON manifests using `jq .` before proceeding
- Create backup copies of marketplace manifest before modification
- Test plugin discovery after registration to ensure proper integration
- Follow gtd-cc naming conventions (kebab-case for all components)
- **Use templates from `../templates/` directory** - don't duplicate template content in workflows

## Process

### 1. Gather plugin specifications

Collect plugin information from user:
- Plugin name (kebab-case)
- Brief description of plugin purpose
- Initial components needed (skill, command, agent)
- Basic functionality requirements

### 2. Create plugin structure using templates

Use templates from `../templates/` directory and directory structure patterns from `../references/common-patterns.md`:

- Follow "Standard Plugin Directory Structure" pattern
- Create plugin manifest using "Plugin Manifest Template"
- Generate initial components using templates (skill, command, agent)

### 3. Update marketplace registration

Use marketplace registration patterns from `../references/common-patterns.md`:
- Follow "Update Marketplace Manifest" pattern completely
- Backup existing marketplace manifest before modification
- Validate all JSON manifests using validation commands

### 4. Test plugin installation

Verify plugin can be discovered and installed:
- Use validation commands from `../references/common-patterns.md`
- Run `/plugin list` to verify discovery
- Test component installation if applicable
- Ensure all manifests are properly formatted

## Final Review

Verify that the plugin creation workflow completed successfully:

- [ ] Plugin directory structure created correctly with all required subdirectories
- [ ] Plugin manifest (.claude-plugin/plugin.json) is valid JSON with required fields
- [ ] Plugin README is comprehensive and accurately describes the plugin
- [ ] Plugin is registered in marketplace manifest with unique name
- [ ] Initial components (skill/command/agent) are created using templates
- [ ] Plugin can be discovered via `/plugin list` command
- [ ] All gtd-cc naming conventions are followed consistently
- [ ] Plugin follows the layered architecture pattern correctly