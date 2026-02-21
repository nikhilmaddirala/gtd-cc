# Manage skills

Install, update, and audit skills across the monorepo through interactive conversation.

## When to use

- User says "install my skills", "set up skills", "what skills do I have"
- After setting up a new machine (fresh monorepo clone)
- When adding or removing skills from the monorepo install
- When auditing what's installed vs what's available

## Critical rules

- Use a hybrid approach:
  - Remote skill sources (`owner/repo`) use `npx skills`
  - Local skill sources (filesystem paths in monorepo) use `local-skills.py`
- Never use `claude plugin install/remove` for skill activation. The plugin system is deprecated for this purpose.
- Do not manually `cp` local skill files into `.agents/skills/`; use the helper script so links stay consistent.

## How it works

### Remote sources (GitHub)

`npx skills add` copies skill files into `.agents/skills/` and creates symlinks from `.claude/skills/`.

### Local sources (monorepo paths)

`local-skills.py add` first runs `npx skills add`, then replaces the copied `.agents` entry with a symlink so local edits are reflected immediately:

- `.agents/skills/<name>` -> `<local source skill dir>`
- `.claude/skills/<name>` -> `../../.agents/skills/<name>`

OpenCode reads via `.opencode/skill` -> `../.claude/skills`, so no separate Opencode link is required.

`local-skills.py add/remove` refreshes `skills-inventory.json` automatically (pass `--no-refresh-manifest` to skip).

## Decision rule

- Source looks like `owner/repo` -> use `npx skills`
- Source is a path (`./...`, `/...`, `../...`) -> use `local-skills.py`

## Process

IMPORTANT: if the user gives specific paths or skill names, skip straight to executing the command. Do not explore the codebase, read config files, or assess state first.

### Direct install/remove (user gives exact source)

Remote source:

```bash
npx skills add owner/repo --skill skill-name -a claude-code opencode -y
```

Local source:

```bash
./scripts/local-skills.py add /absolute/path/to/skill -a claude-code opencode
```

### Open-ended request ("install my skills" / "what do I have")

In this case, assess current state first:

```bash
./scripts/discover-skills.py /path/to/repo
npx skills list
npx skills list -g
./scripts/local-skills.py list
```

Then chat with the user about what they want. Use discovery if needed:

```bash
./scripts/discover-skills.py /path/to/repo
```

## Commands reference

```bash
# Remote/GitHub installs
npx skills add owner/repo --skill skill-name -a claude-code opencode -y
npx skills remove --skill skill-name -y
npx skills list
npx skills list -g

# Local monorepo installs (symlink mode)
./scripts/local-skills.py add ./path/to/my-skill -a claude-code opencode
./scripts/local-skills.py remove --skill my-skill -a claude-code opencode
./scripts/local-skills.py list

# Force replace existing local entry
./scripts/local-skills.py add ./path/to/my-skill -a claude-code opencode --force
```

## Source locations

| Ownership | Source path | Default mechanism | Install scope |
|-----------|-------------|-------------------|---------------|
| Private | your private skills directory | `local-skills.py` | project |
| Public | a published subtree or GitHub repo | `local-skills.py` (if local checkout) or `npx skills` (if GitHub source) | project |
| Project-specific | inside project dir | `local-skills.py` | project |
| GitHub | `owner/repo` | `npx skills` | project |

## Scope policy

Default: everything project-level, no global skills. This keeps cross-machine behavior simple because the monorepo itself is the distribution mechanism.

Only use global (`-g`) if the user explicitly asks for it or needs user-level activation outside the monorepo.

## Verification

After changes, verify with both views:

```bash
npx skills list
./scripts/local-skills.py list
```

## Guidelines

- When the user gives specific path/name inputs, execute immediately using the decision rule
- Prefer local symlink mode for local skill development so edits reflect instantly
- If a skill was previously installed as an `npx` copy and is moving to local symlink mode, remove the old copy first, then add with `local-skills.py`
