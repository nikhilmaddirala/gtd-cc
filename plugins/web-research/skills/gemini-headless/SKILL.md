---
name: gemini-headless
description: Web research and content analysis using Google Gemini CLI in headless mode. Use this skill when you need to analyze web content, process research queries, or synthesize information from multiple sources using the gemini -p flag for automation and scripting.
version: 1.0.0
gemini_cli_version: ">=0.0.1"
last_updated: 2025-01-16
---

# Gemini Headless CLI

## Overview

This skill provides comprehensive support for using Google Gemini CLI in headless mode (`gemini -p`) for web research, content analysis, and automated information processing. The headless mode enables scripting, automation, and integration with other tools without interactive prompts.

## Quick Start

### Installation Check

```bash
# Verify gemini CLI is installed
gemini --version

# If not installed, install via npm or your package manager
npm install -g @google/generative-ai-cli
# or
pip install google-generative-ai
```

### Basic Headless Query

```bash
# Simple query with -p (prompt) flag
gemini -p "What is machine learning?"

# Save output to file
gemini -p "Explain Docker containers" > output.txt

# Use with pipes
cat research.txt | gemini -p "Summarize this content"
```

## Core Headless Mode Fundamentals

### 1. Basic Prompt Flag Usage

The `-p` or `--prompt` flag enables headless mode for non-interactive usage:

```bash
# Direct prompt
gemini -p "Your question here"

# Short form
gemini -p "What is Kubernetes?"

# Multi-word queries
gemini -p "Compare Python and JavaScript for web development"
```

### 2. Input Methods

#### Direct Prompts
```bash
# Single line query
gemini -p "List the benefits of microservices architecture"

# For longer prompts, use quotes
gemini -p "Provide a detailed explanation of machine learning algorithms including supervised, unsupervised, and reinforcement learning"
```

#### Stdin Piping
```bash
# Pipe from echo
echo "Analyze this code for security issues" | gemini -p

# Pipe from cat
cat README.md | gemini -p "Summarize the key points"

# Pipe from other commands
curl https://example.com | gemini -p "Extract the main topics from this webpage"

# Combine with grep
grep "TODO" codebase.txt | gemini -p "What are the priorities?"
```

#### File Input Combined with Prompts
```bash
# Process file content with a query
cat document.txt | gemini -p "Extract the key metrics and statistics"

# Multiple files
cat file1.txt file2.txt | gemini -p "Identify similarities and differences"

# With head/tail for large files
head -100 large_log.txt | gemini -p "Identify error patterns"
```

### 3. Output Formats

#### Text Output (Default)
```bash
# Human-readable text response
gemini -p "Explain REST APIs"

# Save to file
gemini -p "What is GraphQL?" > response.txt

# Append to file
gemini -p "Another question" >> response.txt
```

#### JSON Output
```bash
# Structured JSON output including metadata
gemini -p "List programming languages" --output-format json

# Parse specific field with jq
gemini -p "What is DevOps?" --output-format json | jq '.response'

# Pretty print JSON
gemini -p "Explain containerization" --output-format json | jq '.'

# Extract response only
gemini -p "Define API" --output-format json | jq -r '.response'
```

#### Streaming JSON Output
```bash
# Real-time events as newline-delimited JSON
gemini -p "Generate a detailed tutorial" --output-format stream-json

# Process stream with jq
gemini -p "Create a guide" --output-format stream-json | jq '.event'

# Line-by-line processing
gemini -p "Write a summary" --output-format stream-json | while read line; do
  echo "$line" | jq .
done
```

## Practical Web Research Patterns

### 1. Content Analysis Pipeline

Analyze web content with gemini in automated workflows:

```bash
# Step 1: Fetch content with curl
content=$(curl -s https://example.com/article)

# Step 2: Pipe to gemini for analysis
echo "$content" | gemini -p "Extract the main arguments and supporting evidence"

# Step 3: Save structured analysis
echo "$content" | gemini -p "Provide a bullet-point summary" > analysis.txt
```

### 2. Multi-Source Research

Synthesize information from multiple sources:

```bash
# Combine multiple inputs
{
  echo "=== Source 1 ==="
  curl -s https://source1.com
  echo -e "\n=== Source 2 ==="
  curl -s https://source2.com
} | gemini -p "Compare and synthesize the information from both sources"
```

### 3. Code Review and Analysis

```bash
# Analyze code for issues
cat application.py | gemini -p "Review this Python code for security vulnerabilities and suggest improvements"

# Document code
cat function.js | gemini -p "Generate comprehensive JSDoc comments for this function"

# Explain complex code
cat complex_algorithm.ts | gemini -p "Explain what this code does in simple terms"
```

### 4. Research Query Automation

```bash
# Research a topic systematically
queries=(
  "What are the main use cases for machine learning?"
  "What are the current limitations of ML?"
  "What are emerging trends in ML?"
)

for query in "${queries[@]}"; do
  echo "=== $query ===" >> research.md
  gemini -p "$query" >> research.md
  echo "" >> research.md
done
```

### 5. JSON Parsing for Structured Analysis

```bash
# Get structured response
response=$(gemini -p "List 5 web development frameworks with version numbers" --output-format json)

# Extract response field
frameworks=$(echo "$response" | jq -r '.response')

# Process structured data
echo "$response" | jq '.response' | grep -i "react"
```

### 6. Batch Processing

```bash
# Process multiple queries from a file
while read -r query; do
  echo "Processing: $query"
  gemini -p "$query" --output-format json | jq '.response' >> results.jsonl
done < queries.txt
```

### 7. Real-time Streaming Analysis

```bash
# Stream long-form content generation
gemini -p "Write a comprehensive guide to Docker" --output-format stream-json | jq '.data'

# Monitor stream in real-time
gemini -p "Create a tutorial" --output-format stream-json | while read line; do
  echo "$line" | jq -r '.data'
done
```

## Common Use Cases

### Documentation Generation

```bash
# Create API documentation
{
  echo "Generate OpenAPI documentation for a REST API with:"
  echo "- User endpoints (CRUD)"
  echo "- Product endpoints (CRUD)"
  echo "- Authentication with JWT"
} | gemini -p > api-docs.md
```

### Research Report Generation

```bash
# Multi-section research report
{
  echo "Create a comprehensive research report on AI safety with sections:"
  echo "1. Executive Summary"
  echo "2. Current State of Research"
  echo "3. Key Challenges"
  echo "4. Recommendations"
} | gemini -p > ai_safety_report.md
```

### Log Analysis

```bash
# Analyze application logs
tail -100 app.log | gemini -p "Identify and explain any error patterns or issues"

# Parse JSON logs
cat service.log | gemini -p "Summarize the performance metrics and identify bottlenecks" --output-format json
```

### Content Translation and Summarization

```bash
# Summarize article
curl -s https://news.example.com/article | gemini -p "Provide a brief 3-sentence summary"

# Translate technical content
echo "Technical documentation about React hooks" | gemini -p "Explain this in beginner-friendly language"
```

### Data Extraction

```bash
# Extract specific information
cat document.pdf | gemini -p "Extract all email addresses, phone numbers, and names"

# Parse structured data
curl https://api.example.com/data | gemini -p "Extract key metrics and format as JSON"
```

## Integration Patterns

### 1. Shell Script Integration

```bash
#!/bin/bash
# analyze_content.sh - Automated content analysis

analyze_url() {
  local url=$1
  local query=$2

  echo "Analyzing: $url"
  curl -s "$url" | gemini -p "$query"
}

# Usage
analyze_url "https://example.com" "Summarize the main topic"
```

### 2. Makefile Integration

```makefile
.PHONY: research analyze summarize

research:
	@gemini -p "Research current best practices for $(TOPIC)"

analyze:
	@cat $(FILE) | gemini -p "Analyze this content"

summarize:
	@curl -s $(URL) | gemini -p "Create a concise summary"
```

### 3. Pipeline with jq for Complex Processing

```bash
#!/bin/bash
# Process responses with jq for further analysis

gemini -p "List 10 Python libraries" --output-format json | \
  jq '.response | split("\n")' | \
  jq 'map(select(length > 0))' > libraries.json

# Process and filter
gemini -p "What are data science tools?" --output-format json | \
  jq '.response' | \
  jq 'split("\n") | map(select(. | contains("Python")))'
```

### 4. Conditional Processing

```bash
#!/bin/bash
# Conditional analysis based on content

response=$(cat document.txt | gemini -p "Does this contain security-related content?" --output-format json)

# Check if contains "Yes" or "True"
if echo "$response" | jq '.response' | grep -qi "yes\|true"; then
  echo "Security content detected - running detailed analysis"
  cat document.txt | gemini -p "Identify all security vulnerabilities"
fi
```

### 5. Batch Processing with Error Handling

```bash
#!/bin/bash
# Batch process with error handling

process_queries() {
  local file=$1
  local output=$2

  while IFS= read -r query; do
    echo "Processing: $query"

    if gemini -p "$query" >> "$output" 2>/dev/null; then
      echo "✅ Success"
    else
      echo "❌ Failed: $query"
    fi

    # Rate limiting
    sleep 1
  done < "$file"
}

process_queries queries.txt results.txt
```

## Best Practices

### 1. Headless Usage

- Always use `-p` flag for non-interactive scripting
- Avoid interactive prompts in automated workflows
- Handle errors gracefully with proper exit codes

### 2. Input Handling

```bash
# Use proper quoting for complex queries
gemini -p "Your multi-line query here" # Avoid unquoted strings

# For dynamic content, use variables carefully
query="Analyze this: $content"
gemini -p "$query" # Ensure proper quoting
```

### 3. Output Management

```bash
# Save structured output for reuse
gemini -p "Your query" --output-format json > response.json

# Parse and validate responses
response=$(gemini -p "Query" --output-format json)
if echo "$response" | jq . > /dev/null 2>&1; then
  echo "Valid JSON response"
fi
```

### 4. Rate Limiting and Throttling

```bash
#!/bin/bash
# Implement delays to respect API limits

for query in "${queries[@]}"; do
  gemini -p "$query" > output.txt
  sleep 2  # Wait 2 seconds between requests
done
```

### 5. Error Handling

```bash
#!/bin/bash
# Proper error handling

if ! command -v gemini &> /dev/null; then
  echo "Error: gemini CLI not installed"
  exit 1
fi

if ! gemini -p "test" &> /dev/null; then
  echo "Error: gemini CLI not properly configured"
  exit 1
fi
```

### 6. Performance Optimization

```bash
# Use streaming for large outputs
gemini -p "Generate long content" --output-format stream-json | \
  jq '.data' > large_output.txt

# Process in parallel (with caution)
for query in "${queries[@]}"; do
  gemini -p "$query" > "output_$i.txt" &
done
wait
```

## Combining with Other Tools

### With crawl4ai for Web Research

```bash
#!/bin/bash
# Crawl content and analyze with gemini

# Step 1: Crawl content using crawl4ai
crawl_output=$(crawl4ai crawl https://example.com --format markdown)

# Step 2: Analyze with gemini
echo "$crawl_output" | gemini -p "Extract key findings and actionable insights"
```

### With curl for API Integration

```bash
# Fetch JSON API data and analyze
curl -s https://api.example.com/data | \
  jq '.results[]' | \
  gemini -p "Summarize these API results"
```

### With grep for Log Analysis

```bash
# Find patterns and analyze
grep "ERROR" app.log | gemini -p "What are the common error types and their causes?"
```

## Troubleshooting

### Authentication Issues

```bash
# Verify authentication
gemini -p "test" 2>&1

# Check API credentials
echo $GEMINI_API_KEY  # Ensure API key is set

# Re-authenticate if needed
gemini auth login
```

### Output Issues

```bash
# Check if output is empty
response=$(gemini -p "Your query")
if [ -z "$response" ]; then
  echo "No response received"
fi

# Verify JSON parsing
if ! echo "$response" | jq . &>/dev/null; then
  echo "Invalid JSON response"
  echo "$response"
fi
```

### Rate Limiting

```bash
# If hitting rate limits, increase delays
sleep 5  # Increase delay between requests

# Check response for rate limit errors
response=$(gemini -p "Query" --output-format json)
if echo "$response" | jq '.error' | grep -qi "rate"; then
  echo "Rate limit hit - backing off"
fi
```

## Resources

- [Google Gemini CLI Documentation](https://github.com/google-gemini/gemini-cli)
- [Headless Mode Guide](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/headless.md)
- [JSON Output Documentation](https://github.com/google-gemini/gemini-cli/docs)
- [API Integration Patterns](https://github.com/google-gemini/gemini-cli)

## Integration with gtd-cc

This skill is designed to integrate with other components in the gtd-cc ecosystem:

- **Web Research Plugin** - Combine with crawl4ai for enhanced content analysis
- **GitHub Integration** - Analyze code and generate documentation
- **Obsidian Integration** - Process research notes and generate summaries

When using this skill with other tools:

1. Ensure gemini CLI is installed and authenticated
2. Use `-p` flag for all non-interactive usage
3. Handle output formats consistently (prefer JSON for scripting)
4. Implement proper error handling and rate limiting
5. Document the pipeline for reproducibility
