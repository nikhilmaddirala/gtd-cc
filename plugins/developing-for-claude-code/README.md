# Developing for Claude Code Plugin

This plugin provides guidance for developing Claude Code plugins following the gtd-cc repository's architectural patterns.

## What This Plugin Provides

A single comprehensive skill that teaches the gtd-cc plugin development pattern:
- Central skills with workflow files containing all domain expertise
- Thin wrapper commands (1-2 lines) that reference skill workflows
- Thin wrapper agents that execute workflows autonomously

## Installation

```bash
/plugin marketplace add nikhilmaddirala/gtd-cc
/plugin install developing-for-claude-code@gtd-cc
```

## Usage

Simply ask Claude about developing plugins following gtd-cc patterns:

- "How do I create a new plugin following gtd-cc patterns?"
- "Explain the thin wrapper pattern for commands"
- "Show me how to structure a skill with workflows"
- "Help me build a plugin that follows gtd-cc conventions"

The skill will automatically be invoked and provide guidance.

## The gtd-cc Pattern

All plugins in this marketplace follow a layered architecture:

**Skills** - Foundation layer
- Central SKILL.md describing the domain
- Individual workflow files with step-by-step procedures
- Single source of truth for all logic

**Commands** - Thin wrappers (1-2 lines)
- Reference specific skill workflows
- No inline logic

**Agents** - Autonomous executors
- Follow skill workflows without human interaction
- Thin wrappers with configuration

## Components

### Skills

- **plugin-development-gtd** - Complete guide for developing Claude Code plugins using gtd-cc patterns

## Examples

Study these plugins to see the pattern in action:

- `plugins/github/` - Complex multi-workflow plugin
- `plugins/documentation/` - Simpler structure
- `plugins/developing-for-claude-code/` - This plugin (meta!)

## Key Benefits

- **Maintainability** - All logic centralized in skills
- **Reusability** - Multiple components reference same workflows
- **Clarity** - Clear separation of concerns
- **Consistency** - All plugins follow same pattern
