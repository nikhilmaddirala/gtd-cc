# Vercel Skills (`npx skills`) reference

> Hands-on testing results from 2026-02-08 using v1.3.7.
> Tested in `/tmp/skills-test/` (cleaned up after testing).

## Disk model

When you run `npx skills add`, the CLI creates a canonical copy in `.agents/skills/<skill-name>/` (labeled "universal/opencode" by the CLI). Then it creates symlinks from each targeted agent's directory back to that canonical location.

```
project/
├── .agents/skills/         # Canonical copy (source of truth)
│   └── my-skill/
│       └── SKILL.md
├── .claude/skills/         # Symlink → ../.agents/skills/my-skill
│   └── my-skill -> ../.agents/skills/my-skill
└── .cursor/skills/         # Symlink → ../.agents/skills/my-skill (if targeted)
    └── my-skill -> ../.agents/skills/my-skill
```

Key insight: `.agents/skills/` IS the OpenCode skills directory. The CLI reuses it as the canonical storage location for all agents, so OpenCode gets the real files while everyone else gets symlinks.

## Command reference (tested)

### Install from GitHub

```bash
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices --agent claude-code -y
```

- `--skill` matches on the `name` field in SKILL.md frontmatter, NOT the directory name
- `-y` skips all interactive prompts (picks defaults)
- Tested: creates `.agents/skills/vercel-react-best-practices/SKILL.md` and symlinks `.claude/skills/vercel-react-best-practices`

### Multi-agent install

```bash
npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices --agent claude-code opencode -y
```

- Agents are SPACE-SEPARATED, not comma-separated
- `--agent claude-code,opencode` FAILS with "Invalid agents"
- OpenCode target just uses the canonical `.agents/skills/` directory (no extra symlink needed since that's where the file already lives)

### Local path install

```bash
npx skills add ./path/to/skills-dir --agent claude-code -y
```

- COPIES files, does NOT symlink to source
- This is a critical limitation for monorepo development where you want edit-once-reflect-everywhere
- The canonical copy in `.agents/skills/` is an independent copy, not a symlink back to the source path
- Workaround: use manual symlinks for intra-monorepo skills, use `npx skills add` only for external/GitHub skills

### List installed

```bash
npx skills list
```

- Shows all installed skills grouped by agent
- Indicates which are symlinks vs. copies
- Shows the canonical location

### Remove

```bash
npx skills remove --skill skill-name -y
```

- Removes from ALL agent directories (can't target specific agents)
- `--agent '*'` does NOT work for remove (only for add)
- Removes the canonical copy from `.agents/skills/` and all symlinks

### Init (create new skill)

```bash
npx skills init my-new-skill
```

- Creates a SKILL.md template with frontmatter (name, description)
- Good for scaffolding, but the template is minimal

## Gotchas discovered

### 1. Skill name != directory name
The `--skill` flag matches the `name` field in SKILL.md frontmatter, not the directory name. If the directory is `react-best-practices/` but the SKILL.md has `name: vercel-react-best-practices`, you must use `--skill vercel-react-best-practices`.

### 2. Local installs are copies, not symlinks, and invisible to `check`
`npx skills add ./local-path` copies files into `.agents/skills/`. It does NOT create a symlink back to the source, and it does NOT write a `.skill-lock.json` entry. This means:
- Changes to the source won't be reflected in the installed copy
- `npx skills check` will never detect changes (it only checks skills with a lock entry, i.e. GitHub-sourced skills)
- Symlinks in `.agents/skills/` don't work either — the CLI's directory scanner skips them (tested 2026-02-08)

To update a local skill after making changes, remove and re-add:
```bash
npx skills remove --skill skill-name -y && npx skills add ./path/to/skill -a claude-code opencode -y
```

### 3. Agent flag syntax
- Space-separated: `--agent claude-code opencode` (correct)
- Comma-separated: `--agent claude-code,opencode` (FAILS)
- The `-a` shorthand works: `-a claude-code opencode`

### 4. Remove can't target agents
`npx skills remove` removes from ALL agents. You can't selectively remove from one agent while keeping it for another. To do that, manually delete the symlink.

### 5. The `.agents/skills/` directory is created automatically
Even if you only target `--agent claude-code`, the CLI creates `.agents/skills/` as the canonical location. This means OpenCode will also discover these skills if it's configured to read from `.agents/skills/`.

## Recommended usage for this monorepo

Based on testing, the recommended hybrid approach:

| Use case | Mechanism | Why |
|----------|-----------|-----|
| External/GitHub skills | `npx skills add <repo>` | Handles download, multi-agent symlinks, updates via `check` |
| Intra-monorepo skills | `local-skills.py add/remove/list` | Uses symlinks for instant local edit reflection without copy resync |
| Cross-machine personal skills | Declarative config or `npx skills add -g` | System-managed or easy (npx) |
| Public distribution | Push to GitHub + skills.sh | Zero packaging, automatic registry |
| Legacy plugins with agents/commands | `claude plugin install` | `npx skills` only handles SKILL.md files |

## Hooks and Claude Code-specific frontmatter

> Tested 2026-02-08. Source code analysis + hands-on install/inspect.

### What `npx skills` does with hooks: nothing

The CLI parses SKILL.md frontmatter for `name` and `description` only (via `gray-matter`). All other frontmatter fields — `hooks`, `allowed-tools`, `context`, `model`, etc. — are ignored by the CLI. It copies the file verbatim.

From the source code (`src/skills.ts`):
```typescript
// parseSkillMd only reads name + description
return {
  name: data.name,
  description: data.description,
  path: dirname(skillMdPath),
  rawContent: content,
  metadata: data.metadata,
};
```

The "hooks: Yes" in the README compatibility table means the TARGET AGENT supports hooks, not the CLI.

### What Claude Code does with hooks in SKILL.md: everything

Claude Code DOES support a `hooks` field in SKILL.md frontmatter. Per official docs:

> Hooks can be defined directly in skills and subagents using frontmatter. These hooks are scoped to the component's lifecycle and only run when that component is active.

Supported SKILL.md frontmatter fields (Claude Code):
- `name` — display name
- `description` — what the skill does and when to use it
- `context` — set to `fork` for subagent isolation
- `allowed-tools` — tools Claude can use without permission prompts
- `hooks` — lifecycle-scoped hooks (PreToolUse, PostToolUse, Stop, SessionStart, etc.)
- `model` — model override when skill is active
- `agent` — subagent type for `context: fork`
- `argument-hint` — autocomplete hint
- `disable-model-invocation` — prevent auto-loading
- `user-invocable` — hide from `/` menu

### Hooks format in SKILL.md

```yaml
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
          timeout: 30
        - type: prompt
          prompt: "Verify this operation is safe"
---
```

Key behaviors:
- Hooks are scoped to the skill's lifecycle (only active when skill is loaded)
- Skills support an additional `once` field that runs the hook only once per session
- For subagents, `Stop` hooks are auto-converted to `SubagentStop`
- Hooks are cleaned up when the skill finishes

### Verified: frontmatter survives `npx skills add`

Tested by installing a SKILL.md with hooks, context, and allowed-tools via `npx skills add`:

- `hooks` frontmatter: preserved byte-for-byte in installed copy
- `context: fork` frontmatter: preserved
- `allowed-tools` frontmatter: preserved
- `settings.json`: NOT modified (hash identical before/after)

The flow is:
```
npx skills add → copies SKILL.md verbatim to .agents/skills/
                 → symlinks .claude/skills/ → .agents/skills/
                 → Claude Code reads .claude/skills/*/SKILL.md
                 → Claude Code processes hooks, allowed-tools, context, etc.
```

So `npx skills` is a transparent transport layer. All agent-specific interpretation happens on the agent side.

### Residual artifact: `.agents/skills/` directory

After `npx skills remove`, the `.agents/skills/` directory remains (empty). This is harmless but may be unexpected. It was created during install and not cleaned up on removal.

## Version tested

- CLI version: 1.3.7
- Date: 2026-02-08
- Node: via npx (no global install)
