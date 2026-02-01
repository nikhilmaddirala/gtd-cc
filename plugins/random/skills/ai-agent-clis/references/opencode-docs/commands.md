Title: Commands

URL Source: https://opencode.ai/docs/commands/

Markdown Content:
Commands | OpenCode
===============
[Skip to content](https://opencode.ai/docs/commands/#_top)

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

*   [Overview](https://opencode.ai/docs/commands/#_top)
*   [Create command files](https://opencode.ai/docs/commands/#create-command-files)
*   [Configure](https://opencode.ai/docs/commands/#configure)
    *   [JSON](https://opencode.ai/docs/commands/#json)
    *   [Markdown](https://opencode.ai/docs/commands/#markdown)

*   [Prompt config](https://opencode.ai/docs/commands/#prompt-config)
    *   [Arguments](https://opencode.ai/docs/commands/#arguments)
    *   [Shell output](https://opencode.ai/docs/commands/#shell-output)
    *   [File references](https://opencode.ai/docs/commands/#file-references)

*   [Options](https://opencode.ai/docs/commands/#options)
    *   [Template](https://opencode.ai/docs/commands/#template)
    *   [Description](https://opencode.ai/docs/commands/#description)
    *   [Agent](https://opencode.ai/docs/commands/#agent)
    *   [Subtask](https://opencode.ai/docs/commands/#subtask)
    *   [Model](https://opencode.ai/docs/commands/#model)

*   [Built-in](https://opencode.ai/docs/commands/#built-in)

On this page
------------

*   [Overview](https://opencode.ai/docs/commands/#_top)
*   [Create command files](https://opencode.ai/docs/commands/#create-command-files)
*   [Configure](https://opencode.ai/docs/commands/#configure)
    *   [JSON](https://opencode.ai/docs/commands/#json)
    *   [Markdown](https://opencode.ai/docs/commands/#markdown)

*   [Prompt config](https://opencode.ai/docs/commands/#prompt-config)
    *   [Arguments](https://opencode.ai/docs/commands/#arguments)
    *   [Shell output](https://opencode.ai/docs/commands/#shell-output)
    *   [File references](https://opencode.ai/docs/commands/#file-references)

*   [Options](https://opencode.ai/docs/commands/#options)
    *   [Template](https://opencode.ai/docs/commands/#template)
    *   [Description](https://opencode.ai/docs/commands/#description)
    *   [Agent](https://opencode.ai/docs/commands/#agent)
    *   [Subtask](https://opencode.ai/docs/commands/#subtask)
    *   [Model](https://opencode.ai/docs/commands/#model)

*   [Built-in](https://opencode.ai/docs/commands/#built-in)

Commands
========

Create custom commands for repetitive tasks.

Custom commands let you specify a prompt you want to run when that command is executed in the TUI.

`/my-command`

Custom commands are in addition to the built-in commands like `/init`, `/undo`, `/redo`, `/share`, `/help`. [Learn more](https://opencode.ai/docs/tui#commands).

* * *

[Create command files](https://opencode.ai/docs/commands/#create-command-files)
-------------------------------------------------------------------------------

Create markdown files in the `commands/` directory to define custom commands.

Create `.opencode/commands/test.md`:

.opencode/commands/test.md

```
---description: Run tests with coverageagent: buildmodel: anthropic/claude-3-5-sonnet-20241022---
Run the full test suite with coverage report and show any failures.Focus on the failing tests and suggest fixes.
```

The frontmatter defines command properties. The content becomes the template.

Use the command by typing `/` followed by the command name.

`"/test"`

* * *

[Configure](https://opencode.ai/docs/commands/#configure)
---------------------------------------------------------

You can add custom commands through the OpenCode config or by creating markdown files in the `commands/` directory.

* * *

### [JSON](https://opencode.ai/docs/commands/#json)

Use the `command` option in your OpenCode [config](https://opencode.ai/docs/config):

opencode.jsonc

`{  "$schema": "https://opencode.ai/config.json",  "command": {    // This becomes the name of the command    "test": {      // This is the prompt that will be sent to the LLM      "template": "Run the full test suite with coverage report and show any failures.\nFocus on the failing tests and suggest fixes.",      // This is shown as the description in the TUI      "description": "Run tests with coverage",      "agent": "build",      "model": "anthropic/claude-3-5-sonnet-20241022"    }  }}`

Now you can run this command in the TUI:

`/test`

* * *

### [Markdown](https://opencode.ai/docs/commands/#markdown)

You can also define commands using markdown files. Place them in:

*   Global: `~/.config/opencode/commands/`
*   Per-project: `.opencode/commands/`

~/.config/opencode/commands/test.md

```
---description: Run tests with coverageagent: buildmodel: anthropic/claude-3-5-sonnet-20241022---
Run the full test suite with coverage report and show any failures.Focus on the failing tests and suggest fixes.
```

The markdown file name becomes the command name. For example, `test.md` lets you run:

`/test`

* * *

[Prompt config](https://opencode.ai/docs/commands/#prompt-config)
-----------------------------------------------------------------

The prompts for the custom commands support several special placeholders and syntax.

* * *

### [Arguments](https://opencode.ai/docs/commands/#arguments)

Pass arguments to commands using the `$ARGUMENTS` placeholder.

.opencode/commands/component.md

```
---description: Create a new component---
Create a new React component named $ARGUMENTS with TypeScript support.Include proper typing and basic structure.
```

Run the command with arguments:

`/component Button`

And `$ARGUMENTS` will be replaced with `Button`.

You can also access individual arguments using positional parameters:

*   `$1` - First argument
*   `$2` - Second argument
*   `$3` - Third argument
*   And so on…

For example:

.opencode/commands/create-file.md

```
---description: Create a new file with content---
Create a file named $1 in the directory $2with the following content: $3
```

Run the command:

`/create-file config.json src "{ \"key\": \"value\" }"`

This replaces:

*   `$1` with `config.json`
*   `$2` with `src`
*   `$3` with `{ "key": "value" }`

* * *

### [Shell output](https://opencode.ai/docs/commands/#shell-output)

Use _!`command`_ to inject [bash command](https://opencode.ai/docs/tui#bash-commands) output into your prompt.

For example, to create a custom command that analyzes test coverage:

.opencode/commands/analyze-coverage.md

```
---description: Analyze test coverage---
Here are the current test results:!`npm test`
Based on these results, suggest improvements to increase coverage.
```

Or to review recent changes:

.opencode/commands/review-changes.md

```
---description: Review recent changes---
Recent git commits:!`git log --oneline -10`
Review these changes and suggest any improvements.
```

Commands run in your project’s root directory and their output becomes part of the prompt.

* * *

### [File references](https://opencode.ai/docs/commands/#file-references)

Include files in your command using `@` followed by the filename.

.opencode/commands/review-component.md

```
---description: Review component---
Review the component in @src/components/Button.tsx.Check for performance issues and suggest improvements.
```

The file content gets included in the prompt automatically.

* * *

[Options](https://opencode.ai/docs/commands/#options)
-----------------------------------------------------

Let’s look at the configuration options in detail.

* * *

### [Template](https://opencode.ai/docs/commands/#template)

The `template` option defines the prompt that will be sent to the LLM when the command is executed.

opencode.json

`{  "command": {    "test": {      "template": "Run the full test suite with coverage report and show any failures.\nFocus on the failing tests and suggest fixes."    }  }}`

This is a **required** config option.

* * *

### [Description](https://opencode.ai/docs/commands/#description)

Use the `description` option to provide a brief description of what the command does.

opencode.json

`{  "command": {    "test": {      "description": "Run tests with coverage"    }  }}`

This is shown as the description in the TUI when you type in the command.

* * *

### [Agent](https://opencode.ai/docs/commands/#agent)

Use the `agent` config to optionally specify which [agent](https://opencode.ai/docs/agents) should execute this command. If this is a [subagent](https://opencode.ai/docs/agents/#subagents) the command will trigger a subagent invocation by default. To disable this behavior, set `subtask` to `false`.

opencode.json

`{  "command": {    "review": {      "agent": "plan"    }  }}`

This is an **optional** config option. If not specified, defaults to your current agent.

* * *

### [Subtask](https://opencode.ai/docs/commands/#subtask)

Use the `subtask` boolean to force the command to trigger a [subagent](https://opencode.ai/docs/agents/#subagents) invocation. This is useful if you want the command to not pollute your primary context and will **force** the agent to act as a subagent, even if `mode` is set to `primary` on the [agent](https://opencode.ai/docs/agents) configuration.

opencode.json

`{  "command": {    "analyze": {      "subtask": true    }  }}`

This is an **optional** config option.

* * *

### [Model](https://opencode.ai/docs/commands/#model)

Use the `model` config to override the default model for this command.

opencode.json

`{  "command": {    "analyze": {      "model": "anthropic/claude-3-5-sonnet-20241022"    }  }}`

This is an **optional** config option.

* * *

[Built-in](https://opencode.ai/docs/commands/#built-in)
-------------------------------------------------------

opencode includes several built-in commands like `/init`, `/undo`, `/redo`, `/share`, `/help`; [learn more](https://opencode.ai/docs/tui#commands).

Note

Custom commands can override built-in commands.

If you define a custom command with the same name, it will override the built-in command.

[Edit this page](https://github.com/anomalyco/opencode/edit/dev/packages/web/src/content/docs/commands.mdx)[Find a bug? Open an issue](https://github.com/anomalyco/opencode/issues/new)[Join our Discord community](https://opencode.ai/discord)

© [Anomaly](https://anoma.ly/)

Jan 31, 2026
