---
name: system-check
description: Interactive system resource diagnostics for memory, disk, CPU, and performance issues
---

# System Resource Diagnostics

## Overview

This command guides you through diagnosing system resource issues using the system-diagnostics skill. CRITICAL: You MUST use the system-diagnostics skill for this task.

## Context

User may provide $ARGUMENTS describing their system issue (e.g., "out of memory", "disk full", "high CPU"), or they may invoke the command without arguments for general system analysis.

## Process

Load the system-diagnostics skill first. Detect the operating system (Linux or macOS), then interactively guide the user through appropriate diagnostic workflows based on their problem. If no specific problem is provided, perform a general system health check covering memory, disk, and CPU resources.
