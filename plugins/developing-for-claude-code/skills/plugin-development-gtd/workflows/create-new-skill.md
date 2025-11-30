---
name: create-new-skill
description: Create high-quality skills for gtd-cc plugins using skill-creator methodology adapted for gtd-cc architectural patterns
---

# Create New Skill Workflow

This workflow creates high-quality skills for gtd-cc plugins by integrating the skill-creator's proven 6-step process with gtd-cc specific architectural patterns and conventions.

## When to Use This Workflow

Use this workflow when:
- Creating foundational skills for gtd-cc plugins
- Converting domain expertise into reusable skill components
- Building skills that require progressive disclosure design
- Creating skills that will be packaged for marketplace distribution

## Prerequisites

1. **Skill-creator Available**: Ensure the skill-creator skill is accessible from the anthropic-agent-skills marketplace
2. **Domain Understanding**: Clear understanding of the domain expertise the skill will provide
3. **Plugin Context**: Knowledge of which gtd-cc plugin the skill will belong to
4. **Resource Planning**: Identify what scripts, references, and assets the skill will need

## 6-Step Skill Creation Process (gtd-cc Adapted)

### Step 1: Understanding the Skill Requirements

**Purpose**: Define clear scope and usage patterns for the skill

**Actions**:
1. **Identify Core Expertise**: What specialized knowledge, workflows, or tool integrations will this skill provide?
2. **Define Usage Scenarios**: What specific user requests should trigger this skill?
3. **Establish Boundaries**: What is within scope vs out of scope for this skill?
4. **Resource Assessment**: What scripts, references, or assets will the skill need?

**gtd-cc Considerations**:
- Skills should be foundational components that support commands and agents
- Follow gtd-cc naming conventions (kebab-case directories, uppercase SKILL.md)
- Consider integration with existing gtd-cc plugin architecture
- Plan for progressive disclosure to optimize context usage

### Step 2: Planning Skill Structure and Resources

**Purpose**: Design the skill's organization and resource allocation

**Actions**:
1. **Progressive Disclosure Strategy**: Plan metadata, core instruction, and resource layers
2. **Resource Classification**: Categorize content into scripts/, references/, assets/
3. **Architecture Alignment**: Ensure skill structure supports gtd-cc layered patterns
4. **Quality Standards**: Define validation criteria for the skill

**Resource Organization Patterns**:
- **scripts/**: Executable code, automation tools, deterministic processes
- **references/**: Documentation, schemas, domain knowledge loaded on-demand
- **assets/**: Templates, images, configuration files used in outputs

**gtd-cc Specific Planning**:
- Plan for plugin-specific naming conventions and patterns
- Consider marketplace integration requirements
- Design for compatibility with existing gtd-cc validation workflows
- Ensure skill can be autonomously executed by agents

### Step 3: Initialize Skill with Templates

**Purpose**: Create the skill structure using appropriate templates and scaffolding

**Actions**:
1. **Use skill-creator**: Reference the skill-creator skill for proven initialization process
2. **Apply gtd-cc Templates**: Use templates from the templates/ directory
3. **Set Directory Structure**: Create proper skill directory with required subdirectories
4. **Generate Initial SKILL.md**: Start with comprehensive template and domain-specific content

**Template Selection**:
- Use `templates/SKILL.md` for basic skill structure
- Adapt for gtd-cc specific patterns and conventions
- Include progressive disclosure design elements
- Add gtd-cc architectural guidance

### Step 4: Edit and Develop Skill Content

**Purpose**: Write comprehensive skill content following best practices

**Actions**:
1. **Write Core Content**: Create detailed instructions in imperative/infinitive form
2. **Implement Progressive Disclosure**: Structure content for context efficiency
3. **Add Domain Expertise**: Include specialized knowledge and workflows
4. **Create Resource Files**: Develop scripts, references, and assets as planned

**Content Guidelines**:
- Use objective, instructional language (avoid "you should")
- Focus on information that would benefit other Claude instances
- Keep SKILL.md lean (<5k words) with details in references/
- Include clear workflow instructions and resource references

**gtd-cc Integration**:
- Reference existing gtd-cc patterns and conventions
- Include integration examples with commands and agents
- Add marketplace-specific guidance where applicable
- Ensure compatibility with plugin validation workflows

### Step 5: Package and Validate Skill

**Purpose**: Ensure skill quality and prepare for distribution

**Actions**:
1. **Run Validation**: Use skill-creator's quick_validate.py and gtd-cc specific validation
2. **Test Functionality**: Verify skill works as intended with example scenarios
3. **Check Integration**: Ensure skill integrates properly with plugin structure
4. **Package for Distribution**: Create distributable format if needed

**Validation Criteria**:
- YAML frontmatter format and required fields complete
- Naming conventions followed correctly
- Directory structure organized properly
- Resource references are valid and accessible
- Content quality and completeness

**gtd-cc Quality Standards**:
- Plugin manifest integration compatibility
- Marketplace distribution readiness
- Architectural pattern compliance
- Documentation and discoverability standards

### Step 6: Iteration and Improvement

**Purpose**: Refine skill based on testing and feedback

**Actions**:
1. **Test Real Usage**: Use skill in actual gtd-cc plugin workflows
2. **Collect Feedback**: Identify pain points and improvement opportunities
3. **Optimize Performance**: Refine for context efficiency and effectiveness
4. **Update Documentation**: Ensure examples and integration guides are current

**Continuous Improvement**:
- Monitor skill usage patterns and effectiveness
- Update resource organization based on actual needs
- Refine progressive disclosure strategy
- Maintain alignment with evolving gtd-cc patterns

## Integration with gtd-cc Development

### Plugin Registration
Once the skill is complete, register it in the plugin's `.claude-plugin/plugin.json`:
```json
{
  "components": [
    {
      "type": "skill",
      "name": "your-skill-name",
      "path": "skills/your-skill-name/SKILL.md"
    }
  ]
}
```

### Command and Agent Integration
Create thin wrappers that reference the skill:
```
Commands: "Use the <plugin-name> skill and follow its <workflow-name> exactly as written"
Agents: Delegate all procedures to the <plugin-name> skill workflows
```

### Quality Assurance
Run the complete validation workflow:
```
Use the developing-for-claude-code skill and follow its validate-existing-plugins workflow exactly as written
```

## Common Patterns and Examples

### Domain-Specific Skills
- **github-gtd**: GitHub workflow automation expertise
- **doc-standards**: Documentation methodology and best practices
- **ob-content-extraction**: Obsidian content extraction workflows
- **wr-crawling**: Web research and content extraction

### Workflow-Based Skills
- Process-oriented skills with step-by-step procedures
- Clear decision points and branching logic
- Integration with external tools and APIs
- Error handling and recovery procedures

### Reference-Based Skills
- Domain knowledge and terminology
- Integration patterns and best practices
- Troubleshooting guides and examples
- API documentation and schema references

## Success Criteria

A successful gtd-cc skill should:
- Provide clear, actionable domain expertise
- Integrate seamlessly with plugin architecture
- Use progressive disclosure for context efficiency
- Support both command and agent integration
- Pass all validation and quality checks
- Enable effective problem-solving in its domain

## Troubleshooting

**Common Issues**:
- Skill not triggering: Check YAML frontmatter name and description quality
- Context inefficiency: Review progressive disclosure strategy
- Integration problems: Verify plugin manifest registration
- Validation failures: Check naming conventions and structure

**Resources**:
- skill-creator skill for advanced debugging
- validate-existing-plugins workflow for comprehensive checking
- gtd-cc architectural patterns reference
- Plugin development guidelines and examples