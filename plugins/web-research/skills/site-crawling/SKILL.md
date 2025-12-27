---
name: site-crawling
description: Advanced crawling strategies for discovering and mapping website structure, plus simple site-to-markdown conversion. Use when users need to crawl entire sites, generate sitemaps, analyze link structures, or convert websites to markdown files. Includes intelligent depth control, content categorization, and concurrent crawling patterns.
version: 0.2.0
last_updated: 2025-01-26
---

# Site Crawling & Sitemap Generation

## Overview

This skill provides comprehensive patterns for intelligent website crawling, automatic sitemap generation, and content discovery. It handles both advanced crawling strategies and simple site-to-markdown conversion with proper depth control, rate limiting, and content organization.

## Simple Site-to-Markdown Conversion

Quick approach for converting entire websites to markdown files:

### Basic CLI Pattern

Using crawl4ai's built-in crawl command:

```bash
# Crawl entire site to markdown files
uvx crawl4ai crawl \
  --url "https://example.com" \
  --output-dir "output/example-com-$(date +%Y%m%d-%H%M%S)" \
  --max-depth 3 \
  --format markdown
```

### Recommended Parameters

- `--max-depth 3` - Crawl up to 3 levels deep (sensible default)
- `--format markdown` - Save content as markdown
- Timestamped output directories keep multiple crawls organized

### Output Structure

```
output/
├── example-com-20250122-143022/
│   ├── index.md
│   ├── about.md
│   ├── products/
│   │   ├── product-1.md
│   │   └── product-2.md
│   └── docs/
│       ├── getting-started.md
│       └── api.md
└── another-site-20250122-150000/
    ├── index.md
    └── ...
```

### Python Implementation

```python
import asyncio
import os
from pathlib import Path
from datetime import datetime
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from urllib.parse import urljoin, urlparse

async def crawl_to_markdown(base_url, output_dir, max_depth=3):
    """Crawl entire website and save as markdown files"""

    base_domain = urlparse(base_url).netloc
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    crawl_dir = Path(output_dir) / f"{base_domain}-{timestamp}"
    crawl_dir.mkdir(parents=True, exist_ok=True)

    visited = set()
    queue = [(base_url, 0)]  # (url, depth)

    async with AsyncWebCrawler() as crawler:
        while queue and len(visited) < 100:  # Limit to 100 pages
            url, depth = queue.pop(0)

            if url in visited or depth > max_depth:
                continue

            try:
                result = await crawler.arun(
                    url,
                    config=CrawlerRunConfig(
                        page_timeout=30000,
                        remove_overlay_elements=True
                    )
                )

                if result.success:
                    # Determine output path
                    path = urlparse(url).path
                    if path.endswith('/') or path == '':
                        path = path + 'index.md'
                    else:
                        path = path + '.md' if not path.endswith('.md') else path

                    output_file = crawl_dir / path.lstrip('/')
                    output_file.parent.mkdir(parents=True, exist_ok=True)

                    # Write markdown
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(f"# {result.metadata.get('title', 'Page')}\n\n")
                        f.write(str(result.markdown))

                    visited.add(url)
                    print(f"✅ Saved: {output_file}")

                    # Discover new links
                    for link_info in result.links.get("internal", []):
                        href = link_info.get("href", "")
                        absolute_url = urljoin(base_url, href)

                        # Add to queue if valid
                        if (absolute_url not in visited and
                            not absolute_url.startswith('#') and
                            absolute_url.startswith(base_url)):
                            queue.append((absolute_url, depth + 1))

            except Exception as e:
                print(f"❌ Failed to crawl {url}: {e}")

    print(f"\n📁 Crawl complete: {len(visited)} pages saved to {crawl_dir}")
    return crawl_dir
```

## Intelligent Crawling Strategies

### Adaptive Depth Detection
```python
import asyncio
from urllib.parse import urljoin, urlparse
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

class IntelligentCrawler:
    def __init__(self, base_url, max_depth=5, max_pages=100):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.visited = set()
        self.queue = [(base_url, 0)]  # (url, depth)
        self.discovered_links = {}
        self.content_structure = {}

    async def crawl_intelligently(self):
        """Main crawling method with intelligent depth control"""

        async with AsyncWebCrawler() as crawler:
            while self.queue and len(self.visited) < self.max_pages:
                url, depth = self.queue.pop(0)

                if url in self.visited or depth > self.max_depth:
                    continue

                try:
                    # Crawl current page
                    result = await self._crawl_page(crawler, url, depth)
                    if result:
                        self.discovered_links[url] = result['links']
                        self.content_structure[url] = result['content_info']

                    self.visited.add(url)

                    # Add discovered links to queue
                    new_links = self._filter_links(result['links'], depth + 1)
                    self.queue.extend(new_links)

                    # Adaptive delay based on content
                    await self._adaptive_delay(result)

                except Exception as e:
                    print(f"Failed to crawl {url}: {e}")

        return self.generate_sitemap()

    async def _crawl_page(self, crawler, url, depth):
        """Crawl single page and extract information"""

        config = CrawlerRunConfig(
            page_timeout=30000,
            remove_overlay_elements=True,
            exclude_tags=["script", "style", "nav", "footer"]
        )

        result = await crawler.arun(url, config=config)

        if result.success:
            return {
                "links": {
                    "internal": result.links.get("internal", []),
                    "external": result.links.get("external", [])
                },
                "content_info": {
                    "title": result.metadata.get("title", ""),
                    "description": result.metadata.get("description", ""),
                    "content_length": len(str(result.markdown)),
                    "depth": depth,
                    "url": url
                }
            }
        return None

    def _filter_links(self, links, new_depth):
        """Filter and prioritize discovered links"""

        if new_depth > self.max_depth:
            return []

        filtered_links = []

        for link_info in links.get("internal", []):
            href = link_info.get("href", "")

            # Skip if already visited or invalid
            if href in self.visited or not self._is_valid_internal_link(href):
                continue

            # Prioritize certain content types
            priority = self._calculate_link_priority(href, link_info)

            filtered_links.append((href, new_depth, priority))

        # Sort by priority (higher first)
        filtered_links.sort(key=lambda x: x[2], reverse=True)
        return [(url, depth) for url, depth, _ in filtered_links]

    def _is_valid_internal_link(self, href):
        """Check if link is valid internal link"""

        # Skip fragments, mailto, tel, javascript
        if href.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'ftp:')):
            return False

        # Skip files we don't want to crawl
        skip_extensions = ['.pdf', '.jpg', '.png', '.gif', '.zip', '.exe', '.dmg']
        if any(href.lower().endswith(ext) for ext in skip_extensions):
            return False

        return True

    def _calculate_link_priority(self, href, link_info):
        """Calculate priority for link based on content indicators"""

        href_lower = href.lower()
        text_lower = link_info.get("text", "").lower()

        # High priority indicators
        if any(indicator in href_lower or indicator in text_lower
               for indicator in ["docs", "guide", "tutorial", "api"]):
            return 10

        # Medium priority indicators
        if any(indicator in href_lower or indicator in text_lower
               for indicator in ["blog", "article", "post", "news"]):
            return 7

        # Low priority indicators
        if any(indicator in href_lower for indicator
               in ["tag", "category", "archive", "search"]):
            return 3

        # Default priority
        return 5

    async def _adaptive_delay(self, result):
        """Adaptive delay based on page content and crawl progress"""

        if not result:
            await asyncio.sleep(1)
            return

        content_length = result["content_info"]["content_length"]
        depth = result["content_info"]["depth"]

        # Longer delay for deeper content
        base_delay = 1 + (depth * 0.5)

        # Shorter delay for content-light pages
        if content_length < 1000:
            base_delay *= 0.5

        # Longer delay for content-rich pages
        elif content_length > 5000:
            base_delay *= 1.5

        await asyncio.sleep(base_delay)

    def generate_sitemap(self):
        """Generate comprehensive sitemap"""

        sitemap = {
            "metadata": {
                "base_url": self.base_url,
                "total_pages": len(self.visited),
                "max_depth_reached": max(
                    info["content_info"]["depth"]
                    for info in self.content_structure.values()
                ),
                "crawl_date": asyncio.get_event_loop().time()
            },
            "structure": self._organize_by_depth(),
            "content_analysis": self._analyze_content_types(),
            "link_analysis": self._analyze_link_structure()
        }

        return sitemap

    def _organize_by_depth(self):
        """Organize crawled pages by depth"""

        organized = {}
        for url, info in self.content_structure.items():
            depth = info["content_info"]["depth"]
            if depth not in organized:
                organized[depth] = []
            organized[depth].append({
                "url": url,
                "title": info["content_info"]["title"],
                "content_length": info["content_info"]["content_length"]
            })

        return organized

    def _analyze_content_types(self):
        """Analyze types of content discovered"""

        content_types = {
            "documentation": 0,
            "blog_posts": 0,
            "product_pages": 0,
            "landing_pages": 0,
            "other": 0
        }

        for url, info in self.content_structure.items():
            title = info["content_info"]["title"].lower()
            url_lower = url.lower()

            if any(kw in title or kw in url_lower
                   for kw in ["docs", "guide", "manual", "reference"]):
                content_types["documentation"] += 1
            elif any(kw in title or kw in url_lower
                    for kw in ["blog", "post", "article", "news"]):
                content_types["blog_posts"] += 1
            elif any(kw in title or kw in url_lower
                    for kw in ["product", "service", "feature", "pricing"]):
                content_types["product_pages"] += 1
            elif not info["content_info"]["title"] or "/" in url.split("/")[-2:]:
                content_types["landing_pages"] += 1
            else:
                content_types["other"] += 1

        return content_types

    def _analyze_link_structure(self):
        """Analyze link distribution and patterns"""

        total_internal = sum(
            len(links.get("internal", []))
            for links in self.discovered_links.values()
        )
        total_external = sum(
            len(links.get("external", []))
            for links in self.discovered_links.values()
        )

        return {
            "average_internal_links_per_page": total_internal / len(self.visited) if self.visited else 0,
            "average_external_links_per_page": total_external / len(self.visited) if self.visited else 0,
            "most_linked_pages": self._find_most_linked_pages()
        }

    def _find_most_linked_pages(self):
        """Find pages with most incoming links"""

        link_counts = {}
        for url, links in self.discovered_links.items():
            for internal_link in links.get("internal", []):
                link_url = internal_link.get("href", "")
                if link_url not in link_counts:
                    link_counts[link_url] = 0
                link_counts[link_url] += 1

        # Return top 10 most linked pages
        return sorted(link_counts.items(), key=lambda x: x[1], reverse=True)[:10]


# Usage example
async def crawl_website(base_url):
    crawler = IntelligentCrawler(base_url, max_depth=4, max_pages=50)
    sitemap = await crawler.crawl_intelligently()
    return sitemap
```

## Concurrent Crawling Patterns

### High-Performance Site Crawling
```python
async def concurrent_site_crawl(base_url, max_pages=100, max_concurrent=5):
    """High-performance concurrent crawling"""

    # First, discover initial links
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(base_url)
        if not result.success:
            raise Exception(f"Failed to crawl base URL: {result.error_message}")

        initial_links = result.links.get("internal", [])[:20]  # Start with 20 links

    # Convert to absolute URLs
    from urllib.parse import urljoin
    urls_to_crawl = [
        urljoin(base_url, link.get("href", ""))
        for link in initial_links
        if link.get("href") and not link.get("href", "").startswith("#")
    ]

    # Batch crawl with concurrency control
    config = CrawlerRunConfig(
        page_timeout=30000,
        remove_overlay_elements=True,
        exclude_tags=["script", "style", "nav", "footer"],
        cache_mode=None  # Disable caching for fresh crawl
    )

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(
            urls=urls_to_crawl[:max_pages],
            config=config,
            max_concurrent=max_concurrent
        )

    # Process and organize results
    crawled_data = {}
    for result in results:
        if result.success:
            crawled_data[result.url] = {
                "content": str(result.markdown),
                "title": result.metadata.get("title", ""),
                "links": result.links,
                "content_length": len(str(result.markdown))
            }

    return {
        "base_url": base_url,
        "crawled_pages": len(crawled_data),
        "data": crawled_data
    }
```

### Progressive Crawling with Quality Control
```python
async def progressive_quality_crawl(base_url, quality_threshold=0.7):
    """Progressive crawling with content quality control"""

    async with AsyncWebCrawler() as crawler:
        high_quality_urls = [base_url]
        all_urls = set([base_url])
        crawled_data = {}

        # Progressive crawling rounds
        for round_num in range(3):  # 3 rounds of discovery
            print(f"Crawling round {round_num + 1}...")

            # Current batch of URLs
            current_urls = list(set(high_quality_urls) - set(crawled_data.keys()))

            if not current_urls:
                break

            config = CrawlerRunConfig(
                page_timeout=30000,
                remove_overlay_elements=True
            )

            results = await crawler.arun_many(
                urls=current_urls,
                config=config,
                max_concurrent=3
            )

            # Process results and discover new high-quality URLs
            new_high_quality = []

            for result in results:
                if result.success:
                    quality_score = assess_content_quality(result)
                    crawled_data[result.url] = {
                        "content": str(result.markdown),
                        "quality_score": quality_score,
                        "links": result.links
                    }

                    # Discover new high-quality links
                    if quality_score >= quality_threshold:
                        new_links = extract_quality_links(result.links, quality_threshold)
                        new_high_quality.extend(new_links)
                        all_urls.update(new_links)

            # Add new high-quality URLs for next round
            high_quality_urls.extend(new_high_quality)

            print(f"Round {round_num + 1} complete: {len(crawled_data)} pages crawled")

    return {
        "total_urls_discovered": len(all_urls),
        "high_quality_pages": len(crawled_data),
        "data": crawled_data
    }

def assess_content_quality(result):
    """Assess content quality based on various metrics"""

    content = str(result.markdown)
    title = result.metadata.get("title", "")

    # Quality indicators
    indicators = {
        "content_length": min(len(content) / 2000, 1.0),  # Normalized to 0-1
        "title_present": 0.3 if title else 0,
        "headings": min(content.count("#") / 10, 0.3),
        "code_blocks": min(content.count("```") / 10, 0.2),
        "links": min(len(re.findall(r'\[.*?\]\(.*?\)', content)) / 20, 0.2)
    }

    return sum(indicators.values())

def extract_quality_links(links, threshold=0.5):
    """Extract links that likely lead to quality content"""

    quality_indicators = [
        "docs", "guide", "tutorial", "reference", "api",
        "article", "blog", "post", "news", "learn"
    ]

    quality_links = []
    for link_info in links.get("internal", []):
        href = link_info.get("href", "")
        text = link_info.get("text", "")

        # Check for quality indicators
        if any(indicator in href.lower() or indicator in text.lower()
               for indicator in quality_indicators):
            if href not in quality_links and not href.startswith("#"):
                quality_links.append(href)

    return quality_links[:20]  # Limit to prevent explosion
```

## Sitemap Generation

### XML Sitemap Creation
```python
def create_xml_sitemap(crawled_data, base_url):
    """Create XML sitemap from crawled data"""

    xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for url, data in crawled_data.items():
        xml_content.append('  <url>')
        xml_content.append(f'    <loc>{url}</loc>')
        xml_content.append(f'    <lastmod>{datetime.now().isoformat()}</lastmod>')
        xml_content.append(f'    <changefreq>weekly</changefreq>')

        # Priority based on content quality
        priority = min(data.get("quality_score", 0.5) + 0.3, 1.0)
        xml_content.append(f'    <priority>{priority:.1f}</priority>')
        xml_content.append('  </url>')

    xml_content.append('</urlset>')

    return '\n'.join(xml_content)

def create_markdown_sitemap(crawled_data, organize_by_depth=True):
    """Create markdown sitemap from crawled data"""

    if organize_by_depth:
        # Group by URL depth
        by_depth = {}
        for url, data in crawled_data.items():
            depth = url.count('/') - urlparse(url).path.count('/')
            if depth not in by_depth:
                by_depth[depth] = []
            by_depth[depth].append((url, data))

        md_content = ["# Site Map\n"]
        for depth in sorted(by_depth.keys()):
            md_content.append(f"\n## Depth {depth}\n")
            for url, data in sorted(by_depth[depth]):
                title = data.get("title", url)
                indent = "  " * depth
                md_content.append(f"{indent}- [{title}]({url})")

    else:
        # Flat organization
        md_content = ["# Site Map\n"]
        for url, data in sorted(crawled_data.items()):
            title = data.get("title", url)
            md_content.append(f"- [{title}]({url})")

    return "\n".join(md_content)
```

## Content Analysis and Organization

### Content Type Classification
```python
def classify_content(content, url, title):
    """Classify content type based on patterns"""

    content_lower = content.lower()
    url_lower = url.lower()
    title_lower = title.lower()

    # Documentation indicators
    if any(indicator in content_lower or indicator in url_lower or indicator in title_lower
           for indicator in ["api", "documentation", "reference", "docs", "guide"]):
        return "documentation"

    # Tutorial indicators
    if any(indicator in content_lower or indicator in title_lower
           for indicator in ["tutorial", "how to", "step by step", "getting started"]):
        return "tutorial"

    # Blog post indicators
    if any(indicator in url_lower or indicator in title_lower
           for indicator in ["blog", "post", "article", "news"]):
        return "blog"

    # Product/service indicators
    if any(indicator in content_lower or indicator in title_lower
           for indicator in ["pricing", "features", "product", "service"]):
        return "product"

    return "general"

def analyze_site_structure(crawled_data):
    """Analyze overall site structure and content distribution"""

    content_types = {}
    url_patterns = {}

    for url, data in crawled_data.items():
        # Content type analysis
        content_type = classify_content(
            data.get("content", ""),
            url,
            data.get("title", "")
        )

        if content_type not in content_types:
            content_types[content_type] = 0
        content_types[content_type] += 1

        # URL pattern analysis
        path_parts = [part for part in urlparse(url).path.split('/') if part]
        if path_parts:
            pattern = f"/{path_parts[0]}/"
            if pattern not in url_patterns:
                url_patterns[pattern] = 0
            url_patterns[pattern] += 1

    return {
        "content_distribution": content_types,
        "url_patterns": url_patterns,
        "total_pages": len(crawled_data)
    }
```

## Best Practices

1. **Start with small concurrency** and increase gradually to test server limits
2. **Always implement rate limiting** with adaptive delays based on content complexity
3. **Monitor memory usage** when crawling large sites
4. **Use intelligent depth control** based on content quality rather than fixed depth
5. **Implement quality filtering** to focus on valuable content
6. **Generate multiple sitemap formats** for different use cases (XML for search engines, markdown for humans)
7. **Handle errors gracefully** and continue crawling other pages when individual requests fail
8. **Respect robots.txt** and implement proper crawling etiquette

---

This skill provides comprehensive patterns for large-scale web crawling while maintaining performance, quality, and reliability.