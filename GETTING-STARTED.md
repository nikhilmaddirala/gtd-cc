# Getting Started with GTD-CC

Welcome to GTD-CC, the Getting Things Done toolkit for Claude Code. This guide will help you get up and running in 10 minutes.

## What is GTD-CC?

GTD-CC is a plugin marketplace for Claude Code that provides specialized tools for:
- Automating GitHub workflows (7-stage issue-driven development)
- Managing your knowledge base with Obsidian
- Researching and extracting web content
- Creating professional project documentation

## Installation (2 minutes)

### Step 1: Add the Marketplace

In Claude Code, run:

```bash
/plugin marketplace add nikhilmaddirala/gtd-cc
```

This adds GTD-CC to your available marketplaces.

### Step 2: Install Plugins

Install the plugins you need:

```bash
# GitHub workflow automation
/plugin install github@gtd-cc

# Obsidian knowledge management
/plugin install obsidian@gtd-cc

# Web research and crawling
/plugin install web-research@gtd-cc

# Documentation tools
/plugin install documentation@gtd-cc
```

Or install them one at a time as needed.

### Step 3: Verify Installation

Check that plugins are installed:

```bash
/plugin
```

You should see gtd-cc plugins listed.

## Choosing Your First Plugin (3 minutes)

### For GitHub Project Management

If you manage projects on GitHub, the **GitHub Workflow Plugin** automates the entire workflow from issue to merge.

Quick start:

```bash
# Initialize your repository
/gh-repo

# Create your first issue
/gh-issue "Describe what you want to build"

# Plan the implementation
/gh-plan 1

# (After approval) Build it
/gh-build 1

# Review the code
/gh-review 1

# Merge when ready
/gh-merge 1
```

Learn more: See [plugins/github/README.md](plugins/github/README.md)

### For Knowledge Management

If you use Obsidian, the **Obsidian Workflow Plugin** helps you organize and capture knowledge.

Quick start:
- Sync GitHub tasks to your daily notes
- Create linked notes with PARA methodology
- Capture learning from research

Learn more: See [plugins/obsidian/README.md](plugins/obsidian/README.md)

### For Web Research

If you need to gather information from websites, the **Web Research Plugin** automates crawling and analysis.

Quick start:

```bash
# Crawl a website
uvx crawl4ai crawl \
  --url "https://example.com" \
  --output-dir "./crawled-content" \
  --max-depth 2 \
  --format markdown
```

Learn more: See [plugins/web-research/README.md](plugins/web-research/README.md)

### For Project Documentation

If you need to improve your project documentation, the **Documentation Plugin** provides structure and guidance.

Quick start:

```bash
# Initialize documentation
/doc-init

# Audit existing documentation
/doc-audit

# Update documentation when code changes
/doc-update
```

Learn more: See [plugins/documentation/README.md](plugins/documentation/README.md)

## Common Workflows (5 minutes)

### Workflow 1: Create and Ship a GitHub Feature

1. Create an issue describing the feature
2. Plan the implementation
3. Build the code in an isolated branch
4. Review and get approval
5. Merge to main

Command flow:

```bash
/gh-issue "Add dark mode toggle"      # Creates issue #1
/gh-plan 1                             # Plans implementation
/gh-build 1                            # Implements the feature
/gh-review 1                           # Reviews the code
/gh-merge 1                            # Merges to main
```

### Workflow 2: Research and Document

1. Research a topic using Web Research plugin
2. Capture findings in Obsidian using Obsidian plugin
3. Document results in your project using Documentation plugin

### Workflow 3: Maintain Project Documentation

1. Review current documentation state
2. Update documentation for recent changes
3. Verify all links work
4. Schedule next review

Command flow:

```bash
/doc-audit                             # Assess current state
/doc-update                            # Update docs
# Schedule quarterly review
```

## Where to Find Help

### For Specific Plugin Questions

See the plugin's README:
- [GitHub Plugin](plugins/github/README.md)
- [Obsidian Plugin](plugins/obsidian/README.md)
- [Web Research Plugin](plugins/web-research/README.md)
- [Documentation Plugin](plugins/documentation/README.md)

### For Detailed Procedures

Check the skill documentation inside each plugin. For example:
- GitHub workflow details: `plugins/github/skills/github-gtd/SKILL.md`
- Documentation standards: `plugins/documentation/skills/doc-standards/SKILL.md`

### For Architecture and Design

See the reference documentation:
- [Plugin Marketplaces Guide](references/docs/plugin-marketplaces.md)
- [Architecture Principles](references/docs/architecture-principles.md)

### For Contributing

See the [Contributing Guide](CONTRIBUTING.md)

## Keyboard Shortcuts & Quick References

### GitHub Workflow Commands

```
/gh-issue    - Create a new issue
/gh-plan     - Develop implementation plan
/gh-build    - Implement code changes
/gh-review   - Review implementation
/gh-approve  - Approve for merge
/gh-merge    - Merge and clean up
```

### Documentation Commands

```
/doc-init    - Initialize documentation structure
/doc-update  - Update docs after code changes
/doc-audit   - Assess documentation health
```

## Troubleshooting

### Plugins not showing up

1. Verify marketplace is added: `/plugin marketplace list`
2. Check marketplace is accessible
3. Reinstall if needed: `/plugin marketplace remove nikhilmaddirala/gtd-cc` then re-add

### Command not found

1. Verify plugin is installed: `/plugin list`
2. Check command name spelling and formatting
3. Some commands may require initialization (e.g., `/gh-repo` before `/gh-issue`)

### Want to learn more

- Read the [main README](README.md) for project overview
- Check [plugins directory](plugins/README.md) for plugin selection guidance
- Review specific plugin README for detailed usage
- See [contributing guide](CONTRIBUTING.md) for development guidelines

## Next Steps

Choose one:

1. **Go deep on GitHub workflows**: Read [plugins/github/README.md](plugins/github/README.md)
2. **Set up Obsidian integration**: Read [plugins/obsidian/README.md](plugins/obsidian/README.md)
3. **Master web research**: Read [plugins/web-research/README.md](plugins/web-research/README.md)
4. **Improve project docs**: Read [plugins/documentation/README.md](plugins/documentation/README.md)
5. **Contribute to GTD-CC**: Read [CONTRIBUTING.md](CONTRIBUTING.md)

## Quick Facts

- **Installation time**: 2 minutes
- **First issue creation**: 5 minutes
- **Full workflow (issue to merge)**: 15-60 minutes depending on code complexity
- **Documentation audit**: 10-15 minutes
- **All plugins available**: Free (MIT licensed)

## Questions?

- Check the [main README](README.md)
- Review plugin-specific documentation
- See [contributing guide](CONTRIBUTING.md) for support options

Happy coding!
