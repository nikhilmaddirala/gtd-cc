# Random Plugin

Miscellaneous productivity and development skills for specialized workflows.

## Skills

This plugin provides specialized skills:

### Backlog.md GTD Task Management

Comprehensive GTD task management using the Backlog.md CLI tool. Implements the four GTD phases (Capture, Organize, Execute, Review) with practical CLI examples and team collaboration patterns.

**Key features:**
- Task creation and organization with acceptance criteria
- GTD methodology implementation
- Team assignment and progress tracking
- Search and discovery patterns
- Bug/feature templates and workflows

See `skills/backlog-md-skill/SKILL.md` for complete documentation and CLI examples.

### Catppuccin Port Creation

Automated Catppuccin theme generation and validation for creating theme ports. Handles color mapping, validation against official palettes, and preparation for theme submissions.

**Key features:**
- Theme generation for all four Catppuccin flavors (Latte, Frappé, Macchiato, Mocha)
- Color validation and WCAG contrast checking
- Target application analysis and theming system research
- Preview composition and documentation generation

See `skills/catppuccin-port-creation/SKILL.md` for workflow details and submission guidelines.

### Langfuse CLI

Query and analyze LLM traces, sessions, observations, scores, and metrics from Langfuse via the Python SDK and REST API. Essential for debugging agent runs, tracking costs, and evaluating agent quality.

- Trace querying and inspection (list, filter, drill-down)
- Session and observation analysis
- Score retrieval and evaluation workflows
- Cost and token usage analytics via Metrics API
- Ready-to-run scripts using uv inline metadata

See `skills/langfuse-cli/SKILL.md` for complete API reference and workflow examples.

## Installation

Install as part of the gtd-cc marketplace:

```bash
/plugin install random@gtd-cc
```

## Usage

These skills are designed to be used by agents and commands that need specialized domain expertise. The Backlog.md skill provides task management patterns, the Catppuccin skill handles theme creation, and the Langfuse skill enables LLM observability and evaluation workflows.