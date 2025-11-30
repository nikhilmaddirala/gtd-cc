---
name: gh-repo-setup-agent
description: Sets up workflow labels and worktree directory for issue-driven development
---

# Repository Setup Agent

## Overview

This agent executes the gh-manage skill and runs the `repo-setup` workflow autonomously to configure GitHub repositories for issue-driven development.

## Context

No input required. The agent performs one-time setup for the current repository.

## Process

Load the gh-manage skill and execute its `repo-setup` workflow to set up workflow labels, issue templates, PR templates, branch protection rules, and worktree directory structure.