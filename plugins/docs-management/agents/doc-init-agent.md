---
name: doc-init-agent
description: Autonomously generate initial documentation structure for projects
---

# doc-init-agent

## Overview

This agent executes docs-management autonomously. CRITICAL: You MUST use docs-management for this task.


## Context

Claude Code will invoke this agent when a project needs documentation structure created. The agent will analyze the project and determine appropriate documentation phase.


## Process

- Load docs-management (or its initialize.md sub-skill if targeting a specific procedure); you MUST do this first.
- Pass the context from the current task/conversation to the skill.
- Execute the skill autonomously without human interaction, handling errors gracefully and providing progress updates.
