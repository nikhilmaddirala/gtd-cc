# gtd-cc Plugin Development

## Overview

- Applies gtd-cc architectural patterns to Claude Code plugin development
- Wraps the official plugin-dev plugin, adding thin wrapper philosophy and centralization
- Provides templates for skills, commands, agents, and READMEs


## User guide

### Quick start

```bash
# Install official plugin-dev first
/plugin install plugin-dev@claude-code-marketplace

# Install this plugin
/plugin install gtd-cc-plugin-dev@gtd-cc
```

### Configuration

Requires the official plugin-dev plugin to be installed. This plugin wraps plugin-dev for mechanics and adds gtd-cc patterns on top.

### Usage

Use the gtd-pl-* commands to create plugins with gtd-cc patterns:

```bash
# Create a new marketplace plugin or project-local skill
/gtd-pl-create

# Add components (commands, agents, skills) to existing plugin
/gtd-pl-update

# Validate plugins follow gtd-cc patterns
/gtd-pl-validate

# Refactor existing plugin to follow gtd-cc patterns
/gtd-pl-refactor
```


## Developer guide

### Directory map

```
gtd-cc-plugin-dev/
├── .claude-plugin/plugin.json
├── commands/
│   ├── gtd-pl-create.md
│   ├── gtd-pl-update.md
│   ├── gtd-pl-validate.md
│   └── gtd-pl-refactor.md
├── skills/
│   └── gtd-cc-plugin-dev/
│       ├── SKILL.md                # Main skill (common patterns, routes to sub-skills)
│       ├── sub-skills/
│       │   ├── create.md           # New marketplace plugin or project-local skill
│       │   ├── update.md           # Add components to existing plugin
│       │   ├── validate.md         # Validate gtd-cc patterns
│       │   └── refactor.md         # Refactor plugin to gtd-cc patterns
│       └── templates/              # gtd-cc templates
└── README.md
```

### Contributing

- **Templates:** Improve gtd-cc templates
- **Sub-skills:** Better plugin-dev wrapping
- **Documentation:** README and skill improvements


## Roadmap

- [x] Simplify to thin wrapper around plugin-dev
- [x] Unified skill template (merged skill + sub-skill)
- [x] Update command/agent templates
- [x] Rewrite sub-skills as thin wrappers
- [x] Update main plugin README (this file)
- [x] Rename to gtd-cc-plugin-dev to avoid confusion with official plugin-dev
- [x] Add prerequisite check for plugin-dev availability
- [x] Consolidate sub-skills and commands (6 → 4)
- [ ] Migrate to official plugin dependencies when [Issue #9444](https://github.com/anthropics/claude-code/issues/9444) is implemented


## References

- [Claude Code plugins documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Plugin dependencies feature request](https://github.com/anthropics/claude-code/issues/9444) - tracking official dependency support


## Appendix

### gtd-cc philosophy

This plugin follows its own philosophy: be a thin wrapper. All plugin development mechanics are handled by the official plugin-dev plugin. This plugin adds:

- **Thin wrapper pattern**: Commands and agents reference skills, no inline logic
- **Centralization**: All domain logic lives in skills
- **Templates**: gtd-cc-specific templates showing the patterns
- **Marketplace registration**: gtd-cc marketplace conventions
