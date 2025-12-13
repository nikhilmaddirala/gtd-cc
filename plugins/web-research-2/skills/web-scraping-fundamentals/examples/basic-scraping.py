#!/usr/bin/env python3
"""
Basic web scraping example using crawl4ai
Extract content from a simple webpage
"""

import asyncio
from crawl4ai import AsyncWebCrawler

async def scrape_simple_page(url):
    """Extract content from a simple webpage"""

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url)

        if result.success:
            return {
                "url": url,
                "title": result.metadata.get("title", ""),
                "content": str(result.markdown)[:1000],  # First 1000 chars
                "content_length": len(str(result.markdown)),
                "links_found": len(result.links.get("internal", []))
            }
        else:
            raise Exception(f"Failed to scrape {url}: {result.error_message}")

# Example usage
if __name__ == "__main__":
    # Test with a simple site
    url = "https://example.com"

    try:
        data = asyncio.run(scrape_simple_page(url))
        print(f"Successfully scraped: {data['url']}")
        print(f"Title: {data['title']}")
        print(f"Content length: {data['content_length']} characters")
        print(f"Links found: {data['links_found']}")
        print(f"Content preview: {data['content'][:200]}...")

    except Exception as e:
        print(f"Error: {e}")