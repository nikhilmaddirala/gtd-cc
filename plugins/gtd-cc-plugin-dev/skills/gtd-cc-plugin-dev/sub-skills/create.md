---
description: Create new gtd-cc marketplace plugin or repository-specific .claude/ automation
---

# Create new plugin

## Process

- Gather plugin specifications from user (name in kebab-case, description, initial commands/agents)
- Determine target:
  - **Marketplace plugin**: target is `plugins/<name>/` directory; register in `.claude-plugin/marketplace.json` after creation
  - **Repo plugin**: target is the repo's `.claude/` directory; no marketplace registration needed
- Invoke plugin-dev to create the plugin structure at the target location
- Apply gtd-cc patterns per the "Applying gtd-cc patterns to components" appendix in SKILL.md
- Verify plugin follows gtd-cc thin wrapper architecture
