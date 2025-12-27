---
name: fetch-page
description: Extract content from a single webpage and save as markdown. Use web-fetch skill for articles with images, or crawl4ai-toolkit for advanced extraction options.
---

# Fetch Page Content

## Overview

This command guides you through extracting content from a single webpage and saving it as markdown. Choose between simple article fetching (with images) or advanced extraction with filtering options.

## Context

User provides a URL to extract content from. The command offers two extraction modes based on needs:

1. **Simple Article Fetch** (web-fetch skill) - Best for blog posts, news articles, documentation
2. **Advanced Extraction** (crawl4ai-toolkit skill) - Best for dynamic sites, custom filtering, structured data

## Process

### Step 1: Ask for URL

Request the URL to extract content from:
```
Enter the URL to fetch content from:
```

### Step 2: Determine Extraction Mode

Ask user about their needs:
```
What type of extraction do you need?

1. Simple article fetch (includes images)
2. Advanced extraction (custom filtering, JS support)
```

### Step 3: Execute Appropriate Skill

**Option 1: Simple Article Fetch (web-fetch)**

Use web-fetch skill patterns:
```bash
# Create output directory
mkdir -p references/article-name/images

# Fetch article using Jina AI Reader (preferred)
curl "https://r.jina.ai/[URL]" > article.md

# Alternative: Use WebFetch tool
```

Then extract and download images, update markdown paths.

**Option 2: Advanced Extraction (crawl4ai-toolkit)**

Use crawl4ai-toolkit scripts:
```bash
# Use basic_crawler.py for simple extraction
python skills/crawl4ai-toolkit/scripts/basic_crawler.py [URL]

# Or use extraction_pipeline.py for structured data
python skills/crawl4ai-toolkit/scripts/extraction_pipeline.py [URL]
```

### Step 4: Verify Output

Check that content was extracted successfully and save to appropriate location.

## Common Use Cases

### Blog Post with Images
```bash
# Use web-fetch skill
curl "https://r.jina.ai/https://blog.example.com/post" > article.md
# Then download images and update paths
```

### Documentation Page
```bash
# Use crawl4ai-toolkit
python skills/crawl4ai-toolkit/scripts/basic_crawler.py https://docs.example.com/guide
```

### Product Page with Structured Data
```bash
# Use extraction_pipeline.py with schema
python skills/crawl4ai-toolkit/scripts/extraction_pipeline.py \
  --generate-schema https://shop.example.com/product \
  "extract product name, price, description, specs"
```

## Skills Used

- web-fetch - For articles with images
- crawl4ai-toolkit - For advanced extraction options
