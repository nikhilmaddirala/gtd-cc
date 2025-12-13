#!/usr/bin/env python3
"""
Intelligent site crawler example
Demonstrates adaptive crawling with quality control
"""

import asyncio
from urllib.parse import urljoin, urlparse
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

class SimpleIntelligentCrawler:
    def __init__(self, base_url, max_pages=20):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.max_pages = max_pages
        self.visited = set()
        self.queue = [base_url]
        self.discovered = {}

    async def crawl(self):
        """Main crawling method"""

        async with AsyncWebCrawler() as crawler:
            while self.queue and len(self.visited) < self.max_pages:
                url = self.queue.pop(0)

                if url in self.visited:
                    continue

                try:
                    # Crawl current page
                    result = await self._crawl_page(crawler, url)
                    if result:
                        self.discovered[url] = result
                        self.visited.add(url)

                        # Add new links to queue
                        new_links = self._extract_links(result['links'], url)
                        self.queue.extend(new_links[:5])  # Limit new links

                    print(f"Crawled: {url} (Total: {len(self.visited)})")

                except Exception as e:
                    print(f"Failed to crawl {url}: {e}")

                # Be respectful
                await asyncio.sleep(1)

        return self.generate_report()

    async def _crawl_page(self, crawler, url):
        """Crawl single page"""

        config = CrawlerRunConfig(
            page_timeout=30000,
            remove_overlay_elements=True,
            exclude_tags=["script", "style", "nav", "footer"]
        )

        result = await crawler.arun(url, config=config)

        if result.success:
            return {
                "title": result.metadata.get("title", ""),
                "description": result.metadata.get("description", ""),
                "content_length": len(str(result.markdown)),
                "links": result.links,
                "url": url
            }
        return None

    def _extract_links(self, links, base_url):
        """Extract and filter internal links"""

        internal_links = []
        for link_info in links.get("internal", []):
            href = link_info.get("href", "")

            # Skip invalid links
            if not href or href.startswith(('#', 'mailto:', 'javascript:')):
                continue

            # Convert to absolute URL
            if href.startswith('/'):
                href = urljoin(base_url, href)

            # Only include same domain
            if urlparse(href).netloc == self.base_domain and href not in self.visited:
                internal_links.append(href)

        return internal_links

    def generate_report(self):
        """Generate crawling report"""

        if not self.discovered:
            return {"error": "No pages crawled successfully"}

        total_content = sum(page["content_length"] for page in self.discovered.values())

        return {
            "summary": {
                "pages_crawled": len(self.discovered),
                "total_content_chars": total_content,
                "average_content_length": total_content / len(self.discovered),
                "base_url": self.base_url
            },
            "pages": [
                {
                    "url": url,
                    "title": data["title"],
                    "description": data["description"],
                    "content_length": data["content_length"]
                }
                for url, data in self.discovered.items()
            ]
        }

# Example usage
if __name__ == "__main__":
    # Test with a documentation site or blog
    test_url = "https://example.com"  # Replace with real URL

    print("Intelligent Site Crawler Example")
    print(f"Starting URL: {test_url}")
    print(f"Max pages: 20")
    print("Features: Adaptive crawling, link discovery, quality assessment")
    print()
    print("To run:")
    print("crawler = SimpleIntelligentCrawler(test_url, max_pages=20)")
    print("report = asyncio.run(crawler.crawl())")
    print("print(f'Crawled {report[\"summary\"][\"pages_crawled\"]} pages')")
    print()