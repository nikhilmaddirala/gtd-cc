Title: Custom Tools

URL Source: https://opencode.ai/docs/custom-tools/

Markdown Content:
Custom Tools | OpenCode
===============
[Skip to content](https://opencode.ai/docs/custom-tools/#_top)

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

*   [Overview](https://opencode.ai/docs/custom-tools/#_top)
*   [Creating a tool](https://opencode.ai/docs/custom-tools/#creating-a-tool)
    *   [Location](https://opencode.ai/docs/custom-tools/#location)
    *   [Structure](https://opencode.ai/docs/custom-tools/#structure)
    *   [Arguments](https://opencode.ai/docs/custom-tools/#arguments)
    *   [Context](https://opencode.ai/docs/custom-tools/#context)

*   [Examples](https://opencode.ai/docs/custom-tools/#examples)
    *   [Write a tool in Python](https://opencode.ai/docs/custom-tools/#write-a-tool-in-python)

On this page
------------

*   [Overview](https://opencode.ai/docs/custom-tools/#_top)
*   [Creating a tool](https://opencode.ai/docs/custom-tools/#creating-a-tool)
    *   [Location](https://opencode.ai/docs/custom-tools/#location)
    *   [Structure](https://opencode.ai/docs/custom-tools/#structure)
    *   [Arguments](https://opencode.ai/docs/custom-tools/#arguments)
    *   [Context](https://opencode.ai/docs/custom-tools/#context)

*   [Examples](https://opencode.ai/docs/custom-tools/#examples)
    *   [Write a tool in Python](https://opencode.ai/docs/custom-tools/#write-a-tool-in-python)

Custom Tools
============

Create tools the LLM can call in opencode.

Custom tools are functions you create that the LLM can call during conversations. They work alongside opencode’s [built-in tools](https://opencode.ai/docs/tools) like `read`, `write`, and `bash`.

* * *

[Creating a tool](https://opencode.ai/docs/custom-tools/#creating-a-tool)
-------------------------------------------------------------------------

Tools are defined as **TypeScript** or **JavaScript** files. However, the tool definition can invoke scripts written in **any language** — TypeScript or JavaScript is only used for the tool definition itself.

* * *

### [Location](https://opencode.ai/docs/custom-tools/#location)

They can be defined:

*   Locally by placing them in the `.opencode/tools/` directory of your project.
*   Or globally, by placing them in `~/.config/opencode/tools/`.

* * *

### [Structure](https://opencode.ai/docs/custom-tools/#structure)

The easiest way to create tools is using the `tool()` helper which provides type-safety and validation.

.opencode/tools/database.ts

```
import { tool } from "@opencode-ai/plugin"
export default tool({  description: "Query the project database",  args: {    query: tool.schema.string().describe("SQL query to execute"),  },  async execute(args) {    // Your database logic here    return `Executed query: ${args.query}`  },})
```

The **filename** becomes the **tool name**. The above creates a `database` tool.

* * *

#### [Multiple tools per file](https://opencode.ai/docs/custom-tools/#multiple-tools-per-file)

You can also export multiple tools from a single file. Each export becomes **a separate tool** with the name **`<filename>_<exportname>`**:

.opencode/tools/math.ts

```
import { tool } from "@opencode-ai/plugin"
export const add = tool({  description: "Add two numbers",  args: {    a: tool.schema.number().describe("First number"),    b: tool.schema.number().describe("Second number"),  },  async execute(args) {    return args.a + args.b  },})
export const multiply = tool({  description: "Multiply two numbers",  args: {    a: tool.schema.number().describe("First number"),    b: tool.schema.number().describe("Second number"),  },  async execute(args) {    return args.a * args.b  },})
```

This creates two tools: `math_add` and `math_multiply`.

* * *

### [Arguments](https://opencode.ai/docs/custom-tools/#arguments)

You can use `tool.schema`, which is just [Zod](https://zod.dev/), to define argument types.

`args: {  query: tool.schema.string().describe("SQL query to execute")}`

You can also import [Zod](https://zod.dev/) directly and return a plain object:

```
import { z } from "zod"
export default {  description: "Tool description",  args: {    param: z.string().describe("Parameter description"),  },  async execute(args, context) {    // Tool implementation    return "result"  },}
```

* * *

### [Context](https://opencode.ai/docs/custom-tools/#context)

Tools receive context about the current session:

.opencode/tools/project.ts

```
import { tool } from "@opencode-ai/plugin"
export default tool({  description: "Get project information",  args: {},  async execute(args, context) {    // Access context information    const { agent, sessionID, messageID, directory, worktree } = context    return `Agent: ${agent}, Session: ${sessionID}, Message: ${messageID}, Directory: ${directory}, Worktree: ${worktree}`  },})
```

Use `context.directory` for the session working directory. Use `context.worktree` for the git worktree root.

* * *

[Examples](https://opencode.ai/docs/custom-tools/#examples)
-----------------------------------------------------------

### [Write a tool in Python](https://opencode.ai/docs/custom-tools/#write-a-tool-in-python)

You can write your tools in any language you want. Here’s an example that adds two numbers using Python.

First, create the tool as a Python script:

.opencode/tools/add.py

```
import sys
a = int(sys.argv[1])b = int(sys.argv[2])print(a + b)
```

Then create the tool definition that invokes it:

.opencode/tools/python-add.ts

```
import { tool } from "@opencode-ai/plugin"import path from "path"
export default tool({  description: "Add two numbers using Python",  args: {    a: tool.schema.number().describe("First number"),    b: tool.schema.number().describe("Second number"),  },  async execute(args, context) {    const script = path.join(context.worktree, ".opencode/tools/add.py")    const result = await Bun.$`python3 ${script} ${args.a} ${args.b}`.text()    return result.trim()  },})
```

Here we are using the [`Bun.$`](https://bun.com/docs/runtime/shell) utility to run the Python script.

[Edit this page](https://github.com/anomalyco/opencode/edit/dev/packages/web/src/content/docs/custom-tools.mdx)[Find a bug? Open an issue](https://github.com/anomalyco/opencode/issues/new)[Join our Discord community](https://opencode.ai/discord)

© [Anomaly](https://anoma.ly/)

Jan 31, 2026
