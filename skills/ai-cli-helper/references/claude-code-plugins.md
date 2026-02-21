---
global-type: misc-software
tags: [software, tool, claude-code, plugins]
status: legacy
type: cli
---

# Claude Code plugins (legacy reference)

> The plugin system is deprecated for skill management in this monorepo. All skill installation and activation uses `npx skills` (see `subskills/manage-skills.md`).
>
> This reference is kept for diagnosing plugin conflicts, understanding stale `enabledPlugins` entries in settings.json, and knowing how to uninstall legacy plugins during cleanup. Do not use these commands for installing or managing skills.

## Overview

- Source: https://code.claude.com/docs/plugins
- Category: AI agent extensibility
- Key concepts:
  - A plugin is a bundle (skills, agents, hooks, MCP/LSP servers) with a manifest at `.claude-plugin/plugin.json`
  - A marketplace is a catalog (`marketplace.json`) that lists plugins and their sources
  - Plugins are namespaced: `plugin-name:skill-name` (e.g. `/random:langfuse-cli`)
  - See the Claude Code docs for full plugin system reference

## Usage notes

- If you maintain a custom marketplace, point it at a local directory for rapid iteration
- The official Anthropic marketplace (`claude-plugins-official`) provides first-party plugins
- Management principle: always use CLI commands, never the TUI (interactive `/plugin` interface inside Claude Code)
- Scope principle: always prefer project-level install over user or local install

## Config architecture: three layers

### 1) User-level settings (`~/.claude/settings.json`)

May be declaratively managed (e.g. via Nix, dotfiles). If so, do not edit directly.

Contains global hooks, statusline config, output style, and thinking preferences. May also contain user-scope `enabledPlugins` (prefer migrating these to project scope).

Check your system documentation for the config source location.

To check current state: read `~/.claude/settings.json` (follows symlink)

### 2) Project-level settings (`<repo>/.claude/settings.json`)

Checked into git, shared with collaborators. Contains project-specific permissions, hooks, env vars, and enabled/disabled plugins.

To check current state: read `.claude/settings.json` in the repo root

### 3) Local settings (`<repo>/.claude/settings.local.json`)

Gitignored, machine-specific overrides. Used for extra bash permissions or local-only tweaks.

To check current state: read `.claude/settings.local.json` in the repo root

## Marketplaces

Common marketplace types:

- `claude-plugins-official`: source `github:anthropics/claude-plugins-official`
  - First-party Anthropic plugins (LSP servers, external integrations, dev workflows, output styles)
- Custom marketplaces: source `directory:<path>` for local development, or `github:<owner>/<repo>` for published versions
  - Add a custom marketplace via `claude plugin marketplace add <owner>/<repo>`

To check current marketplaces: read `~/.claude/plugins/known_marketplaces.json` or run `claude plugin marketplace list`

## Plugin discovery

Plugins exist at two scopes:

- **Project-scope** (preferred): Configured in `.claude/settings.json` under `enabledPlugins` and `disabledPlugins`. These only apply when working in that project.
- **User-scope** (use sparingly): Stored in `~/.claude/plugins/installed_plugins.json`. Apply globally across all projects.

To discover current state:

```bash
# List all plugins with status and scope
claude plugin list

# Check project-level enabled/disabled
cat .claude/settings.json | jq '.enabledPlugins, .disabledPlugins'

# Check user-level installed
cat ~/.claude/plugins/installed_plugins.json
```

## Standalone skills (not plugins)

The monorepo also has standalone skills in `.claude/skills/` that are not packaged as plugins. These are project-scoped by nature.

To discover: `ls .claude/skills/`

## Workflows and operations

### Marketplace operations

```bash
# add a marketplace (from GitHub)
claude plugin marketplace add owner/repo

# add a marketplace (from local directory)
claude plugin marketplace add ./path/to/marketplace

# list registered marketplaces
claude plugin marketplace list

# refresh a marketplace's plugin listings
claude plugin marketplace update my-marketplace

# remove a marketplace (also uninstalls its plugins)
claude plugin marketplace remove marketplace-name
```

### Plugin install and uninstall

```bash
# install to project scope (preferred)
claude plugin install plugin-name@marketplace-name --scope project

# install to user scope (cross-project, use sparingly)
claude plugin install plugin-name@marketplace-name --scope user

# uninstall from project scope
claude plugin uninstall plugin-name@marketplace-name --scope project

# uninstall from user scope
claude plugin uninstall plugin-name@marketplace-name --scope user
```

### Plugin enable and disable

```bash
# enable at project scope (preferred)
claude plugin enable plugin-name@marketplace-name --scope project

# disable at project scope
claude plugin disable plugin-name@marketplace-name --scope project
```

### Plugin update

```bash
# update a specific plugin
claude plugin update plugin-name@marketplace-name --scope project
```

### Validation and debugging

```bash
# validate a marketplace or plugin directory
claude plugin validate .

# debug plugin loading (shows registration, errors, MCP init)
claude --debug

# test a plugin during development without installing
claude --plugin-dir ./path/to/plugin

# clear stale plugin cache
rm -rf ~/.claude/plugins/cache
```

## Key files (where to look)

- User settings: `~/.claude/settings.json` (may be system-managed)
- User instructions: `~/.claude/CLAUDE.md` (may be system-managed)
- User installed plugins: `~/.claude/plugins/installed_plugins.json`
- User known marketplaces: `~/.claude/plugins/known_marketplaces.json`
- User plugin cache: `~/.claude/plugins/cache/`
- Project settings: `<repo>/.claude/settings.json`
- Project local settings: `<repo>/.claude/settings.local.json`
- Marketplace source: your marketplace directory's `.claude-plugin/marketplace.json`
- Standalone skills: `<repo>/.claude/skills/`
- Config source: check your system documentation
- Hooks: `~/.claude/hooks/` (user-level) and `<repo>/.claude/hooks/` (project-level)
