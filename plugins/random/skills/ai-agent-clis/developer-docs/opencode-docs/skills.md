Title: Agent Skills

URL Source: https://opencode.ai/docs/skills/

Markdown Content:
Agent Skills | OpenCode
===============
[Skip to content](https://opencode.ai/docs/skills/#_top)

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

*   [Overview](https://opencode.ai/docs/skills/#_top)
*   [Place files](https://opencode.ai/docs/skills/#place-files)
*   [Understand discovery](https://opencode.ai/docs/skills/#understand-discovery)
*   [Write frontmatter](https://opencode.ai/docs/skills/#write-frontmatter)
*   [Validate names](https://opencode.ai/docs/skills/#validate-names)
*   [Follow length rules](https://opencode.ai/docs/skills/#follow-length-rules)
*   [Use an example](https://opencode.ai/docs/skills/#use-an-example)
*   [Recognize tool description](https://opencode.ai/docs/skills/#recognize-tool-description)
*   [Configure permissions](https://opencode.ai/docs/skills/#configure-permissions)
*   [Override per agent](https://opencode.ai/docs/skills/#override-per-agent)
*   [Disable the skill tool](https://opencode.ai/docs/skills/#disable-the-skill-tool)
*   [Troubleshoot loading](https://opencode.ai/docs/skills/#troubleshoot-loading)

On this page
------------

*   [Overview](https://opencode.ai/docs/skills/#_top)
*   [Place files](https://opencode.ai/docs/skills/#place-files)
*   [Understand discovery](https://opencode.ai/docs/skills/#understand-discovery)
*   [Write frontmatter](https://opencode.ai/docs/skills/#write-frontmatter)
*   [Validate names](https://opencode.ai/docs/skills/#validate-names)
*   [Follow length rules](https://opencode.ai/docs/skills/#follow-length-rules)
*   [Use an example](https://opencode.ai/docs/skills/#use-an-example)
*   [Recognize tool description](https://opencode.ai/docs/skills/#recognize-tool-description)
*   [Configure permissions](https://opencode.ai/docs/skills/#configure-permissions)
*   [Override per agent](https://opencode.ai/docs/skills/#override-per-agent)
*   [Disable the skill tool](https://opencode.ai/docs/skills/#disable-the-skill-tool)
*   [Troubleshoot loading](https://opencode.ai/docs/skills/#troubleshoot-loading)

Agent Skills
============

Define reusable behavior via SKILL.md definitions

Agent skills let OpenCode discover reusable instructions from your repo or home directory. Skills are loaded on-demand via the native `skill` tool—agents see available skills and can load the full content when needed.

* * *

[Place files](https://opencode.ai/docs/skills/#place-files)
-----------------------------------------------------------

Create one folder per skill name and put a `SKILL.md` inside it. OpenCode searches these locations:

*   Project config: `.opencode/skills/<name>/SKILL.md`
*   Global config: `~/.config/opencode/skills/<name>/SKILL.md`
*   Project Claude-compatible: `.claude/skills/<name>/SKILL.md`
*   Global Claude-compatible: `~/.claude/skills/<name>/SKILL.md`

* * *

[Understand discovery](https://opencode.ai/docs/skills/#understand-discovery)
-----------------------------------------------------------------------------

For project-local paths, OpenCode walks up from your current working directory until it reaches the git worktree. It loads any matching `skills/*/SKILL.md` in `.opencode/` and any matching `.claude/skills/*/SKILL.md` along the way.

Global definitions are also loaded from `~/.config/opencode/skills/*/SKILL.md` and `~/.claude/skills/*/SKILL.md`.

* * *

[Write frontmatter](https://opencode.ai/docs/skills/#write-frontmatter)
-----------------------------------------------------------------------

Each `SKILL.md` must start with YAML frontmatter. Only these fields are recognized:

*   `name` (required)
*   `description` (required)
*   `license` (optional)
*   `compatibility` (optional)
*   `metadata` (optional, string-to-string map)

Unknown frontmatter fields are ignored.

* * *

[Validate names](https://opencode.ai/docs/skills/#validate-names)
-----------------------------------------------------------------

`name` must:

*   Be 1–64 characters
*   Be lowercase alphanumeric with single hyphen separators
*   Not start or end with `-`
*   Not contain consecutive `--`
*   Match the directory name that contains `SKILL.md`

Equivalent regex:

`^[a-z0-9]+(-[a-z0-9]+)*$`

* * *

[Follow length rules](https://opencode.ai/docs/skills/#follow-length-rules)
---------------------------------------------------------------------------

`description` must be 1-1024 characters. Keep it specific enough for the agent to choose correctly.

* * *

[Use an example](https://opencode.ai/docs/skills/#use-an-example)
-----------------------------------------------------------------

Create `.opencode/skills/git-release/SKILL.md` like this:

```
---name: git-releasedescription: Create consistent releases and changelogslicense: MITcompatibility: opencodemetadata:  audience: maintainers  workflow: github---
## What I do
- Draft release notes from merged PRs- Propose a version bump- Provide a copy-pasteable `gh release create` command
## When to use me
Use this when you are preparing a tagged release.Ask clarifying questions if the target versioning scheme is unclear.
```

* * *

[Recognize tool description](https://opencode.ai/docs/skills/#recognize-tool-description)
-----------------------------------------------------------------------------------------

OpenCode lists available skills in the `skill` tool description. Each entry includes the skill name and description:

`<available_skills>  <skill>    <name>git-release</name>    <description>Create consistent releases and changelogs</description>  </skill></available_skills>`

The agent loads a skill by calling the tool:

`skill({ name: "git-release" })`

* * *

[Configure permissions](https://opencode.ai/docs/skills/#configure-permissions)
-------------------------------------------------------------------------------

Control which skills agents can access using pattern-based permissions in `opencode.json`:

`{  "permission": {    "skill": {      "*": "allow",      "pr-review": "allow",      "internal-*": "deny",      "experimental-*": "ask"    }  }}`

| Permission | Behavior |
| --- | --- |
| `allow` | Skill loads immediately |
| `deny` | Skill hidden from agent, access rejected |
| `ask` | User prompted for approval before loading |

Patterns support wildcards: `internal-*` matches `internal-docs`, `internal-tools`, etc.

* * *

[Override per agent](https://opencode.ai/docs/skills/#override-per-agent)
-------------------------------------------------------------------------

Give specific agents different permissions than the global defaults.

**For custom agents** (in agent frontmatter):

`---permission:  skill:    "documents-*": "allow"---`

**For built-in agents** (in `opencode.json`):

`{  "agent": {    "plan": {      "permission": {        "skill": {          "internal-*": "allow"        }      }    }  }}`

* * *

[Disable the skill tool](https://opencode.ai/docs/skills/#disable-the-skill-tool)
---------------------------------------------------------------------------------

Completely disable skills for agents that shouldn’t use them:

**For custom agents**:

`---tools:  skill: false---`

**For built-in agents**:

`{  "agent": {    "plan": {      "tools": {        "skill": false      }    }  }}`

When disabled, the `<available_skills>` section is omitted entirely.

* * *

[Troubleshoot loading](https://opencode.ai/docs/skills/#troubleshoot-loading)
-----------------------------------------------------------------------------

If a skill does not show up:

1.   Verify `SKILL.md` is spelled in all caps
2.   Check that frontmatter includes `name` and `description`
3.   Ensure skill names are unique across all locations
4.   Check permissions—skills with `deny` are hidden from agents

[Edit this page](https://github.com/anomalyco/opencode/edit/dev/packages/web/src/content/docs/skills.mdx)[Find a bug? Open an issue](https://github.com/anomalyco/opencode/issues/new)[Join our Discord community](https://opencode.ai/discord)

© [Anomaly](https://anoma.ly/)

Jan 31, 2026
