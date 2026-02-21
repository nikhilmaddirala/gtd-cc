# Nix garbage collection learnings (moondancer and seasmoke)

Date: 2026-02-17

## Why this note exists

We saw repeated confusion around "GC is enabled" versus "disk is still full". This note records what actually happened on moondancer and seasmoke, what root causes mattered, and what operational pattern works.

## Key findings

- Determinate Nix GC can be enabled and active while total disk pressure remains high.
- Nix GC only frees Nix-reclaimable store objects. It does not clean app data, browser data, user caches, container layers, or service caches.
- Large apparent Nix usage can still be "live" due to roots (profiles and running processes), not because GC failed.
- On Linux hosts, non-Nix directories can dominate unexpectedly (for seasmoke: `/var/lib/containers`).

## Moondancer-specific finding (Darwin + Determinate Nix)

- nix-darwin `nix.gc` is intentionally disabled when Determinate Nix is enabled.
- In this repo, that is controlled by:
  - `40-code/41-subtrees/dragonix/modules/base/nix-settings/darwin.nix`
  - `40-code/41-subtrees/dragonix/hosts/moondancer/configuration.nix`
- Determinate Nixd handles GC policy instead of nix-darwin timer-based GC.

Implication:

- Do not assume `nix.gc.automatic` settings apply on moondancer when `determinateNix.enable = true`.

## Seasmoke investigation summary

Initial state during deep investigation:

- Root FS: `150G` total, `120G` used, `23G` free
- Top-level usage with root privileges:
  - `/nix` about `69G`
  - `/var` about `20G`
  - `/home` about `17G`

Critical correction:

- Non-root `du` under-reported actual usage. Root-level `du` was required to reconcile to `df`.

### What looked like "Nix bloat" but was root retention

- `nix-store --gc --print-dead` initially showed reclaimable dead paths, then reached 0 after cleanup.
- Even with dead paths at 0, store remained large because many paths were still rooted.
- Biggest root categories:
  - user profile generations under `~/.local/state/nix/profiles/*`
  - `/proc/*` roots from long-running services/processes

### High-impact cleanup that worked

- Aggressive GC on root and users
  - root: `nix-collect-garbage -d`
  - per user: explicit `nix-env -p <profile> --delete-generations old`
- Additional non-Nix cleanup:
  - rootless container layers under user home
  - netdata cache
  - open-webui embedding cache

Net effect in this run:

- Root FS improved from `120G used / 23G free` to `82G used / 61G free`
- `/nix/store` reduced from about `69G` to about `39G`

## Why auto-GC did not fully solve it alone

- Timer-based GC removed dead store objects, but old profile links persisted in user profile trees.
- Those profile links remained valid roots until explicitly pruned.
- Running daemons and long-lived processes kept additional paths alive through `/proc` roots.

## Practical runbook

### 1) Verify true disk distribution (as root)

```bash
sudo du -xhd 1 / | sort -hr
df -h /
```

### 2) Measure Nix state

```bash
sudo du -sh /nix/store /nix/var
sudo nix-store --gc --print-dead | wc -l
sudo nix-store --gc --print-roots
```

### 3) Prune all profile generations, not just system

```bash
sudo nix-collect-garbage -d

# Example per-user profile pruning
sudo runuser -u <user> -- sh -c '
  nix-env -p "$HOME/.local/state/nix/profiles/profile" --delete-generations old
  nix-env -p "$HOME/.local/state/nix/profiles/home-manager" --delete-generations old
'
```

### 4) Re-run store GC

```bash
sudo nix-store --gc
```

### 5) Clean non-Nix heavy hitters

```bash
# examples from seasmoke incident
sudo podman system prune --volumes -f
sudo rm -rf /var/cache/netdata/*
sudo rm -rf /var/lib/open-webui/data/cache/*
```

## Operational recommendations

- Keep automatic GC enabled, but add periodic explicit user-profile generation pruning where profile churn is high.
- Track and alert on top-level root usage (`/nix`, `/var`, `/home`) rather than only free space.
- Include root-level (`sudo`) disk scans in diagnostics workflows by default.
- On hosts with multiple service users, inspect each user's profile roots and cache directories.
- Treat container storage (`/var/lib/containers` and rootless storage) as first-class disk pressure sources.
