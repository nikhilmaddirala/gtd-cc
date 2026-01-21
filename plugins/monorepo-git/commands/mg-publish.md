---
name: mg-publish
description: Curated push to selected subtrees with interactive selection
---

# Publish to Subtrees

## Overview

This command lets you publish changes to subtree remotes with interactive selection. Unlike daily monorepo pushes, this is a curated operation for sharing batched work.

CRITICAL: You MUST use the monorepo-git skill (publish sub-skill) for this task.

## Context

If the user has provided any additional context (e.g., specific subtree name), pass that into the skill invocation: $ARGUMENTS

## Process

1. Load the monorepo-git skill's `publish` sub-skill
2. Execute the publish workflow:
   - Detect subtrees with pending changes
   - Show interactive selection with commit summaries
   - Let user choose which to publish
   - Push selected subtrees
   - Show summary of results
