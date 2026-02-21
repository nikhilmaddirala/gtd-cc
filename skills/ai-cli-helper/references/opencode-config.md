---
global-type: misc-software
tags: [software, tool, opencode, config]
status: active
type: cli
---

# Opencode configuration

> How Opencode is set up, where configs live, and how to manage them.

## Overview

- Source: https://opencode.ai/docs
- Category: AI agent CLI tool (terminal-based coding assistant)
- Installable via your system package manager or from source
- User-level config may be declaratively managed (e.g. via Nix, dotfiles, etc.)

## Config architecture

### Three layers (in precedence order)

- **User-level** (`~/.config/opencode/`): May be system-managed. If declaratively managed, do not edit directly -- change the source and rebuild.
  - Key files: `opencode.json`, `AGENTS.md`, `ask-prompt.txt`, `oh-my-opencode.json`, `themes/`
- **Project-level** (`.opencode/` in repo root): Project-specific files. Bun manages plugin dependencies here.
  - Key files: `package.json`, `bun.lock`, `node_modules/`
  - Symlinks to Claude Code: `skill` → `../.claude/skills/`, `command` → `../.claude/commands/`
- **No local override layer**: Unlike Claude Code's `settings.local.json`, Opencode has no built-in local override file

### Config source structure

If you manage config declaratively (e.g. via Nix, dotfiles), your source directory will typically contain:
- Main config (e.g. `opencode.json` or a template that generates it)
- oh-my-opencode plugin config
- System prompt files
- Theme files
- Shared agent instructions (same file used by Claude Code)

Check your system documentation for the exact source file locations.

### How to discover current state

```bash
# Check installed version
opencode --version

# Check what config files exist and where they point
ls -la ~/.config/opencode/
ls -la .opencode/

# Read effective config (follows symlinks if declaratively managed)
cat ~/.config/opencode/opencode.json

# Check oh-my-opencode config
cat ~/.config/opencode/oh-my-opencode.json

# Check project-level plugin dependencies
cat .opencode/package.json
```

## Plugin system

Opencode uses two plugin mechanisms:

- **oh-my-opencode**: Community plugin framework. Configured via `oh-my-opencode.json` (may be system-managed). Supports agent model overrides, disabled agents/hooks/MCPs, Google auth, LSP servers, and OmO orchestrator settings.
- **Bun packages**: Project-level plugin dependencies in `.opencode/package.json`. Installed with `bun install` in the `.opencode/` directory.

Neither uses a marketplace system like Claude Code. Plugin management is more manual.

## Agent modes

Opencode has three built-in modes with distinct permission profiles:
- **build**: Full coding agent with ask-permission for destructive bash commands
- **plan**: Read-only planning (edit tool disabled)
- **ask**: Strict read-only with custom system prompt enforcing no modifications

Permissions are configured per-mode under `agent.<mode>.permission.bash` in the opencode config. Check your config source for current permission rules.

## Cross-tool sharing with Claude Code

- Skills shared via symlink: `.opencode/skill` → `.claude/skills/`
- Commands shared via symlink: `.opencode/command` → `.claude/commands/`
- Agent instructions can be shared: both tools use `AGENTS.md`
- Provider configs are independent (Claude Code uses built-in Anthropic; Opencode uses configurable providers)

## Cross-tool equivalences

| Concept | Claude Code | Opencode |
|---------|------------|----------|
| Main config | `settings.json` | `opencode.json` |
| Agent instructions | `CLAUDE.md` | `AGENTS.md` (shared source) |
| Hooks | `hooks` key in settings.json | oh-my-opencode hooks |
| Permissions | `permissions` in settings.json | `agent.*.permission` in opencode.json |
| Plugins | marketplace + `claude plugin` CLI | oh-my-opencode + bun packages |
| Skills | `.claude/skills/` | `.opencode/skill/` (symlink to claude) |
| Commands | `.claude/commands/` | `.opencode/command/` (symlink to claude) |
| Agent modes | n/a (single mode) | build / plan / ask |
| Provider | built-in Anthropic | `provider` block in opencode.json |

## Workflows and operations

### Changing user-level config

1. Edit the source file in your config management system
2. Validate the changes using your system's check/dry-run command
3. Run the appropriate rebuild/apply command
4. Restart opencode to pick up changes

### Changing oh-my-opencode settings

Same as above -- edit the oh-my-opencode config source, rebuild.

### Managing project-level plugins

```bash
cd .opencode/
bun add @opencode-ai/some-plugin
bun remove @opencode-ai/some-plugin
```

### Debugging

```bash
# Check if config is loading correctly
opencode --version   # confirms binary works
cat ~/.config/opencode/opencode.json  # check effective config
ls -la ~/.config/opencode/  # verify symlinks are intact

# If symlinks are broken after a rebuild
# Re-run your config management apply/switch command
```

## Key files (where to look)

- Config source: check your system documentation
- Shared config source: check your system documentation
- User config (runtime): `~/.config/opencode/`
- Project config: `.opencode/`
- Upstream docs: https://opencode.ai/docs
