---
name: web-crawl-site
description: Crawl entire website and save content as markdown files. Uses site-crawling skill for intelligent crawling with depth control and sitemap generation.
---

# Crawl website

## Overview

This command guides users through website crawling interactively. CRITICAL: You MUST use site-crawling skill for this task.


## Context

If the user has provided any additional context, pass that into the skill invocation. Here is the context provided by the user: $ARGUMENTS


## Process

- Load site-crawling skill; you MUST do this first.
- Parse the user input and understand how it relates to the skill.
- Interactively guide the user through the skill step by step, collecting inputs and executing each step with confirmation.
- For advanced crawling implementation, also reference the crawl4ai-toolkit skill.
