---
name: gemini-web-research
description: Web research coordination using Google Gemini CLI in headless mode. Use this skill when you need to perform web searches as an alternative to built-in web search tools. This skill teaches any calling agent how to craft precise instructions for Gemini CLI to perform web research and return properly formatted results.
---

# Gemini Web Research CLI Coordination

## Agent Coordination Model

This skill operates on a two-agent model:

**Your Role (Calling Agent):**
- Analyzes user's web search requirements
- Crafts precise instructions for Gemini CLI
- Executes `gemini -p` commands with properly formatted prompts
- Processes and presents Gemini CLI's responses to users

**Gemini CLI (General Purpose Agent):**
- A general-purpose coding and research agent that can perform web searches when specifically instructed
- Accesses current information beyond knowledge cutoffs when asked to do web search
- Formats responses with source citations when requested
- Returns structured results based on received instructions

## Core Principle
You do NOT perform web searches directly. Instead, you act as an intelligent prompt coordinator that crafts optimal instructions for Gemini CLI to execute web searches effectively.


## Crafting Instructions for Gemini CLI

### Basic Web Search Instructions

When users need simple web searches, craft these prompts for Gemini CLI:

**Template for current information:**
```
Do a web search to find the latest information about [TOPIC]. Focus on recent developments, current status, and up-to-date data. Include sources with publication dates and provide comprehensive coverage of recent changes.
```

**Template for fact-checking:**
```
Search the web to verify the accuracy of [CLAIM]. Look for authoritative sources, fact-checking websites, and recent coverage. Provide evidence for or against the claim with proper source attribution.
```

**Template for recent developments:**
```
Conduct web research to answer: [QUESTION]. Focus on information from the past 6-12 months, recent news, and current developments. Prioritize recent sources and provide timeline context.
```

### Domain-Specific Search Instructions

**Site-specific research:**
```
Do web search on site:github.com for [QUERY]. Look for repositories, documentation, discussions, and issues related to [TOPIC]. Include repository stats, recent activity, and community feedback.
```

**Multiple domain restriction:**
```
Search the web on site:stackoverflow.com OR site:docs.microsoft.com OR site:medium.com for [TECHNICAL QUESTION]. Focus on recent solutions, best practices, and current documentation.
```

**News and industry sources:**
```
Conduct web research on site:techcrunch.com OR site:theverge.com OR site:arstechnica.com about [TOPIC]. Focus on recent coverage, industry analysis, and expert opinions from the past year.
```

### Advanced Research Instructions

**Competitive analysis:**
```
Do comprehensive web research to compare [PRODUCT A] vs [PRODUCT B]. Include recent reviews, pricing information, feature comparisons, user feedback, and market position. Look for sources from the past 6 months and provide balanced analysis with specific examples.
```

**Industry trends and statistics:**
```
Search the web for current trends and statistics about [INDUSTRY OR MARKET]. Focus on recent reports, market research, expert analysis, and quantitative data from the past 12 months. Include sources like industry reports, research firms, and reputable business publications.
```

**Technical documentation and examples:**
```
Do web search for latest best practices, documentation, and examples about [TECHNOLOGY]. Focus on official documentation, recent tutorials, community discussions, and current conventions. Include code examples and practical implementation guidance from 2024-2025.
```

## Execution Commands

### Basic Command Structure

```bash
# Direct web search with crafted instruction
gemini -p "[CRAFTED_INSTRUCTION_FOR_TOPIC]"

# Pipe content to Gemini with analysis instruction
cat [FILE] | gemini -p "Analyze this content and do web search for [RESEARCH_TOPIC]"
```

### JSON Output for Structured Data

```bash
# Get structured JSON response
gemini -p "[INSTRUCTION]" --output-format json | jq '.response'

# Extract sources from JSON response
gemini -p "[INSTRUCTION]" --output-format json | jq '.sources[]'

# Process streaming responses for long content
gemini -p "[COMPREHENSIVE_INSTRUCTION]" --output-format stream-json
```

## Response Processing

### Handling Gemini CLI Responses

After executing `gemini -p`, process the returned information:

**For standard text responses:**
- Extract main content and source citations
- Verify that sources are properly formatted with URLs
- Check for publication dates and source authority
- Present information in user-friendly format

**For JSON responses:**
```bash
# Extract main response content
gemini -p "[INSTRUCTION]" --output-format json | jq -r '.response'

# Extract structured sources
gemini -p "[INSTRUCTION]" --output-format json | jq '.sources[] | "\(.title): \(.url)"'

# Get metadata about search quality
gemini -p "[INSTRUCTION]" --output-format json | jq '.metadata'
```

### Quality Validation Guidelines

When processing Gemini CLI responses, verify:

1. **Source currency** - Check if information reflects recent developments
2. **Source reliability** - Assess credibility of cited sources
3. **Information completeness** - Ensure user's question is fully addressed
4. **Source accessibility** - Verify URLs are accessible and relevant

### Error Handling Strategies

If Gemini CLI returns inadequate results:

1. **Refine the instruction** with more specific requirements:
   ```
   Do web search for [TOPIC]. Focus on sources from 2024-2025, look for official documentation, and include specific examples and data points.
   ```

2. **Add domain constraints** for better source quality:
   ```
   Search the web on site:official-docs.com OR site:reputable-news.com about [TOPIC]. Focus on recent coverage and expert analysis.
   ```

3. **Request specific source types**:
   ```
   Do web research about [TOPIC]. Look for academic papers, industry reports, and government statistics from the past 12 months.
   ```

## Common Usage Scenarios

### Replacing Claude Code's WebSearch

**When user asks:** "What are the latest developments in AI?"

**Claude Code action:**
```bash
gemini -p "Do web search for latest developments in AI and machine learning. Focus on breakthrough technologies, recent product launches, and research advances from 2024-2025. Include specific examples, company announcements, and expert analysis with proper source attribution."
```

### Technical Research

**When user asks:** "How do I implement authentication in React?"

**Claude Code action:**
```bash
gemini -p "Search the web for current best practices and examples of implementing authentication in React applications. Focus on modern libraries like Auth0, Firebase Auth, and Next.js auth from 2024-2025. Include code examples, security considerations, and official documentation sources."
```

### Current Events Verification

**When user asks:** "Is [company] still in business?"

**Claude Code action:**
```bash
gemini -p "Search the web to verify the current business status of [COMPANY]. Look for recent news, official company announcements, financial reports, and reliable business sources from the past 6 months. Provide evidence of current operational status or changes."
```

## Integration with Local Content

### Code Analysis with Current Context

```bash
# Analyze codebase with current best practices
cat codebase.txt | gemini -p "Analyze this code structure and do web search for current best practices, security vulnerabilities, and modern alternatives for [TECHNOLOGY] as of 2024-2025. Focus on recent documentation and community recommendations."

# Update outdated patterns
README.md | gemini -p "Review this documentation and do web search for current project standards, formatting conventions, and comprehensive examples for [TOPIC]. Focus on recent guidelines and community best practices."
```

## Resources

- [Google Gemini CLI](https://github.com/google-gemini/gemini-cli) - Tool you're coordinating with
- [Headless Mode Guide](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/headless.md) - Execution patterns
- [JSON Output Documentation](https://github.com/google-gemini/gemini-cli/docs) - Response processing
- [Search Operators Reference](https://developers.google.com/search/docs/essentials/search_operators) - Instruction crafting
