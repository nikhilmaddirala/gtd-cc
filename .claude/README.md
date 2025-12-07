# Claude Code Configuration Guide

This directory contains Claude Code's configuration and custom components for the gtd-cc project.

## Files

- **CLAUDE.md** - Main project configuration that tells Claude how to behave when working with this project
- **skills/** - Custom project-specific skills (currently none)

## Configuration Details

The `CLAUDE.md` file configures:

- Project overview and plugin architecture
- File naming conventions
- Common development tasks and workflows
- Error handling guidelines
- Plugin installation and management commands

## Usage

Claude Code automatically reads `CLAUDE.md` to understand:
- This is a plugin marketplace with 4 main plugins
- How to validate JSON manifests
- The three-layer architecture (skills, commands, agents)
- Where to find different components

## Adding Custom Components

To add project-specific skills:

1. Create directory: `.claude/skills/your-skill-name/`
2. Add comprehensive `SKILL.md` with domain expertise
3. Skill will be automatically available to Claude

Note: Most functionality should be in the `plugins/` directory. This directory is for project-specific configuration only.