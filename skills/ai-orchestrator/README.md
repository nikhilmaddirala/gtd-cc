# ai-orchestrator

## Overview

- Orchestrates external AI agent instances (Claude Code, Opencode, Gemini CLI) via CLI or SDK
- Core principle: this skill NEVER does work itself — it always delegates to an external agent instance
- Workflow: pick a tool → pick a model → configure flags → get approval → run → verify

## Architecture

Three content layers, each with a distinct reading mode:

```
SKILL.md          → Router: "which tool should I pick?"        (read first, every time)
sub-skills/       → Procedures: "walk me through using it"     (read top-to-bottom, ~30-50 lines)
references/       → Lookups: "what's the flag for X?"          (scan for a specific entry)
```

For edge cases not covered by references, fetch upstream docs on demand via WebFetch (URLs listed in SKILL.md).

### How the layers connect

```
SKILL.md: "Use Claude SDK for this task"
    → loads sub-skills/claude-sdk.md
        → step 2: "pick a model" → consult references/providers-models.md
        → step 3: "set permissions" → consult references/claude-sdk-options.md
        → edge case not covered → WebFetch upstream docs URL
```

## Skill structure

```
ai-orchestrator/
├── SKILL.md                      # Router: pick a tool, orchestration-only philosophy
├── README.md                     # This file
├── sub-skills/                   # Procedural instructions (~30-50 lines each)
│   ├── claude-sdk.md             # Dispatch via Claude Agent SDK (Python/TS) + CLI shorthand
│   ├── opencode-sdk.md           # Dispatch via Opencode JS/TS SDK + CLI shorthand
│   └── gemini-cli.md             # Dispatch via Gemini CLI (no SDK available)
├── references/                   # Lookup tables (flags, models, options)
│   ├── claude-code-flags.md      # Claude Code headless flag reference + patterns
│   ├── claude-sdk-options.md     # Agent SDK key options + prerequisites
│   ├── opencode-flags.md         # Opencode CLI flags + env vars + useful commands
│   ├── plugins-skills.md         # Cross-tool plugin/skill compatibility
│   └── providers-models.md       # Available models, costs, optimization
└── examples/
    ├── basic-dispatch.md         # Simplest pattern: dispatch, stream, follow up
    ├── dispatch-web-fetch.md     # Skill-backed dispatch with plugin loading
    └── iterative-loop.md         # Ralph wiggum loop: iterative retry with completion promise
```

## Sub-skills

| Sub-skill | Tool | When to use |
|-----------|------|-------------|
| claude-sdk | Claude Agent SDK + CLI shorthand | Default. Best toolset, `ClaudeSDKClient` for interactive, `query()` for fire-and-forget, CLI `claude -p` for one-offs |
| opencode-sdk | Opencode SDK + CLI shorthand | Free/cheap models, different providers, serve/attach pattern, Opencode web UI for observability |
| gemini-cli | Gemini CLI | Daily free quota, Google Search grounding for web research tasks |

## References

| Reference | Content |
|-----------|---------|
| providers-models.md | Available providers, model aliases, cost tiers, optimization strategy |
| claude-code-flags.md | 28 headless CLI flags, system prompt options, observability, prompting tips |
| claude-sdk-options.md | SDK key options (Python + TypeScript), prerequisites, SDK vs CLI comparison |
| opencode-flags.md | Run/serve flags, environment variables, useful commands |
| plugins-skills.md | Cross-compatibility analysis between Claude Code and Opencode plugin/skill systems |
| sources.md | Canonical upstream documentation URLs for all tools (fetch on demand via WebFetch) |

## Developer guide

### Adding a new tool

- Create `sub-skills/<tool-name>.md` with procedural steps (~30-50 lines)
- Create `references/<tool-name>-flags.md` with flag tables and lookup content
- Add the tool to SKILL.md's sub-skills section and "when to use which tool" comparison
- Update `references/providers-models.md` with available models
- Add the upstream docs URL to SKILL.md's "Upstream docs" section
- Add a section to `examples/dispatch-web-fetch.md` showing the new tool

### Content placement rules

- Procedural ("do this, then this") → `sub-skills/`
- Lookup tables (flags, env vars, options) → `references/`
- End-to-end walkthroughs → `examples/`
- Full vendor docs → fetch on demand via WebFetch (URLs in SKILL.md)

## Roadmap

- [x] Gemini CLI: minimal sub-skill added
- [x] Opencode SDK: minimal sub-skill added with working example
- [ ] Gemini CLI: download upstream docs from geminicli.com and flesh out reference
- [ ] Opencode SDK: flesh out with more usage patterns as they emerge
- [ ] Pipeline patterns: if multi-step orchestration becomes a repeatable pattern, promote to sub-skill
- [ ] Session management: if session continuation becomes a distinct workflow, promote to sub-skill
- [ ] Dispatch helper script: wrap tool selection and common flags in a shell script
- [ ] Prompt templates: reusable prompt patterns for reliable headless execution
- [ ] Skill routing: orchestrator should identify which skill the spawned agent needs and attach it — skills are the universal cross-tool concept (works across Claude, Opencode, Gemini); figure out plugin integration (Claude-specific `--plugin-dir`) as a separate concern later
- [x] Revisit SKILL.md delegation boundary: removed `--plugin-dir` from Quick Start and delegation boundary; framed in terms of skills
- [x] Interactive vs headless config separation (phase 1): moved personal/interactive-only configs (life-coach skill, focus gate hook) from project-level `.claude/` to user-level `~/.claude/` via Nix home-manager. Headless agents running in the monorepo no longer inherit interactive hooks.
  - Life-coach skill: `dragonix/modules/apps/ai/common/skills/life-coach/` → deployed via `programs.claude-code.skillsDir`
  - Focus gate hook: `dragonix/modules/apps/ai/claude/hooks/focus-reminder.sh` → deployed via `home.file`
  - SessionStart hook config: moved from `.claude/settings.json` to user-level `~/.claude/settings.json` (Nix-managed)
  - Cross-machine sync preserved: dragonix Nix config is in the monorepo subtree, syncs via git
  - Skills dir is in `common/` (not `claude/`) because skills are cross-tool
- [ ] Interactive vs headless config separation (phase 2): remaining work
  - Orchestrator sub-skills should document `CLAUDE_CONFIG_DIR` env var for cases where even user-level hooks need to be stripped (e.g., dispatching from a non-monorepo context)
  - Verify Opencode and Gemini CLI have equivalent config dir env vars
  - ~~Clean up project-level `.claude/skills/life-coach/` and `.claude/hooks/focus-reminder.sh`~~ done
