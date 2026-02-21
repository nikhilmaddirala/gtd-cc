---
description: Validate that marketplace plugins or project-local skills follow gtd-cc patterns
---

# Validate existing plugin or project-local skill

## Process

- Determine target type (marketplace plugin or project-local skill)
- Follow the appropriate checklist below
- Generate validation report listing violations with specific fix recommendations

## Marketplace plugin checklist

- Run plugin-dev validation (directory structure, manifests, component registration)
- Check gtd-cc-specific patterns:
  - Commands/agents are thin wrappers (no inline logic, reference skills)
  - Skills have proper structure (Overview, Context, Process, Guidelines)
  - Naming follows plugin prefix conventions
  - Marketplace registration exists in `.claude-plugin/marketplace.json`

## Project-local skill checklist

Structure:
- SKILL.md exists with proper frontmatter (`name`, `description`)
- SKILL.md follows structure: Overview, Context, Sub-skills (if any), Process, Guidelines
- README.md exists with usage and setup documentation
- Sub-skills (if any) have `description` frontmatter
- Naming follows prefix conventions for related skills (e.g., `gh-tasks`, `gh-subtrees`)
- No orphaned sub-skills (every sub-skill is referenced in SKILL.md)

Content separation:
- README.md is for human developers only — does not duplicate content from SKILL.md or sub-skills
- SKILL.md Context section is delivery-agnostic (describes what inputs are needed, not where they come from like directories or upload mechanisms)
- Domain reference material (thresholds, interpretation rules, troubleshooting) lives in SKILL.md if needed by Claude, not duplicated in README
