Title: LSP Servers

URL Source: https://opencode.ai/docs/lsp/

Markdown Content:
LSP Servers | OpenCode
===============
[Skip to content](https://opencode.ai/docs/lsp/#_top)

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

*   [Overview](https://opencode.ai/docs/lsp/#_top)
*   [Built-in](https://opencode.ai/docs/lsp/#built-in)
*   [How It Works](https://opencode.ai/docs/lsp/#how-it-works)
*   [Configure](https://opencode.ai/docs/lsp/#configure)
    *   [Environment variables](https://opencode.ai/docs/lsp/#environment-variables)
    *   [Initialization options](https://opencode.ai/docs/lsp/#initialization-options)
    *   [Disabling LSP servers](https://opencode.ai/docs/lsp/#disabling-lsp-servers)
    *   [Custom LSP servers](https://opencode.ai/docs/lsp/#custom-lsp-servers)

*   [Additional Information](https://opencode.ai/docs/lsp/#additional-information)
    *   [PHP Intelephense](https://opencode.ai/docs/lsp/#php-intelephense)

On this page
------------

*   [Overview](https://opencode.ai/docs/lsp/#_top)
*   [Built-in](https://opencode.ai/docs/lsp/#built-in)
*   [How It Works](https://opencode.ai/docs/lsp/#how-it-works)
*   [Configure](https://opencode.ai/docs/lsp/#configure)
    *   [Environment variables](https://opencode.ai/docs/lsp/#environment-variables)
    *   [Initialization options](https://opencode.ai/docs/lsp/#initialization-options)
    *   [Disabling LSP servers](https://opencode.ai/docs/lsp/#disabling-lsp-servers)
    *   [Custom LSP servers](https://opencode.ai/docs/lsp/#custom-lsp-servers)

*   [Additional Information](https://opencode.ai/docs/lsp/#additional-information)
    *   [PHP Intelephense](https://opencode.ai/docs/lsp/#php-intelephense)

LSP Servers
===========

OpenCode integrates with your LSP servers.

OpenCode integrates with your Language Server Protocol (LSP) to help the LLM interact with your codebase. It uses diagnostics to provide feedback to the LLM.

* * *

[Built-in](https://opencode.ai/docs/lsp/#built-in)
--------------------------------------------------

OpenCode comes with several built-in LSP servers for popular languages:

| LSP Server | Extensions | Requirements |
| --- | --- | --- |
| astro | .astro | Auto-installs for Astro projects |
| bash | .sh, .bash, .zsh, .ksh | Auto-installs bash-language-server |
| clangd | .c, .cpp, .cc, .cxx, .c++, .h, .hpp, .hh, .hxx, .h++ | Auto-installs for C/C++ projects |
| csharp | .cs | `.NET SDK` installed |
| clojure-lsp | .clj, .cljs, .cljc, .edn | `clojure-lsp` command available |
| dart | .dart | `dart` command available |
| deno | .ts, .tsx, .js, .jsx, .mjs | `deno` command available (auto-detects deno.json/deno.jsonc) |
| elixir-ls | .ex, .exs | `elixir` command available |
| eslint | .ts, .tsx, .js, .jsx, .mjs, .cjs, .mts, .cts, .vue | `eslint` dependency in project |
| fsharp | .fs, .fsi, .fsx, .fsscript | `.NET SDK` installed |
| gleam | .gleam | `gleam` command available |
| gopls | .go | `go` command available |
| jdtls | .java | `Java SDK (version 21+)` installed |
| kotlin-ls | .kt, .kts | Auto-installs for Kotlin projects |
| lua-ls | .lua | Auto-installs for Lua projects |
| nixd | .nix | `nixd` command available |
| ocaml-lsp | .ml, .mli | `ocamllsp` command available |
| oxlint | .ts, .tsx, .js, .jsx, .mjs, .cjs, .mts, .cts, .vue, .astro, .svelte | `oxlint` dependency in project |
| php intelephense | .php | Auto-installs for PHP projects |
| prisma | .prisma | `prisma` command available |
| pyright | .py, .pyi | `pyright` dependency installed |
| ruby-lsp (rubocop) | .rb, .rake, .gemspec, .ru | `ruby` and `gem` commands available |
| rust | .rs | `rust-analyzer` command available |
| sourcekit-lsp | .swift, .objc, .objcpp | `swift` installed (`xcode` on macOS) |
| svelte | .svelte | Auto-installs for Svelte projects |
| terraform | .tf, .tfvars | Auto-installs from GitHub releases |
| tinymist | .typ, .typc | Auto-installs from GitHub releases |
| typescript | .ts, .tsx, .js, .jsx, .mjs, .cjs, .mts, .cts | `typescript` dependency in project |
| vue | .vue | Auto-installs for Vue projects |
| yaml-ls | .yaml, .yml | Auto-installs Red Hat yaml-language-server |
| zls | .zig, .zon | `zig` command available |

LSP servers are automatically enabled when one of the above file extensions are detected and the requirements are met.

Note

You can disable automatic LSP server downloads by setting the `OPENCODE_DISABLE_LSP_DOWNLOAD` environment variable to `true`.

* * *

[How It Works](https://opencode.ai/docs/lsp/#how-it-works)
----------------------------------------------------------

When opencode opens a file, it:

1.   Checks the file extension against all enabled LSP servers.
2.   Starts the appropriate LSP server if not already running.

* * *

[Configure](https://opencode.ai/docs/lsp/#configure)
----------------------------------------------------

You can customize LSP servers through the `lsp` section in your opencode config.

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "lsp": {}}`

Each LSP server supports the following:

| Property | Type | Description |
| --- | --- | --- |
| `disabled` | boolean | Set this to `true` to disable the LSP server |
| `command` | string[] | The command to start the LSP server |
| `extensions` | string[] | File extensions this LSP server should handle |
| `env` | object | Environment variables to set when starting server |
| `initialization` | object | Initialization options to send to the LSP server |

Let’s look at some examples.

* * *

### [Environment variables](https://opencode.ai/docs/lsp/#environment-variables)

Use the `env` property to set environment variables when starting the LSP server:

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "lsp": {    "rust": {      "env": {        "RUST_LOG": "debug"      }    }  }}`

* * *

### [Initialization options](https://opencode.ai/docs/lsp/#initialization-options)

Use the `initialization` property to pass initialization options to the LSP server. These are server-specific settings sent during the LSP `initialize` request:

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "lsp": {    "typescript": {      "initialization": {        "preferences": {          "importModuleSpecifierPreference": "relative"        }      }    }  }}`

Note

Initialization options vary by LSP server. Check your LSP server’s documentation for available options.

* * *

### [Disabling LSP servers](https://opencode.ai/docs/lsp/#disabling-lsp-servers)

To disable **all** LSP servers globally, set `lsp` to `false`:

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "lsp": false}`

To disable a **specific** LSP server, set `disabled` to `true`:

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "lsp": {    "typescript": {      "disabled": true    }  }}`

* * *

### [Custom LSP servers](https://opencode.ai/docs/lsp/#custom-lsp-servers)

You can add custom LSP servers by specifying the command and file extensions:

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "lsp": {    "custom-lsp": {      "command": ["custom-lsp-server", "--stdio"],      "extensions": [".custom"]    }  }}`

* * *

[Additional Information](https://opencode.ai/docs/lsp/#additional-information)
------------------------------------------------------------------------------

### [PHP Intelephense](https://opencode.ai/docs/lsp/#php-intelephense)

PHP Intelephense offers premium features through a license key. You can provide a license key by placing (only) the key in a text file at:

*   On macOS/Linux: `$HOME/intelephense/licence.txt`
*   On Windows: `%USERPROFILE%/intelephense/licence.txt`

The file should contain only the license key with no additional content.

[Edit this page](https://github.com/anomalyco/opencode/edit/dev/packages/web/src/content/docs/lsp.mdx)[Find a bug? Open an issue](https://github.com/anomalyco/opencode/issues/new)[Join our Discord community](https://opencode.ai/discord)

© [Anomaly](https://anoma.ly/)

Jan 31, 2026
