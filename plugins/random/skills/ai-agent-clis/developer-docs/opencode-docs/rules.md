Title: Rules

URL Source: https://opencode.ai/docs/rules/

Markdown Content:
Rules | OpenCode
===============
[Skip to content](https://opencode.ai/docs/rules/#_top)

[![Image 1](https://opencode.ai/docs/_astro/logo-dark.DOStV66V.svg)![Image 2](https://opencode.ai/docs/_astro/logo-light.B0yzR0O5.svg) OpenCode](https://opencode.ai/)

[Home](https://opencode.ai/)[Docs](https://opencode.ai/docs/)

[](https://github.com/anomalyco/opencode)[](https://opencode.ai/discord)

Search Ctrl K

 Cancel 

*   [Intro](https://opencode.ai/docs/)
*   [Config](https://opencode.ai/docs/config/)
*   [Providers](https://opencode.ai/docs/providers/)
*   [Network](https://opencode.ai/docs/network/)
*   [Enterprise](https://opencode.ai/docs/enterprise/)
*   [Troubleshooting](https://opencode.ai/docs/troubleshooting/)
*   [Migrating to 1.0](https://opencode.ai/docs/1-0/)
*   
Usage 
    *   [TUI](https://opencode.ai/docs/tui/)
    *   [CLI](https://opencode.ai/docs/cli/)
    *   [Web](https://opencode.ai/docs/web/)
    *   [IDE](https://opencode.ai/docs/ide/)
    *   [Zen](https://opencode.ai/docs/zen/)
    *   [Share](https://opencode.ai/docs/share/)
    *   [GitHub](https://opencode.ai/docs/github/)
    *   [GitLab](https://opencode.ai/docs/gitlab/)

*   
Configure 
    *   [Tools](https://opencode.ai/docs/tools/)
    *   [Rules](https://opencode.ai/docs/rules/)
    *   [Agents](https://opencode.ai/docs/agents/)
    *   [Models](https://opencode.ai/docs/models/)
    *   [Themes](https://opencode.ai/docs/themes/)
    *   [Keybinds](https://opencode.ai/docs/keybinds/)
    *   [Commands](https://opencode.ai/docs/commands/)
    *   [Formatters](https://opencode.ai/docs/formatters/)
    *   [Permissions](https://opencode.ai/docs/permissions/)
    *   [LSP Servers](https://opencode.ai/docs/lsp/)
    *   [MCP servers](https://opencode.ai/docs/mcp-servers/)
    *   [ACP Support](https://opencode.ai/docs/acp/)
    *   [Agent Skills](https://opencode.ai/docs/skills/)
    *   [Custom Tools](https://opencode.ai/docs/custom-tools/)

*   
Develop 
    *   [SDK](https://opencode.ai/docs/sdk/)
    *   [Server](https://opencode.ai/docs/server/)
    *   [Plugins](https://opencode.ai/docs/plugins/)
    *   [Ecosystem](https://opencode.ai/docs/ecosystem/)

[GitHub](https://github.com/anomalyco/opencode)[Discord](https://opencode.ai/discord)

Select theme 

On this page

*   [Overview](https://opencode.ai/docs/rules/#_top)
*   [Initialize](https://opencode.ai/docs/rules/#initialize)
*   [Example](https://opencode.ai/docs/rules/#example)
*   [Types](https://opencode.ai/docs/rules/#types)
    *   [Project](https://opencode.ai/docs/rules/#project)
    *   [Global](https://opencode.ai/docs/rules/#global)
    *   [Claude Code Compatibility](https://opencode.ai/docs/rules/#claude-code-compatibility)

*   [Precedence](https://opencode.ai/docs/rules/#precedence)
*   [Custom Instructions](https://opencode.ai/docs/rules/#custom-instructions)
*   [Referencing External Files](https://opencode.ai/docs/rules/#referencing-external-files)
    *   [Using opencode.json](https://opencode.ai/docs/rules/#using-opencodejson)
    *   [Manual Instructions in AGENTS.md](https://opencode.ai/docs/rules/#manual-instructions-in-agentsmd)

On this page
------------

*   [Overview](https://opencode.ai/docs/rules/#_top)
*   [Initialize](https://opencode.ai/docs/rules/#initialize)
*   [Example](https://opencode.ai/docs/rules/#example)
*   [Types](https://opencode.ai/docs/rules/#types)
    *   [Project](https://opencode.ai/docs/rules/#project)
    *   [Global](https://opencode.ai/docs/rules/#global)
    *   [Claude Code Compatibility](https://opencode.ai/docs/rules/#claude-code-compatibility)

*   [Precedence](https://opencode.ai/docs/rules/#precedence)
*   [Custom Instructions](https://opencode.ai/docs/rules/#custom-instructions)
*   [Referencing External Files](https://opencode.ai/docs/rules/#referencing-external-files)
    *   [Using opencode.json](https://opencode.ai/docs/rules/#using-opencodejson)
    *   [Manual Instructions in AGENTS.md](https://opencode.ai/docs/rules/#manual-instructions-in-agentsmd)

Rules
=====

Set custom instructions for opencode.

You can provide custom instructions to opencode by creating an `AGENTS.md` file. This is similar to Cursor’s rules. It contains instructions that will be included in the LLM’s context to customize its behavior for your specific project.

* * *

[Initialize](https://opencode.ai/docs/rules/#initialize)
--------------------------------------------------------

To create a new `AGENTS.md` file, you can run the `/init` command in opencode.

Tip

You should commit your project’s `AGENTS.md` file to Git.

This will scan your project and all its contents to understand what the project is about and generate an `AGENTS.md` file with it. This helps opencode to navigate the project better.

If you have an existing `AGENTS.md` file, this will try to add to it.

* * *

[Example](https://opencode.ai/docs/rules/#example)
--------------------------------------------------

You can also just create this file manually. Here’s an example of some things you can put into an `AGENTS.md` file.

AGENTS.md

```
# SST v3 Monorepo Project
This is an SST v3 monorepo with TypeScript. The project uses bun workspaces for package management.
## Project Structure
- `packages/` - Contains all workspace packages (functions, core, web, etc.)- `infra/` - Infrastructure definitions split by service (storage.ts, api.ts, web.ts)- `sst.config.ts` - Main SST configuration with dynamic imports
## Code Standards
- Use TypeScript with strict mode enabled- Shared code goes in `packages/core/` with proper exports configuration- Functions go in `packages/functions/`- Infrastructure should be split into logical files in `infra/`
## Monorepo Conventions
- Import shared modules using workspace names: `@my-app/core/example`
```

We are adding project-specific instructions here and this will be shared across your team.

* * *

[Types](https://opencode.ai/docs/rules/#types)
----------------------------------------------

opencode also supports reading the `AGENTS.md` file from multiple locations. And this serves different purposes.

### [Project](https://opencode.ai/docs/rules/#project)

Place an `AGENTS.md` in your project root for project-specific rules. These only apply when you are working in this directory or its sub-directories.

### [Global](https://opencode.ai/docs/rules/#global)

You can also have global rules in a `~/.config/opencode/AGENTS.md` file. This gets applied across all opencode sessions.

Since this isn’t committed to Git or shared with your team, we recommend using this to specify any personal rules that the LLM should follow.

### [Claude Code Compatibility](https://opencode.ai/docs/rules/#claude-code-compatibility)

For users migrating from Claude Code, OpenCode supports Claude Code’s file conventions as fallbacks:

*   **Project rules**: `CLAUDE.md` in your project directory (used if no `AGENTS.md` exists)
*   **Global rules**: `~/.claude/CLAUDE.md` (used if no `~/.config/opencode/AGENTS.md` exists)
*   **Skills**: `~/.claude/skills/` — see [Agent Skills](https://opencode.ai/docs/skills/) for details

To disable Claude Code compatibility, set one of these environment variables:

Terminal window

`export OPENCODE_DISABLE_CLAUDE_CODE=1        # Disable all .claude supportexport OPENCODE_DISABLE_CLAUDE_CODE_PROMPT=1 # Disable only ~/.claude/CLAUDE.mdexport OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1 # Disable only .claude/skills`

* * *

[Precedence](https://opencode.ai/docs/rules/#precedence)
--------------------------------------------------------

When opencode starts, it looks for rule files in this order:

1.   **Local files** by traversing up from the current directory (`AGENTS.md`, `CLAUDE.md`)
2.   **Global file** at `~/.config/opencode/AGENTS.md`
3.   **Claude Code file** at `~/.claude/CLAUDE.md` (unless disabled)

The first matching file wins in each category. For example, if you have both `AGENTS.md` and `CLAUDE.md`, only `AGENTS.md` is used. Similarly, `~/.config/opencode/AGENTS.md` takes precedence over `~/.claude/CLAUDE.md`.

* * *

[Custom Instructions](https://opencode.ai/docs/rules/#custom-instructions)
--------------------------------------------------------------------------

You can specify custom instruction files in your `opencode.json` or the global `~/.config/opencode/opencode.json`. This allows you and your team to reuse existing rules rather than having to duplicate them to AGENTS.md.

Example:

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "instructions": ["CONTRIBUTING.md", "docs/guidelines.md", ".cursor/rules/*.md"]}`

You can also use remote URLs to load instructions from the web.

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "instructions": ["https://raw.githubusercontent.com/my-org/shared-rules/main/style.md"]}`

Remote instructions are fetched with a 5 second timeout.

All instruction files are combined with your `AGENTS.md` files.

* * *

[Referencing External Files](https://opencode.ai/docs/rules/#referencing-external-files)
----------------------------------------------------------------------------------------

While opencode doesn’t automatically parse file references in `AGENTS.md`, you can achieve similar functionality in two ways:

### [Using opencode.json](https://opencode.ai/docs/rules/#using-opencodejson)

The recommended approach is to use the `instructions` field in `opencode.json`:

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "instructions": ["docs/development-standards.md", "test/testing-guidelines.md", "packages/*/AGENTS.md"]}`

### [Manual Instructions in AGENTS.md](https://opencode.ai/docs/rules/#manual-instructions-in-agentsmd)

You can teach opencode to read external files by providing explicit instructions in your `AGENTS.md`. Here’s a practical example:

AGENTS.md

```
# TypeScript Project Rules
## External File Loading
CRITICAL: When you encounter a file reference (e.g., @rules/general.md), use your Read tool to load it on a need-to-know basis. They're relevant to the SPECIFIC task at hand.
Instructions:
- Do NOT preemptively load all references - use lazy loading based on actual need- When loaded, treat content as mandatory instructions that override defaults- Follow references recursively when needed
## Development Guidelines
For TypeScript code style and best practices: @docs/typescript-guidelines.mdFor React component architecture and hooks patterns: @docs/react-patterns.mdFor REST API design and error handling: @docs/api-standards.mdFor testing strategies and coverage requirements: @test/testing-guidelines.md
## General Guidelines
Read the following file immediately as it's relevant to all workflows: @rules/general-guidelines.md.
```

This approach allows you to:

*   Create modular, reusable rule files
*   Share rules across projects via symlinks or git submodules
*   Keep AGENTS.md concise while referencing detailed guidelines
*   Ensure opencode loads files only when needed for the specific task

Tip

For monorepos or projects with shared standards, using `opencode.json` with glob patterns (like `packages/*/AGENTS.md`) is more maintainable than manual instructions.

[Edit this page](https://github.com/anomalyco/opencode/edit/dev/packages/web/src/content/docs/rules.mdx)[Find a bug? Open an issue](https://github.com/anomalyco/opencode/issues/new)[Join our Discord community](https://opencode.ai/discord)

© [Anomaly](https://anoma.ly/)

Jan 31, 2026
