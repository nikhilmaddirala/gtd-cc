---
name: documentation-extraction
description: Specialized patterns for extracting structured documentation from websites. Use when users need to extract API docs, tutorials, reference guides, or knowledge bases. Handles common documentation platforms like Docusaurus, GitBook, ReadTheDocs, and Sphinx sites.
version: 0.1.0
last_updated: 2025-01-07
---

# Documentation Extraction

## Overview

This skill provides specialized patterns for extracting documentation from various platforms and formats. It automatically detects documentation structures, preserves code examples, and organizes content for optimal readability.

## Documentation Platform Detection

### Platform-Specific Selectors

**Docusaurus Sites**
```python
# Common Docusaurus patterns
config = CrawlerRunConfig(
    css_selector="article, .markdown, .theme-doc-markdown",
    wait_for="css:article, .theme-doc-markdown",
    exclude_tags=["nav", "footer", ".pagination", ".table-of-contents"]
)
```

**GitBook Sites**
```python
# GitBook extraction
config = CrawlerRunConfig(
    css_selector=".gitbook-root, .page-body, .theme-doc",
    exclude_tags=["nav", "header", ".sidebar", ".navigation"]
)
```

**ReadTheDocs Sites**
```python
# ReadTheDocs extraction
config = CrawlerRunConfig(
    css_selector=".document, .role-content, .bd-content",
    exclude_tags=["nav", ".sidebar", ".toctree", ".related-topics"]
)
```

**Sphinx Documentation**
```python
# Sphinx-based sites
config = CrawlerRunConfig(
    css_selector=".document, .body, .section",
    exclude_tags=["nav", ".related", ".sphinxsidebar", ".toctree-wrapper"]
)
```

## Universal Documentation Extraction

### Auto-Detection Pattern
```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def extract_documentation(url):
    """Universal documentation extractor with platform detection"""

    # Comprehensive selectors for common doc platforms
    content_selectors = [
        "article",                     # Generic articles
        ".markdown",                   # Markdown content
        ".theme-doc-markdown",         # Docusaurus
        ".gitbook-root",               # GitBook
        ".document",                   # ReadTheDocs/Sphinx
        ".bd-content",                 # Bootstrap docs
        ".page-body",                  # Generic page content
        ".role-content",               # Sphinx roles
        ".section",                    # Document sections
        ".main-content",               # Common main content area
        "[role='main']"                # ARIA main content
    ]

    # Combine selectors with fallback
    css_selector = ", ".join(content_selectors)

    config = CrawlerRunConfig(
        css_selector=css_selector,
        wait_for="css:article, .markdown, .document, [role='main']",
        remove_overlay_elements=True,
        exclude_tags=[
            "nav", "header", "footer",
            ".sidebar", ".navigation", ".menu",
            ".table-of-contents", ".toc",
            ".pagination", ".breadcrumbs",
            ".related-topics", ".suggestions",
            "script", "style", "noscript"
        ],
        page_timeout=45000
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)

        if result.success:
            return {
                "content": str(result.markdown),
                "metadata": result.metadata,
                "platform": detect_platform(result.html),
                "structure": analyze_doc_structure(str(result.markdown))
            }
        else:
            raise Exception(f"Failed to extract documentation: {result.error_message}")

def detect_platform(html_content):
    """Detect documentation platform from HTML patterns"""
    import re

    if 'docusaurus' in html_content.lower():
        return "docusaurus"
    elif 'gitbook' in html_content.lower():
        return "gitbook"
    elif 'readthedocs' in html_content.lower() or 'sphinx' in html_content.lower():
        return "readthedocs"
    elif 'mkdocs' in html_content.lower():
        return "mkdocs"
    else:
        return "unknown"

def analyze_doc_structure(content):
    """Analyze documentation structure for better organization"""
    import re

    structure = {
        "headings": re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE),
        "code_blocks": re.findall(r'```(\w+)?\n(.*?)\n```', content, re.DOTALL),
        "tables": len(re.findall(r'\|.*\|', content)),
        "links": len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)),
        "images": len(re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content))
    }

    return structure
```

## Content Filtering for Documentation

### Relevance-Based Extraction
```python
from crawl4ai.content_filter_strategy import BM25ContentFilter

async def extract_relevant_docs(url, focus_area):
    """Extract documentation focused on specific topics"""

    # Create relevance filter
    bm25_filter = BM25ContentFilter(
        user_query=focus_area,
        bm25_threshold=1.2,  # Higher threshold for focused extraction
        include_tables=True,
        include_code=True
    )

    md_generator = DefaultMarkdownGenerator(
        content_filter=bm25_filter,
        options={
            "ignore_links": False,  # Keep internal links for navigation
            "ignore_images": False,
            "image_alt_text": True,
            "code_block_format": "fenced"  # Ensure proper code formatting
        }
    )

    config = CrawlerRunConfig(
        css_selector="article, .document, .markdown",
        markdown_generator=md_generator
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)

        return {
            "focused_content": str(result.markdown.fit_markdown),
            "raw_content": str(result.markdown.raw_markdown),
            "relevance_score": len(str(result.markdown.fit_markdown)) / len(str(result.markdown.raw_markdown))
        }
```

### Section-Based Extraction
```python
def extract_sections(content):
    """Extract and organize documentation sections"""
    import re

    # Split by headers
    sections = []
    current_section = {"title": "Introduction", "level": 0, "content": []}

    for line in content.split('\n'):
        header_match = re.match(r'^(#{1,6})\s+(.+)$', line)

        if header_match:
            # Save current section
            if current_section["content"]:
                sections.append(current_section)

            # Start new section
            level = len(header_match.group(1))
            title = header_match.group(2)
            current_section = {
                "title": title,
                "level": level,
                "content": [line]
            }
        else:
            current_section["content"].append(line)

    # Add final section
    if current_section["content"]:
        sections.append(current_section)

    return sections

async def extract_structured_docs(url):
    """Extract documentation with section organization"""

    config = CrawlerRunConfig(
        css_selector="article, .document, .markdown",
        remove_overlay_elements=True
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)

        if result.success:
            content = str(result.markdown)
            sections = extract_sections(content)

            return {
                "sections": sections,
                "toc": generate_toc(sections),
                "metadata": result.metadata
            }

def generate_toc(sections):
    """Generate table of contents from sections"""
    toc = []
    for section in sections:
        indent = "  " * (section["level"] - 1)
        toc.append(f"{indent}- [{section['title']}](#{section['title'].lower().replace(' ', '-')})")
    return "\n".join(toc)
```

## Multi-Page Documentation

### Table of Contents Discovery
```python
async def discover_documentation_structure(base_url):
    """Discover multi-page documentation structure"""

    config = CrawlerRunConfig(
        css_selector="nav, .sidebar, .toctree, .table-of-contents",
        exclude_tags=["script", "style", "footer"]
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(base_url, config=config)

        if result.success:
            # Extract navigation links
            toc_links = []
            for link_info in result.links.get("internal", []):
                href = link_info.get("href", "")
                text = link_info.get("text", "")

                # Focus on documentation links
                if any(keyword in href.lower() for keyword in ["docs", "guide", "tutorial", "api", "reference"]):
                    toc_links.append({
                        "url": href,
                        "title": text,
                        "type": categorize_link(href, text)
                    })

            return organize_links(toc_links)
        else:
            return []

def categorize_link(url, text):
    """Categorize documentation links"""
    url_lower = url.lower()
    text_lower = text.lower()

    if any(kw in url_lower or kw in text_lower for kw in ["api", "reference"]):
        return "api-reference"
    elif any(kw in url_lower or kw in text_lower for kw in ["tutorial", "guide", "how-to"]):
        return "tutorial"
    elif any(kw in url_lower or kw in text_lower for kw in ["intro", "getting-started", "overview"]):
        return "introduction"
    else:
        return "general"

def organize_links(links):
    """Organize links by category and hierarchy"""
    organized = {
        "introduction": [],
        "tutorials": [],
        "api-reference": [],
        "general": []
    }

    for link in links:
        category = link.pop("type")
        if category == "tutorial":
            organized["tutorials"].append(link)
        else:
            organized[category].append(link)

    return organized
```

### Batch Documentation Extraction
```python
async def extract_complete_docs(base_url, max_pages=50):
    """Extract complete documentation site"""

    # First, discover structure
    structure = await discover_documentation_structure(base_url)

    # Collect all URLs
    all_urls = [base_url]
    for category_links in structure.values():
        all_urls.extend(link["url"] for link in category_links)

    # Remove duplicates and limit
    unique_urls = list(dict.fromkeys(all_urls))[:max_pages]

    # Convert to absolute URLs
    from urllib.parse import urljoin
    absolute_urls = [urljoin(base_url, url) if url.startswith('/') else url for url in unique_urls]

    # Extract content from all pages
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(
            urls=absolute_urls,
            config=CrawlerRunConfig(
                css_selector="article, .document, .markdown",
                remove_overlay_elements=True,
                page_timeout=30000
            ),
            max_concurrent=3
        )

        # Organize results
        extracted_docs = {}
        for i, result in enumerate(results):
            if result.success:
                url = absolute_urls[i]
                sections = extract_sections(str(result.markdown))
                extracted_docs[url] = {
                    "sections": sections,
                    "metadata": result.metadata,
                    "structure": analyze_doc_structure(str(result.markdown))
                }

        return extracted_docs
```

## Specialized Extraction Patterns

### API Documentation
```python
schema = {
    "name": "api_endpoints",
    "baseSelector": ".api-endpoint, .method, .endpoint",
    "fields": [
        {"name": "method", "selector": ".http-method, .verb", "type": "text"},
        {"name": "path", "selector": ".path, .route", "type": "text"},
        {"name": "description", "selector": ".description", "type": "text"},
        {"name": "parameters", "selector": ".parameters", "type": "text"},
        {"name": "example", "selector": ".example, .code-example", "type": "text"}
    ]
}

async def extract_api_docs(url):
    extraction_strategy = JsonCssExtractionStrategy(schema=schema)
    config = CrawlerRunConfig(
        css_selector=".api-reference, .endpoints, .methods",
        extraction_strategy=extraction_strategy
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)
        return result.extracted_content
```

### Tutorial Extraction
```python
async def extract_tutorials(url):
    """Extract tutorial content with step-by-step instructions"""

    # Focus on tutorial-specific elements
    config = CrawlerRunConfig(
        css_selector=".tutorial, .guide, .how-to, .steps",
        wait_for="css:.step, .instruction, .tutorial-content",
        remove_overlay_elements=True
    )

    # Content filter for instructional content
    bm25_filter = BM25ContentFilter(
        user_query="tutorial steps instructions how to guide",
        bm25_threshold=1.0
    )

    md_generator = DefaultMarkdownGenerator(
        content_filter=bm25_filter,
        options={"ignore_links": False, "code_block_format": "fenced"}
    )

    config.markdown_generator = md_generator

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)

        if result.success:
            content = str(result.markdown.fit_markdown)
            return {
                "content": content,
                "steps": extract_tutorial_steps(content),
                "code_examples": extract_code_examples(content)
            }

def extract_tutorial_steps(content):
    """Extract numbered steps or instructions"""
    import re

    step_patterns = [
        r'^\d+\.\s+(.+)$',           # "1. Step description"
        r'^\*\s+Step\s+\d+:?\s*(.+)$',  # "* Step 1: description"
        r'^###\s+Step\s+\d+:?\s*(.+)$'  # "### Step 1: description"
    ]

    steps = []
    for line in content.split('\n'):
        for pattern in step_patterns:
            match = re.match(pattern, line.strip())
            if match:
                steps.append(match.group(1))
                break

    return steps

def extract_code_examples(content):
    """Extract code examples from tutorial"""
    import re

    code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', content, re.DOTALL)

    return [
        {
            "language": lang or "text",
            "code": code.strip(),
            "lines": len(code.split('\n'))
        }
        for lang, code in code_blocks
    ]
```

## Output Formatting

### Structured Documentation Output
```python
def format_documentation_output(extracted_docs, output_format="markdown"):
    """Format extracted documentation for different use cases"""

    if output_format == "structured":
        return {
            "summary": generate_summary(extracted_docs),
            "table_of_contents": generate_master_toc(extracted_docs),
            "content": extracted_docs,
            "metadata": {
                "total_pages": len(extracted_docs),
                "total_sections": sum(len(doc["sections"]) for doc in extracted_docs.values())
            }
        }

    elif output_format == "single-file":
        # Combine all documentation into single markdown file
        combined_content = []
        combined_content.append("# Complete Documentation\n")
        combined_content.append(generate_master_toc(extracted_docs))
        combined_content.append("---\n")

        for url, doc in extracted_docs.items():
            combined_content.append(f"## {doc['metadata'].get('title', url)}\n")
            for section in doc["sections"]:
                combined_content.extend(section["content"])
            combined_content.append("\n---\n")

        return "\n".join(combined_content)

    else:  # markdown default
        return extracted_docs

def generate_summary(extracted_docs):
    """Generate summary of extracted documentation"""

    total_pages = len(extracted_docs)
    api_pages = sum(1 for doc in extracted_docs.values()
                   if "api" in doc["metadata"].get("title", "").lower())
    tutorial_pages = sum(1 for doc in extracted_docs.values()
                        if "tutorial" in doc["metadata"].get("title", "").lower() or
                           "guide" in doc["metadata"].get("title", "").lower())

    return {
        "pages_extracted": total_pages,
        "api_documentation": api_pages,
        "tutorials_guides": tutorial_pages,
        "other_pages": total_pages - api_pages - tutorial_pages
    }
```

## Best Practices

1. **Platform Detection**: Always attempt to detect the documentation platform for optimal extraction
2. **Content Filtering**: Use BM25 filtering to focus on relevant documentation sections
3. **Structure Preservation**: Maintain heading hierarchy and code block formatting
4. **Link Handling**: Preserve internal navigation links for context
5. **Batch Processing**: Use `arun_many()` for multi-page documentation with appropriate concurrency limits
6. **Rate Limiting**: Add delays between requests when extracting large documentation sites
7. **Error Recovery**: Implement retry logic for individual page failures

---

This skill provides comprehensive patterns for extracting documentation from virtually any platform while maintaining structure, readability, and context.