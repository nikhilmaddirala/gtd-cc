---
description: Create new gtd-cc marketplace plugin or project-local skill
---

# Create new plugin or project-local skill

## Process

- Gather specifications from user (name in kebab-case, description)
- Determine target:
  - **Marketplace plugin**: full plugin with commands, skills, agents; target is `plugins/<name>/` directory; register in `.claude-plugin/marketplace.json` after creation
  - **Project-local skill**: lightweight skill in the repo's `.claude/skills/<name>/` directory; no plugin.json, no commands, no marketplace registration
- Follow the appropriate workflow below

## Marketplace plugin

- Invoke plugin-dev to create the plugin structure at `plugins/<name>/`
- Apply gtd-cc patterns per the "Applying gtd-cc patterns to components" appendix in SKILL.md
- Register in `.claude-plugin/marketplace.json`
- Verify plugin follows gtd-cc thin wrapper architecture

## Project-local skill

A project-local skill is a lightweight alternative to a full plugin. It lives directly in `.claude/skills/<name>/` and is auto-discovered by Claude Code without any installation step.

### Structure

```
.claude/skills/<name>/
├── SKILL.md          # Coordinator (required) - uses templates/SKILL.md pattern
├── README.md         # User guide
├── sub-skills/       # Specific workflows (if needed)
│   ├── workflow-a.md
│   └── workflow-b.md
├── templates/        # Output format templates (optional)
├── scripts/          # Executable tools (optional)
└── references/       # Deep-dive docs (optional)
```

### Namespacing conventions

Project-local skills live in a flat directory. Use these conventions to keep them organized:

- **Prefix grouping**: use kebab-case prefixes for loosely related skills that have independent triggers (e.g., `gh-tasks`, `gh-subtrees` share the `gh-` prefix but have separate descriptions and use cases)
- **Sub-skill consolidation**: for tightly coupled workflows that share context, consolidate into one skill with sub-skill routing (e.g., one `media` skill with sub-skills for sonarr, radarr rather than separate top-level skills)
- **When to choose which**: if each skill has a distinct trigger and description, use prefixes; if the skills share a natural router and overlap in context, consolidate

### Process

- Create the skill directory at `.claude/skills/<name>/`
- Create SKILL.md following the `templates/SKILL.md` structure (Overview, Context, Sub-skills, Process, Guidelines)
- Create README.md with user guide and setup instructions
- Add sub-skills if the skill has multiple workflows
- No plugin-dev invocation needed (no plugin.json, no commands layer)
