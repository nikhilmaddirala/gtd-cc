---
name: gh-plan
description: Develops detailed implementation plans with options analysis for GitHub issues
---

# Plan Implementation

## Overview

This command guides you through creating detailed implementation plans for GitHub issues using the gh-plan skill. CRITICAL: You MUST use the gh-plan skill for this task.

## Context

User will provide an issue number via $ARGUMENTS. If not provided, recent issues with "status-planning-todo" label will be shown for selection.

## Process

Load the gh-plan skill first. Interactively guide the user through the `plan` workflow step by step, collecting information and executing each step with confirmation. The workflow includes:
1. Understanding issue requirements and acceptance criteria
2. Researching the codebase for existing patterns and conventions
3. Analyzing implementation options and tradeoffs
4. Developing a detailed technical approach
5. Posting the implementation plan as an issue comment using the template from SKILL.md
