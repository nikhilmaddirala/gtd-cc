---
description: Refactor existing marketplace plugin or project-local skill to follow gtd-cc patterns
---

# Refactor to gtd-cc patterns

## Process

- Determine target type (marketplace plugin or project-local skill)
- Create refactoring plan and present to user for approval before making changes
- Follow the appropriate workflow below

## Marketplace plugin

- For each command/agent with inline logic: identify which skill to create or reference
- For skills missing structure: note which sections to add
- Extract inline logic from commands/agents into skills
- Convert commands/agents to thin wrappers per `templates/command.md` and `templates/agent.md`
- Apply naming conventions per the appendix in SKILL.md
- Update plugin.json with any new/renamed components

## Project-local skill

- For monolithic SKILL.md files: identify workflows that should become sub-skills
- Break out sub-skills into `sub-skills/` directory with description frontmatter
- Restructure SKILL.md as a coordinator that routes to sub-skills
- Ensure SKILL.md follows template structure (Overview, Context, Sub-skills, Process, Guidelines)
- Add README.md if missing
- Apply naming conventions (prefix grouping for related skills)

## Guidelines

- Preserve all original functionality - refactoring changes structure, not behavior
- Get user approval before destructive changes
- Complete each component conversion fully before moving to next
