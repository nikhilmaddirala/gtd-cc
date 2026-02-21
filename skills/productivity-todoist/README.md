# Todoist

## Overview
- Read Todoist tasks from synced markdown files, manage via Python SDK
- Provides task context to other skills (e.g., life-coach planning) and supports direct CLI task management
- Read path: sync script writes markdown files, Claude reads them — no direct API calls needed for queries
- Write path: triage script uses `todoist-api-python` SDK for task actions (close, reschedule, label)

## Usage

Describe the skill to Claude or reference it by name. No installation needed.

### Configuration
- Token: `~/.config/todoist-cli/config.json` (set up via `npx @doist/todoist-cli auth token`)
- For project structure and labels, see the "Todoist organization reference" appendix in `todoist-sync/README.md`

## Directory map
```
todoist/
├── SKILL.md          # Coordinator (Claude reads this)
├── README.md         # This file (humans read this)
└── scripts/
    └── todoist-triage.py   # Batch triage (drop/complete/reschedule/someday)
```

Related:
```
todoist-sync/
├── scripts/sync.py        # One-way sync from Todoist to markdown
├── sync-status.yml        # Sync metadata (last sync, duration, counts)
├── tasks/                 # Synced markdown files (read-only, source of truth for reads)
│   ├── work/
│   ├── personal/
│   └── ...
└── README.md              # Todoist organization reference (appendix)
```
