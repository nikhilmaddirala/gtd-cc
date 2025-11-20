---
name: command-template
description: Template for creating interactive slash commands
type: interactive
---

# Command Template

This template provides the standard structure for creating interactive slash commands in the gtd-cc plugin marketplace. Commands are triggered by slash notation (e.g., `/command-name`) and guide users through workflows with input, decision-making, and output.

## Overview

[Brief explanation of what this command does and the value it provides. Include the user workflow and expected outcomes. Example: "This command guides you through creating a new project structure with proper initialization."]

## Required Information

Document what inputs or selections the command needs:

- **Input 1 Name**: Description of what this input is, expected format, and examples
  - Example: `project-name` or `/command --flag value`
  - Constraints: Must be unique, min 3 characters, etc.

- **Input 2 Name**: Description and format requirements
  - Provide concrete examples of valid and invalid inputs

## Prerequisites

Verify these conditions before starting the command:

- ✅ Plugin installed and properly configured
- ✅ Required permissions or access available
- ✅ Dependencies or external tools available
- ✅ Related commands or skills available

## Process

Describe the step-by-step process the user follows:

1. **Step 1 Name**: What happens in this step
   - Sub-action 1: What the AI or user does
   - Sub-action 2: What decision or validation occurs
   - Outcome: What result or state change occurs

2. **Step 2 Name**: What happens in this step
   - Include decision points and conditional branches
   - Document what happens for each path

3. **Step 3 Name**: Final step completing the command
   - Summary of what was accomplished
   - Next steps the user might take

## Expected Outputs

Document what the user receives after completing the command:

- **Output 1 Name**: Description, format, and location
  - Example: "A new project directory at `~/projects/my-project` with initialized files"
  - What the user can do next with this output

- **Output 2 Name**: Secondary outputs or artifacts
  - Format and structure
  - How to verify completeness

## Common Issues & Solutions

Document problems users might encounter and how to resolve them:

- **Issue**: Clear problem description
  - Symptom: How the user would notice this problem
  - Cause: Why this happens
  - Solution: Step-by-step fix

- **Issue**: Another common problem
  - Symptom: Specific error message or behavior
  - Cause: Root cause explanation
  - Solution: Resolution steps with examples

## Integration

Document how this command fits into the larger system:

- **Related Commands**: List other commands that work together or in sequence
  - Example: `/command-a` creates structure, this command populates it, `/command-c` publishes it

- **Follow-up Commands**: What users might do after completing this command
  - Workflow example showing the natural progression

- **Required Skills**: Which skills provide the knowledge for this command
  - Example: Uses the `plugin-development` skill for best practices

- **Affected Plugins**: Which plugins this command can work with
  - Example: Works with any plugin type (integration, utility, workflow, data)

## Examples

### Example 1: Typical Usage
```
/command-name input-value
```
Expected result: Shows what happens with normal inputs

### Example 2: Advanced Usage
```
/command-name input-value --flag additional-option
```
Expected result: Shows behavior with additional options

## See Also

Link to related documentation:
- Related skill: [Skill Name](../skills/skill-name/SKILL.md)
- Related commands: `/other-command`
- Workflow guide: [Documentation](../DEVELOPMENT.md#section)
