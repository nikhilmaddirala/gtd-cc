---
name: plugin-development-gtd
description: Guide for developing Claude Code plugins following gtd-cc architectural patterns with skills, workflows, commands, and agents.
---

# Plugin Development Skill

## Overview

This skill provides expertise for developing Claude Code plugins following the gtd-cc architectural patterns. This skill should be used when creating new plugins, updating existing ones, or setting up repository-specific automation. Commands and agents should reference specific workflows from the `workflows/` directory and follow the detailed procedures exactly as written.

## Workflows

Use the appropriate workflow from the `workflows/` directory:

- **create-new-plugin.md**: For building new gtd-cc marketplace plugins from scratch
- **update-existing-plugin.md**: For adding components to existing gtd-cc plugins
- **validate-existing-plugins.md**: For checking plugin health before releases or contributions
- **create-repo-plugin.md**: For creating repository-specific `.claude/` automation

## Resources

- **templates/**: Contains template files for skills, commands, agents, workflows, and READMEs
- **references/**: Contains gtd-cc architectural patterns and conventions

## Guidelines

Follow these general guidelines when executing any workflow in this skill:

- **Always validate JSON manifests** before modification using `jq .` or similar validation tools
- **Use absolute paths** for all file operations to avoid ambiguity
- **Maintain git hygiene** - keep working directories clean and use conventional commit messages
- **Provide clear error messages** with actionable next steps when operations fail
- **Backup before modification** - create copies of files before making significant changes
- **Test locally** before publishing or submitting changes to validate functionality
- **Use templates instead of duplicating content** - when writing detailed code or templates in workflows, reference the files in `templates/` directory instead of embedding content directly

## Additional Information

This section can contain any additional domain-specific information needed for the skill, such as:
- Domain concepts and terminology
- Integration patterns with other plugins
- Best practices and conventions
- Architecture patterns
- Troubleshooting guidance
- Examples and use cases

### gtd-cc Architecture Pattern

All plugins in this marketplace follow a layered architecture:

**Skills - Foundation Layer**
- Central SKILL.md describes the domain and lists workflows
- Individual workflow files in workflows/ subdirectory contain detailed procedures
- Single source of truth for all domain expertise

**Commands - Interactive Wrappers**
- Thin wrappers (3-6 lines) that reference specific skill workflows
- No inline logic - just pointers to workflows
- Example: "Use the <skill-name> and follow its <workflow-name> exactly as written"

**Agents - Autonomous Executors**
- Configuration plus instructions to execute workflows autonomously
- Maintain context across multi-step processes
- Delegate all procedures to skill workflows

**Key Principles**
- **Single Source of Truth**: Skills contain all logic in workflow files
- **Layered Architecture**: Skills → Commands → Agents for clear separation
- **Maintainability**: Update workflow once, affects all commands/agents using it
- **Consistency**: All plugins follow the same pattern, making the codebase predictable

### gtd-cc Naming Conventions

**File Naming Patterns**
- **Plugins**: kebab-case (e.g., `create-new-plugin`, `doc-audit`, `pl-create`)
- **Agents**: kebab-case with descriptive suffix (e.g., `gtd-github-agent`, `build-test-deploy-agent`)
- **Skills**: kebab-case directories with uppercase `SKILL.md` files (e.g., `plugin-development`)
- **Workflows**: kebab-case with `.md` extension (e.g., `create-new-plugin`, `validate-existing-plugins`)
- **Commands**: kebab-case with `.md` extension, typically prefixed by plugin (e.g., `gh-issue`, `doc-init`)

**Component Structure Standards**
- **Plugin directories**: `plugins/<plugin-name>/`
- **Skill directories**: `plugins/<plugin-name>/skills/<skill-name>/`
- **Command files**: `plugins/<plugin-name>/commands/<command-name>.md`
- **Agent files**: `plugins/<plugin-name>/agents/<agent-name>.md`
- **Workflow files**: `plugins/<plugin-name>/skills/<skill-name>/workflows/<workflow-name>.md`

**Path Registration in Manifests**
All paths in plugin manifests should be relative to plugin root with `./` prefix:
- Commands: `./commands/command-name.md`
- Agents: `./agents/agent-name.md`
- Skills: `./skills/skill-name` (reference the directory, not SKILL.md file)

**Manifest Structure Requirements**
Each plugin must have a `.claude-plugin/plugin.json` with:
- `name`: Plugin name (kebab-case)
- `version`: Semantic version (e.g., "1.0.0")
- `description`: Brief description of plugin purpose
- `author`: Author object with name field
- `commands`: Array of command file paths (e.g., `"./commands/command-name.md"`)
- `agents`: Array of agent file paths (e.g., `"./agents/agent-name.md"`)
- `skills`: Array of skill directory paths (e.g., `"./skills/skill-name"`)

### Component Naming Relationships

Components within a plugin should have consistent naming relationships:

**Plugin Prefix Pattern**: All component names are prefixed with the plugin name
- Plugin: `github` → Components: `gh-*`
- Plugin: `documentation` → Components: `doc-*`
- Plugin: `obsidian` → Components: `ob-*`
- Plugin: `web-research` → Components: `wr-*`

**Example: GitHub Plugin**
```
Plugin: github
Skill: github-gtd
Workflows: gh-build, gh-plan, gh-manage, gh-merge, gh-review
Commands: gh-build, gh-plan, gh-manage, gh-merge, gh-review
Agents: gh-build-agent, gh-plan-agent, gh-manage-agent, gh-merge-agent, gh-review-agent
```

**Example: Documentation Plugin**
```
Plugin: documentation
Skill: doc-standards
Workflows: doc-init, doc-update, doc-audit, doc-compress
Commands: doc-init, doc-update, doc-audit, doc-compress
Agents: doc-init-agent, doc-update-agent, doc-audit-agent, doc-compress-agent
```