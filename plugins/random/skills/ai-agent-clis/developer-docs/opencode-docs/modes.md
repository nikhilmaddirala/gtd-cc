Title: Modes

URL Source: https://opencode.ai/docs/modes/

Markdown Content:
Modes | OpenCode
===============
[Skip to content](https://opencode.ai/docs/modes/#_top)

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

*   [Overview](https://opencode.ai/docs/modes/#_top)
*   [Built-in](https://opencode.ai/docs/modes/#built-in)
    *   [Build](https://opencode.ai/docs/modes/#build)
    *   [Plan](https://opencode.ai/docs/modes/#plan)

*   [Switching](https://opencode.ai/docs/modes/#switching)
*   [Configure](https://opencode.ai/docs/modes/#configure)
    *   [JSON Configuration](https://opencode.ai/docs/modes/#json-configuration)
    *   [Markdown Configuration](https://opencode.ai/docs/modes/#markdown-configuration)
    *   [Model](https://opencode.ai/docs/modes/#model)
    *   [Temperature](https://opencode.ai/docs/modes/#temperature)
    *   [Prompt](https://opencode.ai/docs/modes/#prompt)
    *   [Tools](https://opencode.ai/docs/modes/#tools)

*   [Custom modes](https://opencode.ai/docs/modes/#custom-modes)
    *   [Using JSON configuration](https://opencode.ai/docs/modes/#using-json-configuration)
    *   [Using markdown files](https://opencode.ai/docs/modes/#using-markdown-files)
    *   [Use cases](https://opencode.ai/docs/modes/#use-cases)

On this page
------------

*   [Overview](https://opencode.ai/docs/modes/#_top)
*   [Built-in](https://opencode.ai/docs/modes/#built-in)
    *   [Build](https://opencode.ai/docs/modes/#build)
    *   [Plan](https://opencode.ai/docs/modes/#plan)

*   [Switching](https://opencode.ai/docs/modes/#switching)
*   [Configure](https://opencode.ai/docs/modes/#configure)
    *   [JSON Configuration](https://opencode.ai/docs/modes/#json-configuration)
    *   [Markdown Configuration](https://opencode.ai/docs/modes/#markdown-configuration)
    *   [Model](https://opencode.ai/docs/modes/#model)
    *   [Temperature](https://opencode.ai/docs/modes/#temperature)
    *   [Prompt](https://opencode.ai/docs/modes/#prompt)
    *   [Tools](https://opencode.ai/docs/modes/#tools)

*   [Custom modes](https://opencode.ai/docs/modes/#custom-modes)
    *   [Using JSON configuration](https://opencode.ai/docs/modes/#using-json-configuration)
    *   [Using markdown files](https://opencode.ai/docs/modes/#using-markdown-files)
    *   [Use cases](https://opencode.ai/docs/modes/#use-cases)

Modes
=====

Different modes for different use cases.

Caution

Modes are now configured through the `agent` option in the opencode config. The `mode` option is now deprecated. [Learn more](https://opencode.ai/docs/agents).

Modes in opencode allow you to customize the behavior, tools, and prompts for different use cases.

It comes with two built-in modes: **build** and **plan**. You can customize these or configure your own through the opencode config.

You can switch between modes during a session or configure them in your config file.

* * *

[Built-in](https://opencode.ai/docs/modes/#built-in)
----------------------------------------------------

opencode comes with two built-in modes.

* * *

### [Build](https://opencode.ai/docs/modes/#build)

Build is the **default** mode with all tools enabled. This is the standard mode for development work where you need full access to file operations and system commands.

* * *

### [Plan](https://opencode.ai/docs/modes/#plan)

A restricted mode designed for planning and analysis. In plan mode, the following tools are disabled by default:

*   `write` - Cannot create new files
*   `edit` - Cannot modify existing files, except for files located at `.opencode/plans/*.md` to detail the plan itself
*   `patch` - Cannot apply patches
*   `bash` - Cannot execute shell commands

This mode is useful when you want the AI to analyze code, suggest changes, or create plans without making any actual modifications to your codebase.

* * *

[Switching](https://opencode.ai/docs/modes/#switching)
------------------------------------------------------

You can switch between modes during a session using the _Tab_ key. Or your configured `switch_mode` keybind.

See also: [Formatters](https://opencode.ai/docs/formatters) for information about code formatting configuration.

* * *

[Configure](https://opencode.ai/docs/modes/#configure)
------------------------------------------------------

You can customize the built-in modes or create your own through configuration. Modes can be configured in two ways:

### [JSON Configuration](https://opencode.ai/docs/modes/#json-configuration)

Configure modes in your `opencode.json` config file:

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "mode": {    "build": {      "model": "anthropic/claude-sonnet-4-20250514",      "prompt": "{file:./prompts/build.txt}",      "tools": {        "write": true,        "edit": true,        "bash": true      }    },    "plan": {      "model": "anthropic/claude-haiku-4-20250514",      "tools": {        "write": false,        "edit": false,        "bash": false      }    }  }}`

### [Markdown Configuration](https://opencode.ai/docs/modes/#markdown-configuration)

You can also define modes using markdown files. Place them in:

*   Global: `~/.config/opencode/modes/`
*   Project: `.opencode/modes/`

~/.config/opencode/modes/review.md

```
---model: anthropic/claude-sonnet-4-20250514temperature: 0.1tools:  write: false  edit: false  bash: false---
You are in code review mode. Focus on:
- Code quality and best practices- Potential bugs and edge cases- Performance implications- Security considerations
Provide constructive feedback without making direct changes.
```

The markdown file name becomes the mode name (e.g., `review.md` creates a `review` mode).

Let’s look at these configuration options in detail.

* * *

### [Model](https://opencode.ai/docs/modes/#model)

Use the `model` config to override the default model for this mode. Useful for using different models optimized for different tasks. For example, a faster model for planning, a more capable model for implementation.

opencode.json

`{  "mode": {    "plan": {      "model": "anthropic/claude-haiku-4-20250514"    }  }}`

* * *

### [Temperature](https://opencode.ai/docs/modes/#temperature)

Control the randomness and creativity of the AI’s responses with the `temperature` config. Lower values make responses more focused and deterministic, while higher values increase creativity and variability.

opencode.json

`{  "mode": {    "plan": {      "temperature": 0.1    },    "creative": {      "temperature": 0.8    }  }}`

Temperature values typically range from 0.0 to 1.0:

*   **0.0-0.2**: Very focused and deterministic responses, ideal for code analysis and planning
*   **0.3-0.5**: Balanced responses with some creativity, good for general development tasks
*   **0.6-1.0**: More creative and varied responses, useful for brainstorming and exploration

opencode.json

`{  "mode": {    "analyze": {      "temperature": 0.1,      "prompt": "{file:./prompts/analysis.txt}"    },    "build": {      "temperature": 0.3    },    "brainstorm": {      "temperature": 0.7,      "prompt": "{file:./prompts/creative.txt}"    }  }}`

If no temperature is specified, opencode uses model-specific defaults (typically 0 for most models, 0.55 for Qwen models).

* * *

### [Prompt](https://opencode.ai/docs/modes/#prompt)

Specify a custom system prompt file for this mode with the `prompt` config. The prompt file should contain instructions specific to the mode’s purpose.

opencode.json

`{  "mode": {    "review": {      "prompt": "{file:./prompts/code-review.txt}"    }  }}`

This path is relative to where the config file is located. So this works for both the global opencode config and the project specific config.

* * *

### [Tools](https://opencode.ai/docs/modes/#tools)

Control which tools are available in this mode with the `tools` config. You can enable or disable specific tools by setting them to `true` or `false`.

`{  "mode": {    "readonly": {      "tools": {        "write": false,        "edit": false,        "bash": false,        "read": true,        "grep": true,        "glob": true      }    }  }}`

If no tools are specified, all tools are enabled by default.

* * *

#### [Available tools](https://opencode.ai/docs/modes/#available-tools)

Here are all the tools can be controlled through the mode config.

| Tool | Description |
| --- | --- |
| `bash` | Execute shell commands |
| `edit` | Modify existing files |
| `write` | Create new files |
| `read` | Read file contents |
| `grep` | Search file contents |
| `glob` | Find files by pattern |
| `list` | List directory contents |
| `patch` | Apply patches to files |
| `todowrite` | Manage todo lists |
| `todoread` | Read todo lists |
| `webfetch` | Fetch web content |

* * *

[Custom modes](https://opencode.ai/docs/modes/#custom-modes)
------------------------------------------------------------

You can create your own custom modes by adding them to the configuration. Here are examples using both approaches:

### [Using JSON configuration](https://opencode.ai/docs/modes/#using-json-configuration)

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "mode": {    "docs": {      "prompt": "{file:./prompts/documentation.txt}",      "tools": {        "write": true,        "edit": true,        "bash": false,        "read": true,        "grep": true,        "glob": true      }    }  }}`

### [Using markdown files](https://opencode.ai/docs/modes/#using-markdown-files)

Create mode files in `.opencode/modes/` for project-specific modes or `~/.config/opencode/modes/` for global modes:

.opencode/modes/debug.md

```
---temperature: 0.1tools:  bash: true  read: true  grep: true  write: false  edit: false---
You are in debug mode. Your primary goal is to help investigate and diagnose issues.
Focus on:
- Understanding the problem through careful analysis- Using bash commands to inspect system state- Reading relevant files and logs- Searching for patterns and anomalies- Providing clear explanations of findings
Do not make any changes to files. Only investigate and report.
```

~/.config/opencode/modes/refactor.md

```
---model: anthropic/claude-sonnet-4-20250514temperature: 0.2tools:  edit: true  read: true  grep: true  glob: true---
You are in refactoring mode. Focus on improving code quality without changing functionality.
Priorities:
- Improve code readability and maintainability- Apply consistent naming conventions- Reduce code duplication- Optimize performance where appropriate- Ensure all tests continue to pass
```

* * *

### [Use cases](https://opencode.ai/docs/modes/#use-cases)

Here are some common use cases for different modes.

*   **Build mode**: Full development work with all tools enabled
*   **Plan mode**: Analysis and planning without making changes
*   **Review mode**: Code review with read-only access plus documentation tools
*   **Debug mode**: Focused on investigation with bash and read tools enabled
*   **Docs mode**: Documentation writing with file operations but no system commands

You might also find different models are good for different use cases.

[Edit this page](https://github.com/anomalyco/opencode/edit/dev/packages/web/src/content/docs/modes.mdx)[Find a bug? Open an issue](https://github.com/anomalyco/opencode/issues/new)[Join our Discord community](https://opencode.ai/discord)

© [Anomaly](https://anoma.ly/)

Jan 31, 2026
