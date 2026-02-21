# gtd-cc - Getting Things Done with Claude Code

Welcome to GTD-CC, the Getting Things Done toolkit for Claude Code.

## What is GTD-CC?

GTD-CC is a plugin marketplace providing specialized tools for:
- Automating GitHub workflows with 7-stage issue-driven development
- Managing your knowledge base with Obsidian integration
- Researching and analyzing web content
- Creating professional project documentation
- Developing plugins for Claude Code marketplace

## Quick Start (2 minutes)

### 1. Install the Marketplace

```bash
/plugin marketplace add nikhilmaddirala/gtd-cc
```

### 2. Install Plugins You Need

```bash
# GitHub workflow automation
/plugin install github@gtd-cc

# Obsidian knowledge management
/plugin install obsidian@gtd-cc

# Web research and crawling
/plugin install web-research@gtd-cc

# Documentation tools
/plugin install documentation@gtd-cc

# Plugin development guide
/plugin install developing-for-claude-code@gtd-cc
```

### 3. Get Started

First-time users: Continue reading this guide for plugin selection.

## Choose Your Path (5-10 minutes)

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

# Build it (after approval)
/gh-build 1

# Review the code
/gh-review 1

# Merge when ready
/gh-merge 1
```

### For Knowledge Management

If you use Obsidian, the **Obsidian Workflow Plugin** helps you organize and capture knowledge.

Features:
- Sync GitHub tasks to your daily notes
- Create linked notes with PARA methodology
- Capture learning from research
- Extract content from web sources

### For Web Research

If you need to gather information from websites, the **Web Research Plugin** automates crawling and analysis.

Quick start:
```bash
# Crawl a website
skill web-research:crawl4ai
# Follow the prompts to crawl your target website
```

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

### For Plugin Development

If you want to create your own plugins, the **Developing for Claude Code Plugin** provides templates and workflows.

Quick start:
```bash
# Create a new plugin
/pl-create

# Setup plugin repository
/pl-repo

# Create a skill
/pl-skill
```

## Available Plugins

| Plugin | Purpose | Use When |
|--------|---------|----------|
| **GitHub** | Issue-driven development automation | Managing GitHub projects, automating workflows |
| **Obsidian** | Knowledge management and task sync | Building personal knowledge base, capturing learning |
| **Web Research** | Content crawling and analysis | Researching topics, gathering competitive intelligence |
| **Documentation** | Professional documentation tools | Setting up docs, improving existing documentation |
| **Developing for Claude Code** | Plugin development guide | Creating plugins for Claude Code marketplace |

Plugin details: See [plugins/README.md](plugins/README.md)

## Common Workflows

### Create and Ship a GitHub Feature

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

### Create a New Plugin

```bash
/pl-create my-plugin
/pl-repo
# Add your components
/pl-validate
```

## Documentation Structure

GTD-CC uses a three-layer documentation model:

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

## How to Contribute

We welcome contributions! Here's how to get started:

### Quick Contributions

1. **Report Issues**: Found a bug or have a suggestion? Open an issue.
2. **Improve Documentation**: Help us keep documentation accurate and clear.
3. **Share Feedback**: Tell us what's working and what isn't.

### Development Contributions

#### Adding a New Command

1. Identify which plugin it belongs to
2. Create command file: `plugins/<plugin-name>/commands/<name>.md`
3. Add it to the plugin manifest: `.claude-plugin/plugin.json`
4. Update the plugin README.md
5. Test locally with `/command-name`

#### Adding a New Skill

1. Create skill directory: `plugins/<plugin-name>/skills/<skill-name>/`
2. Create comprehensive `SKILL.md` documentation
3. Add skill to plugin manifest if needed
4. Update plugin README to reference the skill

#### Creating a New Plugin

1. Create plugin directory: `plugins/<new-plugin-name>/`
2. Create structure: `mkdir -p plugins/<new-plugin-name>/{.claude-plugin,commands,agents,skills}`
3. Create plugin manifest: `.claude-plugin/plugin.json`
4. Create plugin README.md
5. Add plugin to root `.claude-plugin/marketplace.json`
6. Implement initial components

### Conventions

- **Commands**: kebab-case, prefixed by plugin (e.g., `gh-issue`)
- **Agents**: kebab-case with `-agent` suffix
- **Skills**: kebab-case directories with uppercase `SKILL.md`
- **Plugins**: kebab-case directories

### Pull Request Guidelines

1. **Title**: Use conventional format: `feat:`, `fix:`, `docs:`, etc.
2. **Description**: Explain what components were added/modified and why
3. **Changes**: Keep PRs focused on specific features
4. **Testing**: Describe how changes were tested

## Quick Reference

### GitHub Workflow Commands

```
/gh-repo      - Initialize repository
/gh-issue     - Create a new issue
/gh-plan      - Develop implementation plan
/gh-build     - Implement code changes
/gh-review    - Review implementation
/gh-approve   - Approve for merge
/gh-merge     - Merge and clean up
/gh-manage    - Manage workflow
```

### Documentation Commands

```
/doc-init     - Initialize documentation structure
/doc-update   - Update docs after code changes
/doc-audit    - Assess documentation health
/doc-compress - Reduce documentation bloat
```

### Plugin Development Commands

```
/pl-create    - Create new plugin
/pl-repo      - Setup repository
/pl-skill     - Create skill
/pl-update    - Update plugin
/pl-validate  - Validate plugin
```

### Obsidian Skills

```
obsidian:content-extraction-skill
obsidian:options-analysis-skill
```

### Web Research Skills

```
web-research:crawl4ai
web-research:gemini-web-research
web-research:web-crawler
```

### Documentation Skills

```
docs-management
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

### Git workflow issues

1. Ensure you have a GitHub repository
2. Check permissions for the repository
3. Verify Git is configured correctly

### Documentation issues

1. Check that all links in README work
2. Validate JSON manifests with `jq . .claude-plugin/marketplace.json`
3. Run `/doc-audit` to identify issues

## Next Steps

Choose your path:

1. **Dive deeper**: Read individual plugin READMEs in [plugins/](plugins/)
2. **Start using**: Try the quick start commands for your chosen plugin
3. **Contribute**: Create a new plugin or improve existing ones
4. **Learn more**: Check skill documentation in individual plugins

## Questions?

- Check plugin-specific documentation in [plugins/](plugins/)
- Open an issue for bug reports or suggestions
- Review the quick reference commands above

Happy coding!

---

*Total lines: ~398 (within 200-500 line guideline)*

---

## Migration plan: plugins → flat skills

> This repo is migrating from Claude Code plugin format to flat `npx skills` (Vercel) format.
> See monorepo `ai-cli-helper/decisions.md` for full rationale (decisions D1-D8).

### Why

- `npx skills` supports 35+ agents (Claude Code, Opencode, Cursor, etc.) — plugins are Claude Code only
- Skills are the only unit of distribution going forward (D5: drop agents, commands, hooks — they were thin wrappers)
- Plugin packaging overhead (plugin.json, marketplace.json, nested directory structure) adds no value for skills
- Publishing = push to GitHub, discoverable on skills.sh — no marketplace registration needed

### Current structure

```
gtd-cc/
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── plugins/
│   ├── doc-parsing/        # 5 skills, 1 command
│   ├── docs-management/    # 1 skill, 3 commands, 2 agents
│   ├── github/             # 1 skill, 6 commands (disabled, superseded by gh-tasks)
│   ├── gtd-cc-plugin-dev/  # 1 skill, 4 commands
│   ├── obsidian/           # 2 skills, 2 agents (disabled)
│   ├── random/             # 6 skills, 6 commands, broken ai-orchestrator ref
│   └── web-research/       # 5 skills, 4 commands
└── README.md
```

### Target structure

Category prefixes: `web-`, `docs-`, `tools-`, `obsidian-`, or none for standalone skills.

```
gtd-cc/
├── skills/
│   ├── web-search/                # from web-research
│   ├── web-fetch/                 # from web-research
│   ├── web-deep-research/         # from web-research (renamed from deep-research)
│   ├── web-crawl4ai/              # from web-research (renamed from crawl4ai-toolkit)
│   ├── web-content-extraction/    # from web-research (renamed from content-extraction)
│   ├── web-browser/               # from monorepo .claude/skills/browser-automation/ (richer version replaces random's thin wrapper)
│   ├── documentation/             # from docs-management (project documentation: READMEs, changelogs, etc.)
│   ├── docs-pptx/                 # from doc-parsing (renamed from pptx-to-markdown)
│   ├── docs-docx/                 # from doc-parsing (renamed from docx-parsing)
│   ├── docs-xlsx/                 # from doc-parsing (renamed from xlsx-parsing)
│   ├── docs-pdf/                  # from doc-parsing (renamed from pdf-parsing)
│   ├── docs-pbix/                 # from doc-parsing (renamed from pbix-parsing)
│   ├── obsidian-gtd/              # from obsidian
│   ├── obsidian-options/          # from obsidian (renamed from options-analysis-skill)
│   ├── gtd-skills-dev/            # from gtd-cc-plugin-dev (skill/plugin development guide)
│   ├── tools-langfuse/            # from random (renamed from langfuse-cli)
│   ├── tools-secrets/             # from random (renamed from secrets-management)
│   ├── tools-diagnostics/         # from random (renamed from system-diagnostics)
│   ├── tools-backlog/             # from random (renamed from backlog-md-skill)
│   └── tools-catppuccin/          # from random (renamed from catppuccin-port-creation)
└── README.md
```

### Steps

- Create `skills/` directory
- Move skills from `plugins/*/skills/*/` into flat `skills/*/` (use `git mv` to preserve history)
- Move monorepo `.claude/skills/browser-automation/` (2 sub-skills, 6 refs, 3 templates) here as the canonical version, replacing the thin `random` plugin wrapper
- Rename skills (directory name + SKILL.md `name` field):
  - `deep-research` → `web-deep-research`
  - `crawl4ai-toolkit` → `web-crawl4ai`
  - `content-extraction` → `web-content-extraction`
  - `browser-automation` → `web-browser`
  - `docs-management` → `documentation`
  - `pptx-to-markdown` → `docs-pptx`
  - `docx-parsing` → `docs-docx`
  - `xlsx-parsing` → `docs-xlsx`
  - `pdf-parsing` → `docs-pdf`
  - `pbix-parsing` → `docs-pbix`
  - `obsidian-gtd` → `obsidian-gtd` (no change)
  - `options-analysis-skill` → `obsidian-options`
  - `gtd-cc-plugin-dev` → `gtd-skills-dev`
  - `langfuse-cli` → `tools-langfuse`
  - `secrets-management` → `tools-secrets`
  - `system-diagnostics` → `tools-diagnostics`
  - `backlog-md-skill` → `tools-backlog`
  - `catppuccin-port-creation` → `tools-catppuccin`
- Update `name` field in each renamed SKILL.md frontmatter to match new directory name
- Delete `github` plugin entirely (superseded by `gh-tasks` private skill)
- Remove all non-skill components:
  - `plugins/docs-management/agents/` (2 agents)
  - `plugins/docs-management/commands/` (3 commands)
  - `plugins/obsidian/agents/` (2 agents)
  - `plugins/web-research/commands/` (4 commands)
  - `plugins/random/commands/` (6 commands)
  - `plugins/gtd-cc-plugin-dev/commands/` (4 commands)
  - `plugins/doc-parsing/commands/` (1 command)
- Remove plugin infrastructure: `.claude-plugin/`, all `plugins/*/` directories (after skills extracted), `plugins/README.md`
- Update this README (replace plugin install instructions with `npx skills add`)
- Subtree-push to sync new structure to public repo
- Verify `npx skills add nikhilmaddirala/gtd-cc` discovers all skills in `skills/`

### Decisions to make during restructure

- Keep or archive doc-parsing skills (5 skills, currently disabled plugin)?
- Keep or archive obsidian skills (2 skills, currently disabled plugin)?

### Consumer migration

Users currently installing via `claude plugin install`:
```bash
# Old way (will stop working after restructure)
claude plugin install web-research@gtd-cc --scope project

# New way
npx skills add nikhilmaddirala/gtd-cc -a claude-code
```

`npx skills` has backwards compatibility — it detects `.claude-plugin/plugin.json` during transition. But once the plugin infrastructure is removed, only `npx skills add` works.