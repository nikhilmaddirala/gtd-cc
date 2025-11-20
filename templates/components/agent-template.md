---
name: agent-template
description: Template for creating autonomous agents that execute complex workflows
type: autonomous
---

# Agent Template

This template provides the standard structure for creating autonomous agents in the gtd-cc plugin marketplace. Agents execute complex, multi-step workflows without human intervention, making decisions and adapting to changing conditions.

## Overview

[Brief explanation of what this agent does, the value it provides, and the workflows it automates. Example: "This agent autonomously builds code from approved implementation plans, conducting tests and handling review feedback without human intervention."]

## Autonomy Scope

Define the boundaries of this agent's autonomous operation:

- **Decisions Made Autonomously**: List decisions this agent makes independently
  - Example: "Chooses implementation approach based on approval notes"
  - Example: "Determines which tests to run based on code changes"

- **Human Decision Points**: When the agent escalates to humans
  - Example: "Halts and escalates if acceptance tests fail"
  - Example: "Requires human approval for structural breaking changes"

- **Escalation Triggers**: Conditions that require human intervention
  - List specific error conditions, policy violations, or edge cases

## Prerequisites

Verify these conditions before starting the agent:

- ✅ All required plugins installed and configured
- ✅ Required permissions and credentials available
- ✅ Related commands or agents available
- ✅ Initial state preconditions met (e.g., approved plan exists)
- ✅ External dependencies accessible (APIs, databases, etc.)

## Workflow and Logic

Document the agent's execution flow in detail:

### Phase 1: Initialization and Validation

- **Step 1.1**: Agent receives or discovers task
  - Validation: Verify preconditions are met
  - Branching: What happens if preconditions fail?
  - Action: Initialize internal state and logging

- **Step 1.2**: Analyze input and determine workflow path
  - Decision points: What conditions determine the path?
  - Path options: Describe different execution paths
  - Validation: Confirm chosen path is appropriate

### Phase 2: Main Execution

- **Step 2.1**: Core task execution
  - Sub-task 1: Description and logic
  - Error handling: How are errors handled? Retry strategy?
  - Success criteria: How do we know this step succeeded?

- **Step 2.2**: Validate intermediate results
  - Checks performed: What validations run?
  - Error scenarios: What if validation fails?
  - Recovery: How does the agent recover from failures?

### Phase 3: Completion and Reporting

- **Step 3.1**: Final validation and cleanup
  - Cleanup actions: What state needs cleaning?
  - Final checks: Verification of work quality

- **Step 3.2**: Generate reports and document results
  - Output format: What information is provided?
  - Success documentation: How is success recorded?
  - Failure documentation: How are failures logged?

## Error Handling and Recovery

Document how the agent handles failures:

### Error Category 1: Recoverable Errors
- **Error Types**: List specific errors that can be recovered
- **Detection**: How the agent recognizes this error
- **Recovery Strategy**: Steps to recover (e.g., retry with backoff)
- **Max Attempts**: How many times before escalation
- **Escalation**: When to give up and escalate to human

### Error Category 2: Non-recoverable Errors
- **Error Types**: Errors requiring human intervention
- **Detection**: How the agent recognizes this error
- **Escalation Action**: Information provided to human
- **Required Human Action**: What the human needs to do
- **Resume Strategy**: How the agent resumes after human intervention

## Decision Points and Logic

Document key decisions the agent makes:

### Decision 1: Condition
```
IF [condition]
  THEN [action 1]
       [action 2]
       ...
ELSE [alternative action]
     [fallback action]
     ...
```

[Explanation of why this decision matters and consequences of each path]

### Decision 2: Another Condition
[Similar structure]

## Integration Points

Document how this agent integrates with other components:

- **Related Commands**: Which commands trigger or use this agent
  - Example: `/command-name` invokes this agent with specific parameters

- **Related Agents**: Other agents this agent coordinates with
  - Example: Calls `other-agent` for specific subtasks

- **Required Skills**: Which skills provide domain knowledge
  - Example: Uses `skill-name` skill for decision logic and best practices

- **External APIs/Tools**: External systems this agent interacts with
  - APIs: Which endpoints and what operations
  - Tools: Which CLI tools or services are invoked
  - Authentication: How credentials are handled securely

## State Management

Document how the agent maintains state:

- **Initial State**: What state is set when agent starts
- **State Updates**: How state changes during execution
- **State Persistence**: Where and how is state stored?
- **State Recovery**: How does the agent recover state after failure?
- **State Cleanup**: When and how is state cleaned up after completion?

## Examples and Use Cases

### Use Case 1: Typical Execution
[Describe a typical workflow scenario]

**Steps:**
1. Agent receives input with these characteristics
2. Agent follows Phase 1 (initialization)
3. Agent follows Phase 2 (execution)
4. Agent follows Phase 3 (completion)
5. Result: Describes what user sees at the end

**Verification:**
- How to verify success
- Expected outputs and artifacts

### Use Case 2: Error Handling
[Describe a scenario where an error occurs]

**Setup:** Initial conditions that lead to error
**Error Trigger:** What causes the error
**Agent Response:** How the agent responds
**Escalation:** What information is provided to human
**Resolution:** How the workflow continues after human intervention

## Testing and Validation

Document how to test and validate this agent:

### Unit Tests
- Test 1: Description of what is tested
- Test 2: Testing error paths
- Test 3: Testing decision logic

### Integration Tests
- Test 1: Interaction with related commands
- Test 2: Interaction with related agents
- Test 3: Interaction with external APIs

### Manual Testing Checklist
- [ ] Agent handles successful completion case
- [ ] Agent handles all documented error conditions
- [ ] Agent escalates appropriately on critical errors
- [ ] Agent logs sufficient detail for debugging
- [ ] All integration points work as documented

## Monitoring and Logging

Document what the agent logs and how to monitor it:

- **Success Logging**: What information is logged on success
- **Error Logging**: What debug information is captured on errors
- **Performance Metrics**: What performance data is tracked
- **Audit Trail**: How can operations be audited or traced?

## Maintenance Notes

- **Update Frequency**: How often does this agent need updates?
- **Dependencies**: External factors affecting this agent (API changes, etc.)
- **Known Limitations**: Current constraints or boundaries
- **Future Enhancements**: Planned improvements or additions
- **Related Issues**: GitHub issues tracking known problems or enhancements

## See Also

Link to related documentation:

- Related skill: [Skill Name](../skills/skill-name/SKILL.md)
- Related commands: `/command-name`
- Related agents: [Other Agent](./other-agent-name.md)
- Integration guide: [Developer Guide](../DEVELOPMENT.md#integration-patterns)
