# GTD-CC Plugins

This directory contains the core plugins that make up the gtd-cc marketplace. Each plugin provides specialized tools and workflows for a specific area of Getting Things Done methodology.

## Available Plugins

### GitHub Workflow Plugin

Complete automation for GitHub-based issue-driven development with a structured 7-stage workflow.

Location: `github/`

Core capabilities:
- Repository setup and configuration
- Issue creation and planning
- Autonomous implementation and code review
- Merge and deployment orchestration

When to use: Managing projects with GitHub issues and pull requests, automating development workflows, enforcing process consistency.

Learn more: See [github/README.md](github/README.md)

### Obsidian Workflow Plugin

Knowledge management integration with PARA methodology and Zettelkasten note-taking patterns.

Location: `obsidian/`

Core capabilities:
- Task synchronization with GitHub issues
- Knowledge base organization and linking
- Daily planning and review workflows
- Learning capture automation

When to use: Building a personal knowledge base, connecting GitHub tasks to Obsidian notes, maintaining project documentation.

Learn more: See [obsidian/README.md](obsidian/README.md)

### Web Research Plugin

Comprehensive web crawling, content analysis, and research automation toolkit.

Location: `web-research/`

Core capabilities:
- Full-website crawling and markdown conversion
- JavaScript-heavy page handling
- Content extraction with schema generation
- AI-powered content analysis and synthesis

When to use: Researching technologies, gathering competitive intelligence, building knowledge bases from web sources, analyzing online content.

Learn more: See [web-research/README.md](web-research/README.md)

### Documentation Plugin

Professional documentation tools following the Best README Template and three-layer documentation model.

Location: `documentation/`

Core capabilities:
- Three-layer documentation structure (README → directory docs → deep dives)
- Documentation initialization and templates
- Quality auditing and maintenance guidance
- Multi-phase project support (small to enterprise)

When to use: Setting up documentation for new projects, maintaining existing documentation, conducting documentation audits, establishing documentation standards.

Learn more: See [documentation/README.md](documentation/README.md)

### Developing for Claude Code Plugin

Comprehensive guide and toolkit for creating plugins for Claude Code marketplace.

Location: `developing-for-claude-code/`

Core capabilities:
- Plugin development patterns and templates
- Command, agent, and skill creation guidelines
- Repository setup and validation tools
- GTD architectural patterns for plugins

When to use: Creating new plugins for Claude Code, learning plugin development best practices, setting up plugin repository structure.

Learn more: See [developing-for-claude-code/README.md](developing-for-claude-code/README.md)

## Plugin Architecture

All plugins follow a consistent architecture:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          Plugin manifest with component metadata
├── README.md                Plugin overview and quick start
├── commands/                Interactive slash commands
│   └── *.md                 Individual command definitions
├── agents/                  Autonomous workflow agents
│   └── *.md                 Individual agent definitions
└── skills/                  Foundation knowledge and expertise
    └── */SKILL.md          Detailed skill documentation
```

## Choosing a Plugin

### I want to automate GitHub workflows
Start with the **GitHub Workflow Plugin** (`github/`). It provides:
- Interactive slash commands for every workflow stage
- Autonomous agents for batch operations
- Detailed procedural documentation
- 7-stage structured workflow

### I want to manage my knowledge base
Use the **Obsidian Workflow Plugin** (`obsidian/`). It includes:
- Note creation and organization patterns
- Task-knowledge synchronization
- Daily planning templates
- Learning capture workflows

### I need to research and analyze web content
Use the **Web Research Plugin** (`web-research/`). It provides:
- Website crawling and archiving
- Content extraction and parsing
- AI-powered analysis and synthesis
- Multi-URL batch processing

### I need better project documentation
Use the **Documentation Plugin** (`documentation/`). It offers:
- Documentation structure templates
- Quality assessment and improvement guidance
- Best practices for README formatting
- Maintenance checklists and automation

### I want to create plugins for Claude Code
Use the **Developing for Claude Code Plugin** (`developing-for-claude-code/`). It provides:
- Plugin development templates and patterns
- Step-by-step creation workflows
- Validation and testing tools
- GTD-based architectural guidance

## Common Workflows

### Create and implement a GitHub issue
1. Use `/gh-issue` from the **GitHub plugin** to create an issue
2. Run `/gh-plan` to develop an implementation approach
3. Run `/gh-build` to implement and create a PR
4. Document changes using `/doc-update` from the **Documentation plugin**

### Build a project knowledge base
1. Use the **Web Research plugin** to crawl and archive sources
2. Use the **Obsidian plugin** to organize findings in your vault
3. Use the **Documentation plugin** to create reference documentation
4. Link everything together in `/docs/` structure

### Create a new plugin
1. Use the **Developing for Claude Code plugin** to create a plugin template
2. Follow the GTD architectural patterns for plugin design
3. Use the provided validation tools to check your work
4. Submit your plugin to the marketplace

### Conduct quarterly documentation review
1. Run `/doc-audit` from the **Documentation plugin** to assess current state
2. Address identified issues with `/doc-update`
3. Update team documentation standards
4. Schedule next review in your calendar

## Integration Between Plugins

Plugins are designed to work together:

- **GitHub + Documentation**: Document features as part of PR reviews using `/doc-update`
- **GitHub + Obsidian**: Sync GitHub issues to your Obsidian daily notes for personal task tracking
- **Web Research + Obsidian**: Research and capture findings directly into your knowledge base
- **Web Research + Documentation**: Use crawled content as reference material for project documentation
- **Developing for Claude Code + All Plugins**: Use development patterns to create new plugins that integrate with existing ones

## Plugin Installation

To use plugins from this marketplace:

```bash
# Add the marketplace
/plugin marketplace add nikhilmaddirala/gtd-cc

# Install individual plugins
/plugin install github@gtd-cc
/plugin install obsidian@gtd-cc
/plugin install web-research@gtd-cc
/plugin install documentation@gtd-cc
/plugin install developing-for-claude-code@gtd-cc
```

## Next Steps

1. **New to GTD-CC?** Start with [Getting Started Guide](../GETTING-STARTED.md)
2. **Want to learn about a specific plugin?** See the plugin-specific README
3. **Need detailed procedures?** Check the skill documentation in each plugin
4. **Want to create a plugin?** See the [Developing for Claude Code plugin](developing-for-claude-code/README.md)
5. **Contributing?** See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines

## Related Documentation

- [Marketplace Overview](../README.md) - GTD-CC project overview
- [Getting Started](../GETTING-STARTED.md) - First-time user guide
- [Contributing Guide](../CONTRIBUTING.md) - Developer guidelines
- [References](../references/README.md) - Detailed reference materials
