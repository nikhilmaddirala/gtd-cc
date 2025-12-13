---
name: crawl-site
description: Interactive guide for crawling entire websites and generating sitemaps
allowed-tools: [Read, Write, Edit, Bash, AskUserQuestion]
argument-hint: [URL] - the website to crawl starting point
---

# Crawl Website

This command guides you through systematic website crawling using the site-crawling skill. It helps you discover site structure, generate sitemaps, and extract organized content.

## Interactive Crawling Process

### Step 1: Site Analysis
**Provide the starting URL for the website you want to crawl.**

I'll analyze the site and ask about:
- **Crawl scope** (entire site, specific sections, or depth-limited)
- **Content focus** (all pages, documentation, blog posts, etc.)
- **Crawl depth** (intelligent detection or fixed depth)

### Step 2: Crawling Strategy

Based on your goals, I'll configure:
- **Concurrent crawling** (number of simultaneous requests)
- **Rate limiting** (delays between requests)
- **Content filtering** (quality thresholds and content types)
- **Output organization** (by depth, by content type, or by URL structure)

### Step 3: Execution and Analysis

I'll guide you through:
- **Intelligent link discovery** and filtering
- **Progress monitoring** with status updates
- **Quality control** and duplicate detection
- **Sitemap generation** in multiple formats

## Crawling Strategies

### Exploratory Crawling
```
Purpose: Discover site structure and content types
Depth: Intelligent (3-5 levels based on content)
Focus: All page types
Output: Site structure analysis and sitemap
```

### Content-Focused Crawling
```
Purpose: Extract specific content types
Depth: Variable based on content relevance
Focus: Documentation, blog posts, or product pages
Output: Organized content by category
```

### Sitemap Generation
```
Purpose: Create comprehensive site maps
Depth: Complete site structure
Focus: All accessible pages
Output: XML sitemap, markdown structure, link analysis
```

## Configuration Options

### Depth Control
- **Intelligent**: Automatic depth detection based on content changes
- **Fixed**: Maximum depth (2-6 levels recommended)
- **Content-based**: Stop when content becomes repetitive

### Quality Filtering
- **Content length**: Minimum content requirements
- **Relevance scoring**: Focus on valuable content
- **Duplicate detection**: Skip similar or duplicate pages

### Performance Settings
- **Concurrent requests**: 1-10 (start low, increase gradually)
- **Rate limiting**: Adaptive delays based on server response
- **Timeout settings**: 30-60 seconds per page

## Output Formats

### Site Structure Report
```
- Total pages discovered
- Content type distribution
- URL structure analysis
- Link density and connectivity
- Quality assessment
```

### Sitemap Files
```
- XML sitemap (for search engines)
- Markdown sitemap (for humans)
- JSON structure (for analysis)
- Link analysis report
```

### Organized Content
```
- Content by type (docs, blog, products)
- Content by depth/structure
- High-quality content prioritized
- Metadata and analysis
```

## Best Practices

1. **Start conservatively** - Begin with low concurrency and short depth
2. **Monitor server response** - Watch for rate limiting or blocking
3. **Respect robots.txt** - Avoid restricted areas
4. **Quality over quantity** - Focus on valuable content
5. **Incremental crawling** - Start small, expand if needed

## Common Use Cases

### Documentation Site Mapping
```
URL: https://docs.example.com
Strategy: Content-focused crawling
Depth: Intelligent (follow doc structure)
Focus: Documentation pages only
Output: Structured knowledge base
```

### Blog Discovery
```
URL: https://blog.example.com
Strategy: Content-type filtering
Depth: Medium (post archives)
Focus: Blog posts and articles
Output: Organized content by date/topic
```

### Competitive Analysis
```
URL: https://competitor-site.com
Strategy: Comprehensive crawling
Depth: Deep (site structure)
Focus: All content types
Output: Site structure and content analysis
```

## Getting Started

Provide the website URL you want to crawl, and I'll guide you through selecting the optimal crawling strategy for your needs!