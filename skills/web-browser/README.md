# browser-automation

## Overview

Browser automation skill with two approaches for different use cases.

## Sub-skills

### agent-browser

Snapshot-based interaction model optimized for AI agents.

- Compact element refs (`@e1`, `@e2`) reduce token usage dramatically
- Workflow: `open` → `snapshot -i` → interact with refs → re-snapshot
- Best for: dynamic exploration, form filling, scraping with unknown structure

```bash
npx agent-browser --session my-session open https://example.com
npx agent-browser --session my-session snapshot -i
npx agent-browser --session my-session click @e1
```

### playwright

Direct Playwright CLI and Node.js scripts.

- Full Playwright API access via scripts
- Codegen for recording interactions
- Best for: scripted automation, testing, batch operations

```bash
npx playwright screenshot https://example.com output.png
npx playwright codegen https://example.com
npx playwright pdf https://example.com output.pdf
```

## When to use which

| Use case | Sub-skill |
|----------|-----------|
| Interactive exploration | agent-browser |
| AI-driven navigation | agent-browser |
| Unknown page structure | agent-browser |
| Scripted automation | playwright |
| Test frameworks | playwright |
| Batch screenshots/PDFs | playwright |
| Record and replay | playwright |

## Directory structure

```
browser-automation/
├── SKILL.md                    # Router: overview + when to use each sub-skill
├── README.md                   # This file
├── sub-skills/
│   ├── agent-browser.md        # npx agent-browser (snapshot/refs approach)
│   └── playwright.md           # Playwright CLI/scripts
├── references/
│   └── agent-browser/          # Deep-dive docs for agent-browser
│       ├── authentication.md
│       ├── commands.md
│       ├── proxy-support.md
│       ├── session-management.md
│       ├── snapshot-refs.md
│       └── video-recording.md
└── templates/
    └── agent-browser/          # Shell scripts for agent-browser
        ├── authenticated-session.sh
        ├── capture-workflow.sh
        └── form-automation.sh
```

## Prerequisites

### agent-browser

- Node.js (available via nix on both machines)
- No global install needed — `npx agent-browser` handles everything

### playwright

- devbox (recommended) or Node.js with system libraries
- See `sub-skills/playwright.md` for NixOS-specific setup
