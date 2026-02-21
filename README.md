# gtd-cc

AI agent skills for getting things done. Works with Claude Code, OpenCode, Cursor, Codex, and 30+ other agents via [npx skills](https://skills.sh).

## Install

```bash
# All skills
npx skills add nikhilmaddirala/gtd-cc -a claude-code -y

# Single skill
npx skills add nikhilmaddirala/gtd-cc --skill web-deep-research -a claude-code -y
```

## Skills

### web- : web research and browser automation

- **web-search** - web search patterns and techniques
- **web-fetch** - download articles as markdown
- **web-deep-research** - multi-step deep research with synthesis
- **web-crawl4ai** - Crawl4AI SDK for scraping and data extraction
- **web-content-extraction** - extract docs from Mintlify, Docusaurus, GitBook, etc.
- **web-browser** - Playwright and agent-browser automation

### docs- : document format parsing

- **docs-pptx** - PowerPoint to markdown with images
- **docs-docx** - Word documents to markdown
- **docs-xlsx** - Excel spreadsheets to CSV/JSON
- **docs-pdf** - PDF to markdown and text
- **docs-pbix** - Power BI files to JSON/CSV

### documentation : project documentation

- **documentation** - layered documentation system for READMEs, changelogs, and project docs

### obsidian- : Obsidian vault integration

- **obsidian-gtd** - vault management and GTD workflows
- **obsidian-options** - comparative evaluation and options research

### tools- : utilities

- **tools-langfuse** - Langfuse trace querying and observability
- **tools-secrets** - 1Password and Infisical secrets management
- **tools-diagnostics** - system resource analysis and troubleshooting
- **tools-backlog** - GTD task management with Backlog.md
- **tools-catppuccin** - Catppuccin theme port creation

### gtd-skills-dev : skill development

- **gtd-skills-dev** - patterns for developing skills and Claude Code plugins

## Structure

```
gtd-cc/
├── skills/           # 20 skills, flat directory
├── docs/             # per-category documentation
├── archive/          # legacy plugin infrastructure (to be removed)
└── README.md
```

## Contributing

- Each skill lives in `skills/<name>/` with a `SKILL.md` entry point
- The `name` field in SKILL.md frontmatter must match the directory name
- Push to GitHub and skills are automatically discoverable on [skills.sh](https://skills.sh)
