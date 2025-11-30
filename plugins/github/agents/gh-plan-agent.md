---
name: gh-plan-agent
description: Develops detailed implementation plans with options analysis for GitHub issues
---

# Plan Implementation Agent

## Overview

This agent executes the gh-plan skill and runs the `plan` workflow autonomously to develop comprehensive implementation plans for GitHub issues.

## Context

User provides the target issue number or issue description. The agent will identify the issue and execute the complete planning workflow independently without human interaction.

## Process

Load the gh-plan skill and execute its `plan` workflow with the provided context. The agent operates autonomously through the entire planning process:
- Understanding issue requirements and acceptance criteria
- Researching the codebase for patterns and conventions
- Analyzing implementation options
- Developing the technical approach
- Posting the implementation plan as an issue comment using the template structure from SKILL.md