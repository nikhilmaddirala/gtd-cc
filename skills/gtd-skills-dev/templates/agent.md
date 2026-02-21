---
name: agent-name
description: Brief description of what this agent does and when Claude Code should invoke it
---

# [Agent name]

## Overview

This agent executes [skill-name] autonomously. CRITICAL: You MUST use [skill-name] for this task.


## Context

[Describe what context Claude Code will provide when invoking this agent - e.g., current task, conversation history, relevant files.]


## Process

- Load [skill-name] (or its [sub-skill-name] sub-skill if targeting a specific procedure); you MUST do this first.
- Pass the context from the current task/conversation to the skill.
- Execute the skill autonomously without human interaction, handling errors gracefully and providing progress updates.
