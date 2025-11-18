---
description: Domain expertise for gtd-cc plugin marketplace operations
---

# gtd-cc-skill

Domain expertise for the gtd-cc plugin marketplace, providing comprehensive workflows for plugin lifecycle management including creation, updates, and validation.

## When to use this skill

Use this skill when you need to:
- Create new plugins in the gtd-cc marketplace
- Update existing plugins with new components or modifications
- Validate plugin structure, manifests, and documentation
- Ensure marketplace consistency across all plugins

## Available workflows

### update-existing-plugin
Add new components (commands/agents/skills) to existing plugins, update manifests, and maintain consistency.

**Use when**: You need to modify an existing plugin by adding new workflows, commands, agents, or skills.

### create-new-plugin
Complete plugin scaffolding with directory structure, manifests, initial components, and marketplace registration.

**Use when**: You need to create a brand new plugin from scratch in the gtd-cc marketplace.

### validate-existing-plugins
Comprehensive validation of all plugins: structure, manifests, documentation completeness, and marketplace consistency.

**Use when**: You need to check the health and correctness of existing plugins before releases or contributions.

## Integration with github-gtd

This skill complements the github-gtd workflows by providing plugin-specific context:
- Works with github-gtd issue creation to generate plugin-specific implementation plans
- Enhances github-gtd review workflows with plugin-specific validation checks
- Extends github-gtd release workflows with marketplace-specific publishing steps

## Success criteria

- All plugins follow consistent directory structure and naming conventions
- Plugin manifests are valid and properly reference all components
- Documentation is complete and cross-referenced correctly
- Marketplace configuration is synchronized with actual plugin files