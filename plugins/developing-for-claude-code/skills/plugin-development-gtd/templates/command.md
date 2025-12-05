---
name: command-template
description: Template for creating interactive slash commands that guide users through workflows
---

# Command Name

## Overview

This command guides users through [skill name] - [workflow-name] interactively. CRITICAL: You MUST use [skill name] for this task.

## Context

User will provide $ARGUMENTS. [Describe user input and how this command should parse the inputs].

## Process

- Load [skill name] and (if applicable) [workflow name]; you MUST do this first.
- Parse the user input and understand how it relates to [skill name]/[workflow name]. 
- Interactively guide the user through [skill name]/[workflow name] step by step, collecting inputs and executing each step with confirmation.
