# Claude Code Configuration Guide

This directory contains Claude Code specific configuration files that guide Claude's behavior when working with this repository.

## Overview

The `.claude/` directory is the configuration layer for Claude Code. Files here control:
- How Claude understands the project
- What behaviors Claude should follow
- How Claude should interact with the codebase
- Development patterns and conventions

## Files in This Directory

### CLAUDE.md

The main configuration file for Claude's interaction with this project.

Location: `CLAUDE.md` (at root level, referenced from this directory)

Contains:
- Project overview and architecture
- Development task instructions
- File structure conventions
- Plugin-specific guidelines
- Error handling principles

Read this before: Starting any development work, creating new components, understanding how Claude should behave.

### Directory Structure

```
.claude/
├── README.md                This file
├── commands/                Custom slash commands
│   └── *.md                 Individual command definitions
├── agents/                  Custom agents
│   └── *.md                 Individual agent definitions
└── skills/                  Custom skills
    └── */SKILL.md          Skill documentation
```

## Custom Components

In addition to plugin components, projects can define custom components at the root level:

### Root-Level Commands

Custom commands defined in `.claude/commands/` are available project-wide:

```bash
/command-name
```

These commands complement plugin commands and provide project-specific workflows.

### Root-Level Agents

Custom agents in `.claude/agents/` perform autonomous work across the entire project:

```bash
Agent Name - Autonomous operations
```

### Root-Level Skills

Custom skills in `.claude/skills/` provide project-specific knowledge and expertise.

## Using This Configuration

### For Users

If you're using this project:
1. Read the main `CLAUDE.md` file for project guidelines
2. Check the plugin-specific README files for plugin guidance
3. Consult skills documentation for detailed procedures

### For Developers

If you're contributing to this project:
1. Follow the conventions outlined in `CLAUDE.md`
2. Review existing code structure and patterns
3. Ensure your contributions align with documented practices
4. Document new components in their respective directories

### For Claude (AI Assistant)

This configuration tells Claude:
- The project architecture and organization
- Naming conventions and file structure
- Common development patterns
- How to create new components
- Error handling and validation practices

## Key Principles

The `.claude/` directory is organized around these principles:

1. **Clear Configuration** - Project guidelines are explicit, not implicit
2. **Layered Information** - Basic guidance at root, detailed procedures in skills
3. **Convention Over Code** - Patterns documented in CLAUDE.md are enforced
4. **Extensibility** - Custom components can augment plugin components
5. **Consistency** - All components follow documented naming and structure conventions

## Updating Configuration

When the project's conventions change:

1. Update `CLAUDE.md` with the new guidance
2. Document the change in commit message
3. Optionally create new skills to guide Claude on the new process
4. Update plugin documentation if relevant

## Related Documentation

- [Main CLAUDE.md](../CLAUDE.md) - Project configuration
- [Plugins Guide](../plugins/README.md) - Plugin directory
- [Getting Started](../GETTING-STARTED.md) - User onboarding
- [Contributing Guide](../CONTRIBUTING.md) - Developer guidelines
- [Skill Documentation](../plugins/*/skills/*/SKILL.md) - Detailed procedures

## When to Consult This Directory

Use this directory when:
- You need to understand Claude's expected behavior
- You're implementing changes that affect how Claude should work
- You're creating new project-level commands or agents
- You need to reference project conventions and patterns
