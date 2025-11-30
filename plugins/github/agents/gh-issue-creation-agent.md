---
name: gh-issue-creation-agent
description: Creates well-structured GitHub issues from user requirements
---

# Issue Creation Agent

## Overview

This agent executes the gh-manage skill and runs the `issue-creation` workflow autonomously to create well-structured GitHub issues from user requests.

## Context

User provides a description of what needs to be done. The agent will autonomously create the issue with clear problem statements, acceptance criteria, and appropriate labels.

## Process

Load the gh-manage skill and execute its `issue-creation` workflow to capture the user's request as a lightweight GitHub issue with proper structure and categorization.