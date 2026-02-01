Title: ACP Support

URL Source: https://opencode.ai/docs/acp/

Markdown Content:
ACP Support | OpenCode
===============
[Skip to content](https://opencode.ai/docs/acp/#_top)

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

*   [Overview](https://opencode.ai/docs/acp/#_top)
*   [Configure](https://opencode.ai/docs/acp/#configure)
    *   [Zed](https://opencode.ai/docs/acp/#zed)
    *   [JetBrains IDEs](https://opencode.ai/docs/acp/#jetbrains-ides)
    *   [Avante.nvim](https://opencode.ai/docs/acp/#avantenvim)
    *   [CodeCompanion.nvim](https://opencode.ai/docs/acp/#codecompanionnvim)

*   [Support](https://opencode.ai/docs/acp/#support)

On this page
------------

*   [Overview](https://opencode.ai/docs/acp/#_top)
*   [Configure](https://opencode.ai/docs/acp/#configure)
    *   [Zed](https://opencode.ai/docs/acp/#zed)
    *   [JetBrains IDEs](https://opencode.ai/docs/acp/#jetbrains-ides)
    *   [Avante.nvim](https://opencode.ai/docs/acp/#avantenvim)
    *   [CodeCompanion.nvim](https://opencode.ai/docs/acp/#codecompanionnvim)

*   [Support](https://opencode.ai/docs/acp/#support)

ACP Support
===========

Use OpenCode in any ACP-compatible editor.

OpenCode supports the [Agent Client Protocol](https://agentclientprotocol.com/) or (ACP), allowing you to use it directly in compatible editors and IDEs.

Tip

For a list of editors and tools that support ACP, check out the [ACP progress report](https://zed.dev/blog/acp-progress-report#available-now).

ACP is an open protocol that standardizes communication between code editors and AI coding agents.

* * *

[Configure](https://opencode.ai/docs/acp/#configure)
----------------------------------------------------

To use OpenCode via ACP, configure your editor to run the `opencode acp` command.

The command starts OpenCode as an ACP-compatible subprocess that communicates with your editor over JSON-RPC via stdio.

Below are examples for popular editors that support ACP.

* * *

### [Zed](https://opencode.ai/docs/acp/#zed)

Add to your [Zed](https://zed.dev/) configuration (`~/.config/zed/settings.json`):

~/.config/zed/settings.json

`{  "agent_servers": {    "OpenCode": {      "command": "opencode",      "args": ["acp"]    }  }}`

To open it, use the `agent: new thread` action in the **Command Palette**.

You can also bind a keyboard shortcut by editing your `keymap.json`:

keymap.json

`[  {    "bindings": {      "cmd-alt-o": [        "agent::NewExternalAgentThread",        {          "agent": {            "custom": {              "name": "OpenCode",              "command": {                "command": "opencode",                "args": ["acp"]              }            }          }        }      ]    }  }]`

* * *

### [JetBrains IDEs](https://opencode.ai/docs/acp/#jetbrains-ides)

Add to your [JetBrains IDE](https://www.jetbrains.com/) acp.json according to the [documentation](https://www.jetbrains.com/help/ai-assistant/acp.html):

acp.json

`{  "agent_servers": {    "OpenCode": {      "command": "/absolute/path/bin/opencode",      "args": ["acp"]    }  }}`

To open it, use the new ‘OpenCode’ agent in the AI Chat agent selector.

* * *

### [Avante.nvim](https://opencode.ai/docs/acp/#avantenvim)

Add to your [Avante.nvim](https://github.com/yetone/avante.nvim) configuration:

`{  acp_providers = {    ["opencode"] = {      command = "opencode",      args = { "acp" }    }  }}`

If you need to pass environment variables:

`{  acp_providers = {    ["opencode"] = {      command = "opencode",      args = { "acp" },      env = {        OPENCODE_API_KEY = os.getenv("OPENCODE_API_KEY")      }    }  }}`

* * *

### [CodeCompanion.nvim](https://opencode.ai/docs/acp/#codecompanionnvim)

To use OpenCode as an ACP agent in [CodeCompanion.nvim](https://github.com/olimorris/codecompanion.nvim), add the following to your Neovim config:

`require("codecompanion").setup({  interactions = {    chat = {      adapter = {        name = "opencode",        model = "claude-sonnet-4",      },    },  },})`

This config sets up CodeCompanion to use OpenCode as the ACP agent for chat.

If you need to pass environment variables (like `OPENCODE_API_KEY`), refer to [Configuring Adapters: Environment Variables](https://codecompanion.olimorris.dev/getting-started#setting-an-api-key) in the CodeCompanion.nvim documentation for full details.

[Support](https://opencode.ai/docs/acp/#support)
------------------------------------------------

OpenCode works the same via ACP as it does in the terminal. All features are supported:

Note

Some built-in slash commands like `/undo` and `/redo` are currently unsupported.

*   Built-in tools (file operations, terminal commands, etc.)
*   Custom tools and slash commands
*   MCP servers configured in your OpenCode config
*   Project-specific rules from `AGENTS.md`
*   Custom formatters and linters
*   Agents and permissions system

[Edit this page](https://github.com/anomalyco/opencode/edit/dev/packages/web/src/content/docs/acp.mdx)[Find a bug? Open an issue](https://github.com/anomalyco/opencode/issues/new)[Join our Discord community](https://opencode.ai/discord)

© [Anomaly](https://anoma.ly/)

Jan 31, 2026
