---
name: browser-automation
description: Browser automation using Playwright CLI for testing, scraping, screenshots, and workflow automation
version: 1.0.0
author: gtd-cc

# Skill metadata
domain: web-automation
category: testing-and-scraping
tags: [playwright, browser, automation, testing, web-scraping, e2e, screenshots, cli]

# Skill classification
type: domain-expertise
complexity: intermediate
scope: comprehensive

# Usage information
prerequisites:
  - "devbox installed (recommended) OR Node.js with system libraries"

provides:
  - "Browser automation via CLI commands"
  - "Screenshot and PDF generation"
  - "Interactive code generation with codegen"
  - "Web scraping script patterns"
  - "End-to-end testing workflows"

# Integration notes
compatible_tools:
  - devbox
  - npx
  - node
  - playwright

# Learning objectives
objectives:
  - "Use Playwright CLI for quick browser tasks"
  - "Generate automation scripts with codegen"
  - "Write and run Playwright scripts"
  - "Capture screenshots and PDFs"
  - "Build web scraping workflows"
---

# Browser Automation with Playwright CLI

A standalone skill for browser automation using Playwright directly via bash commands and Node.js scripts. No plugins or MCP required - just npx and node.

## Quick Start

### 1. Setup with devbox (recommended)

```bash
# Initialize devbox in your project (one-time)
devbox init

# Add playwright (includes Node.js and browser binaries)
devbox add playwright-driver.browsers nodejs

# Enter the devbox shell
devbox shell

# Now playwright commands just work!
npx playwright screenshot https://example.com screenshot.png
```

**Why devbox?** Playwright needs browser binaries with specific system libraries. Devbox handles all of this automatically, especially on NixOS where library paths are non-standard.

### Alternative: Standard npm setup

If you're on Ubuntu/Debian/macOS and prefer not to use devbox:

```bash
# Install browsers (downloads to ~/.cache/ms-playwright/)
npx playwright install chromium

# Or install all browsers
npx playwright install
```

### 2. Quick screenshot

```bash
# Take a screenshot of any URL
npx playwright screenshot https://example.com screenshot.png

# Full page screenshot
npx playwright screenshot --full-page https://example.com full.png
```

### 3. Generate PDF

```bash
# Save webpage as PDF
npx playwright pdf https://example.com page.pdf
```

### 4. Record interactions (codegen)

```bash
# Open browser and record your actions as code
npx playwright codegen https://example.com
```

## CLI Commands Reference

### Screenshots

```bash
# Basic screenshot
npx playwright screenshot <url> <output.png>

# Full page (scrolls entire page)
npx playwright screenshot --full-page <url> <output.png>

# Specific viewport size
npx playwright screenshot --viewport-size=1920,1080 <url> <output.png>

# Wait for network idle before screenshot
npx playwright screenshot --wait-for-timeout=3000 <url> <output.png>

# Use specific browser
npx playwright screenshot --browser=firefox <url> <output.png>

# Device emulation
npx playwright screenshot --device="iPhone 13" <url> <output.png>
```

### PDF Generation

```bash
# Basic PDF
npx playwright pdf <url> <output.pdf>

# With options
npx playwright pdf --format=A4 <url> <output.pdf>

# Landscape orientation
npx playwright pdf --landscape <url> <output.pdf>
```

### Code Generation (codegen)

The most powerful CLI feature - records your browser interactions and generates code:

```bash
# Basic codegen - opens browser, records actions
npx playwright codegen <url>

# Save generated code to file
npx playwright codegen --output=script.js <url>

# Generate Python code instead of JavaScript
npx playwright codegen --target=python <url>

# With specific viewport
npx playwright codegen --viewport-size=1280,720 <url>

# Device emulation
npx playwright codegen --device="iPhone 13" <url>

# Save authentication state for reuse
npx playwright codegen --save-storage=auth.json <url>

# Load saved authentication
npx playwright codegen --load-storage=auth.json <url>
```

### Open Browser Inspector

```bash
# Open Playwright inspector for debugging
npx playwright open <url>

# With specific browser
npx playwright open --browser=webkit <url>
```

## Writing Playwright Scripts

For more complex automation, write Node.js scripts:

### Basic script template

```javascript
#!/usr/bin/env node
// save as: automation.js
// run with: node automation.js

const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto('https://example.com');

  // Your automation here
  console.log(await page.title());

  await browser.close();
})();
```

Run with:
```bash
# If playwright is installed globally or in project
node automation.js

# Or use npx to run without installing
npx playwright-core test automation.js
```

### One-liner script execution

For quick tasks, use Node's `-e` flag:

```bash
# Get page title
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://example.com');
  console.log(await page.title());
  await browser.close();
})();
"
```

### Using npx for dependency-free scripts

Create self-contained scripts that install their own dependencies:

```javascript
#!/usr/bin/env node
// Run with: npx playwright-core ./script.js
// Or ensure playwright is in node_modules

const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto(process.argv[2] || 'https://example.com');
  await page.screenshot({ path: 'output.png', fullPage: true });

  console.log('Screenshot saved to output.png');
  await browser.close();
})();
```

## Common Automation Patterns

### Screenshot with custom viewport

```javascript
#!/usr/bin/env node
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page = await context.newPage();

  await page.goto('https://example.com');
  await page.screenshot({
    path: 'screenshot.png',
    fullPage: true
  });

  await browser.close();
})();
```

### Form filling and submission

```javascript
#!/usr/bin/env node
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false }); // visible browser
  const page = await browser.newPage();

  await page.goto('https://example.com/login');

  // Fill form fields
  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'secretpassword');

  // Click submit
  await page.click('button[type="submit"]');

  // Wait for navigation
  await page.waitForURL('**/dashboard');

  console.log('Logged in successfully!');
  await browser.close();
})();
```

### Web scraping - extract data

```javascript
#!/usr/bin/env node
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto('https://news.ycombinator.com');

  // Extract data using page.evaluate
  const stories = await page.evaluate(() => {
    const items = document.querySelectorAll('.titleline > a');
    return Array.from(items).slice(0, 10).map(item => ({
      title: item.textContent,
      url: item.href
    }));
  });

  console.log(JSON.stringify(stories, null, 2));
  await browser.close();
})();
```

### Wait for dynamic content

```javascript
#!/usr/bin/env node
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto('https://example.com/dynamic-page');

  // Wait for specific element
  await page.waitForSelector('.loaded-content');

  // Or wait for text to appear
  await page.waitForSelector('text=Data loaded');

  // Or wait for network to be idle
  await page.waitForLoadState('networkidle');

  // Now extract content
  const content = await page.textContent('.loaded-content');
  console.log(content);

  await browser.close();
})();
```

### Handle authentication and save session

```javascript
#!/usr/bin/env node
const { chromium } = require('playwright');
const fs = require('fs');

const AUTH_FILE = 'auth-state.json';

(async () => {
  const browser = await chromium.launch({ headless: false });

  // Load existing auth if available
  let context;
  if (fs.existsSync(AUTH_FILE)) {
    context = await browser.newContext({ storageState: AUTH_FILE });
    console.log('Loaded existing session');
  } else {
    context = await browser.newContext();
  }

  const page = await context.newPage();
  await page.goto('https://example.com');

  // Check if logged in, if not, perform login
  const isLoggedIn = await page.$('.user-profile');
  if (!isLoggedIn) {
    console.log('Performing login...');
    await page.click('text=Login');
    await page.fill('#email', 'user@example.com');
    await page.fill('#password', 'password');
    await page.click('button[type="submit"]');
    await page.waitForSelector('.user-profile');

    // Save authentication state
    await context.storageState({ path: AUTH_FILE });
    console.log('Session saved');
  }

  // Continue with authenticated session
  console.log('Authenticated!');
  await browser.close();
})();
```

### Multiple pages / tabs

```javascript
#!/usr/bin/env node
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext();

  // Open multiple pages
  const page1 = await context.newPage();
  const page2 = await context.newPage();

  // Navigate in parallel
  await Promise.all([
    page1.goto('https://example.com'),
    page2.goto('https://example.org')
  ]);

  console.log('Page 1:', await page1.title());
  console.log('Page 2:', await page2.title());

  await browser.close();
})();
```

### Download files

```javascript
#!/usr/bin/env node
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto('https://example.com/downloads');

  // Wait for download to start
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.click('a.download-link')
  ]);

  // Save to specific path
  await download.saveAs('./downloaded-file.pdf');
  console.log('Downloaded:', download.suggestedFilename());

  await browser.close();
})();
```

### Intercept and modify requests

```javascript
#!/usr/bin/env node
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Log all requests
  page.on('request', request => {
    console.log('>>', request.method(), request.url());
  });

  // Log all responses
  page.on('response', response => {
    console.log('<<', response.status(), response.url());
  });

  // Block specific resources (images, fonts, etc.)
  await page.route('**/*.{png,jpg,jpeg,gif,webp}', route => route.abort());

  await page.goto('https://example.com');
  await browser.close();
})();
```

## Bash Integration Patterns

### Screenshot multiple URLs

```bash
#!/bin/bash
# screenshot-urls.sh

urls=(
  "https://example.com"
  "https://example.org"
  "https://example.net"
)

for url in "${urls[@]}"; do
  filename=$(echo "$url" | sed 's|https://||; s|/|_|g').png
  echo "Capturing $url -> $filename"
  npx playwright screenshot --full-page "$url" "$filename"
done
```

### Batch PDF generation

```bash
#!/bin/bash
# urls-to-pdf.sh

while read -r url; do
  filename=$(echo "$url" | md5sum | cut -c1-8).pdf
  echo "Converting $url -> $filename"
  npx playwright pdf "$url" "pdfs/$filename"
done < urls.txt
```

### Monitor page changes

```bash
#!/bin/bash
# monitor-page.sh

URL="https://example.com/status"
INTERVAL=60

while true; do
  timestamp=$(date +%Y%m%d_%H%M%S)
  npx playwright screenshot "$URL" "screenshots/${timestamp}.png"
  echo "Captured at $timestamp"
  sleep $INTERVAL
done
```

### Quick page content extraction

```bash
#!/bin/bash
# get-page-text.sh

node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('$1');
  console.log(await page.textContent('body'));
  await browser.close();
})();
" 2>/dev/null
```

Usage: `./get-page-text.sh https://example.com`

## Playwright Test CLI

For structured testing:

### Initialize test project

```bash
# Create new test project
npm init playwright@latest

# Or add to existing project
npm install -D @playwright/test
npx playwright install
```

### Run tests

```bash
# Run all tests
npx playwright test

# Run specific test file
npx playwright test tests/example.spec.js

# Run with visible browser
npx playwright test --headed

# Run in specific browser
npx playwright test --project=chromium

# Debug mode (step through)
npx playwright test --debug

# Generate HTML report
npx playwright test --reporter=html
npx playwright show-report
```

### Test file structure

```javascript
// tests/example.spec.js
const { test, expect } = require('@playwright/test');

test('homepage has title', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example/);
});

test('can search', async ({ page }) => {
  await page.goto('https://example.com');
  await page.fill('input[name="q"]', 'playwright');
  await page.press('input[name="q"]', 'Enter');
  await expect(page.locator('.results')).toBeVisible();
});
```

## Troubleshooting

### Browser not found

```bash
# Install specific browser
npx playwright install chromium

# Install all browsers
npx playwright install

# Install with dependencies (Linux)
npx playwright install-deps chromium
```

### NixOS / library issues

On NixOS (or if you see errors about missing `libstdc++.so.6`), use devbox:

```bash
# One-time setup
devbox init
devbox add playwright-driver.browsers nodejs

# Run commands inside devbox shell
devbox shell
npx playwright screenshot https://example.com out.png

# Or run directly without entering shell
devbox run -- npx playwright screenshot https://example.com out.png
```

**Why this works:** `playwright-driver.browsers` from nixpkgs includes pre-built browsers with all required system libraries properly linked. No manual LD_LIBRARY_PATH needed.

Alternative using nix-shell directly:
```bash
nix-shell -p nodejs playwright-driver.browsers --run "npx playwright screenshot https://example.com out.png"
```

### Headless vs headed

```bash
# CLI commands are headless by default

# For scripts, control with launch option:
# headless: true  (default, no visible browser)
# headless: false (shows browser window)
```

### Timeout issues

```javascript
// Increase default timeout in scripts
const browser = await chromium.launch();
const context = await browser.newContext();
context.setDefaultTimeout(60000); // 60 seconds

// Or per-operation
await page.click('button', { timeout: 10000 });
await page.waitForSelector('.element', { timeout: 30000 });
```

### Debug scripts

```bash
# Enable Playwright debug logging
DEBUG=pw:api node script.js

# Or use inspector
PWDEBUG=1 node script.js
```

## Best Practices

- Use `headless: true` for automation, `headless: false` for debugging
- Always close browser in finally block or use try/finally
- Use `waitForSelector` or `waitForLoadState` before interacting
- Save authentication state to avoid repeated logins
- Use `page.evaluate` for complex DOM operations
- Set reasonable timeouts for flaky networks
- Use codegen to bootstrap scripts, then refine manually

## Quick Reference

| Task | Command |
|------|---------|
| Screenshot | `npx playwright screenshot <url> <file.png>` |
| Full page screenshot | `npx playwright screenshot --full-page <url> <file.png>` |
| PDF | `npx playwright pdf <url> <file.pdf>` |
| Record actions | `npx playwright codegen <url>` |
| Open inspector | `npx playwright open <url>` |
| Install browsers | `npx playwright install` |
| Run tests | `npx playwright test` |
| Show test report | `npx playwright show-report` |
| Debug tests | `npx playwright test --debug` |

This skill provides standalone browser automation without requiring any Claude Code plugins or MCP servers.
