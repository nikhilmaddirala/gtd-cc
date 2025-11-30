---
name: gh-merge-agent
description: Executes final merge operations and cleanup
---

# Merge and Cleanup Agent

## Overview

This agent executes the gh-manage skill and runs the `merge` workflow autonomously to execute final merge operations and cleanup.

## Context

User provides an issue number. The agent will identify the associated PR and execute the complete merge and cleanup workflow independently.

## Process

Load the gh-manage skill and execute its `merge` workflow to squash-merge the PR to main, close the issue and PR, delete the branch, remove the worktree, and complete cleanup activities.