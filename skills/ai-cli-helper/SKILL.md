---
name: ai-cli-helper
description: View and manage configurations and skills for AI agent CLI tools (Claude Code, Opencode). Use when checking config files, listing or managing skills, viewing model settings, comparing configs across tools, or performing common config operations.
---

# AI CLI helper

## Overview

This skill manages configuration and skills for AI agent CLI tools (Claude Code, Opencode). It understands the full config stack — from user settings through project and local scopes — and can inspect, modify, debug, synchronize, and research configuration across both tools.

Use this skill when:
- Installing, updating, or managing skills
- Inspecting or modifying configs at any scope
- Debugging config conflicts, scope issues, or skill activation failures
- Comparing or syncing settings between Claude Code and Opencode
- Researching latest upstream config options and applying them


## Context

The user runs both Claude Code and Opencode, managed declaratively (e.g. via Nix, dotfiles, etc.). Both tools share agent instructions (AGENTS.md) and skills via `.agents/skills/`. The detailed setup for each tool is documented in the references/ directory.


## Process

IMPORTANT: for skill install/remove requests where the user gives specific paths or names, go directly to the manage-skills subskill and execute. Do NOT read references, explore the codebase, or assess state first. Run the right command directly: `npx skills` for remote sources and `local-skills.py` for local filesystem sources.

For everything else:
- Inspection/debugging: read the relevant reference doc, then read config files
- Config modifications: see manage-configs subskill
- Skill operations (open-ended): see manage-skills subskill
- Research: delegate to web-research skill
- Verify results after changes


## Resources

- **subskills/manage-skills.md**: install, update, discover, and audit skills with a hybrid flow (`npx skills` for remote, `local-skills.py` for local)
- **subskills/manage-configs.md**: inspect and modify config files, rebuild workflow, scope rules
- **references/opencode-config.md**: Opencode config structure, config management, oh-my-opencode, agent modes
- **references/vercel-skills.md**: `npx skills` CLI disk model, gotchas, recommended usage patterns
- **references/claude-code-plugins.md**: legacy plugin system reference — for diagnosing plugin conflicts and cleaning up old installs only


## Guidelines

### Skill management

- Use a hybrid model for skill activation:
  - Remote skills (`owner/repo`) -> `npx skills`
  - Local monorepo skills (filesystem paths) -> `scripts/local-skills.py` (`npx add` bootstrap + symlink swap)
- Never use `claude plugin install/remove/enable/disable` for managing skills — the plugin system is deprecated for this purpose
- After skill changes, verify with both `npx skills list` and `scripts/local-skills.py list`
- For development iteration on monorepo skills, prefer `scripts/local-skills.py` because it symlinks instead of copying

### Scope and editability

- User-level settings may be declaratively managed (e.g. via Nix). See the manage-configs subskill before editing directly.
- Project-level settings are checked into git and can be edited directly
- Local settings (`.claude/settings.local.json`) are gitignored and can be edited directly
- When unsure which scope to modify, prefer project scope

### Cross-tool awareness

- Claude Code and Opencode share skills via `.agents/skills/` (canonical store, managed by `npx skills` for remote skills and symlinks for local skills)
- Both tools reference the same AGENTS.md
- Config concepts overlap but syntax differs — always check both reference docs when comparing
- Claude Code uses `settings.json` with hooks/permissions; Opencode uses `opencode.json` with agent modes and permission blocks

### Legacy plugin conflicts

- Old plugins may still be installed from before the migration to `npx skills`
- If a skill isn't loading correctly or behavior is unexpected, check for stale `enabledPlugins` in settings.json and legacy entries in `~/.claude/plugins/installed_plugins.json`
- Use `references/claude-code-plugins.md` for the commands needed to inspect and uninstall legacy plugins
- Run `claude plugin list` to check for stale plugin installs that may conflict

### Research

- For upstream research, delegate to the web-research skill
- Always tie findings back to "here's what this means for your setup" with specific file paths and scope recommendations
- Check both https://docs.anthropic.com/en/docs/claude-code and https://opencode.ai/docs for official docs

### General

- Only read reference docs when the task requires understanding config structure or debugging — not for straightforward install/remove operations
- When presenting config state, show all three layers (user -> project -> local) to make precedence clear


## Appendix

### Quick reference: CLI commands

```bash
# Skill operations (remote/GitHub via npx skills)
npx skills list                                              # show installed skills
npx skills list -g                                           # show global skills
npx skills add owner/repo --skill name -a claude-code -y     # install from GitHub
npx skills remove --skill name -y                            # remove from all agents

# Skill operations (local filesystem via local-skills.py)
./scripts/local-skills.py add ./path/to/my-skill -a claude-code opencode
./scripts/local-skills.py remove --skill my-skill -a claude-code opencode
./scripts/local-skills.py list

# Discovery
./scripts/discover-skills.py /path/to/monorepo  # writes unified discovery+activation manifest

# Legacy plugin inspection (for debugging conflicts only)
claude plugin list                                           # check for stale installs
claude plugin uninstall name@marketplace --scope project     # clean up legacy plugin

# Opencode
opencode --version
# Opencode plugins managed via oh-my-opencode.json and bun dependencies
```
