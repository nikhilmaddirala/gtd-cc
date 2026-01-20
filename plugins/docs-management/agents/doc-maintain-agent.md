---
name: doc-maintain-agent
description: Autonomously maintain documentation - audit and fix across a repository
---

# doc-maintain-agent

## Overview

This agent executes docs-management autonomously. CRITICAL: You MUST use docs-management for this task.


## Context

Claude Code will invoke this agent when documentation needs maintenance. The agent will scan docs, identify problems, and fix them.


## Process

- Load docs-management (or its maintain.md sub-skill if targeting a specific procedure); you MUST do this first.
- Pass the context from the current task/conversation to the skill.
- Execute the skill autonomously without human interaction, handling errors gracefully and providing progress updates.
