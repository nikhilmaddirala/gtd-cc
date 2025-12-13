---
name: web-crawler
description: Crawl entire websites and save markdown files to obsidian-2025-07/05-misc/web-crawl using crawl4ai
---

# Web Crawler Skill

This skill uses crawl4ai to crawl entire websites and save content as markdown files to `~/repos/obsidian-2025-07/05-misc/web-crawl/`.

## Instructions

1. **Get the website URL** - User provides the URL to crawl
2. **Create output directory** - Create a timestamped subdirectory in the web-crawl folder
3. **Run crawler with sensible defaults** - Use crawl4ai via uvx with max-depth 3
4. **Verify output** - Check that markdown files were created and are readable

## Usage

When you have a URL to crawl:

```bash
uvx crawl4ai crawl \
  --url "https://example.com" \
  --output-dir "/Users/nikhilmaddirala/repos/obsidian-2025-07/05-misc/web-crawl/example-com-$(date +%Y%m%d-%H%M%S)" \
  --max-depth 3 \
  --format markdown
```

## Default Parameters

- `--max-depth 3` - Crawl up to 3 levels deep from the root URL (sensible default)
- `--format markdown` - Save content as markdown
- Output goes to timestamped subdirectory in web-crawl folder for easy organization

## Example Output

Running the crawler creates files like:
```
/Users/nikhilmaddirala/repos/obsidian-2025-07/05-misc/web-crawl/
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

## Tips

- Max depth of 3 prevents crawling too deep into unimportant pages
- Timestamped directories keep multiple crawls organized
- Each crawl is self-contained and easy to review in Obsidian
- Check the markdown output for content quality before using

## References

- [crawl4ai GitHub](https://github.com/unclecode/crawl4ai)
- [crawl4ai Documentation](https://crawl4ai.com)
