# [Skill name]

## Overview
- Bullet: Problem it solves
- Bullet: Key capability

## Usage

[Describe the skill to Claude or reference it by name. No installation needed.]

### Sub-skills
- **[sub-skill-name]**: [what it does and when to use it]

### Configuration
[Environment variables, external tools, or setup steps required]

## Directory map
```
.claude/skills/[name]/
├── SKILL.md          # Coordinator (Claude reads this)
├── README.md         # This file (humans read this)
├── sub-skills/       # Workflow implementations
├── templates/        # Output format templates (optional)
├── scripts/          # Executable tools (optional)
└── references/       # Deep-dive docs (optional)
```

## Appendix

[Optional. Keep minimal — this file is for human developers, not the AI agent.]

IMPORTANT: Do not duplicate content from SKILL.md or sub-skills here. If information is needed by Claude to execute the skill, it belongs in SKILL.md. The README covers only: what this skill does, how to set it up, how to extend it, and what's planned next.
