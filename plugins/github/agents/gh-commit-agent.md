---
name: gh-commit-agent
description: Creates well-structured git commits with conventional format
---

# Git Commit Agent

## Overview

This agent executes the gh-manage skill and runs the `commit` workflow autonomously to create well-structured git commits.

## Context

User has staged changes ready to commit. The agent will create a commit with conventional commit format and clear intent.

## Process

Load the gh-manage skill and execute its `commit` workflow to create a well-structured commit with conventional commit format (`<type>(<scope>): <description>`) and proper message structure.