---
description: Add new components or update existing plugin structure
---

# Update Existing Plugin Workflow

## Overview

This workflow updates an existing plugin in the gtd-cc marketplace by adding new components (commands, agents, skills), modifying existing ones, or updating plugin configuration. Commands and agents should reference this workflow directly and follow the process exactly as written.

## Context

User provides the target plugin name and details about what needs to be updated (new components, modifications, configuration changes). This workflow validates the plugin exists and analyzes current structure before making changes.

## Guidelines

Follow these general guidelines when executing this workflow:

- Always backup plugin manifests and configuration before modification
- Use absolute paths for all file operations to avoid ambiguity
- Validate all JSON manifests using `jq .` before proceeding
- Test component functionality after updates
- Follow gtd-cc naming conventions (kebab-case for all components)
- **Use templates from `../templates/` directory** - don't duplicate template content in workflows
- **Reference common patterns from `../references/common-patterns.md`** for registration and validation

## Process

### 1. Identify and validate target plugin

- List available plugins using plugin discovery
- Select target plugin for update
- Validate plugin directory exists and is accessible
- Confirm user has necessary permissions for modification

### 2. Analyze current plugin structure

- Examine existing plugin structure using discovery commands
- Review current plugin manifest for component registration
- Identify gaps or areas needing updates
- Document current state before making changes

### 3. Add or update components using templates

Use templates from `../templates/` directory:
- Copy appropriate templates for new components (skill, command, agent)
- Customize template content for plugin-specific needs
- Follow naming conventions from `../references/common-patterns.md`
- Create any required subdirectories for component organization

### 4. Update plugin manifest registration

Use component registration patterns from `../references/common-patterns.md`:
- Follow "Register Component in Plugin Manifest" pattern completely
- Update manifest with new component paths and metadata
- Validate all JSON manifests using validation commands
- Ensure all paths are relative to plugin root

### 5. Test updated plugin functionality

Verify all updates work correctly:
- Use validation commands from `../references/common-patterns.md`
- Test new commands if added
- Validate agent functionality if added
- Check skill discovery for new skills
- Run `/plugin list` to verify plugin integrity

## Final Review

Verify that the plugin update workflow completed successfully:

- [ ] Target plugin exists and is valid
- [ ] Plugin structure analyzed and understood
- [ ] New components created using appropriate templates
- [ ] Plugin manifest updated correctly with new components
- [ ] All JSON manifests validate successfully
- [ ] Updated functionality works as expected
- [ ] Plugin maintains gtd-cc architectural patterns
- [ ] All naming conventions are followed consistently