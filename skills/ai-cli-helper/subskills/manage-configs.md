# Manage configs

Inspect, modify, and debug configuration for AI agent CLI tools (Claude Code, Opencode) across all scopes.

## When to use

- When checking or modifying settings.json, opencode.json, or system-level config
- When debugging scope conflicts or unexpected behavior from config layering
- When comparing configuration between Claude Code and Opencode
- When a rebuild is needed after changing user-level settings

## Important: declaratively managed files

User-level settings may be declaratively managed (e.g. via Nix, dotfiles, etc.). If so, do NOT edit them directly. Instead, edit the source files and rebuild.

- Claude Code: `~/.claude/settings.json` (check your system documentation for the source location)
- Opencode: `~/.config/opencode/opencode.json` (check your system documentation for the source location)

## Config file locations

| Scope | Claude Code | Opencode |
|-------|-------------|----------|
| User settings | `~/.claude/settings.json` (may be system-managed) | `~/.config/opencode/opencode.json` (may be system-managed) |
| Project settings | `.claude/settings.json` | `.opencode/opencode.json` |
| Local overrides | `.claude/settings.local.json` | n/a |
| User instructions | `~/.claude/CLAUDE.md` (may be system-managed) | `~/.config/opencode/AGENTS.md` (may be system-managed) |
| Project instructions | `CLAUDE.md` | `AGENTS.md` |
| Opencode extensions | n/a | `~/.config/opencode/oh-my-opencode.json`, `.opencode/package.json` |
| Hooks | `hooks` key in settings.json | oh-my-opencode hooks |
| Config source | check your system documentation | check your system documentation |

## Process

### Inspect config

Read all three layers to understand effective config (later layers override earlier):

```bash
# Claude Code
cat ~/.claude/settings.json          # user (may be system-managed)
cat .claude/settings.json            # project
cat .claude/settings.local.json      # local overrides

# Opencode
cat ~/.config/opencode/opencode.json # user (may be system-managed)
cat .opencode/opencode.json          # project
```

When presenting config state, show all layers to make precedence clear.

### Modify config at correct scope

| Scope | Method |
|-------|--------|
| User-level | Edit the config source, rebuild if declaratively managed (see rebuild workflow below) |
| Project-level | Edit the file directly, commit to git |
| Local overrides | Edit `.claude/settings.local.json` directly (gitignored) |

When unsure which scope to modify, prefer project scope.

### Rebuild workflow

When user-level settings are declaratively managed and need to change:

- Edit the source file for your config management system (e.g. Nix module, dotfiles repo, etc.)
- Validate the changes using your system's check/dry-run command
- Run the appropriate rebuild/apply command for your system

## Cross-tool equivalences

| Concept | Claude Code | Opencode |
|---------|-------------|----------|
| Main config | `settings.json` | `opencode.json` |
| Agent instructions | `CLAUDE.md` | `AGENTS.md` (shared source) |
| Hooks | `hooks` key in settings.json | oh-my-opencode hooks |
| Permissions | `permissions` in settings.json | `agent.*.permission` in opencode.json |
| Skills | `.claude/skills/` (symlinks) | `.agents/skills/` (canonical) |
| Commands | `.claude/commands/` | `.opencode/command/` (symlink to claude) |
| Agent modes | n/a (single mode) | build / plan / ask |
| Provider | built-in Anthropic | `provider` block in opencode.json |

## Guidelines

- Always read the relevant reference doc (`references/opencode-config.md` for Opencode details) before taking action
- When presenting config state, show all three layers (user -> project -> local) to make precedence clear
- Config concepts overlap between tools but syntax differs -- always check both reference docs when comparing
- For upstream research, delegate to the web-research skill, then tie findings back to specific file paths and scope recommendations
- Check both https://docs.anthropic.com/en/docs/claude-code and https://opencode.ai/docs for official docs
