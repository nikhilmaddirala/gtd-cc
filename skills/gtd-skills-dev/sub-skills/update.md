---
description: Add components to an existing marketplace plugin or project-local skill
---

# Update existing plugin or project-local skill

## Process

- Determine target type (marketplace plugin or project-local skill)
- Gather new component specifications:
  - Component type and purpose
  - For plugins: command, agent, skill, or sub-skill; which skill it should reference (for commands/agents)
  - For project-local skills: sub-skill, template, script, or reference
- Follow the appropriate workflow below

## Marketplace plugin

- Use plugin-dev to assess current plugin structure and confirm it follows gtd-cc patterns
- Create the component using the appropriate template from `templates/`
  - Commands/agents: thin wrappers referencing a skill
  - Skills: full structure with sub-skills if needed; ensure SKILL.md has Overview, Context, Process, Guidelines sections
- Update plugin.json with new component
- Re-validate with plugin-dev

## Project-local skill

- Assess current skill structure (SKILL.md, sub-skills/, README.md)
- Add the new component:
  - Sub-skill: create markdown file in `sub-skills/` with description frontmatter
  - Template/script/reference: add to the appropriate directory
- Update SKILL.md to reference the new component (sub-skills list, resources section)
- Update README.md if the new component changes usage or setup
- No plugin-dev invocation needed
