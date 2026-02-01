Title: SDK

URL Source: https://opencode.ai/docs/sdk/

Markdown Content:
SDK | OpenCode
===============
[Skip to content](https://opencode.ai/docs/sdk/#_top)

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

*   [Overview](https://opencode.ai/docs/sdk/#_top)
*   [Install](https://opencode.ai/docs/sdk/#install)
*   [Create client](https://opencode.ai/docs/sdk/#create-client)
*   [Config](https://opencode.ai/docs/sdk/#config)
*   [Client only](https://opencode.ai/docs/sdk/#client-only)
*   [Types](https://opencode.ai/docs/sdk/#types)
*   [Errors](https://opencode.ai/docs/sdk/#errors)
*   [APIs](https://opencode.ai/docs/sdk/#apis)
    *   [Global](https://opencode.ai/docs/sdk/#global)
    *   [App](https://opencode.ai/docs/sdk/#app)
    *   [Project](https://opencode.ai/docs/sdk/#project)
    *   [Path](https://opencode.ai/docs/sdk/#path)
    *   [Config](https://opencode.ai/docs/sdk/#config-1)
    *   [Sessions](https://opencode.ai/docs/sdk/#sessions)
    *   [Files](https://opencode.ai/docs/sdk/#files)
    *   [TUI](https://opencode.ai/docs/sdk/#tui)
    *   [Auth](https://opencode.ai/docs/sdk/#auth)
    *   [Events](https://opencode.ai/docs/sdk/#events)

On this page
------------

*   [Overview](https://opencode.ai/docs/sdk/#_top)
*   [Install](https://opencode.ai/docs/sdk/#install)
*   [Create client](https://opencode.ai/docs/sdk/#create-client)
*   [Config](https://opencode.ai/docs/sdk/#config)
*   [Client only](https://opencode.ai/docs/sdk/#client-only)
*   [Types](https://opencode.ai/docs/sdk/#types)
*   [Errors](https://opencode.ai/docs/sdk/#errors)
*   [APIs](https://opencode.ai/docs/sdk/#apis)
    *   [Global](https://opencode.ai/docs/sdk/#global)
    *   [App](https://opencode.ai/docs/sdk/#app)
    *   [Project](https://opencode.ai/docs/sdk/#project)
    *   [Path](https://opencode.ai/docs/sdk/#path)
    *   [Config](https://opencode.ai/docs/sdk/#config-1)
    *   [Sessions](https://opencode.ai/docs/sdk/#sessions)
    *   [Files](https://opencode.ai/docs/sdk/#files)
    *   [TUI](https://opencode.ai/docs/sdk/#tui)
    *   [Auth](https://opencode.ai/docs/sdk/#auth)
    *   [Events](https://opencode.ai/docs/sdk/#events)

SDK
===

Type-safe JS client for opencode server.

The opencode JS/TS SDK provides a type-safe client for interacting with the server. Use it to build integrations and control opencode programmatically.

[Learn more](https://opencode.ai/docs/server) about how the server works. For examples, check out the [projects](https://opencode.ai/docs/ecosystem#projects) built by the community.

* * *

[Install](https://opencode.ai/docs/sdk/#install)
------------------------------------------------

Install the SDK from npm:

Terminal window

`npm install @opencode-ai/sdk`

* * *

[Create client](https://opencode.ai/docs/sdk/#create-client)
------------------------------------------------------------

Create an instance of opencode:

```
import { createOpencode } from "@opencode-ai/sdk"
const { client } = await createOpencode()
```

This starts both a server and a client

#### [Options](https://opencode.ai/docs/sdk/#options)

| Option | Type | Description | Default |
| --- | --- | --- | --- |
| `hostname` | `string` | Server hostname | `127.0.0.1` |
| `port` | `number` | Server port | `4096` |
| `signal` | `AbortSignal` | Abort signal for cancellation | `undefined` |
| `timeout` | `number` | Timeout in ms for server start | `5000` |
| `config` | `Config` | Configuration object | `{}` |

* * *

[Config](https://opencode.ai/docs/sdk/#config)
----------------------------------------------

You can pass a configuration object to customize behavior. The instance still picks up your `opencode.json`, but you can override or add configuration inline:

```
import { createOpencode } from "@opencode-ai/sdk"
const opencode = await createOpencode({  hostname: "127.0.0.1",  port: 4096,  config: {    model: "anthropic/claude-3-5-sonnet-20241022",  },})
console.log(`Server running at ${opencode.server.url}`)
opencode.server.close()
```

[Client only](https://opencode.ai/docs/sdk/#client-only)
--------------------------------------------------------

If you already have a running instance of opencode, you can create a client instance to connect to it:

```
import { createOpencodeClient } from "@opencode-ai/sdk"
const client = createOpencodeClient({  baseUrl: "http://localhost:4096",})
```

#### [Options](https://opencode.ai/docs/sdk/#options-1)

| Option | Type | Description | Default |
| --- | --- | --- | --- |
| `baseUrl` | `string` | URL of the server | `http://localhost:4096` |
| `fetch` | `function` | Custom fetch implementation | `globalThis.fetch` |
| `parseAs` | `string` | Response parsing method | `auto` |
| `responseStyle` | `string` | Return style: `data` or `fields` | `fields` |
| `throwOnError` | `boolean` | Throw errors instead of return | `false` |

* * *

[Types](https://opencode.ai/docs/sdk/#types)
--------------------------------------------

The SDK includes TypeScript definitions for all API types. Import them directly:

`import type { Session, Message, Part } from "@opencode-ai/sdk"`

All types are generated from the server’s OpenAPI specification and available in the [types file](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts).

* * *

[Errors](https://opencode.ai/docs/sdk/#errors)
----------------------------------------------

The SDK can throw errors that you can catch and handle:

`try {  await client.session.get({ path: { id: "invalid-id" } })} catch (error) {  console.error("Failed to get session:", (error as Error).message)}`

* * *

[APIs](https://opencode.ai/docs/sdk/#apis)
------------------------------------------

The SDK exposes all server APIs through a type-safe client.

* * *

### [Global](https://opencode.ai/docs/sdk/#global)

| Method | Description | Response |
| --- | --- | --- |
| `global.health()` | Check server health and version | `{ healthy: true, version: string }` |

* * *

#### [Examples](https://opencode.ai/docs/sdk/#examples)

`const health = await client.global.health()console.log(health.data.version)`

* * *

### [App](https://opencode.ai/docs/sdk/#app)

| Method | Description | Response |
| --- | --- | --- |
| `app.log()` | Write a log entry | `boolean` |
| `app.agents()` | List all available agents | [`Agent[]`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) |

* * *

#### [Examples](https://opencode.ai/docs/sdk/#examples-1)

```
// Write a log entryawait client.app.log({  body: {    service: "my-app",    level: "info",    message: "Operation completed",  },})
// List available agentsconst agents = await client.app.agents()
```

* * *

### [Project](https://opencode.ai/docs/sdk/#project)

| Method | Description | Response |
| --- | --- | --- |
| `project.list()` | List all projects | [`Project[]`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) |
| `project.current()` | Get current project | [`Project`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) |

* * *

#### [Examples](https://opencode.ai/docs/sdk/#examples-2)

```
// List all projectsconst projects = await client.project.list()
// Get current projectconst currentProject = await client.project.current()
```

* * *

### [Path](https://opencode.ai/docs/sdk/#path)

| Method | Description | Response |
| --- | --- | --- |
| `path.get()` | Get current path | [`Path`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) |

* * *

#### [Examples](https://opencode.ai/docs/sdk/#examples-3)

`// Get current path informationconst pathInfo = await client.path.get()`

* * *

### [Config](https://opencode.ai/docs/sdk/#config-1)

| Method | Description | Response |
| --- | --- | --- |
| `config.get()` | Get config info | [`Config`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) |
| `config.providers()` | List providers and default models | `{ providers:`[`Provider[]`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts)`, default: { [key: string]: string } }` |

* * *

#### [Examples](https://opencode.ai/docs/sdk/#examples-4)

```
const config = await client.config.get()
const { providers, default: defaults } = await client.config.providers()
```

* * *

### [Sessions](https://opencode.ai/docs/sdk/#sessions)

| Method | Description | Notes |
| --- | --- | --- |
| `session.list()` | List sessions | Returns [`Session[]`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) |
| `session.get({ path })` | Get session | Returns [`Session`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) |
| `session.children({ path })` | List child sessions | Returns [`Session[]`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) |
| `session.create({ body })` | Create session | Returns [`Session`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) |
| `session.delete({ path })` | Delete session | Returns `boolean` |
| `session.update({ path, body })` | Update session properties | Returns [`Session`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) |
| `session.init({ path, body })` | Analyze app and create `AGENTS.md` | Returns `boolean` |
| `session.abort({ path })` | Abort a running session | Returns `boolean` |
| `session.share({ path })` | Share session | Returns [`Session`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) |
| `session.unshare({ path })` | Unshare session | Returns [`Session`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) |
| `session.summarize({ path, body })` | Summarize session | Returns `boolean` |
| `session.messages({ path })` | List messages in a session | Returns `{ info:`[`Message`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts)`, parts:`[`Part[]`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts)`}[]` |
| `session.message({ path })` | Get message details | Returns `{ info:`[`Message`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts)`, parts:`[`Part[]`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts)`}` |
| `session.prompt({ path, body })` | Send prompt message | `body.noReply: true` returns UserMessage (context only). Default returns [`AssistantMessage`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) with AI response |
| `session.command({ path, body })` | Send command to session | Returns `{ info:`[`AssistantMessage`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts)`, parts:`[`Part[]`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts)`}` |
| `session.shell({ path, body })` | Run a shell command | Returns [`AssistantMessage`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) |
| `session.revert({ path, body })` | Revert a message | Returns [`Session`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) |
| `session.unrevert({ path })` | Restore reverted messages | Returns [`Session`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) |
| `postSessionByIdPermissionsByPermissionId({ path, body })` | Respond to a permission request | Returns `boolean` |

* * *

#### [Examples](https://opencode.ai/docs/sdk/#examples-5)

```
// Create and manage sessionsconst session = await client.session.create({  body: { title: "My session" },})
const sessions = await client.session.list()
// Send a prompt messageconst result = await client.session.prompt({  path: { id: session.id },  body: {    model: { providerID: "anthropic", modelID: "claude-3-5-sonnet-20241022" },    parts: [{ type: "text", text: "Hello!" }],  },})
// Inject context without triggering AI response (useful for plugins)await client.session.prompt({  path: { id: session.id },  body: {    noReply: true,    parts: [{ type: "text", text: "You are a helpful assistant." }],  },})
```

* * *

### [Files](https://opencode.ai/docs/sdk/#files)

| Method | Description | Response |
| --- | --- | --- |
| `find.text({ query })` | Search for text in files | Array of match objects with `path`, `lines`, `line_number`, `absolute_offset`, `submatches` |
| `find.files({ query })` | Find files and directories by name | `string[]` (paths) |
| `find.symbols({ query })` | Find workspace symbols | [`Symbol[]`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) |
| `file.read({ query })` | Read a file | `{ type: "raw" | "patch", content: string }` |
| `file.status({ query? })` | Get status for tracked files | [`File[]`](https://github.com/anomalyco/opencode/blob/dev/packages/sdk/js/src/gen/types.gen.ts) |

`find.files` supports a few optional query fields:

*   `type`: `"file"` or `"directory"`
*   `directory`: override the project root for the search
*   `limit`: max results (1–200)

* * *

#### [Examples](https://opencode.ai/docs/sdk/#examples-6)

```
// Search and read filesconst textResults = await client.find.text({  query: { pattern: "function.*opencode" },})
const files = await client.find.files({  query: { query: "*.ts", type: "file" },})
const directories = await client.find.files({  query: { query: "packages", type: "directory", limit: 20 },})
const content = await client.file.read({  query: { path: "src/index.ts" },})
```

* * *

### [TUI](https://opencode.ai/docs/sdk/#tui)

| Method | Description | Response |
| --- | --- | --- |
| `tui.appendPrompt({ body })` | Append text to the prompt | `boolean` |
| `tui.openHelp()` | Open the help dialog | `boolean` |
| `tui.openSessions()` | Open the session selector | `boolean` |
| `tui.openThemes()` | Open the theme selector | `boolean` |
| `tui.openModels()` | Open the model selector | `boolean` |
| `tui.submitPrompt()` | Submit the current prompt | `boolean` |
| `tui.clearPrompt()` | Clear the prompt | `boolean` |
| `tui.executeCommand({ body })` | Execute a command | `boolean` |
| `tui.showToast({ body })` | Show toast notification | `boolean` |

* * *

#### [Examples](https://opencode.ai/docs/sdk/#examples-7)

```
// Control TUI interfaceawait client.tui.appendPrompt({  body: { text: "Add this to prompt" },})
await client.tui.showToast({  body: { message: "Task completed", variant: "success" },})
```

* * *

### [Auth](https://opencode.ai/docs/sdk/#auth)

| Method | Description | Response |
| --- | --- | --- |
| `auth.set({ ... })` | Set authentication credentials | `boolean` |

* * *

#### [Examples](https://opencode.ai/docs/sdk/#examples-8)

`await client.auth.set({  path: { id: "anthropic" },  body: { type: "api", key: "your-api-key" },})`

* * *

### [Events](https://opencode.ai/docs/sdk/#events)

| Method | Description | Response |
| --- | --- | --- |
| `event.subscribe()` | Server-sent events stream | Server-sent events stream |

* * *

#### [Examples](https://opencode.ai/docs/sdk/#examples-9)

`// Listen to real-time eventsconst events = await client.event.subscribe()for await (const event of events.stream) {  console.log("Event:", event.type, event.properties)}`

[Edit this page](https://github.com/anomalyco/opencode/edit/dev/packages/web/src/content/docs/sdk.mdx)[Find a bug? Open an issue](https://github.com/anomalyco/opencode/issues/new)[Join our Discord community](https://opencode.ai/discord)

© [Anomaly](https://anoma.ly/)

Jan 31, 2026
