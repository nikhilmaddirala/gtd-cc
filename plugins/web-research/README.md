# Web Research Plugin

Comprehensive toolkit for web crawling, content analysis, and research automation. Provides both interactive commands for beginners and skill-based access for advanced users.

## Overview

This plugin enables efficient web research workflows through two complementary approaches:

1. **Interactive Commands** - Guided workflows for common tasks (ideal for beginners)
2. **Advanced Skills** - Powerful tools for complex automation and custom workflows

Whether you need to extract structured data from websites, perform AI-powered content analysis, or build automated web data pipelines, this plugin has the right tool for your workflow.

## Quick Start

### Installation

```bash
/plugin install web-research@gtd-cc
```

### Choose Your Approach

**For quick, interactive tasks:**
```bash
/fetch-page        # Extract content from a single page
/crawl-site        # Crawl entire websites
/get-docs          # Extract documentation from sites
```

**For advanced automation and scripting:**
- Use skills directly for programmatic access
- Combine multiple skills in custom workflows
- Build automated data pipelines

## Interactive Commands

### `/fetch-page` - Extract Single Page Content
Interactive guide for extracting content from a single URL with options for:
- Content filtering and cleaning
- Multiple output formats (markdown, JSON, text)
- JavaScript rendering support
- Custom extraction patterns

### `/crawl-site` - Crawl Entire Websites
Guided workflow for comprehensive site crawling:
- Automatic depth detection and control
- Sitemap generation and discovery
- Organized output by URL structure
- Progress tracking and resume capability

### `/get-docs` - Documentation Extraction
Specialized workflow for extracting structured documentation:
- Automatic detection of documentation patterns
- Table of contents generation
- Code example preservation
- API documentation structuring

## Advanced Skills

### Core Crawling Skills

#### 1. Web Scraping Fundamentals
Foundation patterns for web content extraction:
- Basic page fetching and parsing
- JavaScript handling strategies
- Error handling and retry logic
- Content cleaning and normalization

**Use when:** You need fundamental scraping patterns or are new to web scraping

#### 2. Crawl4AI Toolkit
Complete web crawling and data extraction SDK:
- Async crawling for performance
- Schema generation for structured data
- Batch processing capabilities
- Advanced JavaScript support

**Use when:** You need programmatic access or are building automated workflows

#### 3. Site Crawling & Sitemaps
Advanced crawling strategies for complex sites:
- Intelligent crawl depth management
- Sitemap discovery and parsing
- Rate limiting and politeness policies
- Large-scale site mapping

**Use when:** You need to crawl entire sites or handle complex navigation

### Specialized Skills

#### 4. Documentation Extraction
Specialized patterns for documentation sites:
- API documentation detection
- Tutorial and guide extraction
- Code example preservation
- Cross-link and reference mapping

**Use when:** You're working with technical documentation or knowledge bases

#### 5. Gemini Web Research
AI-powered content analysis using Google Gemini:
- Content summarization and synthesis
- Research question answering
- Multi-source analysis
- Headless mode for automation

**Use when:** You need AI-assisted content analysis or research synthesis

#### 6. Web Crawler
Simple site-to-markdown conversion:
- Timestamped crawl outputs
- Markdown formatting for knowledge management
- Obsidian vault compatibility
- Offline reference creation

**Use when:** You want to archive sites or build personal knowledge bases


#### 7. Web Fetch with images
Fetch webpage as markdown file with images


## Common Workflows

### Extract Product Information from E-commerce Site
```bash
# Interactive approach
/fetch-page
# Follow prompts for URL and extraction pattern

# Programmatic approach
skill: crawl4ai
python scripts/extraction_pipeline.py \
  --generate-schema https://shop.example.com \
  "extract product name, price, and description"
```

### Research and Analyze Multiple Sources
```bash
# Interactive approach
/crawl-site
# Enter research site, then use gemini for analysis

# Programmatic approach
skill: gemini-web-research
cat content.txt | gemini -p "Summarize key findings"
```

### Build Documentation Knowledge Base
```bash
# Interactive approach
/get-docs
# Extract docs directly to your Obsidian vault

# Programmatic approach
skill: documentation-extraction
# Use provided scripts for batch processing
```

### Archive Website for Offline Reference
```bash
# Interactive approach
/crawl-site
# Set depth and output directory

# Programmatic approach
skill: web-crawler
uvx crawl4ai crawl \
  --url "https://docs.example.com" \
  --output-dir "./archived-docs" \
  --max-depth 2
```

## Configuration

### Plugin Settings
Create `.claude/web-research.local.md` for custom configuration:
```yaml
cache:
  duration: 3600  # Cache duration in seconds

crawling:
  default_depth: 3
  concurrency: 4
  delay: 1  # Seconds between requests

output:
  format: markdown  # markdown, json, text
  include_metadata: true

filters:
  exclude_patterns: [".*/login.*", ".*/admin.*"]
  content_selectors: ["main", "article", "#content"]
```

### Skill-Specific Configuration
Each skill can be configured independently:
- **Crawl4AI**: Install with `pip install crawl4ai>=0.7.4`
- **Gemini**: Install and configure Google Gemini CLI
- **Web Crawler**: Configure output formats and directory structures

See individual skill documentation for detailed configuration options.

## Requirements

### Core Dependencies
- Python 3.8+
- crawl4ai library (v0.7.4+)

### Optional Dependencies
- Google Gemini CLI (for AI-powered analysis)
- jq (for JSON processing)
- lynx (for text-only fallback)

## Installation Checklist

```bash
# 1. Install core dependencies
pip install crawl4ai

# 2. Verify installation
crawl4ai-doctor

# 3. (Optional) Install Gemini CLI
# Follow: https://github.com/google-gemini/gemini-cli

# 4. Test the plugin
/fetch-page
# Enter https://example.com to verify everything works
```

## File Structure

```
plugins/web-research/
├── README.md                    # This file
├── .claude-plugin/
│   └── plugin.json             # Plugin manifest
├── commands/                   # Interactive command definitions
│   ├── fetch-page.md
│   ├── crawl-site.md
│   └── get-docs.md
└── skills/                     # Advanced skill definitions
    ├── web-scraping-fundamentals/
    ├── crawl4ai/
    ├── site-crawling/
    ├── documentation-extraction/
    ├── gemini-web-research/
    └── web-crawler/
```

## Best Practices

### For Beginners
1. Start with `/fetch-page` for simple extraction
2. Use `/get-docs` for documentation sites
3. Progress to `/crawl-site` when you need more comprehensive data

### For Advanced Users
1. Combine skills for complex workflows
2. Use schema generation for reliable data extraction
3. Leverage batch processing for multiple URLs
4. Integrate with automation pipelines

### Performance Tips
- Use appropriate crawl depths (3 is usually sufficient)
- Configure rate limiting to avoid overwhelming sites
- Cache results when possible
- Use async patterns for large-scale crawling

## Troubleshooting

### Common Issues

**JavaScript not rendering:**
- Ensure crawl4ai is properly installed: `crawl4ai-setup`
- Check browser automation dependencies

**Rate limiting:**
- Increase delays between requests
- Respect robots.txt files
- Use appropriate concurrency settings

**Memory issues with large sites:**
- Limit crawl depth
- Process in batches
- Use streaming for large outputs

See individual skill documentation for detailed troubleshooting guides.

## Related Documentation

- [Web Scraping Fundamentals SKILL.md](skills/web-scraping-fundamentals/SKILL.md)
- [Crawl4AI SKILL.md](skills/crawl4ai/SKILL.md)
- [Site Crawling SKILL.md](skills/site-crawling/SKILL.md)
- [Documentation Extraction SKILL.md](skills/documentation-extraction/SKILL.md)
- [Gemini Web Research SKILL.md](skills/gemini-web-research/SKILL.md)
- [Web Crawler SKILL.md](skills/web-crawler/SKILL.md)

## Support

For issues or questions:
1. Check individual skill documentation first
2. Review troubleshooting guides
3. Refer to the main [GTD-CC Plugin Marketplace](../../README.md) for general questions

---

*This plugin is part of the GTD-CC marketplace. See the main repository for additional plugins and workflows.*
