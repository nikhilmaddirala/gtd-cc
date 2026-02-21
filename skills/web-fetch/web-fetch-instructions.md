# Web Fetch Instructions: Downloading Articles with Images

Download web articles with images and save as clean markdown for offline reference.

## Process

1. **Fetch** article content as markdown
2. **Download** all images locally
3. **Update** markdown with local image paths

## Step-by-Step

### 1. Fetch Article Content

**Option A: WebFetch (Claude Code):**
```plaintext
WebFetch(
  url: "https://example.com/article",
  prompt: "Convert this entire article to clean, well-formatted markdown.
           Include all headings, paragraphs, code blocks, lists, and
           preserve all image URLs with their alt text in markdown format
           ![alt text](url). Capture the full article including title,
           author, date, and all sections."
)
```

**Option B: Jina AI Reader (free API, no install):**
```bash
curl "https://r.jina.ai/https://example.com/article" > article.md
```

**Option C: curl + pandoc (local conversion):**
```bash
# Download HTML
curl "https://example.com/article" -o article.html

# Convert to markdown
pandoc -f html -t markdown article.html -o article.md

# Install pandoc if needed:
# macOS: brew install pandoc
# Ubuntu: apt install pandoc
```

**Option D: lynx (text browser, preserves structure):**
```bash
lynx -dump -nolist "https://example.com/article" > article.md

# Install if needed:
# macOS: brew install lynx
# Ubuntu: apt install lynx
```

**Option E: w3m (alternative text browser):**
```bash
w3m -dump "https://example.com/article" > article.md

# Install if needed:
# macOS: brew install w3m
# Ubuntu: apt install w3m
```

**Option F: html2text (Python tool, good markdown conversion):**
```bash
curl "https://example.com/article" | html2text > article.md

# Install if needed:
# pip install html2text
```

### 2. Create Directory Structure

```bash
mkdir -p references/article-name/images
```

### 3. Download Images

**Parallel download (recommended for multiple images):**
```bash
curl -s -o "references/article-name/images/01-image.png" "https://cdn.example.com/image1.png" &
curl -s -o "references/article-name/images/02-image.png" "https://cdn.example.com/image2.png" &
curl -s -o "references/article-name/images/03-image.png" "https://cdn.example.com/image3.png" &
wait
```

Flags: `-s` (silent), `-o` (output file), `&` (background), `wait` (wait for all)

### 4. Update Markdown Paths

Replace remote URLs with local paths:
```markdown
# Before:
![Alt text](https://cdn.example.com/image.png)

# After:
![Alt text](images/01-image.png)
```

Add source metadata:
```markdown
# Article Title

**Source:** [Original Article](https://example.com/article)
**Downloaded:** 2024-12-11
**Authors:** Name Here

---

[Content...]
```

### 5. Verify

```bash
ls -lh references/article-name/
ls -lh references/article-name/images/
```

---

## Complete Example

Using Jina AI Reader (Option B):

```bash
# 1. Setup
mkdir -p references/building-effective-agents/images

# 2. Fetch article (using Jina AI - no install needed)
curl "https://r.jina.ai/https://www.anthropic.com/engineering/building-effective-agents" > temp.md

# 3. Download images (parallel)
curl -s -o "references/building-effective-agents/images/01-augmented-llm.png" \
     "https://cdn.sanity.io/images/4zrzovbb/website/d3083d3f40bb2b6f477901cc9a240738d3dd1371-2401x1000.png" &
curl -s -o "references/building-effective-agents/images/02-prompt-chaining.png" \
     "https://cdn.sanity.io/images/4zrzovbb/website/7418719e3dab222dccb379b8879e1dc08ad34c78-2401x1000.png" &
wait

# 4. Update paths (manual edit or sed)
# Use Write tool or text editor to replace URLs with local paths

# 5. Verify
ls -lh references/building-effective-agents/
```

---

## Advanced: Auto-Extract Image URLs

Extract all image URLs from markdown:
```bash
grep -o '!\[.*\](https://[^)]*)' article.md | sed 's/!\[.*\](\(.*\))/\1/'
```

Extract and download automatically:
```bash
grep -o '!\[.*\](https://[^)]*)' article.md | \
  sed 's/!\[.*\](\(.*\))/\1/' | \
  while IFS= read -r url; do
    filename=$(basename "$url")
    curl -s -o "images/$filename" "$url" &
  done
wait
```

---

## Troubleshooting

**404 errors or 0-byte files:**
```bash
# Remove -s to see errors
curl -o "image.png" "https://example.com/image.png"

# Follow redirects
curl -L -o "image.png" "https://example.com/image.png"

# Add user agent
curl -A "Mozilla/5.0" -o "image.png" "https://example.com/image.png"
```

**Images don't render:**
```bash
# Use relative paths (images/01.png) not absolute paths
# Verify files exist
ls -la images/
```

**JavaScript-required sites (Notion, etc.):**
```bash
# Some sites won't render content without JavaScript execution
# Solutions:
# 1. Use a headless browser: puppeteer, playwright, or selenium
# 2. Access the article through alternative sources
# 3. Fall back to copy-paste from browser rendering
# Not recommended: These tools require Node.js/Python and significant setup
```

---

## Learnings from Practical Extraction (Dec 2025)

### Recommended Tool Priority

**Tier 1: Jina AI Reader (Best)** ✅
```bash
curl "https://r.jina.ai/https://example.com/article" > article.md
```
- Works reliably across most sites (Anthropic, Medium, Analytics Vidhya, Google Cloud)
- Converts HTML to clean markdown automatically
- Preserves image URLs with alt text
- No installation required
- Handles redirects well
- Often better than WebFetch for large articles

**Tier 2: WebFetch (Good for exploration)**
- Useful for initial investigation
- Sometimes provides better formatting than Jina
- Good fallback for sites that block curl

**Tier 3: Local tools (When needed)**
- pandoc, lynx, html2text → More control but require installation
- Use only if Jina fails

### Source-Specific Learnings

#### Academic/Journal Sites (MDPI)
- Jina conversion works well for content
- **Challenge:** Embedded figures are in HTML, not directly downloadable
- **Solution:** Extract images directly from HTML source or search for figure URLs
- Markdown conversion captures text but may reference figures by number only
- Consider noting missing figures in converted markdown

```bash
# Search for embedded images in HTML
curl "https://www.mdpi.com/article-url" | grep -oE 'src="[^"]*\.(png|jpg)' | head -10
```

#### Medium Articles
- Jina handles content extraction well
- **Challenge:** Article content may reference images as "Press enter or click to view..."
- **Solution:** Search for actual image URLs in the markdown output
- Author avatars and embedded images can be found with:

```bash
grep -oE "https://miro\.medium\.com/[^[:space:]]*\.(png|jpg)" article.md
```

#### Blog Posts (Analytics Vidhya, Google Cloud, Anthropic)
- Jina works extremely well
- Images are usually directly referenced and downloadable
- Use auto-extract method (see section below)

#### Notion Pages
- ⚠️ **Requires JavaScript to render** - Cannot fetch with standard curl
- WebFetch may fail with 403 or render JavaScript placeholder
- Workaround: Copy-paste from browser or use headless browser tools

### Image URL Extraction Patterns

**For images in markdown:**
```bash
grep -oE '!\[.*\]\(https://[^)]*\)' article.md | sed 's/.*(\(.*\))/\1/' | sort -u
```

**For generic image URLs in HTML:**
```bash
grep -oE 'https://[^[:space:]]*\.(png|jpg|jpeg|gif|webp)' article.md | sort -u
```

**For CDN images with special characters:**
```bash
# Some CDNs use % encoding - decode them:
grep -oE "https://[^[:space:]]*%20[^[:space:]]*\.(png|jpg)" article.md | \
  sed 's/%20/ /g'
```

### Image Download Best Practices

**Sequential numbering:**
```bash
# Always use 01-, 02-, 03- format for easy sorting and reference
curl -s -L -o "images/01-first-image.png" "URL1" &
curl -s -L -o "images/02-second-image.png" "URL2" &
wait
```

**Use -L flag for redirects:**
```bash
# Many CDNs redirect - always include -L
curl -L -o "image.png" "https://cdn.example.com/image.png"
```

**Timeout for slow/failing downloads:**
```bash
# Add timeout to prevent hanging
curl -m 10 --connect-timeout 5 -L -o "image.png" "URL" &
```

### Markdown Metadata Format

Maintain consistency with this template:

```markdown
# Article Title

**Source:** [Full Link](https://example.com/article)
**Published:** Month DD, YYYY
**Author(s):** Name(s)

---

## Content...
```

### Final Checklist

✅ Create directory: `mkdir -p references/article-name/images`
✅ Try Jina first: `curl "https://r.jina.ai/FULL_URL" > article.md`
✅ Extract image URLs: `grep -oE 'https://.*\.(png|jpg)'`
✅ Download images with `-L` flag
✅ Update markdown paths: replace `https://...` with `images/01-name.png`
✅ Add source metadata block at top
✅ Verify: `ls -lh` both directories
✅ Test markdown renders locally

### Real-World Workflow Example

**Scenario:** Extracting 4+ articles from presentation references

```bash
# 1. Batch fetch using Jina (non-interactive, reliable)
mkdir -p references/{article1,article2,article3,article4}/images

curl "https://r.jina.ai/https://www.analyticsvidhya.com/blog/2023/05/..." > /tmp/analytics.md
curl "https://r.jina.ai/https://cloud.google.com/blog/..." > /tmp/google.md
curl "https://r.jina.ai/https://medium.com/..." > /tmp/medium.md

# 2. Extract image URLs from each
grep -oE "https://[^[:space:]]*\.(png|jpg|jpeg|gif)" /tmp/analytics.md > /tmp/urls-analytics.txt
grep -oE "https://[^[:space:]]*\.(png|jpg|jpeg|gif)" /tmp/google.md > /tmp/urls-google.txt
grep -oE "https://[^[:space:]]*\.(png|jpg|jpeg|gif)" /tmp/medium.md > /tmp/urls-medium.txt

# 3. Download images in parallel (watch for 0-byte files)
while read url; do
  filename=$(echo "$url" | sed 's/.*\///' | sed 's/%20/-/g')
  curl -s -L -m 10 -o "references/analytics/images/$filename" "$url" &
done < /tmp/urls-analytics.txt
wait

# 4. Check for failed downloads
find references/ -name "*.png" -size 0 -delete  # Remove 0-byte files
find references/ -name "*.png" -exec ls -lh {} \;  # Verify sizes

# 5. In markdown: replace https://cdn... with images/filename.png
sed -i '' 's|https://cdn\.analyticsvidhya\.com[^)]*|images/01-diagram.png|g' article.md
```

**Key insights:**
- Jina is reliable enough to batch multiple URLs
- Parallel downloads with `&` and `wait` significantly faster
- Always check for 0-byte files (indicates download failure)
- `-m 10` timeout prevents hanging on slow CDNs
- `-L` flag essential for redirects
- `sed` batch replacement saves manual editing

---

## Case Study: Extracting AI Presentation References (Dec 2025)

**Goal:** Extract 5 reference articles from presentation.md with all images

**Results:**
| Article | Source | Extraction | Images | Status |
|---------|--------|-----------|--------|--------|
| Building Effective Agents | Anthropic | Jina (success) | 8/8 ✓ | Complete |
| RLHF Fundamentals | Analytics Vidhya | Jina (success) | 1/1 ✓ | Complete |
| Spam → Tech Support | Google Cloud | Jina (success) | 1/1 ✓ | Complete |
| AI vs ML Framework | Medium | Jina (success) | 1/1 ✓ | Complete |
| AI in Education | MDPI Journal | Jina (success) | 0/n | Text-only |

**Learnings:**

✅ **What Worked:**
- Jina AI Reader extracted all 5 articles cleanly and reliably
- Direct CDN downloads (Analytics Vidhya, Google Cloud) successful on first attempt
- Parallel downloads with `&` and `wait` worked without issue
- Sequential image numbering (01-, 02-, ...) made organization clear

⚠️ **Challenges Encountered:**
- Medium article: Images existed but weren't obvious in markdown output
  - Solution: `grep -oE "https://miro\.medium\.com/.*\.jpeg"` found them
- MDPI article: Figures embedded in HTML, not directly downloadable
  - Impact: Left as text-only reference (academic journals often have this)
  - Workaround: Added note in markdown pointing readers to source
- One Notion page: Required JavaScript rendering
  - Abandoned that reference (not worth headless browser setup)

🔍 **Image Extraction Insights:**
- Not all images in markdown are content images
  - Author avatars, badges, logos often included
  - Filter by context (look for `![diagram`, `![figure`, `![chart`)
- CDN image URLs vary widely:
  - Some need `-L` for redirects
  - Some have URL-encoded spaces (`%20` → space)
  - Some need timeout because CDN is slow

✅ **Best Practices Confirmed:**
- Create directories first (prevents races)
- Jina > WebFetch for this use case (more reliable)
- Always download with `-L` flag
- Sequential numbering beats random filenames
- Metadata block (Source/Author/Date) improves usability
- Check file sizes after download (`ls -lh`)

**Timeline:**
- Article extraction: 5 URLs → 5 markdown files (parallel with Jina) = ~30 seconds
- Image discovery: grep patterns across 5 files = ~1 minute
- Image downloads: 11 images, parallel with curl = ~10 seconds
- Markdown updates: Manual + sed replacements = ~5 minutes

**Total:** ~50 minutes for complete extraction and verification
**If repeated:** Would take ~15 minutes (script-friendly now)

---

## CLI Alternatives

**Jina AI Reader:**
```bash
curl "https://r.jina.ai/YOUR_URL"
```

**wget (download page with assets):**
```bash
wget --page-requisites --convert-links -E -H -k -p https://example.com/article
```

**httrack (mirror entire site):**
```bash
httrack https://example.com/article -O ./output
```

**pandoc (HTML to markdown):**
```bash
pandoc -f html -t markdown https://example.com/article -o article.md
```

---

## Quick Reference

```bash
# 1. Create structure
mkdir -p references/ARTICLE_NAME/images

# 2. Fetch content (choose one):
# Jina AI (no install):
curl "https://r.jina.ai/URL" > article.md
# OR pandoc (local):
curl "URL" | pandoc -f html -t markdown -o article.md
# OR lynx:
lynx -dump -nolist "URL" > article.md
# OR html2text:
curl "URL" | html2text > article.md

# 3. Download images (parallel with &)
curl -s -o "images/01.png" "IMAGE_URL" &

# 4. Update markdown: replace URLs with images/01.png

# 5. Verify
ls -lh references/ARTICLE_NAME/
```
