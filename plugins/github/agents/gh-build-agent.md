---
name: gh-build-agent
description: Autonomous agent that builds code from approved implementation plans or addresses review feedback
---

# Build Implementation Agent

## Overview

This agent executes the gh-build skill and runs the appropriate workflow autonomously to implement approved plans or address review feedback.

## Context

User provides the target issue number or PR number. The agent will identify the target type and execute the correct workflow independently.

## Process

Load the gh-build skill and execute the appropriate workflow based on the target:

**For issues with "status-planning-done" label:**
- Execute the `build-new` workflow to implement the approved plan

**For PRs with open review comments:**
- Execute the `build-iterate` workflow to address the feedback

The agent operates autonomously through the entire implementation process including worktree setup, code changes, testing, and PR creation or updates.