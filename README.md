# gtd-cc - Getting Things Done with Claude Code

Welcome to GTD-CC, the Getting Things Done toolkit for Claude Code.

## What is GTD-CC?

GTD-CC is a plugin marketplace providing specialized tools for:
- Automating GitHub workflows with 7-stage issue-driven development
- Managing your knowledge base with Obsidian integration
- Researching and analyzing web content
- Creating professional project documentation

## Quick Start (2 minutes)

### 1. Install the Marketplace

```bash
/plugin marketplace add nikhilmaddirala/gtd-cc
```

### 2. Install Plugins You Need

```bash
/plugin install github@gtd-cc      # GitHub automation
/plugin install obsidian@gtd-cc    # Knowledge management
/plugin install web-research@gtd-cc # Web crawling & analysis
/plugin install documentation@gtd-cc # Project documentation
```

### 3. Get Started

First-time users: See [Getting Started Guide](GETTING-STARTED.md)

Choose your first plugin:
- **GitHub automation?** See [plugins/github/README.md](plugins/github/README.md)
- **Knowledge management?** See [plugins/obsidian/README.md](plugins/obsidian/README.md)
- **Web research?** See [plugins/web-research/README.md](plugins/web-research/README.md)
- **Project documentation?** See [plugins/documentation/README.md](plugins/documentation/README.md)

## Available Plugins

| Plugin | Purpose | Use When |
|--------|---------|----------|
| **GitHub** | Issue-driven development automation | Managing GitHub projects, automating workflows |
| **Obsidian** | Knowledge management and task sync | Building personal knowledge base, capturing learning |
| **Web Research** | Content crawling and analysis | Researching topics, gathering competitive intelligence |
| **Documentation** | Professional documentation tools | Setting up docs, improving existing documentation |

Full plugin descriptions: See [plugins/README.md](plugins/README.md)

## Documentation Structure

GTD-CC uses a three-layer documentation model for clarity:

**Layer 1: This file**
- Overview and quick start
- Plugin selection guidance
- Installation instructions

**Layer 2: Plugin READMEs**
- Plugin overview and value proposition
- Available commands and agents
- Plugin-specific workflows
- Integration with other plugins

**Layer 3: Detailed Documentation**
- Skill documentation (plugins/*/skills/*/SKILL.md) - Step-by-step procedures
- Reference guides (references/) - Architectural and design information
- Component documentation - Implementation details

Start at Layer 1, dive deeper as needed.

## Common Workflows

### Create and Merge a GitHub Feature

```bash
/gh-issue "Add dark mode toggle"
/gh-plan 1
/gh-build 1
/gh-review 1
/gh-merge 1
```

### Research and Document

1. Use Web Research plugin to crawl websites
2. Capture findings in Obsidian
3. Document results with Documentation plugin

### Conduct Documentation Review

```bash
/doc-audit
/doc-update
```

See [plugins/README.md](plugins/README.md) for more workflows.

## Directory Navigation

```
gtd-cc/
├── README.md                    Entry point (this file)
├── GETTING-STARTED.md          First-time user guide
├── CONTRIBUTING.md             Developer guidelines
├── plugins/                    Plugin directory
│   ├── README.md              Plugin selection guide
│   ├── github/               GitHub workflow plugin
│   ├── obsidian/             Obsidian integration
│   ├── web-research/         Web crawling & analysis
│   └── documentation/        Documentation tools
├── references/               Detailed reference docs
│   ├── README.md            Reference guide index
│   └── *.md                 Architectural references
├── .claude/                  Claude Code configuration
│   ├── README.md           Configuration guide
│   └── skills/             Custom project skills
└── .claude-plugin/         Marketplace config
```

See [Directory Structure Guide](#directory-structure-guide) below for what each part contains.

## Next Steps

Choose one based on your needs:

### New to GTD-CC?
- Read [Getting Started Guide](GETTING-STARTED.md) - 10-minute onboarding
- Browse available plugins at [plugins/README.md](plugins/README.md)

### Ready to use a plugin?
- GitHub automation: [plugins/github/README.md](plugins/github/README.md)
- Knowledge management: [plugins/obsidian/README.md](plugins/obsidian/README.md)
- Web research: [plugins/web-research/README.md](plugins/web-research/README.md)
- Documentation: [plugins/documentation/README.md](plugins/documentation/README.md)

### Want to contribute?
- See [CONTRIBUTING.md](CONTRIBUTING.md) for developer guidelines
- Review [Claude Code configuration](.claude/README.md) for project conventions

### Need deep technical information?
- See [references/README.md](references/README.md) for architectural guides

## Directory Structure Guide

### plugins/

Contains all plugin components (commands, agents, skills).

- **plugins/README.md** - Plugin selection and overview
- **plugins/github/** - GitHub workflow automation
- **plugins/obsidian/** - Obsidian knowledge management
- **plugins/web-research/** - Web crawling and analysis
- **plugins/documentation/** - Project documentation tools

Each plugin has:
- `README.md` - Plugin overview and quick start
- `commands/` - Interactive slash commands
- `agents/` - Autonomous workflow agents
- `skills/` - Detailed procedural documentation

### references/

Detailed reference documentation and architectural guides.

- **references/README.md** - Reference documentation index
- **references/plugin-marketplaces.md** - Marketplace architecture
- **references/Github-projects-ai-workflow.md** - GitHub workflow design
- **references/ai-agents-README.md** - Agent architecture

For step-by-step procedures, see skill documentation in each plugin instead.

### .claude/

Claude Code configuration and custom components.

- **.claude/README.md** - Configuration guide
- **CLAUDE.md** - Main project configuration for Claude Code

Tells Claude how to behave when working with this project, naming conventions, and development patterns.

## Plugin Architecture

All plugins use a consistent architecture:

- **Skills** - Foundation layer with domain expertise
- **Commands** - Interactive workflows (`/command-name`)
- **Agents** - Autonomous execution without human interaction

This layering keeps logic reusable and components focused.

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Project structure conventions
- How to add new commands, agents, and skills
- Development workflow guidelines
- Testing and validation procedures

## Support

- **Getting started?** See [GETTING-STARTED.md](GETTING-STARTED.md)
- **Plugin questions?** Check the plugin's README.md
- **Procedures and how-tos?** See SKILL.md files in each plugin
- **Architecture and design?** See references/ directory
- **Contributing?** See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Bugs?** Report via GitHub Issues

## Key Principles

- **User-focused navigation** - Documentation guides you based on your needs
- **Three-layer structure** - Overview → plugin level → detailed procedures
- **One fact, one place** - Information is linked, not duplicated
- **Consistent patterns** - All plugins follow the same architecture
- **Progressive disclosure** - Basic usage first, deep dives when needed

---

**License:** MIT
**Maintainer:** Nikhil Maddirala
**Repository:** https://github.com/nikhilmaddirala/gtd-cc
