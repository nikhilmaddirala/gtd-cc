#!/usr/bin/env python3
"""
Structured data extraction example using CSS selectors
Extract specific information from web pages
"""

import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def extract_articles(url):
    """Extract articles from a blog or news site"""

    # Define extraction schema for articles
    schema = {
        "name": "articles",
        "baseSelector": "article, .post, .entry",
        "fields": [
            {"name": "title", "selector": "h1, h2, .title", "type": "text"},
            {"name": "author", "selector": ".author, .byline", "type": "text"},
            {"name": "date", "selector": ".date, time, .published", "type": "text"},
            {"name": "summary", "selector": ".summary, .excerpt", "type": "text"},
            {"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}
        ]
    }

    extraction_strategy = JsonCssExtractionStrategy(schema=schema)
    config = CrawlerRunConfig(extraction_strategy=extraction_strategy)

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)

        if result.success:
            return result.extracted_content
        else:
            raise Exception(f"Failed to extract from {url}: {result.error_message}")

async def extract_products(url):
    """Extract product information from an e-commerce site"""

    schema = {
        "name": "products",
        "baseSelector": ".product, .item",
        "fields": [
            {"name": "name", "selector": ".title, .name", "type": "text"},
            {"name": "price", "selector": ".price, .cost", "type": "text"},
            {"name": "description", "selector": ".description", "type": "text"},
            {"name": "rating", "selector": ".rating, .stars", "type": "text"},
            {"name": "availability", "selector": ".stock, .availability", "type": "text"}
        ]
    }

    extraction_strategy = JsonCssExtractionStrategy(schema=schema)
    config = CrawlerRunConfig(extraction_strategy=extraction_strategy)

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url, config=config)

        if result.success:
            return result.extracted_content
        else:
            raise Exception(f"Failed to extract from {url}: {result.error_message}")

# Example usage
if __name__ == "__main__":
    # Note: Replace with actual URLs when testing
    blog_url = "https://example-blog.com"
    shop_url = "https://example-shop.com"

    print("Article Extraction Example:")
    print("URL:", blog_url)
    print("Schema extracts: title, author, date, summary, link")
    print("Run: asyncio.run(extract_articles(blog_url))")
    print()

    print("Product Extraction Example:")
    print("URL:", shop_url)
    print("Schema extracts: name, price, description, rating, availability")
    print("Run: asyncio.run(extract_products(shop_url))")