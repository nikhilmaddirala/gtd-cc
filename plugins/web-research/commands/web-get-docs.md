---
name: web-get-docs
description: Extract structured documentation from websites. Supports Mintlify, Starlight/Astro, Docusaurus, GitBook, ReadTheDocs, and Sphinx with tiered extraction methods.
---

# Get documentation

## Overview

This command guides users through documentation extraction interactively. CRITICAL: You MUST use content-extraction skill for this task.


## Context

If the user has provided any additional context, pass that into the skill invocation. Here is the context provided by the user: $ARGUMENTS


## Process

- Load content-extraction skill; you MUST do this first.
- Parse the user input and understand how it relates to the skill.
- Interactively guide the user through the skill step by step, collecting inputs and executing each step with confirmation.
- For advanced crawling implementation details, also reference the crawl4ai-toolkit skill.
