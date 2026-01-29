---
description: Add components (commands, agents, skills, sub-skills) to an existing plugin with gtd-cc patterns
---

# Update existing plugin

## Process

- Use plugin-dev to assess current plugin structure and confirm it follows gtd-cc patterns
- Gather new component specifications:
  - Component type (command, agent, skill, sub-skill)
  - Name and purpose
  - Which skill it should reference (for commands/agents)
- Create the component using the appropriate template from `templates/`
  - Commands/agents: thin wrappers referencing a skill
  - Skills: full structure with sub-skills if needed; ensure SKILL.md has Overview, Context, Process, Guidelines sections
- Update plugin.json with new component
- Re-validate with plugin-dev
