# AI CLI helper

Manages configuration and skills for AI agent CLI tools (Claude Code, Opencode).

## Usage

Reference this skill by name or describe what you need:
- "What skills do I have?" (runs the discovery script)
- "Why isn't my hook firing?"
- "Compare my Claude Code and Opencode permission setups"

## Directory map

```
ai-cli-helper/
├── SKILL.md                # Coordinator (Claude reads this)
├── README.md               # This file
├── scripts/
│   ├── discover-skills.py  # Auto-discovers all SKILL.md files in monorepo
│   └── local-skills.py     # Symlink-based local skill manager
├── skills-inventory.json   # Unified manifest (discovery + activation)
├── subskills/
│   ├── manage-configs.md   # Config inspection, modification, rebuild workflow
│   └── manage-skills.md    # Install, update, and inventory skills
└── references/
    ├── claude-code-plugins.md   # Legacy plugin system (for debugging conflicts)
    ├── opencode-config.md       # Opencode config structure
    └── vercel-skills.md         # npx skills CLI reference
```

## Architecture

Skill sources live where their owner lives (ownership determines location):

| Ownership | Source location |
|-----------|---------------|
| Private | your private skills directory |
| Public / shared | a published subtree or GitHub repo |
| Project-specific | inside the project itself |

Activation is separate from source:
- `.agents/skills/` is the canonical store (remote skills are typically `npx` copies, local skills can be symlinks)
- `.claude/skills/` contains symlinks pointing into `.agents/skills/`
- Opencode reads `.agents/skills/` directly

Registry is computed, not maintained:
- `scripts/discover-skills.py` builds one manifest with both discovery and activation status
- Output written to `skills-inventory.json`
- `scripts/local-skills.py add/remove` refreshes this manifest automatically

## Architecture decisions

All decisions closed. These define why the system is the way it is.

- D1: use a hybrid skill model (`npx skills` for remote sources, `local-skills.py` symlinks for local sources)
- D2: legacy plugins migrate to flat `npx skills` packaging
- D3: private skills live in a dedicated directory
- D4: public distribution uses a separate repo or subtree
- D5: drop non-skill plugin components (agents, commands, hooks from plugins)
- D6: dissolve `random` plugin; use naming conventions for grouping
- D7: everything monorepo-scoped for now (no cross-machine deployment)
- D8: skill registry = auto-discovery script (computed, not maintained)

## Deferred items

- Complete migration of existing local copied skills to local symlink mode
- Uninstall old `claude plugin` entries and remove `enabledPlugins` from settings.json (migration phase 5)
- Remove legacy `skillsDir` config after activation is verified (migration phase 5)
- Restructure from plugins to flat skills
- Settings.json cleanup (stale entries)
- Fix skill validation issues
- Fix stale docs
- Research oh-my-opencode skill handling
- Cross-machine skill deployment (revisit after living with npx skills)

## Migration guide

Move from `npx` local-copy installs to a hybrid model:

- Keep remote skills on `npx skills`
- Move local monorepo skills to `local-skills.py` symlinks (`npx add` bootstrap, then `.agents` swap)

This keeps local development fast because edits to source skills appear immediately without remove/re-add copy cycles.

### Prerequisites

- Use script: `./scripts/local-skills.py`
- Remote skills continue to use `npx skills add/remove`

### Step 1: audit current state

```bash
./scripts/local-skills.py list
./scripts/discover-skills.py /path/to/repo
npx skills list
ls -la .agents/skills
ls -la .claude/skills
```

Interpretation:

- Directory entry in `.agents/skills/<name>` means copy-style install
- Symlink entry in `.agents/skills/<name>` means local-symlink mode

### Step 2: migrate one local skill

```bash
# Remove old npx-managed copy (if present)
npx skills remove --skill my-skill -y

# Add local symlink-managed skill
./scripts/local-skills.py add ./path/to/my-skill -a claude-code opencode
```

### Step 3: verify

```bash
./scripts/local-skills.py list
npx skills list
```

### Step 4: repeat for each local skill

Use the same remove-then-add pattern for every local skill source path you want in symlink mode.

### Rollback a skill to npx copy mode

```bash
./scripts/local-skills.py remove --skill my-skill -a claude-code opencode
npx skills add ./path/to/my-skill -a claude-code opencode -y
```

### Troubleshooting

- If add fails because path exists, rerun with `--force` only when you want replacement
- If a skill name is unexpected, check `name:` in that skill's `SKILL.md` frontmatter
- If Claude does not see a skill, verify `.claude/skills/<name>` is a symlink to `.agents/skills/<name>`
