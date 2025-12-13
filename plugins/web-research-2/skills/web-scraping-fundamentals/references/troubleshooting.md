# Web Scraping Troubleshooting Guide

## Common Issues and Solutions

### 1. Timeouts and Slow Loading Pages

**Problem**: Pages take too long to load or timeout

**Solutions**:
```python
# Increase timeout
config = CrawlerRunConfig(page_timeout=90000)  # 90 seconds

# Wait for specific content
config = CrawlerRunConfig(
    wait_for="css:.main-content"  # Wait for main content to appear
)

# Handle slow JavaScript
config = CrawlerRunConfig(
    js_code="""
    // Wait for dynamic content
    await new Promise(resolve => setTimeout(resolve, 3000));
    """
)
```

### 2. Bot Detection and Blocking

**Problem**: Site detects and blocks scraping attempts

**Solutions**:
```python
# Rotate user agents
import random
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
]

browser_config = BrowserConfig(
    headless=False,  # Sometimes visible browser helps
    user_agent=random.choice(user_agents),
    viewport_width=1920,
    viewport_height=1080
)

# Add delays between requests
await asyncio.sleep(random.uniform(2, 5))
```

### 3. Missing Content

**Problem**: Content appears but isn't extracted

**Solutions**:
```python
# Wait for specific elements
config = CrawlerRunConfig(
    wait_for=[
        "css:.article-content",    # Wait for content area
        "js:window.dataLoaded"     # Wait for JavaScript flag
    ]
)

# Try different CSS selectors
config = CrawlerRunConfig(
    css_selector="article, .main, .content, #main-content"
)

# Remove overlay elements that might hide content
config = CrawlerRunConfig(remove_overlay_elements=True)
```

### 4. Rate Limiting

**Problem**: Server blocks requests after too many attempts

**Solutions**:
```python
# Limit concurrent requests
results = await crawler.arun_many(
    urls=many_urls,
    max_concurrent=2  # Reduce from default 5
)

# Add delays between batches
for i, url_batch in enumerate(url_batches):
    results = await crawler.arun_many(url_batch)
    if i < len(url_batches) - 1:
        await asyncio.sleep(10)  # 10 second delay between batches
```

### 5. Content Not Fully Loaded

**Problem**: JavaScript-heavy sites don't load all content

**Solutions**:
```python
# Scroll to trigger lazy loading
config = CrawlerRunConfig(
    js_code="""
    // Scroll to bottom of page
    window.scrollTo(0, document.body.scrollHeight);

    // Wait for content to load
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Click load more buttons
    const loadMoreBtn = document.querySelector('.load-more');
    if (loadMoreBtn) loadMoreBtn.click();
    """
)
```

### 6. Extraction Errors

**Problem**: Data extraction fails or returns empty results

**Solutions**:
```python
# Debug what's available
result = await crawler.arun(url)
print(f"HTML length: {len(result.html)}")
print(f"Links found: {len(result.links)}")

# Test CSS selectors in browser console
# document.querySelectorAll('.product').length

# Use more flexible selectors
schema = {
    "name": "items",
    "baseSelector": ".product, .item, article",
    "fields": [
        {"name": "title", "selector": "h1, h2, h3, .title, .name", "type": "text"}
    ]
}
```

### 7. Memory Issues

**Problem**: Large crawls consume too much memory

**Solutions**:
```python
# Process results in batches
batch_size = 10
for i in range(0, len(urls), batch_size):
    batch = urls[i:i + batch_size]
    results = await crawler.arun_many(batch)

    # Process immediately, don't store all results
    for result in results:
        process_result(result)  # Your processing function

    # Clear memory
    del results
```

## Debugging Techniques

### 1. Enable Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### 2. Take Screenshots
```python
config = CrawlerRunConfig(screenshot=True)
# Check screenshot.png to see what the crawler sees
```

### 3. Inspect HTML
```python
result = await crawler.arun(url)
# Save HTML for inspection
with open("debug.html", "w") as f:
    f.write(result.html)
```

### 4. Test in Browser
Use browser developer tools to:
- Check if content loads via JavaScript
- Test CSS selectors
- Look for API calls that load data
- Identify rate limiting headers

## Best Practices to Avoid Issues

1. **Start small**: Test with single URLs before batch processing
2. **Respect robots.txt**: Check /robots.txt for crawling rules
3. **Use delays**: Add delays between requests to avoid overwhelming servers
4. **Monitor responses**: Check status codes and response times
5. **Handle errors gracefully**: Always wrap requests in try-catch blocks
6. **Test selectors**: Verify CSS selectors in browser console first
7. **Use appropriate timeouts**: Set realistic timeout values based on site performance