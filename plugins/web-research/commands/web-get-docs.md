---
name: web-get-docs
description: Extract structured documentation from websites using content-extraction skill. Handles documentation platforms like Docusaurus, GitBook, ReadTheDocs, and Sphinx.
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
- For multi-page documentation crawling, also reference the site-crawling skill.
