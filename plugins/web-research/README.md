# Web Research Plugin

Comprehensive toolkit for web crawling, content analysis, and research automation. Extract structured data from websites, perform headless research queries, and build automated web data pipelines.

## Overview

This plugin provides three specialized skills for web research workflows:

- **Crawl4AI** - Full-featured web crawling and data extraction with schema generation
- **Gemini Web Research** - AI-powered content analysis and research synthesis using Google Gemini CLI
- **Web Crawler** - Automated website crawling with organized markdown output

These skills enable rapid information gathering, content analysis, and research automation for your development and knowledge management workflows.

## Skills

### 1. Crawl4AI

Complete toolkit for web crawling and data extraction using the Crawl4AI library.

**Best for:**
- Extracting structured data from websites
- Handling JavaScript-heavy pages
- Crawling multiple URLs in a pipeline
- Building automated web scraping workflows
- Generating extraction schemas for complex pages

**Quick example:**
```bash
python scripts/basic_crawler.py https://example.com
```

**Key features:**
- Async web crawling for performance
- Markdown extraction and formatting
- Batch processing of multiple URLs
- Schema generation for LLM-free extraction
- Handles dynamic content with JavaScript

See `skills/crawl4ai/SKILL.md` for comprehensive documentation and SDK reference.

### 2. Gemini Web Research

Web research and content analysis using Google Gemini CLI in headless mode for automation and scripting.

**Best for:**
- Analyzing and summarizing web content
- Performing research queries without interactive prompts
- Synthesizing information from multiple sources
- Scripting research workflows
- Processing content through AI analysis

**Quick example:**
```bash
gemini -p "What is machine learning?"
```

**Key features:**
- Headless mode (`-p` flag) for non-interactive usage
- Piping support for content processing
- Integration with shell scripts and automation
- Fast content analysis and synthesis
- Scriptable research workflows

See `skills/gemini-web-research/SKILL.md` for comprehensive documentation and usage patterns.

### 3. Web Crawler

Crawl entire websites and save content as organized markdown files for knowledge management systems like Obsidian.

**Best for:**
- Saving website content for offline access
- Building knowledge bases from web sources
- Archiving reference materials
- Creating markdown-based documentation
- Organizing crawled content by URL structure

**Quick example:**
```bash
uvx crawl4ai crawl \
  --url "https://example.com" \
  --output-dir "./web-crawl/example-com" \
  --max-depth 3 \
  --format markdown
```

**Key features:**
- Automated depth-based crawling (default: 3 levels)
- Timestamped output directories
- Preserves website structure in file organization
- Markdown formatting for easy integration
- Handles multiple pages automatically

See `skills/web-crawler/SKILL.md` for configuration options and advanced usage.

## Getting Started

### Installation

The web-research plugin is installed as part of the gtd-cc marketplace:

```bash
/plugin install web-research@gtd-cc
```

### Choose Your Use Case

**Extracting structured data from a single site:**
- Use Crawl4AI with schema generation
- Specify target extraction patterns
- Process results programmatically

**Analyzing and summarizing content:**
- Use Gemini Headless for quick analysis
- Pipe content through AI synthesis
- Integrate with automation scripts

**Building a knowledge base from websites:**
- Use Web Crawler for full site capture
- Save to your Obsidian vault or knowledge system
- Organize by URL structure automatically

## Common Workflows

### Extract Product Information from E-commerce Site

```bash
python scripts/extraction_pipeline.py \
  --generate-schema https://shop.example.com \
  "extract product name, price, and description"
```

### Analyze and Summarize Research Paper

```bash
cat research_paper.txt | gemini -p "Summarize the key findings and methodology in this paper"
```

### Archive Website for Offline Reference

```bash
uvx crawl4ai crawl \
  --url "https://docs.example.com" \
  --output-dir "./archived-docs" \
  --max-depth 2
```

### Batch Process Multiple URLs

```bash
python scripts/batch_crawler.py urls.txt
```

## Configuration

Each skill can be configured independently:

- **Crawl4AI**: Adjust depth, output format, extraction patterns
- **Gemini Headless**: Configure API keys, model selection, prompt templates
- **Web Crawler**: Set depth limits, output directory, markdown formatting

See individual skill documentation for configuration details.

## Requirements

- Crawl4AI: Python 3.8+, Crawl4AI library (v0.7.4+)
- Gemini Headless: Google Gemini CLI installed and configured
- Web Crawler: Crawl4AI (via uvx) or local installation

## Related Documentation

- [Crawl4AI SKILL.md](skills/crawl4ai/SKILL.md) - Complete SDK reference and examples
- [Gemini Web Research SKILL.md](skills/gemini-web-research/SKILL.md) - Headless mode guide and patterns
- [Web Crawler SKILL.md](skills/web-crawler/SKILL.md) - Website crawling workflows
- [GTD-CC Plugin Marketplace](../../README.md) - Overview of all available plugins

## Support

For issues or questions about specific skills, see the detailed documentation in each skill directory. For marketplace-wide questions, see the main gtd-cc README.
