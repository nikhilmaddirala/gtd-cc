# Web Research Plugin Skills Refactoring Plan

## Executive Summary
The web-research plugin currently has 7 skills with significant overlap and fragmentation. This plan consolidates to 4 focused skills while preserving all functionality.

## Current State Analysis

### Existing Skills (7)
1. **web-scraping-fundamentals** - Core crawl4ai patterns and examples
2. **crawl4ai** - Complete SDK toolkit with scripts and references  
3. **site-crawling** - Advanced site mapping and discovery
4. **documentation-extraction** - Doc-specific extraction patterns
5. **gemini-web-research** - AI-powered web search coordination
6. **web-crawler** - Simple site-to-markdown conversion
7. **web-fetch** - Article download instructions (not in manifest)

### Identified Issues
- **Major Overlap**: crawl4ai and web-scraping-fundamentals both provide comprehensive Crawl4AI coverage
- **Fragmentation**: 7 skills for similar crawling/extraction tasks
- **Unclear Separation**: "fundamentals" vs "complete toolkit" distinction
- **Inconsistency**: web-fetch exists but not in plugin manifest

## Proposed New Structure (4 Skills)

### 1. crawl4ai-toolkit
**Source Skills**: crawl4ai + web-scraping-fundamentals

**Purpose**: Complete Crawl4AI SDK reference and practical implementation guide

**Contents**:
- Full SDK documentation and API reference
- All scripts (basic_crawler.py, batch_crawler.py, extraction_pipeline.py)
- Tests and references directories
- Comprehensive code examples from both original skills
- Error handling, performance optimization, best practices

**Rationale**: Eliminates redundancy between two comprehensive Crawl4AI guides

### 2. site-crawling (Enhanced)
**Source Skills**: site-crawling + web-crawler functionality

**Purpose**: Intelligent website crawling and mapping with simple conversion

**Contents**:
- Advanced crawling strategies with depth control
- Simple markdown conversion (absorbed from web-crawler)
- Sitemap generation and link analysis
- Concurrent crawling patterns
- Obsidian vault integration

**Rationale**: Combines advanced and simple crawling approaches

### 3. content-extraction
**Source Skills**: documentation-extraction + web-fetch

**Purpose**: Specialized content extraction for various formats

**Contents**:
- Documentation platform detection and extraction
- Article downloading with image handling
- Multi-page documentation processing
- Structured data extraction patterns
- Image download and markdown updating

**Rationale**: Unifies content extraction approaches under one skill

### 4. gemini-web-research (Unchanged)
**Purpose**: AI-powered web search coordination

**Rationale**: Unique functionality with no overlaps - preserves as-is

## Benefits

### Quantitative Improvements
- **43% Reduction**: 7 skills → 4 skills
- **Overlap Elimination**: Removes major redundant content
- **Maintainability**: Fewer skills to maintain and update

### Qualitative Improvements
- **Clear Separation**: Each skill has distinct, non-overlapping purpose
- **Complete Coverage**: All existing functionality preserved
- **Better Organization**: Logical grouping of related capabilities

## Implementation Plan

### Phase 1: Content Consolidation
1. Create `crawl4ai-toolkit/` directory
2. Merge content from crawl4ai and web-scraping-fundamentals
3. Enhance `site-crawling/` with web-crawler functionality
4. Create `content-extraction/` merging documentation-extraction and web-fetch
5. Preserve `gemini-web-research/` unchanged

### Phase 2: Documentation Updates
1. Update README.md with new skill descriptions
2. Update plugin.json manifest
3. Update cross-references in documentation

### Phase 3: Cleanup
1. Remove old skill directories
2. Update any internal references
3. Test plugin functionality

## Risk Assessment

### Low Risk
- All functionality preserved in consolidation
- No breaking changes to commands or external APIs
- Backward compatibility maintained

### Mitigation Strategies
- Comprehensive testing of all merged functionality
- Gradual rollout with validation at each step
- Preserve original skills during transition for rollback

## Success Criteria
- [ ] All 4 new skills functional and documented
- [ ] No functionality lost in consolidation
- [ ] README.md accurately reflects new structure
- [ ] Plugin manifest updated correctly
- [ ] Cross-references updated throughout documentation
- [ ] Plugin loads and operates correctly

## Timeline
- **Phase 1**: 2-3 hours (content consolidation)
- **Phase 2**: 1 hour (documentation updates)  
- **Phase 3**: 30 minutes (cleanup and testing)

## Next Steps
1. Review and approve this plan
2. Execute Phase 1 consolidation
3. Validate functionality preservation
4. Complete remaining phases

---
*This plan was created on: 2025-01-13*