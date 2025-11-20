# Data Plugin Template

Data plugins handle data processing, transformation, and management. These plugins provide capabilities for working with data in various formats, structures, and sources.

## Use Cases

Data plugins are ideal when you need to:

- Process and transform data in various formats (CSV, JSON, SQL, etc.)
- Manage data pipelines and ETL workflows
- Provide data analysis and visualization
- Handle bulk data operations and migrations
- Create data connectors and sources

## Core Structure

A data plugin typically includes:

### Commands

Interactive commands for data operations:

- Data processing and transformation commands
- Pipeline configuration and execution
- Data analysis and reporting
- Import/export and data migration

### Agents

Autonomous agents for complex data operations:

- Batch processing and bulk operations
- Pipeline execution and orchestration
- Error recovery and data validation
- Data transformation workflows

### Skills

Comprehensive knowledge about data handling:

- Data format specifications and handling
- Processing algorithms and patterns
- Integration with external data sources
- Best practices and optimization patterns
- Data validation and quality assurance

## Example Structure

```
plugins/my-data/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── README.md                 # Plugin documentation
├── commands/
│   ├── process-data.md       # Data processing command
│   ├── create-pipeline.md    # Pipeline creation
│   └── analyze-data.md       # Analysis command
├── agents/
│   ├── batch-processor.md    # Batch processing agent
│   └── pipeline-executor.md  # Pipeline execution agent
├── skills/
│   └── data-processing/
│       ├── SKILL.md          # Core skill documentation
│       ├── formats.md        # Data format reference
│       ├── algorithms.md     # Processing algorithms
│       └── patterns.md       # Best practices
└── references/
    └── examples/
        ├── csv-processing.md
        └── json-pipeline.md
```

## Plugin Manifest

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "my-data",
  "version": "0.1.0",
  "description": "Data plugin for [data processing domain]",
  "author": "Your Name",
  "homepage": "https://github.com/yourusername/gtd-cc/tree/main/plugins/my-data",
  "license": "MIT",
  "commands": [
    {
      "name": "process-data",
      "path": "commands/process-data.md",
      "description": "Process and transform data"
    },
    {
      "name": "create-pipeline",
      "path": "commands/create-pipeline.md",
      "description": "Create data processing pipeline"
    }
  ],
  "agents": [
    {
      "name": "batch-processor",
      "path": "agents/batch-processor.md",
      "description": "Autonomous batch processing agent"
    },
    {
      "name": "pipeline-executor",
      "path": "agents/pipeline-executor.md",
      "description": "Pipeline execution and monitoring"
    }
  ],
  "skills": [
    {
      "name": "data-processing",
      "path": "skills/data-processing/SKILL.md",
      "description": "Data processing techniques and best practices"
    }
  ]
}
```

## Key Files to Create

### 1. README.md

Document the plugin's data processing capabilities and use cases.

### 2. Commands

Create commands for:
- Data processing and transformation
- Pipeline creation and management
- Data analysis and reporting
- Import/export operations

### 3. Agents

Create agents for:
- Batch processing large datasets
- Pipeline orchestration and execution
- Data validation and quality checks
- Error handling and recovery

### 4. Skills

Create comprehensive skills covering:
- Data format specifications and handling
- Processing algorithms and techniques
- Pipeline design patterns
- Performance optimization
- Data validation and quality assurance
- Integration with data sources

## Development Workflow

1. Define the data formats and sources your plugin handles
2. Create the plugin directory structure
3. Write the plugin manifest
4. Develop commands for common data operations
5. Create agents for complex workflows
6. Document data processing patterns and best practices
7. Implement comprehensive error handling
8. Test with real-world data examples
9. Validate structure and manifest
10. Submit for review

## Testing Checklist

Before publishing:

- [ ] All data operations work correctly
- [ ] Data processing is efficient and performant
- [ ] Error handling works for invalid data
- [ ] All commands execute without errors
- [ ] All agents handle success and error cases
- [ ] Plugin manifest is valid JSON
- [ ] All referenced files exist and are valid
- [ ] Documentation is complete and accurate
- [ ] Examples demonstrate real-world use cases
- [ ] Data validation catches common errors

## Common Patterns

### Data Transformation

Implement clear transformation logic with validation at each step.

### Pipeline Architecture

Design pipelines as composable stages that can be reused.

### Error Handling

Implement comprehensive error handling with data recovery options.

### Performance

Optimize for large datasets with streaming and batch processing.

### Validation

Implement data validation at ingestion, transformation, and export stages.

## Data Plugin Best Practices

- Document all supported data formats clearly
- Implement comprehensive error handling and recovery
- Validate data at each processing stage
- Optimize for performance with large datasets
- Provide clear progress reporting for long operations
- Support both interactive and batch processing
- Design pipelines as reusable, composable units
- Include data quality checks and reporting
- Provide examples with real-world data
- Document assumptions and limitations
