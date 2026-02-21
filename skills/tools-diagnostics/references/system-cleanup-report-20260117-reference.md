# System cleanup report reference (2026-01-17)

Source document:

- `/Users/nikhilmaddirala/Downloads/temp/system-cleanup-report-20260117-132450.md`

This is a compact retained reference for the skill folder.

## Executive summary snapshot

- Before cleanup: 90 percent used, 17G free, critical state
- After cleanup: 75 percent used, 41G free
- Space recovered: about 24G

## High-impact operations from that run

- `rm -rf ~/Library/Containers/com.apple.mediaanalysisd/*` saved about 8.0G
- `brew cleanup --prune=all` saved about 3.9G
- `rm -rf ~/.npm/_cacache ~/.npm/_npx` saved about 2.3G
- `uv cache clean` saved about 2.0G
- Browser caches saved about 2.4G
- `rm -rf ~/Library/Caches/ms-playwright` saved about 998M
- Nix tarball and eval cache cleanup saved about 1.3G

## Key lessons retained

- Cache cleanup gives immediate wins with low risk.
- Media analysis can silently consume multiple GB and is rebuildable.
- Nix state accumulates over time and needs periodic garbage collection.
- System volume numbers can look alarming on macOS; target user data and app data first.
- Automation is necessary to avoid recurring incidents every few months.

## Reusable command set

```bash
brew cleanup --prune=all
uv cache clean
rm -rf ~/.npm/_cacache ~/.npm/_npx
rm -rf ~/Library/Caches/{Vivaldi,Google,zen}
rm -rf ~/Library/Caches/ms-playwright
rm -rf ~/.cache/nix/tarball-cache/* ~/.cache/nix/eval-cache-v6
nix-collect-garbage -d
```
