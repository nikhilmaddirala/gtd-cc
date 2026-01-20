# gtd-cc Plugin Development

## Overview

- Applies gtd-cc architectural patterns to Claude Code plugin development
- Wraps the official plugin-dev skill, adding thin wrapper philosophy and centralization
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

Requires the official plugin-dev skill to be installed. This plugin wraps plugin-dev for mechanics and adds gtd-cc patterns on top.

### Usage

Use the gtd-pl-* commands to create plugins with gtd-cc patterns:

```bash
# Create a new plugin
/gtd-pl-create

# Add components to existing plugin
/gtd-pl-update

# Validate plugins follow gtd-cc patterns
/gtd-pl-validate

# Create a new skill
/gtd-pl-skill

# Create repository-specific automation
/gtd-pl-repo
```


## Developer guide

### Directory map

```
gtd-cc-plugin-dev/
├── skills/
│   └── gtd-cc-plugin-dev/
│       ├── SKILL.md              # Main skill (routes to sub-skills)
│       ├── sub-skills/           # Thin wrappers around plugin-dev
│       └── templates/            # gtd-cc templates
├── references/
│   └── plugin-dev -> [symlink]   # Official plugin-dev for reference
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
- [ ] Add prerequisite check for plugin-dev availability
- [ ] Migrate to official plugin dependencies when [Issue #9444](https://github.com/anthropics/claude-code/issues/9444) is implemented


## References

- [Official plugin-dev skill](references/plugin-dev/) - symlinked for reference
- [Claude Code plugins documentation](https://docs.anthropic.com/en/docs/claude-code)


## Appendix

### gtd-cc philosophy

This plugin follows its own philosophy: be a thin wrapper. All plugin development mechanics are handled by the official plugin-dev skill. This plugin adds:

- **Thin wrapper pattern**: Commands and agents reference skills, no inline logic
- **Centralization**: All domain logic lives in skills
- **Templates**: gtd-cc-specific templates showing the patterns
- **Marketplace registration**: gtd-cc marketplace conventions
