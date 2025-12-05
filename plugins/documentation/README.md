# Documentation Plugin

Generate, organize, and maintain GitHub project documentation using a scalable three-layer model.

## Overview

This plugin provides comprehensive tools and guidance for implementing professional documentation in any GitHub project. It's based on the Best README Template approach and works for projects of any size, from solo scripts to large teams.

## The Three-Layer Model

Documentation should grow naturally with your project using three layers:

```
README.md          → Entry point (quick facts)
Directory READMEs  → Local context (module explanations)
/docs/             → Deep dives (detailed content)
```

This prevents README bloat, eliminates scattered documentation, and scales from tiny projects to large organizations.

## Quick Start

### Phase Your Project

Determine which documentation phase fits your project:

- **Phase 1 (Small):** Solo developer, simple scripts, MVP — README.md only
- **Phase 2 (Medium):** 2-3 modules, established project — README.md + directory READMEs
- **Phase 3 (Growing):** Complex architecture, multiple teams — README.md + directory READMEs + /docs

### Initialize Documentation

```bash
/doc-init
```

This command guides you through setting up proper documentation structure for your project phase.

### Keep Docs Updated

When code changes require documentation updates:

```bash
/doc-update
```

### Audit Documentation Health

Periodically review your documentation:

```bash
/doc-audit
```

## Components

### Commands (Interactive Workflows)

- **`/doc-init`** - Initialize documentation structure for new or existing projects
- **`/doc-update`** - Update documentation when code changes
- **`/doc-audit`** - Run interactive documentation health audit
- **`/doc-compress`** - Create condensed versions for quick reference

### Agents (Autonomous Execution)

- **`doc-generator-agent`** - Automatically generate missing documentation
- **`doc-auditor-agent`** - Comprehensively audit documentation and generate improvement report

### Skill: docs-management

The **docs-management** skill contains all documentation guidance and workflows:

- **SKILL.md** - Philosophy and core principles
- **initialize.md** - Setting up documentation structure
- **update.md** - Updating documentation across layers
- **maintenance.md** - Keeping documentation fresh
- **compress.md** - Reducing documentation bloat

## Key Principles

1. **README is the front door** - Keep it simple, scannable, user-focused
2. **Directory docs localize complexity** - Explain module-specific context near the module
3. **Deep docs live in /docs** - Multi-page content doesn't belong in README
4. **One fact, one place** - Link instead of duplicating information
5. **Maintenance is continuous** - Document as you code, not after
6. **Documentation grows downward** - Start minimal, add layers as needed
7. **Quarterly reviews prevent rot** - Dedicate time to keeping docs fresh

## Documentation Evolution

### Small Project (Phase 1)

```
README.md              Single entry point
```

When you have:
- Solo developer
- Simple scripts
- <1000 lines of code
- One clear purpose

### Medium Project (Phase 2)

```
README.md              Entry point
src/README.md          Component explanation
tests/README.md        Testing structure
scripts/README.md      Automation scripts
```

When you have:
- 2-3 distinct modules
- 2-5 developers
- Established project
- Contributors need local context

### Growing Project (Phase 3)

```
README.md              Entry point
src/README.md
docs/
  index.md             Navigation hub
  architecture.md      System design
  api-reference.md     API docs
  configuration.md     Configuration
  tutorials/
    getting-started.md
  guides/
    contributing.md
```

When you have:
- Complex architecture
- 4+ major components
- Multiple tutorials
- Multiple teams/audiences

## Common Scenarios

### "I have a project with no documentation"

1. Run `/doc-init` to choose your phase
2. Use provided templates to create README.md
3. Add directory READMEs if Phase 2+
4. Iterate and improve over time

### "My documentation is scattered everywhere"

1. Run `/doc-audit` to assess current state
2. Run `/doc-update` to reorganize content
3. Consolidate duplicated information
4. Set up maintenance practices from `/doc-update`

### "I want to generate documentation automatically"

Use the `doc-generator-agent` to:
- Analyze your project structure
- Generate README.md template
- Create directory READMEs
- Scaffold /docs structure

Then customize the generated documentation with your specific content.

### "I'm preparing for a release"

Follow the release checklist in the **update.md** workflow with scope=all, type=minor:

- [ ] README matches current behavior
- [ ] Quick start instructions work end-to-end
- [ ] Configuration reference is up to date
- [ ] Examples compile and run
- [ ] All links are valid
- [ ] Breaking changes documented

### "Documentation feels out of date"

Run `/doc-audit` to identify:
- Outdated information
- Broken links
- Missing documentation
- Duplication to consolidate
- Coverage gaps

### "I want to establish documentation practices for my team"

From **update.md** with scope=all, type=minor, implement:

1. Add documentation checklist to PR template
2. Establish release documentation checklist
3. Schedule quarterly 2-hour documentation reviews
4. Create documentation maintenance guidelines
5. Make docs part of definition of done

## Structure Comparison

### Before Using Plugin

```
README.md (400 lines, everything)
CONTRIBUTING.md (scattered guidance)
docs/ (inconsistent and incomplete)
Directory folders (no READMEs)
Duplicated content everywhere
Broken links in navigation
```

### After Using Plugin

```
README.md (200 lines, entry point only)
src/README.md (explains source structure)
docs/
  index.md (navigation hub)
  architecture.md (system design)
  api-reference.md (complete API docs)
  tutorials/getting-started.md (setup guide)
  guides/contributing.md (contributor guide)
Content organized by user need
Links verified and working
No duplication across layers
```

## Maintenance Checklists

### Per Pull Request

- [ ] Updated relevant documentation
- [ ] Removed outdated information (didn't just patch around it)
- [ ] Used links instead of duplicating content
- [ ] Verified examples still work
- [ ] Tested Quick Start if commands changed

### Per Release

- [ ] README version matches release
- [ ] Getting Started works end-to-end
- [ ] Configuration documentation is current
- [ ] API reference has no TODOs
- [ ] Architecture matches implementation
- [ ] Breaking changes clearly documented

### Quarterly Review

- [ ] Deleted stale documentation
- [ ] Updated diagrams to match architecture
- [ ] Trimmed README to essentials
- [ ] Verified directory READMEs match reality
- [ ] Fixed broken links
- [ ] Updated version numbers

## Templates Provided

The plugin includes templates for:

### README.md

```markdown
# Project Title
## About
## Built With
## Getting Started
## Usage
## Roadmap
## Contributing
## License
## Contact
```

### Directory README.md

```markdown
# Folder Overview
## Structure
## How to Extend
## Related Docs
```

### /docs Structure

```
docs/index.md              - Navigation
docs/architecture.md       - System design
docs/api-reference.md      - API docs
docs/configuration.md      - Configuration
docs/tutorials/            - Tutorials
docs/guides/               - Guides
docs/diagrams/             - Visual content
```

## Integration with GitHub Workflow Plugin

This documentation plugin works alongside the GitHub workflow plugin:

- Document every feature on the PR that implements it
- Run quarterly documentation audit as part of release checklist
- Use documentation as part of issue definition of done
- Keep documentation history in git

## Common Patterns

### Installation Instructions

**Good:** Put full, tested instructions in README Quick Start section

**Better:** Keep in `/docs/tutorials/getting-started.md`, link from README

### Architecture Explanation

**Avoid:** Don't explain architecture in README

**Do:** Create `/docs/architecture.md` with detailed explanation, reference from README

### Configuration Reference

**Avoid:** Don't list all config options in README

**Do:** Create `/docs/configuration.md` with complete reference table, note in README

### Contribution Guidelines

**Do:** Create `CONTRIBUTING.md` or `/docs/guides/contributing.md`

**Link:** Reference from README and /docs/index.md

### API Reference

**For libraries:** Create `/docs/api-reference.md` with all public functions

**For services:** Create `/docs/api-reference.md` with endpoints and schemas

### Tutorials

**Multiple tutorials?** Use `/docs/tutorials/` folder with separate files

**Example structure:**
- docs/tutorials/getting-started.md
- docs/tutorials/basic-usage.md
- docs/tutorials/advanced-topics.md

## Anti-Patterns to Avoid

- ❌ Everything in README (makes it unwieldy)
- ❌ Duplicating information across layers (causes sync problems)
- ❌ Outdated information commented out (confusing and misleading)
- ❌ Documentation in random markdown files (hard to find)
- ❌ Promising "we'll document later" (never happens)
- ❌ No structure for large /docs folders (hard to navigate)
- ❌ Dead links and references (breaks navigation)

## Support & Resources

### Learn More

- See the **docs-management** skill for detailed procedures
- Read **initialize.md** for setup guidance
- Review **update.md** for ongoing practices
- Check **compress.md** for reducing documentation bloat

### Use Cases

- New project setup
- Existing project reorganization
- Release preparation
- Team documentation standards
- Quarterly documentation review
- Documentation quality assessment

### Workflows

The plugin includes detailed workflows for:

1. **initialize.md** - Choosing your phase and setting up structure
2. **update.md** - Updating documentation across layers
3. **maintenance.md** - Keeping docs fresh and preventing rot
4. **compress.md** - Reducing documentation bloat

## Status

- **Version:** 0.1.0
- **Maturity:** Production Ready
- **Scope:** GitHub projects of all sizes
- **Maintenance:** Ongoing

## Contributing

Contributions welcome for:

- Additional documentation templates
- Workflow enhancements
- Tool integrations
- Real-world examples
- Use case documentation

See the gtd-cc CONTRIBUTING.md for guidelines.

## License

MIT

## Contact

See the gtd-cc README for contact and support information.

---

**Next Steps:**

Ready to improve your project documentation? Start with `/doc-init` to set up proper structure, or run `/doc-audit` to assess your current documentation health.
