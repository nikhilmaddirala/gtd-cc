---
name: web-scraping-fundamentals
description: Core web scraping patterns using crawl4ai and basic tools. Use when users need to extract content from web pages, handle JavaScript-heavy sites, or implement basic crawling strategies. Includes error handling, content filtering, and troubleshooting guidance.
version: 0.1.0
last_updated: 2025-01-07
---

# Web Scraping Fundamentals

## Overview

This skill provides foundational patterns for web scraping using crawl4ai, with fallback to simple tools for basic cases. Focus on clean content extraction, JavaScript handling, and robust error handling.

## Quick Start Patterns

### Basic Page Extraction
For simple content extraction from any webpage:

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def extract_page_content(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url)
        if result.success:
            return result.markdown
        else:
            raise Exception(f"Failed to crawl: {result.error_message}")

# Usage
content = asyncio.run(extract_page_content("https://example.com"))
print(content[:500])  # First 500 characters
```

### Simple Alternative (curl + jq)
For basic HTML pages without JavaScript:

```bash
# Extract text content
curl -s "https://example.com" | \
  jq -r '. // input_text' 2>/dev/null || \
  lynx -dump -stdin

# Extract links
curl -s "https://example.com" | \
  grep -oE 'href="[^"]+"' | \
  sed 's/href="//' | sed 's/"$//' | \
  sort -u
```

## Core Crawling Patterns

### 1. JavaScript-Heavy Content Handling
For sites that rely on JavaScript for content rendering:

```python
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

# Configure for JavaScript-heavy sites
browser_config = BrowserConfig(
    headless=True,
    viewport_width=1920,
    viewport_height=1080,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
)

crawler_config = CrawlerRunConfig(
    page_timeout=60000,  # 60 seconds for JS loading
    wait_for="css:.main-content",  # Wait for specific element
    js_code="""
    // Scroll to trigger lazy loading
    window.scrollTo(0, document.body.scrollHeight);
    // Wait for any async content
    await new Promise(resolve => setTimeout(resolve, 2000));
    """,
    remove_overlay_elements=True
)

async def crawl_dynamic_content(url):
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url, config=crawler_config)
        return result.markdown
```

### 2. Content Filtering
Focus on relevant content while ignoring navigation and footers:

```python
from crawl4ai.content_filter_strategy import BM25ContentFilter, PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

# Option 1: Relevance-based filtering
bm25_filter = BM25ContentFilter(
    user_query="product features documentation",
    bm25_threshold=1.0
)

# Option 2: Quality-based filtering
pruning_filter = PruningContentFilter(threshold=0.4, threshold_type="fixed")

md_generator = DefaultMarkdownGenerator(content_filter=bm25_filter)
config = CrawlerRunConfig(markdown_generator=md_generator)

async def extract_focused_content(url, query):
    # Update filter with user query
    bm25_filter.user_query = query
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)
        return {
            "raw_content": str(result.markdown.raw_markdown),
            "focused_content": str(result.markdown.fit_markdown),
            "metadata": result.metadata
        }
```

### 3. Structured Data Extraction
Extract specific information using CSS selectors:

```python
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

# Define extraction schema
schema = {
    "name": "articles",
    "baseSelector": "article",
    "fields": [
        {"name": "title", "selector": "h1, h2", "type": "text"},
        {"name": "content", "selector": ".content, p", "type": "text"},
        {"name": "date", "selector": ".date, time", "type": "text"},
        {"name": "author", "selector": ".author, .byline", "type": "text"},
        {"name": "tags", "selector": ".tags a, .categories a", "type": "text", "multiple": True}
    ]
}

extraction_strategy = JsonCssExtractionStrategy(schema=schema)
config = CrawlerRunConfig(extraction_strategy=extraction_strategy)

async def extract_structured_data(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)
        return result.extracted_content
```

## Error Handling & Troubleshooting

### Common Issues and Solutions

**1. Timeout Errors**
```python
# Increase timeout for slow sites
config = CrawlerRunConfig(
    page_timeout=90000,  # 90 seconds
    wait_for="js:document.readyState === 'complete'"
)
```

**2. Bot Detection**
```python
# Rotate user agents and add delays
import random
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]

browser_config = BrowserConfig(
    headless=True,
    user_agent=random.choice(user_agents),
    viewport_width=f"{random.choice([1920, 1366, 1440])}",
    viewport_height=f"{random.choice([1080, 768, 900])}"
)

# Add delay between requests
await asyncio.sleep(random.uniform(1, 3))
```

**3. Content Not Loading**
```python
# Wait for specific content
config = CrawlerRunConfig(
    wait_for=[
        "css:.article-content",  # Wait for main content
        "js:window.mainContentLoaded"  # Wait for JS flag
    ],
    js_code="""
    // Trigger any lazy loading
    window.dispatchEvent(new Event('load'));
    """
)
```

### Robust Crawling Template
```python
import asyncio
import random
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.content_filter_strategy import BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def robust_crawl(url, query=None, max_retries=3):
    """Robust crawling with retries and error handling"""

    for attempt in range(max_retries):
        try:
            # Randomize configuration for each attempt
            browser_config = BrowserConfig(
                headless=True,
                viewport_width=random.choice([1920, 1366, 1440]),
                viewport_height=random.choice([1080, 768, 900]),
                user_agent=random.choice([
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                ])
            )

            # Add content filtering if query provided
            config = CrawlerRunConfig(
                page_timeout=45000,
                remove_overlay_elements=True
            )

            if query:
                bm25_filter = BM25ContentFilter(user_query=query, bm25_threshold=1.0)
                md_generator = DefaultMarkdownGenerator(content_filter=bm25_filter)
                config.markdown_generator = md_generator

            async with AsyncWebCrawler(config=browser_config) as crawler:
                result = await crawler.arun(url, config=config)

                if result.success and len(str(result.markdown)) > 100:
                    return {
                        "content": str(result.markdown),
                        "metadata": result.metadata,
                        "links": result.links,
                        "attempt": attempt + 1
                    }
                else:
                    print(f"Attempt {attempt + 1}: Insufficient content extracted")

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")

        # Exponential backoff
        if attempt < max_retries - 1:
            await asyncio.sleep(2 ** attempt)

    raise Exception(f"Failed to extract content after {max_retries} attempts")
```

## Performance Optimization

### Concurrent Crawling
For multiple URLs:

```python
urls = ["https://site1.com", "https://site2.com", "https://site3.com"]

async def crawl_multiple(urls, max_concurrent=3):
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(
            urls=urls,
            config=CrawlerRunConfig(page_timeout=30000),
            max_concurrent=max_concurrent
        )

        return [
            {"url": r.url, "content": str(r.markdown), "success": r.success}
            for r in results if r.success
        ]

results = asyncio.run(crawl_multiple(urls))
```

### Caching Strategy
Enable caching during development:

```python
from crawl4ai import CacheMode

config = CrawlerRunConfig(
    cache_mode=CacheMode.ENABLED,  # Cache successful requests
    excluded_tags=["script", "style"]  # Exclude unnecessary elements
)
```

## Best Practices

1. **Always check result.success** before processing content
2. **Use appropriate timeouts** - 30s for normal sites, 60s+ for JS-heavy
3. **Implement retry logic** with exponential backoff
4. **Add delays between requests** to respect rate limits
5. **Filter content aggressively** to focus on relevant information
6. **Use caching during development** to avoid repeated requests
7. **Monitor memory usage** when crawling large sites

## Common Use Cases

### Blog Post Extraction
```python
config = CrawlerRunConfig(
    css_selector="article, .post, .entry",  # Focus on main content
    remove_forms=True,
    exclude_external_links=True
)
```

### Product Information
```python
schema = {
    "name": "products",
    "baseSelector": ".product, .item",
    "fields": [
        {"name": "name", "selector": ".title, h1", "type": "text"},
        {"name": "price", "selector": ".price, .cost", "type": "text"},
        {"name": "description", "selector": ".description", "type": "text"}
    ]
}
```

### API Documentation
```python
config = CrawlerRunConfig(
    css_selector=".docs, .documentation, .content",
    wait_for="css:.api-endpoint, .code-block",
    remove_overlay_elements=True
)
```

---

For advanced patterns like session management, authentication, or large-scale crawling, see the complete crawl4ai reference documentation.