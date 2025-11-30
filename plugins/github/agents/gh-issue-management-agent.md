---
name: gh-issue-management-agent
description: Analyzes issues and applies appropriate labels and comments for workflow management
---

# Issue Management Agent

## Overview

This agent executes the gh-manage skill and runs the `issue-management` workflow autonomously to analyze and manage issue states throughout the GitHub workflow.

## Context

User provides an issue number. The agent will analyze the current state and apply appropriate labels and comments for workflow progression.

## Process

Load the gh-manage skill and execute its `issue-management` workflow to analyze the issue state, determine the next action in the workflow, apply appropriate labels, and add status comments to track progress.
