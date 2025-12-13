# Web Research Plugin

A comprehensive web scraping and crawling toolkit for Claude Code that enables efficient extraction of web content.

## Features

- **Documentation Extraction**: Automatically detect and extract structured documentation from sites
- **Site Crawling**: Intelligent crawling with automatic depth detection and sitemap generation
- **Page Fetching**: Simple and advanced page content retrieval
- **Content Filtering**: Smart content extraction with relevance-based filtering
- **Multiple Formats**: Output in markdown, JSON, or structured data

## Commands

- `/fetch-page` - Interactive guide for extracting content from a single page
- `/crawl-site` - Interactive guide for crawling entire websites
- `/get-docs` - Interactive guide for extracting documentation

## Skills

- **Web Scraping Fundamentals** - Core crawling patterns and best practices
- **Documentation Extraction** - Specialized patterns for documentation sites
- **Site Crawling & Sitemaps** - Advanced crawling strategies and organization

## Requirements

- Python 3.7+
- crawl4ai library (install with `pip install crawl4ai`)
- For simple operations: `curl` and `jq` command-line tools

## Quick Start

1. Install crawl4ai: `pip install crawl4ai`
2. Run `/fetch-page` to extract content from a single URL
3. Use `/get-docs` to extract documentation from knowledge bases
4. Try `/crawl-site` to discover and map entire websites

## Settings

The plugin uses configuration from `.claude/web-research.local.md` for customization:

- Cache duration and behavior
- Default crawl depth and concurrency
- Output format preferences
- Filtering and exclusion patterns