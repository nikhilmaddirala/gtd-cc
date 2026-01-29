---
description: Refactor existing plugin to follow gtd-cc patterns while preserving functionality
---

# Refactor existing plugin

## Process

- **Create refactoring plan**
  - For each command/agent with inline logic: identify which skill to create or reference
  - For skills missing structure: note which sections to add
  - Present plan to user for approval before making changes
- **Execute refactoring**
  - Extract inline logic from commands/agents into skills
  - Convert commands/agents to thin wrappers per `templates/command.md` and `templates/agent.md`
  - Apply naming conventions per the appendix in SKILL.md
  - Update plugin.json with any new/renamed components

## Guidelines

- Preserve all original functionality - refactoring changes structure, not behavior
- Create skills before converting commands/agents to thin wrappers
- Get user approval before destructive changes
- Complete each component conversion fully before moving to next
