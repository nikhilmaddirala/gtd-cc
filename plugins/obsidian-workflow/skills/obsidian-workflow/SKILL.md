# Obsidian Workflow Skill

## Overview

This skill provides foundation knowledge for integrating with Obsidian vaults, managing notes, organizing knowledge, and supporting GTD (Getting Things Done) methodology through note-based workflows.

## Core Capabilities

### Vault and Note Management
- Opening and reading Obsidian vaults
- Creating and updating notes
- Organizing notes with folders and tags
- Managing internal links and references
- Handling attachments and media

### Knowledge Organization
- Implementing tag hierarchies
- Creating MOCs (Maps of Content)
- Building backlinks and reference networks
- Organizing by projects and areas
- Maintaining a resource index

### Task and Project Integration
- Capturing tasks from external sources
- Creating project templates
- Linking tasks to notes
- Tracking project progress
- Managing dependencies

### Daily Workflows
- Daily notes and reviews
- Weekly planning templates
- Monthly retrospectives
- Calendar integration
- Habit tracking

## Key Patterns

### Note Structure
```
---
tags: [gtd, area, status]
links: [related-note-1, related-note-2]
---

# Note Title

Content with [[internal-links]]
```

### Folder Organization
```
vault/
├── daily/          # Daily notes
├── projects/       # Project files
├── areas/         # Areas of responsibility
├── resources/     # Reference materials
└── archive/       # Completed items
```

### GTD Implementation
- Inbox for capturing new items
- Next Actions for immediate tasks
- Projects for multi-step initiatives
- Areas for ongoing responsibilities
- Resources for reference materials

## Integration Points

This skill integrates with:
- **GitHub workflow**: Syncing GitHub issues to Obsidian
- **Claude Code**: Capturing implementation insights
- **Task management**: Breaking down complex projects
- **Knowledge base**: Building project-specific references

## Future Capabilities

Planned features include:
- Automatic sync between GitHub and Obsidian
- AI-powered task classification and prioritization
- Smart suggestions based on note context
- Integration with calendar and scheduling tools
- Automated report generation
