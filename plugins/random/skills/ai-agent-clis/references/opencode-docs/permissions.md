Title: Permissions

URL Source: https://opencode.ai/docs/permissions/

Markdown Content:
Permissions | OpenCode
===============
[Skip to content](https://opencode.ai/docs/permissions/#_top)

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

*   [Overview](https://opencode.ai/docs/permissions/#_top)
*   [Actions](https://opencode.ai/docs/permissions/#actions)
*   [Configuration](https://opencode.ai/docs/permissions/#configuration)
*   [Granular Rules (Object Syntax)](https://opencode.ai/docs/permissions/#granular-rules-object-syntax)
    *   [Wildcards](https://opencode.ai/docs/permissions/#wildcards)
    *   [Home Directory Expansion](https://opencode.ai/docs/permissions/#home-directory-expansion)
    *   [External Directories](https://opencode.ai/docs/permissions/#external-directories)

*   [Available Permissions](https://opencode.ai/docs/permissions/#available-permissions)
*   [Defaults](https://opencode.ai/docs/permissions/#defaults)
*   [What “Ask” Does](https://opencode.ai/docs/permissions/#what-ask-does)
*   [Agents](https://opencode.ai/docs/permissions/#agents)

On this page
------------

*   [Overview](https://opencode.ai/docs/permissions/#_top)
*   [Actions](https://opencode.ai/docs/permissions/#actions)
*   [Configuration](https://opencode.ai/docs/permissions/#configuration)
*   [Granular Rules (Object Syntax)](https://opencode.ai/docs/permissions/#granular-rules-object-syntax)
    *   [Wildcards](https://opencode.ai/docs/permissions/#wildcards)
    *   [Home Directory Expansion](https://opencode.ai/docs/permissions/#home-directory-expansion)
    *   [External Directories](https://opencode.ai/docs/permissions/#external-directories)

*   [Available Permissions](https://opencode.ai/docs/permissions/#available-permissions)
*   [Defaults](https://opencode.ai/docs/permissions/#defaults)
*   [What “Ask” Does](https://opencode.ai/docs/permissions/#what-ask-does)
*   [Agents](https://opencode.ai/docs/permissions/#agents)

Permissions
===========

Control which actions require approval to run.

OpenCode uses the `permission` config to decide whether a given action should run automatically, prompt you, or be blocked.

As of `v1.1.1`, the legacy `tools` boolean config is deprecated and has been merged into `permission`. The old `tools` config is still supported for backwards compatibility.

* * *

[Actions](https://opencode.ai/docs/permissions/#actions)
--------------------------------------------------------

Each permission rule resolves to one of:

*   `"allow"` — run without approval
*   `"ask"` — prompt for approval
*   `"deny"` — block the action

* * *

[Configuration](https://opencode.ai/docs/permissions/#configuration)
--------------------------------------------------------------------

You can set permissions globally (with `*`), and override specific tools.

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "permission": {    "*": "ask",    "bash": "allow",    "edit": "deny"  }}`

You can also set all permissions at once:

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "permission": "allow"}`

* * *

[Granular Rules (Object Syntax)](https://opencode.ai/docs/permissions/#granular-rules-object-syntax)
----------------------------------------------------------------------------------------------------

For most permissions, you can use an object to apply different actions based on the tool input.

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "permission": {    "bash": {      "*": "ask",      "git *": "allow",      "npm *": "allow",      "rm *": "deny",      "grep *": "allow"    },    "edit": {      "*": "deny",      "packages/web/src/content/docs/*.mdx": "allow"    }  }}`

Rules are evaluated by pattern match, with the **last matching rule winning**. A common pattern is to put the catch-all `"*"` rule first, and more specific rules after it.

### [Wildcards](https://opencode.ai/docs/permissions/#wildcards)

Permission patterns use simple wildcard matching:

*   `*` matches zero or more of any character
*   `?` matches exactly one character
*   All other characters match literally

### [Home Directory Expansion](https://opencode.ai/docs/permissions/#home-directory-expansion)

You can use `~` or `$HOME` at the start of a pattern to reference your home directory. This is particularly useful for [`external_directory`](https://opencode.ai/docs/permissions/#external-directories) rules.

*   `~/projects/*` ->`/Users/username/projects/*`
*   `$HOME/projects/*` ->`/Users/username/projects/*`
*   `~` ->`/Users/username`

### [External Directories](https://opencode.ai/docs/permissions/#external-directories)

Use `external_directory` to allow tool calls that touch paths outside the working directory where OpenCode was started. This applies to any tool that takes a path as input (for example `read`, `edit`, `list`, `glob`, `grep`, and many `bash` commands).

Home expansion (like `~/...`) only affects how a pattern is written. It does not make an external path part of the current workspace, so paths outside the working directory must still be allowed via `external_directory`.

For example, this allows access to everything under `~/projects/personal/`:

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "permission": {    "external_directory": {      "~/projects/personal/**": "allow"    }  }}`

Any directory allowed here inherits the same defaults as the current workspace. Since [`read` defaults to `allow`](https://opencode.ai/docs/permissions/#defaults), reads are also allowed for entries under `external_directory` unless overridden. Add explicit rules when a tool should be restricted in these paths, such as blocking edits while keeping reads:

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "permission": {    "external_directory": {      "~/projects/personal/**": "allow"    },    "edit": {      "~/projects/personal/**": "deny"    }  }}`

Keep the list focused on trusted paths, and layer extra allow or deny rules as needed for other tools (for example `bash`).

* * *

[Available Permissions](https://opencode.ai/docs/permissions/#available-permissions)
------------------------------------------------------------------------------------

OpenCode permissions are keyed by tool name, plus a couple of safety guards:

*   `read` — reading a file (matches the file path)
*   `edit` — all file modifications (covers `edit`, `write`, `patch`, `multiedit`)
*   `glob` — file globbing (matches the glob pattern)
*   `grep` — content search (matches the regex pattern)
*   `list` — listing files in a directory (matches the directory path)
*   `bash` — running shell commands (matches parsed commands like `git status --porcelain`)
*   `task` — launching subagents (matches the subagent type)
*   `skill` — loading a skill (matches the skill name)
*   `lsp` — running LSP queries (currently non-granular)
*   `todoread`, `todowrite` — reading/updating the todo list
*   `webfetch` — fetching a URL (matches the URL)
*   `websearch`, `codesearch` — web/code search (matches the query)
*   `external_directory` — triggered when a tool touches paths outside the project working directory
*   `doom_loop` — triggered when the same tool call repeats 3 times with identical input

* * *

[Defaults](https://opencode.ai/docs/permissions/#defaults)
----------------------------------------------------------

If you don’t specify anything, OpenCode starts from permissive defaults:

*   Most permissions default to `"allow"`.
*   `doom_loop` and `external_directory` default to `"ask"`.
*   `read` is `"allow"`, but `.env` files are denied by default:

opencode.json

`{  "permission": {    "read": {      "*": "allow",      "*.env": "deny",      "*.env.*": "deny",      "*.env.example": "allow"    }  }}`

* * *

[What “Ask” Does](https://opencode.ai/docs/permissions/#what-ask-does)
----------------------------------------------------------------------

When OpenCode prompts for approval, the UI offers three outcomes:

*   `once` — approve just this request
*   `always` — approve future requests matching the suggested patterns (for the rest of the current OpenCode session)
*   `reject` — deny the request

The set of patterns that `always` would approve is provided by the tool (for example, bash approvals typically whitelist a safe command prefix like `git status*`).

* * *

[Agents](https://opencode.ai/docs/permissions/#agents)
------------------------------------------------------

You can override permissions per agent. Agent permissions are merged with the global config, and agent rules take precedence. [Learn more](https://opencode.ai/docs/agents#permissions) about agent permissions.

Note

Refer to the [Granular Rules (Object Syntax)](https://opencode.ai/docs/permissions/#granular-rules-object-syntax) section above for more detailed pattern matching examples.

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "permission": {    "bash": {      "*": "ask",      "git *": "allow",      "git commit *": "deny",      "git push *": "deny",      "grep *": "allow"    }  },  "agent": {    "build": {      "permission": {        "bash": {          "*": "ask",          "git *": "allow",          "git commit *": "ask",          "git push *": "deny",          "grep *": "allow"        }      }    }  }}`

You can also configure agent permissions in Markdown:

~/.config/opencode/agents/review.md

```
---description: Code review without editsmode: subagentpermission:  edit: deny  bash: ask  webfetch: deny---
Only analyze code and suggest changes.
```

Tip

Use pattern matching for commands with arguments. `"grep *"` allows `grep pattern file.txt`, while `"grep"` alone would block it. Commands like `git status` work for default behavior but require explicit permission (like `"git status *"`) when arguments are passed.

[Edit this page](https://github.com/anomalyco/opencode/edit/dev/packages/web/src/content/docs/permissions.mdx)[Find a bug? Open an issue](https://github.com/anomalyco/opencode/issues/new)[Join our Discord community](https://opencode.ai/discord)

© [Anomaly](https://anoma.ly/)

Jan 31, 2026
