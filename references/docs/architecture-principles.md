# Architecture principles 

## Architecture

This configuration system has two layers:

1. **Foundation Layer: Skills** - Where the heavy lifting happens
2. **Orchestration Layer: Commands & Agents** - How skills get invoked

```
┌─────────────────────────────────────────────┐
│         Orchestration Layer                 │
│  ┌──────────────┐      ┌──────────────┐    │
│  │  Commands    │      │   Agents     │    │
│  │  (Human-in-  │      │  (Autonomous │    │
│  │   the-loop)  │      │ orchestration)│   │
│  └──────┬───────┘      └──────┬───────┘    │
│         │                     │             │
│         └──────────┬──────────┘             │
└────────────────────┼──────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│          Foundation Layer                   │
│         ┌─────────────────┐                 │
│         │     Skills      │                 │
│         │ (Domain logic & │                 │
│         │   expertise)    │                 │
│         └─────────────────┘                 │
└─────────────────────────────────────────────┘
```

---

## Component Types

### Skills (Foundation)
**Purpose**: Domain expertise and detailed workflows - this is where the heavy lifting happens

**What they are**: Self-contained knowledge bases with comprehensive documentation, detailed workflows, scripts, and reference material. Skills contain the actual logic and domain expertise.

**Progressive loading**: Skills use progressive disclosure to manage context:
- Skill metadata (name + description) → always available
- Full SKILL.md content → loaded when skill is invoked
- Bundled resources → accessed as needed

**When to create**: Create a skill for any specialized domain knowledge, complex workflow, or reusable capability. Skills are the foundation - most logic should live here.

### Commands (Interactive Orchestrators)
**Purpose**: Human-in-the-loop orchestration of skills

**What they are**: Interactive workflow templates invoked by users (e.g., `/gh-issue`, `/gh-commit`). Commands orchestrate one or more skills while involving the user in decision-making steps.

**How they work**: Commands inject runtime context, guide the user through decisions, and invoke skills as needed. They're for workflows where human input, clarification, or approval is required at various stages.

**Key characteristics**:
- **Interactive**: Asks user for input, clarification, decisions
- **Context injection**: Gathers runtime environment info
- **Skill orchestration**: Can reference/invoke skills for heavy lifting
- **Step-by-step**: Guides user through a workflow

**When to create**: Create a command for workflows that need user input, approval, or decision-making at various steps.


### Agents (Autonomous Orchestrators)
**Purpose**: Autonomous orchestration of skills without user involvement

**What they are**: System prompts that orchestrate one or more skills to accomplish defined goals completely autonomously. Agents execute entire workflows from start to finish without stopping for user input.

**How they work**: Agent files define the goal/workflow and orchestrate skills to achieve it. They make decisions, handle edge cases, and complete tasks without human intervention.

---

## Philosophy

This configuration system is designed to:
- **Skills as building blocks**: Heavy lifting lives in reusable skills; orchestrators stay lightweight
- **Flexible orchestration**: Same skill can be used interactively (commands) or autonomously (agents)
- **Enhance, not constrain**: Provide helpful structure without rigid requirements
- **Adapt, not impose**: Work with existing conventions rather than forcing new ones
- **Scale gracefully**: Handle simple tasks easily while supporting complex workflows
- **Stay maintainable**: Keep components focused and loosely coupled

The goal is to make AI assistants more capable and consistent across projects while remaining flexible and unopinionated. By separating domain logic (skills) from orchestration (commands/agents), we maximize reusability and minimize duplication.

**Key principle**: Both commands and agents should be thin orchestration layers. If you find yourself writing detailed implementation logic, extract it to a skill instead.

## Key Design Principles

### Architecture Principle
**Skills** = Foundation (where logic lives)
**Commands** = Interactive orchestrators (human-in-the-loop)
**Agents** = Autonomous orchestrators (no human involvement)

### 1. Skills as Foundation
Most logic, workflows, and domain expertise lives in skills, not in commands or agents.

**Why**: Skills are reusable across both interactive (command) and autonomous (agent) contexts. By putting heavy lifting in skills, we avoid duplicating logic and make it easier to maintain.

**Example**: The `options-analysis-skill` contains detailed research methodology. Both a command (interactive research) and an agent (autonomous research) can invoke this same skill.

### 2. Orchestration, Not Implementation
Commands and agents orchestrate skills; they don't contain detailed implementation logic.

**Why**: Keeps orchestrators lightweight and focused on coordination. When implementation details change, you only update the skill, not every command/agent that uses it.

**Anti-pattern**: Don't put detailed workflows in commands/agents. Extract them to skills.

### 3. Progressive Disclosure
Load only what's needed when it's needed:
- Skill metadata (name + description) → always available
- Full SKILL.md content → loaded when skill is invoked
- Bundled resources → accessed as needed

**Why**: Manages context window efficiently, especially important for large skill catalogs.

### 4. Context Injection
Commands inject runtime context via bash commands in backticks:
```bash
`gh label list`
`git status`
`git log --oneline -5`
```

**Why**: Gives AI current, accurate information about the environment rather than guessing or using stale data.

### 5. Clear Separation of Concerns
- **Skills** = Domain logic, detailed workflows, expertise (foundation)
- **Commands** = Interactive orchestration (human-in-the-loop)
- **Agents** = Autonomous orchestration (no human involvement)

**Why**: Each layer has a distinct responsibility. Skills can be reused by multiple orchestrators without modification.

### 6. Repository Awareness
Commands and agents adapt to existing conventions rather than imposing rigid structure.

**Example**: The `gh-issue` command checks for existing templates, labels, and recent issue styles, then matches that pattern.

**Why**: Works with any project without requiring project-specific configuration.

### 7. Composability
Skills should be composable - agents and commands can invoke multiple skills to accomplish complex goals.

**Why**: Enables building complex workflows from simple, well-tested building blocks.

**Example**: An agent might use `crawl4ai` skill to fetch content + `options-analysis-skill` to analyze it + document skill to format output.

### 8. Convention Over Configuration
Use consistent naming and structure patterns:
- Agent files: `agent-name.md`
- Command files: `command-name.md`
- Skill directories: `skill-name/SKILL.md`

**Why**: Predictable structure makes the system self-documenting and easier to extend.


