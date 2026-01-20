---
description: Create skill with gtd-cc patterns by wrapping official plugin-dev skill
---

# Create new skill

## Overview

This sub-skill creates a new skill within an existing plugin. It wraps the official plugin-dev skill for mechanics and applies gtd-cc patterns on top.

CRITICAL: You MUST use the official plugin-dev skill for the mechanical aspects of skill creation. Let plugin-dev handle its own internal routing.


## Context

User wants to add a new skill to an existing plugin. They provide the skill name, domain expertise, and sub-skills needed.


## Process

1. Gather skill specifications from user
   - Skill name (kebab-case)
   - Domain expertise description
   - Sub-skills needed (if any)

2. Invoke plugin-dev for mechanics
   - Use the official plugin-dev skill
   - Let plugin-dev handle directory structure, SKILL.md creation, and its own routing

3. Apply gtd-cc patterns
   - Ensure SKILL.md follows `../templates/skill.md` structure
   - Add Context, Process, Guidelines sections
   - Add Appendix for domain-specific information if needed
   - Create sub-skills as thin procedural units

4. Verification: Confirm skill follows gtd-cc structure with proper routing to sub-skills


## Guidelines

- Let plugin-dev handle directory and file creation
- Focus on applying gtd-cc skill structure after plugin-dev completes
- Skills should route to sub-skills for complex procedures
- Use templates from `../templates/` directory
