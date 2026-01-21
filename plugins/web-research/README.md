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
/web-fetch-page        # Extract content from a single page
/web-crawl-site        # Crawl entire websites
/web-get-docs          # Extract documentation from sites
```

**For advanced automation and scripting:**
- Use skills directly for programmatic access
- Combine multiple skills in custom workflows
- Build automated data pipelines

## Interactive Commands

### `/web-fetch-page` - Extract Single Page Content
Interactive guide for extracting content from a single URL with options for:
- Content filtering and cleaning
- Multiple output formats (markdown, JSON, text)
- JavaScript rendering support
- Custom extraction patterns

### `/web-crawl-site` - Crawl Entire Websites
Guided workflow for comprehensive site crawling:
- Automatic depth detection and control
- Sitemap generation and discovery
- Organized output by URL structure
- Progress tracking and resume capability

### `/web-get-docs` - Documentation Extraction
Specialized workflow for extracting structured documentation:
- Automatic detection of documentation patterns
- Table of contents generation
- Code example preservation
- API documentation structuring

## Advanced Skills

### Core Skills

#### 1. Web Search
General web search patterns and techniques:
- Gemini CLI coordination for advanced searches
- Built-in WebSearch tool usage guidelines
- Search query optimization
- Domain-specific search strategies

**Use when:** You need to perform web searches, find current information, or research topics online

#### 2. Web Fetch
Download web articles with images as clean markdown:
- Jina AI Reader (primary method)
- WebFetch tool integration
- Image download and markdown update
- Multiple fallback options

**Use when:** You need to download articles with images for offline reference

#### 3. Crawl4AI Toolkit
Complete Crawl4AI SDK reference and implementation guide:
- Comprehensive SDK documentation
- Ready-to-use scripts for common patterns
- Optimized workflows for efficient data extraction
- Error handling and best practices

**Use when:** You need programmatic access to crawl4ai or are building automated web data pipelines

#### 4. Site Crawling
Intelligent website crawling, sitemap generation, and conversion:
- Advanced crawling strategies with depth control
- Simple site-to-markdown conversion
- Sitemap generation and link analysis
- Concurrent crawling patterns

**Use when:** You need to crawl entire sites, generate sitemaps, or systematically explore web content

#### 5. Content Extraction
Specialized extraction from documentation platforms:
- Documentation platform detection
- API docs, tutorials, and reference guides extraction
- Multi-page documentation processing
- Structured data extraction patterns

**Use when:** You need to extract structured documentation or knowledge base content


## Common Workflows

### Extract Product Information from E-commerce Site
```bash
# Interactive approach
/web-fetch-page
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
/web-crawl-site
# Enter research site, then use web-search for analysis

# Programmatic approach
skill: web-search
cat content.txt | gemini -p "Summarize key findings"
```

### Build Documentation Knowledge Base
```bash
# Interactive approach
/web-get-docs
# Extract docs directly to your Obsidian vault

# Programmatic approach
skill: content-extraction
# Use provided scripts for batch processing
```

### Archive Website for Offline Reference
```bash
# Interactive approach
/web-crawl-site
# Set depth and output directory

# Programmatic approach
skill: site-crawling
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
- **Web Search**: Install and configure Google Gemini CLI
- **Web Fetch**: Configure image download options and fallback methods
- **Crawl4AI Toolkit**: Install with `pip install crawl4ai>=0.7.4`
- **Site Crawling**: Configure crawl depth, output formats, and directory structures
- **Content Extraction**: Configure platform-specific selectors and extraction patterns

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
/web-fetch-page
# Enter https://example.com to verify everything works
```

## File Structure

```
plugins/web-research/
├── README.md                    # This file
├── .claude-plugin/
│   └── plugin.json             # Plugin manifest
├── commands/                   # Interactive command definitions (thin wrappers)
│   ├── web-fetch-page.md
│   ├── web-crawl-site.md
│   └── web-get-docs.md
└── skills/                     # Advanced skill definitions
    ├── web-search/             # General web search patterns
    ├── web-fetch/              # Article download with images
    ├── crawl4ai-toolkit/      # Complete Crawl4AI SDK
    ├── site-crawling/          # Site crawling and conversion
    └── content-extraction/     # Documentation extraction
```

## Best Practices

### For Beginners
1. Start with `/web-fetch-page` for simple extraction
2. Use `/web-get-docs` for documentation sites
3. Progress to `/web-crawl-site` when you need more comprehensive data

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

- [Web Search SKILL.md](skills/web-search/SKILL.md)
- [Web Fetch SKILL.md](skills/web-fetch/SKILL.md)
- [Crawl4AI Toolkit SKILL.md](skills/crawl4ai-toolkit/SKILL.md)
- [Site Crawling SKILL.md](skills/site-crawling/SKILL.md)
- [Content Extraction SKILL.md](skills/content-extraction/SKILL.md)

## Support

For issues or questions:
1. Check individual skill documentation first
2. Review troubleshooting guides
3. Refer to the main [GTD-CC Plugin Marketplace](../../README.md) for general questions

---

*This plugin is part of the GTD-CC marketplace. See the main repository for additional plugins and workflows.*
