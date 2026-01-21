---
name: web-fetch-page
description: Extract content from a single webpage and save as markdown. Use web-fetch skill for articles with images, or crawl4ai-toolkit for advanced extraction options.
---

# Fetch page content

## Overview

This command guides users through web content extraction interactively. CRITICAL: You MUST use web-fetch skill for this task.


## Context

If the user has provided any additional context, pass that into the skill invocation. Here is the context provided by the user: $ARGUMENTS


## Process

- Load web-fetch skill; you MUST do this first.
- Parse the user input and understand how it relates to the skill.
- Interactively guide the user through the skill step by step, collecting inputs and executing each step with confirmation.
- For advanced extraction needs (JavaScript rendering, custom selectors), also reference the crawl4ai-toolkit skill.
