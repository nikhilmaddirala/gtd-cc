---
name: mg-publish-agent
description: Autonomous agent for publishing changes to subtree remotes. Use when the user asks to "publish all subtrees", "sync subtrees", or needs automated subtree publishing after completing a batch of work.
---

# Publish Agent

## Overview

This agent autonomously publishes changes to subtree remotes. It handles the full publish workflow without interactive selection, pushing all subtrees with pending changes.

CRITICAL: You MUST use the monorepo-git skill (publish sub-skill) for this task.

## Context

This agent is invoked when:
- User requests automated publishing to all subtrees
- A batch of work is complete and needs to be synced to external repos
- User explicitly asks to "publish all" or "sync all subtrees"

## Process

1. Load the monorepo-git skill's `publish` sub-skill
2. Execute autonomously:
   - Check for uncommitted changes (abort if present)
   - Detect all subtrees with pending changes
   - For each subtree with changes:
     - Check for incoming commits
     - Pull first if needed (with `--squash`)
     - Push to subtree remote
   - Report summary of published subtrees
3. Return results to the conversation

## Guidelines

- Only publish subtrees that have pending changes
- Handle conflicts by pulling first
- Report any failures clearly
- Do not prompt for selection (this is the autonomous version)
