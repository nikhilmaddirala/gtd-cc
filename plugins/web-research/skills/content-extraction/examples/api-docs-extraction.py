#!/usr/bin/env python3
"""
API documentation extraction example
Extract API endpoints, parameters, and examples from documentation sites
"""

import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def extract_api_endpoints(url):
    """Extract API endpoints from documentation"""

    schema = {
        "name": "api_endpoints",
        "baseSelector": ".api-endpoint, .method, .endpoint, .http-method",
        "fields": [
            {"name": "method", "selector": ".http-method, .verb, .method", "type": "text"},
            {"name": "path", "selector": ".path, .route, .endpoint", "type": "text"},
            {"name": "description", "selector": ".description, .desc", "type": "text"},
            {"name": "parameters", "selector": ".parameters, .params", "type": "text"},
            {"name": "example", "selector": ".example, .code-example, .sample", "type": "text"}
        ]
    }

    extraction_strategy = JsonCssExtractionStrategy(schema=schema)
    config = CrawlerRunConfig(
        css_selector=".api-reference, .endpoints, .methods",
        extraction_strategy=extraction_strategy
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)

        if result.success:
            return result.extracted_content
        else:
            raise Exception(f"Failed to extract API docs from {url}")

async def extract_code_examples(url):
    """Extract code examples from documentation"""

    config = CrawlerRunConfig(
        css_selector=".docs, .documentation, .content",
        remove_overlay_elements=True
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)

        if result.success:
            content = str(result.markdown)

            # Extract code blocks using regex
            import re
            code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', content, re.DOTALL)

            return {
                "url": url,
                "code_examples": [
                    {
                        "language": lang or "text",
                        "code": code.strip(),
                        "lines": len(code.split('\n'))
                    }
                    for lang, code in code_blocks
                ]
            }

# Example usage
if __name__ == "__main__":
    # Replace with actual API documentation URLs
    api_docs_url = "https://docs.example.com/api"

    print("API Documentation Extraction Example")
    print(f"URL: {api_docs_url}")
    print("Extracts: HTTP methods, endpoints, parameters, code examples")
    print("Run: asyncio.run(extract_api_endpoints(api_docs_url))")
    print()
    print("Code Examples Extraction Example")
    print("Extracts all code blocks from documentation")
    print("Run: asyncio.run(extract_code_examples(api_docs_url))")