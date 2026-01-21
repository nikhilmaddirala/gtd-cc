---
name: mg-subtree
description: CRUD operations for subtrees (add, list, pull, move, remove)
---

# Subtree Management

## Overview

This command provides CRUD operations for managing subtrees: add, list, pull, move, and remove.

CRITICAL: You MUST use the monorepo-git skill (subtree-manage sub-skill) for this task.

## Context

Pass the operation and any arguments to the skill: $ARGUMENTS

Examples:
- `/mg-subtree add` - Add a new subtree
- `/mg-subtree list` - List all subtrees
- `/mg-subtree pull project-name` - Pull changes for a subtree
- `/mg-subtree move old-path new-path` - Move a subtree directory
- `/mg-subtree remove project-name` - Remove a subtree

## Process

1. Load the monorepo-git skill's `subtree-manage` sub-skill
2. Parse user intent from arguments
3. Route to appropriate CRUD operation:
   - "add" -> Create: Add subtree
   - "list" -> Read: List subtrees
   - "pull" -> Update: Pull changes
   - "move" -> Update: Move directory
   - "remove" -> Delete: Remove subtree
4. Execute the operation
