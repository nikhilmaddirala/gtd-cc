---
name: crawl-site
description: Crawl entire website and save content as markdown files. Uses site-crawling skill for intelligent crawling with depth control and sitemap generation.
---

# Crawl Website

## Overview

This command guides you through crawling an entire website and saving content as organized markdown files. Offers both simple CLI-based crawling and advanced Python implementation options.

## Context

User provides a base URL to crawl. The command determines appropriate crawling depth and output organization based on site structure and user requirements.

## Process

### Step 1: Ask for URL

Request the base URL to crawl:
```
Enter the website URL to crawl:
```

### Step 2: Determine Crawl Parameters

Ask about crawling preferences:
```
Crawl configuration:

1. Simple crawl (max depth 3, default settings)
2. Custom depth and settings
3. Advanced crawling with quality filtering
```

### Step 3: Execute Crawl

**Option 1: Simple Crawl**

Use crawl4ai CLI with sensible defaults:
```bash
# Create timestamped output directory
uvx crawl4ai crawl \
  --url "[URL]" \
  --output-dir "web-crawl/[domain]-$(date +%Y%m%d-%H%M%S)" \
  --max-depth 3 \
  --format markdown
```

**Option 2: Custom Depth Crawl**

Use crawl4ai CLI with custom parameters:
```bash
uvx crawl4ai crawl \
  --url "[URL]" \
  --output-dir "web-crawl/[domain]-custom" \
  --max-depth [USER_DEPTH] \
  --max-pages [USER_LIMIT] \
  --format markdown
```

**Option 3: Advanced Crawling**

Use site-crawling skill with Python:
```bash
# Use the Python implementation from site-crawling skill
# Run intelligent-crawler.py example
python skills/site-crawling/examples/intelligent-crawler.py [URL]
```

### Step 4: Generate Sitemap

Create sitemap for navigation:
```bash
# Generate markdown sitemap from crawled data
# Or use XML sitemap generation from site-crawling skill
```

### Step 5: Verify Output

Check that content was organized correctly:
```bash
ls -lh web-crawl/[domain]-*/
# Verify markdown files exist
# Check directory structure mirrors site hierarchy
```

## Common Use Cases

### Documentation Site
```bash
# Crawl docs with depth 2
uvx crawl4ai crawl \
  --url "https://docs.example.com" \
  --output-dir "web-crawl/docs-example" \
  --max-depth 2
```

### Blog Archive
```bash
# Crawl blog with higher depth for posts
uvx crawl4ai crawl \
  --url "https://blog.example.com" \
  --output-dir "web-crawl/blog-archive" \
  --max-depth 3
```

### Product Catalog
```bash
# Limit pages for large catalogs
uvx crawl4ai crawl \
  --url "https://shop.example.com/products" \
  --output-dir "web-crawl/products" \
  --max-depth 2 \
  --max-pages 50
```

## Skills Used

- site-crawling - For intelligent crawling strategies and sitemap generation
- crawl4ai-toolkit - For advanced crawling implementation options

## Tips

- Start with depth 3 for most sites (adjust based on needs)
- Use max-pages to limit crawl size for large sites
- Timestamped directories help organize multiple crawls
- Check sitemap to understand discovered structure
