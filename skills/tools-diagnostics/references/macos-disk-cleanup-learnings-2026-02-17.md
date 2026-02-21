# macOS disk cleanup learnings and runbook

Date: 2026-02-17
Host: moondancer (Darwin)

## Purpose

This reference captures practical lessons from recent cleanup work, plus prior guidance from:

- `/Users/nikhilmaddirala/Downloads/temp/macOS-Disk-Cleanup-Guide.md`
- `/Users/nikhilmaddirala/Downloads/temp/system-cleanup-reference-guide.md`
- `/Users/nikhilmaddirala/Downloads/temp/system-cleanup-report-20260117-132450.md`

It is intended as a quick operator guide for future disk pressure incidents.

## What we observed in this session

Initial state during incident triage:

- High memory and swap pressure
- Data volume close to full
- Significant usage in trash, caches, monorepo worktrees, and nix store

After targeted cleanup (trash, caches, nix garbage collection):

- `df -h` improved to about 67 GiB free
- `/System/Volumes/Data` dropped to about 60 percent usage
- `/nix` dropped to about 17 percent usage
- Trash reached 0 B
- Remaining cache footprint became modest (hundreds of MB, not tens of GB)

Current major usage is no longer cache-heavy. It is mostly durable app and user data.

## Current high-usage areas after cleanup

Top durable consumers found in this run:

- `~/Library` about 18G
  - `~/Library/Application Support` about 9.4G
  - `~/Library/Containers` about 3.1G
  - `~/Library/Group Containers` about 1.9G
- `/System/Volumes/Data/Applications` about 15G
- `/System/Volumes/Data/private/var` about 7.6G
  - mostly `var/folders`, `var/db`, and `var/vm`
- `~/repos` about 3.1G (worktrees intentionally retained)

Notable app data details:

- `~/Library/Application Support/Vivaldi` about 4.6G
  - mostly `Default/WebStorage` and `Default/Service Worker`
- `~/Library/Application Support/Google` about 1.8G
- `~/Library/Application Support/OneDrive` about 1.1G

## Safety and cleanup tiers

Use the same risk model from the January references.

Low risk, high value:

- Empty `~/.Trash`
- Clean package/browser caches
- `uv cache clean`
- `brew cleanup --prune=all`
- `rm -rf ~/.npm/_cacache ~/.npm/_npx`

Medium risk with verification:

- `nix-collect-garbage -d` (drops old generations)
- `rm -rf ~/Library/Caches/ms-playwright`
- `rm -rf ~/Library/Containers/com.apple.mediaanalysisd/*` (will rebuild)

Do not delete blindly:

- System paths under `/System`, `/usr`, `/bin`, `/sbin`
- APFS system volumes like Preboot or VM
- App databases in `Application Support` without app-specific validation

## Nix garbage collection behavior on this host

Important host-specific finding:

- Automatic nix-darwin gc is intentionally disabled when Determinate Nix is enabled.

Relevant config:

- `40-code/41-subtrees/dragonix/modules/base/nix-settings/darwin.nix:27`
  - `nix.gc = lib.mkIf (!config.determinateNix.enable) { ... }`
- `40-code/41-subtrees/dragonix/hosts/moondancer/configuration.nix:22`
  - `determinateNix.enable = true;`

Implication:

- On moondancer, do not expect nix-darwin `nix.gc.automatic` scheduling.
- GC needs to be handled by Determinate Nix behavior or explicit user scheduling.

Operational recommendation for diagnostics:

- When disk pressure is high and host uses Determinate Nix, always verify gc assumptions before concluding automation is broken.

## Practical command sequence

Snapshot before cleanup:

```bash
df -h / /nix
du -sh ~/.Trash ~/.cache ~/Library/Caches /nix/store 2>/dev/null
```

Targeted cleanup:

```bash
setopt NULL_GLOB DOT_GLOB
rm -rf ~/.Trash/*
rm -rf ~/.cache/*
rm -rf ~/Library/Caches/*
nix-collect-garbage -d
```

Snapshot after cleanup:

```bash
df -h / /nix
du -sh ~/.Trash ~/.cache ~/Library/Caches /nix/store 2>/dev/null
```

If space is still tight after this, investigate in this order:

1. `~/Library/Application Support`
2. `~/Library/Containers`
3. `~/Library/Group Containers`
4. `/System/Volumes/Data/Applications`
5. Cloud sync local mirrors and browser profile data

## Suggested improvements for the tools-diagnostics skill

- Add a Determinate Nix detection note for macOS systems.
- Add a branch in the flowchart: nix-darwin gc may be disabled by policy.
- Keep a short, host-specific checklist for moondancer:
  - do not run local heavy nix evaluation commands
  - prefer safe cache cleanup first
  - use explicit `nix-collect-garbage -d` when needed
