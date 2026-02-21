# Reference Documentation

This directory contains detailed reference materials, architectural guides, and conceptual documentation for GTD-CC and its plugins.

## Overview

Reference documentation provides deep-dive information about systems, architectures, and concepts that users and developers need to understand. Use this layer when you need to understand "how things work" rather than "how to use it".

## Available References

### Plugin Marketplaces Documentation

File: `docs/plugin-marketplaces.md`

Comprehensive guide to Claude Code plugin marketplace architecture, structure, and best practices.

Covers:
- Marketplace structure and organization
- Plugin manifest format and validation
- Component types (commands, agents, skills)
- Best practices for plugin development
- Distribution and installation

Read this when: Learning about plugin architecture, creating new plugins, understanding marketplace organization.

### Architecture Principles

File: `docs/architecture-principles.md`

Detailed guide to the architectural principles and design patterns used throughout GTD-CC.

Covers:
- Component architecture and layering
- Skill, command, and agent design patterns
- Integration patterns between plugins
- Best practices for extensibility
- Performance and scalability considerations

Read this when: Understanding the overall system design, extending existing plugins, creating new components.

## Documentation Layers

These references form the deepest layer of the three-layer documentation model:

```
README.md (Marketplace level)
  ↓ Links to
Plugin README.md (Plugin level)
  ↓ Links to
This directory + Skill documentation (Detail level)
```

Users should rarely need to consult this layer for basic usage. It's for:
- Developers extending the system
- Architects designing new components
- Troubleshooters debugging complex issues
- Contributors understanding design decisions

## How to Use This Documentation

1. **Start with the plugin README** if you're learning about a plugin
2. **Consult the skill documentation** (`*/SKILL.md` files) for detailed procedures
3. **Read these references** for architectural understanding and deep-dive knowledge

## Reference vs. Skill Documentation

These references differ from skill documentation:

- **References** explain "why" and "how things work" at a systems level
- **Skills** explain "how to do it" with step-by-step procedures
- **References** are conceptual and architectural
- **Skills** are practical and procedural

## Adding New References

When adding new reference documentation:

1. Create a markdown file in this directory (e.g., `my-topic.md`)
2. Update this README with a description and guidance on when to read it
3. Ensure the reference explains architectural/conceptual information
4. Link to relevant skills or commands for procedural guidance
5. Include diagrams and examples where helpful

## Related Documentation

- [Main README](../README.md) - Marketplace overview
- [Plugins Guide](../plugins/README.md) - Plugin selection and overview
- [Getting Started](../GETTING-STARTED.md) - First-time user guide
- [Contributing](../CONTRIBUTING.md) - Developer guidelines
- [Skill Documentation](../plugins/*/skills/*/SKILL.md) - Detailed procedures
