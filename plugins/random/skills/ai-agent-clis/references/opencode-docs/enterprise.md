Title: Enterprise

URL Source: https://opencode.ai/docs/enterprise/

Markdown Content:
Enterprise | OpenCode
===============
[Skip to content](https://opencode.ai/docs/enterprise/#_top)

[![Image 1](https://opencode.ai/docs/_astro/logo-dark.DOStV66V.svg)![Image 2](https://opencode.ai/docs/_astro/logo-light.B0yzR0O5.svg) OpenCode](https://opencode.ai/)

[Home](https://opencode.ai/)[Docs](https://opencode.ai/docs/)

[](https://github.com/anomalyco/opencode)[](https://opencode.ai/discord)

Search Ctrl K

 Cancel 

*   [Intro](https://opencode.ai/docs/)
*   [Config](https://opencode.ai/docs/config/)
*   [Providers](https://opencode.ai/docs/providers/)
*   [Network](https://opencode.ai/docs/network/)
*   [Enterprise](https://opencode.ai/docs/enterprise/)
*   [Troubleshooting](https://opencode.ai/docs/troubleshooting/)
*   [Migrating to 1.0](https://opencode.ai/docs/1-0/)
*   
Usage 
    *   [TUI](https://opencode.ai/docs/tui/)
    *   [CLI](https://opencode.ai/docs/cli/)
    *   [Web](https://opencode.ai/docs/web/)
    *   [IDE](https://opencode.ai/docs/ide/)
    *   [Zen](https://opencode.ai/docs/zen/)
    *   [Share](https://opencode.ai/docs/share/)
    *   [GitHub](https://opencode.ai/docs/github/)
    *   [GitLab](https://opencode.ai/docs/gitlab/)

*   
Configure 
    *   [Tools](https://opencode.ai/docs/tools/)
    *   [Rules](https://opencode.ai/docs/rules/)
    *   [Agents](https://opencode.ai/docs/agents/)
    *   [Models](https://opencode.ai/docs/models/)
    *   [Themes](https://opencode.ai/docs/themes/)
    *   [Keybinds](https://opencode.ai/docs/keybinds/)
    *   [Commands](https://opencode.ai/docs/commands/)
    *   [Formatters](https://opencode.ai/docs/formatters/)
    *   [Permissions](https://opencode.ai/docs/permissions/)
    *   [LSP Servers](https://opencode.ai/docs/lsp/)
    *   [MCP servers](https://opencode.ai/docs/mcp-servers/)
    *   [ACP Support](https://opencode.ai/docs/acp/)
    *   [Agent Skills](https://opencode.ai/docs/skills/)
    *   [Custom Tools](https://opencode.ai/docs/custom-tools/)

*   
Develop 
    *   [SDK](https://opencode.ai/docs/sdk/)
    *   [Server](https://opencode.ai/docs/server/)
    *   [Plugins](https://opencode.ai/docs/plugins/)
    *   [Ecosystem](https://opencode.ai/docs/ecosystem/)

[GitHub](https://github.com/anomalyco/opencode)[Discord](https://opencode.ai/discord)

Select theme 

On this page

*   [Overview](https://opencode.ai/docs/enterprise/#_top)
*   [Trial](https://opencode.ai/docs/enterprise/#trial)
    *   [Data handling](https://opencode.ai/docs/enterprise/#data-handling)
    *   [Code ownership](https://opencode.ai/docs/enterprise/#code-ownership)

*   [Pricing](https://opencode.ai/docs/enterprise/#pricing)
*   [Deployment](https://opencode.ai/docs/enterprise/#deployment)
    *   [Central Config](https://opencode.ai/docs/enterprise/#central-config)
    *   [SSO integration](https://opencode.ai/docs/enterprise/#sso-integration)
    *   [Internal AI gateway](https://opencode.ai/docs/enterprise/#internal-ai-gateway)
    *   [Self-hosting](https://opencode.ai/docs/enterprise/#self-hosting)

*   [FAQ](https://opencode.ai/docs/enterprise/#faq)

On this page
------------

*   [Overview](https://opencode.ai/docs/enterprise/#_top)
*   [Trial](https://opencode.ai/docs/enterprise/#trial)
    *   [Data handling](https://opencode.ai/docs/enterprise/#data-handling)
    *   [Code ownership](https://opencode.ai/docs/enterprise/#code-ownership)

*   [Pricing](https://opencode.ai/docs/enterprise/#pricing)
*   [Deployment](https://opencode.ai/docs/enterprise/#deployment)
    *   [Central Config](https://opencode.ai/docs/enterprise/#central-config)
    *   [SSO integration](https://opencode.ai/docs/enterprise/#sso-integration)
    *   [Internal AI gateway](https://opencode.ai/docs/enterprise/#internal-ai-gateway)
    *   [Self-hosting](https://opencode.ai/docs/enterprise/#self-hosting)

*   [FAQ](https://opencode.ai/docs/enterprise/#faq)

Enterprise
==========

Using OpenCode securely in your organization.

OpenCode Enterprise is for organizations that want to ensure that their code and data never leaves their infrastructure. It can do this by using a centralized config that integrates with your SSO and internal AI gateway.

Note

OpenCode does not store any of your code or context data.

To get started with OpenCode Enterprise:

1.   Do a trial internally with your team.
2.   **[Contact us](mailto:contact@anoma.ly)** to discuss pricing and implementation options.

* * *

[Trial](https://opencode.ai/docs/enterprise/#trial)
---------------------------------------------------

OpenCode is open source and does not store any of your code or context data, so your developers can simply [get started](https://opencode.ai/docs/) and carry out a trial.

* * *

### [Data handling](https://opencode.ai/docs/enterprise/#data-handling)

**OpenCode does not store your code or context data.** All processing happens locally or through direct API calls to your AI provider.

This means that as long as you are using a provider you trust, or an internal AI gateway, you can use OpenCode securely.

The only caveat here is the optional `/share` feature.

* * *

#### [Sharing conversations](https://opencode.ai/docs/enterprise/#sharing-conversations)

If a user enables the `/share` feature, the conversation and the data associated with it are sent to the service we use to host these share pages at opencode.ai.

The data is currently served through our CDN’s edge network, and is cached on the edge near your users.

We recommend you disable this for your trial.

opencode.json

`{  "$schema": "https://opencode.ai/config.json",  "share": "disabled"}`

[Learn more about sharing](https://opencode.ai/docs/share).

* * *

### [Code ownership](https://opencode.ai/docs/enterprise/#code-ownership)

**You own all code produced by OpenCode.** There are no licensing restrictions or ownership claims.

* * *

[Pricing](https://opencode.ai/docs/enterprise/#pricing)
-------------------------------------------------------

We use a per-seat model for OpenCode Enterprise. If you have your own LLM gateway, we do not charge for tokens used. For further details about pricing and implementation options, **[contact us](mailto:contact@anoma.ly)**.

* * *

[Deployment](https://opencode.ai/docs/enterprise/#deployment)
-------------------------------------------------------------

Once you have completed your trial and you are ready to use OpenCode at your organization, you can **[contact us](mailto:contact@anoma.ly)** to discuss pricing and implementation options.

* * *

### [Central Config](https://opencode.ai/docs/enterprise/#central-config)

We can set up OpenCode to use a single central config for your entire organization.

This centralized config can integrate with your SSO provider and ensures all users access only your internal AI gateway.

* * *

### [SSO integration](https://opencode.ai/docs/enterprise/#sso-integration)

Through the central config, OpenCode can integrate with your organization’s SSO provider for authentication.

This allows OpenCode to obtain credentials for your internal AI gateway through your existing identity management system.

* * *

### [Internal AI gateway](https://opencode.ai/docs/enterprise/#internal-ai-gateway)

With the central config, OpenCode can also be configured to use only your internal AI gateway.

You can also disable all other AI providers, ensuring all requests go through your organization’s approved infrastructure.

* * *

### [Self-hosting](https://opencode.ai/docs/enterprise/#self-hosting)

While we recommend disabling the share pages to ensure your data never leaves your organization, we can also help you self-host them on your infrastructure.

This is currently on our roadmap. If you’re interested, **[let us know](mailto:contact@anoma.ly)**.

* * *

[FAQ](https://opencode.ai/docs/enterprise/#faq)
-----------------------------------------------

What is OpenCode Enterprise?
OpenCode Enterprise is for organizations that want to ensure that their code and data never leaves their infrastructure. It can do this by using a centralized config that integrates with your SSO and internal AI gateway.

How do I get started with OpenCode Enterprise?
Simply start with an internal trial with your team. OpenCode by default does not store your code or context data, making it easy to get started.

Then **[contact us](mailto:contact@anoma.ly)** to discuss pricing and implementation options.

How does enterprise pricing work?
We offer per-seat enterprise pricing. If you have your own LLM gateway, we do not charge for tokens used. For further details, **[contact us](mailto:contact@anoma.ly)** for a custom quote based on your organization’s needs.

Is my data secure with OpenCode Enterprise?
Yes. OpenCode does not store your code or context data. All processing happens locally or through direct API calls to your AI provider. With central config and SSO integration, your data remains secure within your organization’s infrastructure.

Can we use our own private NPM registry?
OpenCode supports private npm registries through Bun’s native `.npmrc` file support. If your organization uses a private registry, such as JFrog Artifactory, Nexus, or similar, ensure developers are authenticated before running OpenCode.

To set up authentication with your private registry:

Terminal window

`npm login --registry=https://your-company.jfrog.io/api/npm/npm-virtual/`

This creates `~/.npmrc` with authentication details. OpenCode will automatically pick this up.

Caution

You must be logged into the private registry before running OpenCode.

Alternatively, you can manually configure a `.npmrc` file:

~/.npmrc

`registry=https://your-company.jfrog.io/api/npm/npm-virtual///your-company.jfrog.io/api/npm/npm-virtual/:_authToken=${NPM_AUTH_TOKEN}`

Developers must be logged into the private registry before running OpenCode to ensure packages can be installed from your enterprise registry.

[Edit this page](https://github.com/anomalyco/opencode/edit/dev/packages/web/src/content/docs/enterprise.mdx)[Find a bug? Open an issue](https://github.com/anomalyco/opencode/issues/new)[Join our Discord community](https://opencode.ai/discord)

© [Anomaly](https://anoma.ly/)

Jan 31, 2026
