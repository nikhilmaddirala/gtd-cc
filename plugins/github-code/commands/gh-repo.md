---
description: Create repository
---

## Context: GitHub Environment

```bash
# Check current GitHub authentication
gh auth status

# List existing repositories for reference
gh repo list --limit 10

# Check available organizations (if any)
gh api user/orgs --jq '.[].login' 2>/dev/null || echo "No organizations found"

# Check repository templates (if any)
gh repo list --template --limit 5 2>/dev/null || echo "No template repos found"
```

## Your Task

**Goal**: Create a new GitHub repository with proper configuration and initial setup.

**User's initial request**: $ARGUMENTS

### Process

1. **Understand the request**
   - Chat iteratively with the user to clarify details
   - Determine repository type (public, private, template)
   - Understand purpose, target audience, and initial content needs

2. **Gather repository information and configure settings**
   
   **Required fields:**
   - **Repository name**: What should it be called?
   
   **Optional fields with sensible defaults:**
   - **Description**: Brief description (default: none)
   - **Visibility**: Public or private (default: private)
   - **Template**: Use existing template repository (default: create from scratch)
   - **Organization**: Organization or personal account (default: personal)
   - **README**: Include basic README (default: yes for new repos)
   - **.gitignore**: Language/framework template (default: none, suggest based on context)
   - **License**: MIT, Apache, GPL, etc. (default: none)
   - **Default branch**: Main or master (default: main)
   - **Features**: Enable issues, projects, wiki, discussions (default: all enabled)
   - **Collaborators/Teams**: Who should have access (default: none)

   **Template selection:**
   - If user wants a template, show available options from `gh repo list --template`
   - Allow user to choose from existing template repositories
   - Or create from scratch with standard initialization

3. **Create the repository**
   Use `gh repo create` with appropriate flags:
   ```bash
   gh repo create REPO_NAME [flags]
   ```
   Common flags:
   - `--public` or `--private`
   - `--description "DESCRIPTION"`
   - `--clone` to clone after creation
   - `--template TEMPLATE_REPO` for template-based creation
   - `--readme` to add README
   - `--gitignore LANGUAGE` for .gitignore template
   - `--license LICENSE` for license
   - `--org ORGANIZATION` for organization repos

4. **Post-creation setup** (if requested)
   - Clone the repository locally
   - Add initial files or structure
   - Set up branch protection rules
   - Create initial commit with proper structure
   - Add collaborators or teams

### Guidelines

- Ensure repository name follows GitHub naming conventions
- Create meaningful descriptions that help others understand the purpose
- Initialize with appropriate .gitignore for the technology stack
- Choose appropriate license based on intended use
- Consider security implications of public vs private
- Set up proper access controls if working with teams
- Include basic documentation (README) for better discoverability
- Follow organization standards if creating under an org account