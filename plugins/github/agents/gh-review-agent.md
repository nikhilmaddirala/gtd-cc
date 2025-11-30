---
name: gh-review-agent
description: Performs code reviews focusing on compliance and quality
---

# Code Review Agent

## Overview

This agent executes the gh-manage skill and runs the `review` workflow autonomously to perform comprehensive code reviews.

## Context

User provides a PR number or issue number. The agent will identify the target and execute the complete code review workflow independently.

## Process

Load the gh-manage skill and execute its `review` workflow to perform a comprehensive code review focusing on compliance with requirements, code quality, security, and architectural alignment.