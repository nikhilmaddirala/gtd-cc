# Unified skills and plugins across Claude Code and OpenCode

## 1) Current state of skills and plugins in Claude Code and OpenCode

### 1.1 Claude Code

#### 1.1.1 What exists today

* **Skills**: File-system skills located in:

  * Project: `.claude/skills/<skill-name>/SKILL.md`
  * User: `~/.claude/skills/<skill-name>/SKILL.md`
* **Plugins**: A plugin is a **bundle** with a required manifest at:

  * `.claude-plugin/plugin.json`
  * And optional directories such as `commands/`, `agents/`, `skills/`, `hooks/`, plus optional MCP config.
* **Hook model**: Declarative hook configuration in the plugin bundle (often runs shell commands on lifecycle/tool events).

#### 1.1.2 How to use interactively (TUI)

* Install/enable plugins via Claude Code settings.
* Skills become available once present under `.claude/skills` or included via plugin bundle.
* Slash commands provided by plugins appear in the interactive experience.

#### 1.1.3 How to use headlessly (`claude -p`)

* Use Claude Code headless mode to run prompts in scripts/CI.
* Your enabled plugins and available skills depend on:

  * Current working directory (project `.claude/…`), and
  * User-level settings (unless restricted).
* Recommended: ensure deterministic runs by controlling which settings sources are applied (e.g., project-only for CI).

#### 1.1.4 How to use with the Claude Agent SDK

* The Agent SDK can load the **same plugin bundles** you use in Claude Code.
* SDK runs can explicitly specify plugin paths and constrain settings sources for reproducibility.
* This is the strongest “unified plugin” story: one bundle format loaded by both Claude Code and the SDK.

---

### 1.2 OpenCode

#### 1.2.1 What exists today

* **Skills**: Discovered from multiple roots:

  * Project: `.opencode/skills/<skill-name>/SKILL.md`
  * User: `~/.config/opencode/skills/<skill-name>/SKILL.md`
  * Claude-compatible paths:

    * Project: `.claude/skills/<skill-name>/SKILL.md`
    * User: `~/.claude/skills/<skill-name>/SKILL.md`
* **Agents**: Markdown agent definitions loaded from:

  * Project: `.opencode/agents/*.md`
  * User: `~/.config/opencode/agents/*.md`
* **Commands**: Markdown commands loaded from:

  * Project: `.opencode/commands/*.md`
  * User: `~/.config/opencode/commands/*.md`
* **Plugins**: A plugin is **executable JS/TS code** that runs at startup and can:

  * subscribe to events (tool/session/TUI/etc.)
  * intercept tool execution
  * register custom tools
  * be distributed as local files or npm packages referenced in `opencode.json`.

#### 1.2.2 How to use interactively (TUI)

* Skills/agents/commands become available when present in the discovery roots.
* JS/TS plugins load according to `opencode.json` and local/global plugin directories.
* Plugins can add behaviors and tooling; skills/agents/commands are mostly file-based.

#### 1.2.3 How to use headlessly (`opencode run`)

* Use `opencode run …` for non-interactive invocation.
* Availability of skills/agents/commands depends on:

  * Project `.opencode/…` and `.claude/skills/…` content
  * User config roots (`~/.config/opencode`, `~/.claude/skills`)
  * Plugins enabled via `opencode.json`.
* For CI/reproducibility: prefer project-scoped configuration.

#### 1.2.4 How to use with an OpenCode SDK

* OpenCode exposes a plugin API and an internal client context used by plugins.
* Practically, “SDK usage” today often means:

  * driving OpenCode programmatically by invoking `opencode run`
  * or writing plugins that integrate with your system.
* The most stable integration point is the plugin system: JS/TS code that can orchestrate sessions, tools, and events.

---

## 2) Cross-compatibility problems between Claude and OpenCode, and how adapters resolve them

### 2.1 Differences that cause friction

#### 2.1.1 “Plugin” means different things

* **Claude**: plugin = declarative bundle of content (skills/agents/commands/hooks) with a manifest.
* **OpenCode**: plugin = executable extension module (JS/TS) that hooks runtime events.

**Impact**: A Claude plugin repo cannot be “enabled” in OpenCode simply by listing it under `plugin: […]` — OpenCode expects JS/TS.

#### 2.1.2 Skills are mostly compatible, but grouping is limited

* Both expect **one directory level per skill**: `<skill-name>/SKILL.md`.
* Neither supports nested grouping like `skills/<bundle>/<skill>/SKILL.md` as a discovered layout.

**Impact**: Bundles must be managed via naming conventions and/or an enable/disable mechanism (symlinks/copies), not by folder nesting.

#### 2.1.3 Agents and commands are not fully portable

* Claude plugin bundles can include agents/commands, but OpenCode has its own discovery roots and naming rules.
* OpenCode typically expects flat lists of markdown files in `.opencode/agents` and `.opencode/commands`.

**Impact**: An adapter must map or transform content into OpenCode’s expected directories.

#### 2.1.4 Hooks are not directly portable

* Claude hooks are declarative and often shell-driven.
* OpenCode hooks are programmatic via plugin events.

**Impact**: A no-adapter setup should ignore hooks; an adapter can translate a subset if desired.

---

### 2.2 How to resolve with adapters (high-level strategies)

#### Strategy A: “Symlink surface” bundle manager

Goal: fast enable/disable of a bundle without copying files.

* Store bundles in a shared location.
* Enable a bundle by creating symlinks into the discovery roots:

  * Skills: `.claude/skills/<skill>` (works for both Claude and OpenCode)
  * OpenCode: `.opencode/agents/*.md`, `.opencode/commands/*.md`
* Disable by removing those symlinks.

Why it works:

* Skills become universally visible via `.claude/skills`.
* OpenCode gets its agents/commands in its native roots.
* Claude Code continues to function via `.claude/skills` and its plugin manager (if you also publish a Claude bundle).

#### Strategy B: “Install/uninstall” manager

Goal: simplest implementation.

* Enabling installs/copies files into `.claude`/`.opencode` roots.
* Disabling removes them.

Trade-off:

* More repo churn and slower toggles.

#### Strategy C: “OpenPackage/opkg bridge”

Goal: universal install + transformation pipeline.

* Use OpenPackage to fetch/resolve packages (including Claude marketplaces).
* Convert into an OpenCode-friendly layout.
* Then apply Strategy A (symlink surface) or Strategy B (copy).

Benefits:

* Works across multiple source formats.
* Centralizes versioning and source resolution.

---

### 2.3 The minimum viable unified setup (no hooks)

If you want the simplest cross-tool unification with minimal adapters:

1. Treat **skills** as the universal primitive.

   * Author skills in Claude skill format.
   * Publish them to `.claude/skills/<name>/SKILL.md` (project or user).
   * OpenCode will pick them up from `.claude/skills`.
2. For **agents/commands**, keep tool-specific definitions.

   * Claude: plugin bundles for agents/commands.
   * OpenCode: `.opencode/agents` and `.opencode/commands`.
3. Use naming conventions (prefixes) to emulate grouping.

When you’re ready to improve UX (enable/disable bundles cleanly), add an adapter:

* a bundle manager (symlink/copy) and/or an opkg-based bridge.

