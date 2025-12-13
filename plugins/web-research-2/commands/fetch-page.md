---
name: fetch-page
description: Interactive guide for extracting content from a single web page
allowed-tools: [Read, Write, Edit, Bash, AskUserQuestion]
argument-hint: [URL] - the web page to extract content from
---

# Fetch Page Content

This command guides you through extracting content from a single web page using the web-scraping-fundamentals skill.

## Interactive Extraction Process

I'll help you extract content from a web page by asking a few questions to determine the best approach:

### Step 1: URL and Content Type
**Please provide the URL you want to extract content from.**

I'll analyze the URL and guide you to the appropriate extraction method:

1. **Simple HTML pages** → Use curl/jq for fast extraction
2. **JavaScript-heavy sites** → Use crawl4ai with browser automation
3. **Documentation pages** → Use specialized documentation extraction

### Step 2: Extraction Options

Based on the URL, I'll ask about:
- **Content focus** (specific topics, full content, or particular sections)
- **Output format** (markdown, HTML, or structured JSON)
- **Content filtering** (relevance-based filtering if needed)

### Step 3: Execution and Results

I'll guide you through:
- Selecting the appropriate skill
- Configuring extraction parameters
- Running the extraction with optimal settings
- Formatting and saving the results

## Example Usage Scenarios

### Simple Blog Post
```
URL: https://example.com/blog/my-post
Approach: Basic extraction with curl/jq
Output: Clean markdown
```

### JavaScript Dashboard
```
URL: https://app.example.com/dashboard
Approach: crawl4ai with JavaScript rendering
Wait for: Dynamic content to load
```

### API Documentation
```
URL: https://docs.example.com/api/reference
Approach: Documentation extraction with code preservation
Focus: API endpoints and examples
```

## Troubleshooting Tips

- **Timeout issues**: Increase timeout for slow-loading sites
- **Missing content**: Try CSS selectors to focus on specific content areas
- **JavaScript errors**: Ensure browser automation is enabled
- **Rate limiting**: Add delays between requests if needed

## Getting Started

Provide the URL you want to extract content from, and I'll guide you through the optimal extraction process!