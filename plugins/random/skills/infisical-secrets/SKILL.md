---
name: infisical-secrets
description: Manage secrets with Infisical using CLI and REST API for fully automated workflows without web UI
version: 1.0.0
author: gtd-cc

# Skill metadata
domain: security
category: secrets-management
tags: [infisical, secrets, api, cli, automation, devops, nixos]

# Skill classification
type: domain-expertise
complexity: intermediate
scope: comprehensive

# Usage information
prerequisites:
  - "Infisical account (cloud at app.infisical.com or self-hosted)"
  - "infisical CLI installed"
  - "curl and jq for API operations"

provides:
  - "Project creation via API (no web UI needed)"
  - "Secrets import from .env files"
  - "Machine identity creation and configuration"
  - "Universal Auth setup for server authentication"
  - "Runtime secret fetching for containers"

# Integration notes
compatible_tools:
  - infisical (CLI)
  - curl
  - jq
  - NixOS/systemd
  - podman/docker
---

# Infisical secrets management skill

Manage secrets programmatically using Infisical's CLI and REST API. This skill enables fully automated secrets management workflows without requiring web UI interaction.

## Why Infisical

Infisical provides centralized secrets management with:
- Web UI for easy viewing and editing
- CLI for local development
- REST API for automation
- Machine identities for server authentication
- Audit logs and versioning
- Multiple environments (dev, staging, prod)

## Authentication overview

Infisical has two authentication modes:

| Mode | Use Case | Token Type |
|------|----------|------------|
| User login | Local development, API automation | JWT from browser OAuth |
| Machine identity | Servers, CI/CD, containers | Client ID + Secret |

The user JWT (from `infisical login`) can be used for API calls to create projects, identities, and manage secrets. Machine identities are for runtime secret fetching.

## Quick start: CLI login

```bash
# Interactive browser-based login
infisical login

# Get your JWT token (for API calls)
infisical user get token
# Output: Token: eyJhbGciOiJIUzI1NiIs...
```

## API authentication

After `infisical login`, extract your JWT for API calls:

```bash
# Get token programmatically
TOKEN=$(infisical user get token --silent 2>/dev/null | grep "Token:" | cut -d' ' -f2)

# Use in API calls
curl -H "Authorization: Bearer $TOKEN" "https://app.infisical.com/api/..."
```

The JWT contains your `organizationId` which is needed for project creation.

## Creating projects via API

```bash
TOKEN=$(infisical user get token --silent 2>/dev/null | grep "Token:" | cut -d' ' -f2)
ORG_ID="your-org-id-from-jwt"  # Decode JWT to find this

curl -s -X POST "https://app.infisical.com/api/v2/workspace" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"projectName\": \"my-project\",
    \"organizationId\": \"$ORG_ID\"
  }" | jq '.'
```

Response includes project ID and auto-created environments (dev, staging, prod).

## Linking local directory to project

After creating a project, link your local directory:

```bash
# Create .infisical.json in your project directory
cat > .infisical.json << EOF
{
  "workspaceId": "PROJECT_ID_HERE",
  "defaultEnvironment": "prod",
  "gitBranchToEnvironmentMapping": null
}
EOF
```

## Importing secrets from .env

```bash
# Import all secrets from .env file
infisical secrets set --file .env --env prod

# Or set individual secrets
infisical secrets set "API_KEY=secret-value" --env prod
```

## Creating machine identities

Machine identities allow servers and containers to authenticate with Infisical.

### Step 1: Create the identity

```bash
TOKEN=$(infisical user get token --silent 2>/dev/null | grep "Token:" | cut -d' ' -f2)
ORG_ID="your-org-id"

curl -s -X POST "https://app.infisical.com/api/v1/identities" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"my-server-identity\",
    \"organizationId\": \"$ORG_ID\",
    \"role\": \"member\"
  }" | jq '.'
```

### Step 2: Attach Universal Auth

```bash
IDENTITY_ID="identity-id-from-step-1"

curl -s -X POST "https://app.infisical.com/api/v1/auth/universal-auth/identities/$IDENTITY_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"accessTokenTTL\": 7200,
    \"accessTokenMaxTTL\": 86400,
    \"accessTokenNumUsesLimit\": 0
  }" | jq '.'
```

Response includes the `clientId`.

### Step 3: Create client secret

```bash
curl -s -X POST "https://app.infisical.com/api/v1/auth/universal-auth/identities/$IDENTITY_ID/client-secrets" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"description\": \"production server\",
    \"ttl\": 0,
    \"numUsesLimit\": 0
  }" | jq '.'
```

Save the `clientSecret` from the response (shown only once).

### Step 4: Add identity to project

```bash
PROJECT_ID="your-project-id"

curl -s -X POST "https://app.infisical.com/api/v2/workspace/$PROJECT_ID/identity-memberships/$IDENTITY_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"role\": \"viewer\"}" | jq '.'
```

## Fetching secrets at runtime

### Using machine identity credentials

```bash
CLIENT_ID="your-client-id"
CLIENT_SECRET="your-client-secret"
PROJECT_ID="your-project-id"

# Step 1: Get access token
ACCESS_TOKEN=$(curl -sf -X POST "https://app.infisical.com/api/v1/auth/universal-auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"clientId\": \"$CLIENT_ID\", \"clientSecret\": \"$CLIENT_SECRET\"}" | jq -r '.accessToken')

# Step 2: Fetch secrets
curl -sf "https://app.infisical.com/api/v3/secrets/raw?workspaceId=$PROJECT_ID&environment=prod" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'
```

### Generate .env file from secrets

```bash
curl -sf "https://app.infisical.com/api/v3/secrets/raw?workspaceId=$PROJECT_ID&environment=prod" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  | jq -r '.secrets[] | "\(.secretKey)=\(.secretValue)"' \
  > /path/to/env/file
```

## NixOS integration pattern

Use SOPS for bootstrap credentials (just 2 values), Infisical for all application secrets:

```nix
{ config, pkgs, ... }:
{
  # Fetch secrets from Infisical before starting container
  systemd.services."myapp-fetch-secrets" = {
    description = "Fetch secrets from Infisical";
    wantedBy = [ "podman-myapp.service" ];
    before = [ "podman-myapp.service" ];
    serviceConfig = {
      Type = "oneshot";
      RemainAfterExit = true;
    };
    path = [ pkgs.curl pkgs.jq ];
    script = ''
      set -euo pipefail

      # Read Infisical credentials from SOPS
      CLIENT_ID=$(cat ${config.sops.secrets."infisical/client-id".path})
      CLIENT_SECRET=$(cat ${config.sops.secrets."infisical/client-secret".path})

      # Get access token
      ACCESS_TOKEN=$(curl -sf -X POST "https://app.infisical.com/api/v1/auth/universal-auth/login" \
        -H "Content-Type: application/json" \
        -d "{\"clientId\": \"$CLIENT_ID\", \"clientSecret\": \"$CLIENT_SECRET\"}" | jq -r '.accessToken')

      # Fetch secrets and write to env file
      curl -sf "https://app.infisical.com/api/v3/secrets/raw?workspaceId=PROJECT_ID&environment=prod" \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        | jq -r '.secrets[] | "\(.secretKey)=\(.secretValue)"' \
        > /var/lib/myapp/env

      chmod 0400 /var/lib/myapp/env
    '';
  };

  # Container uses the fetched env file
  virtualisation.oci-containers.containers."myapp" = {
    image = "myapp:latest";
    environmentFiles = [ "/var/lib/myapp/env" ];
  };

  # SOPS stores only Infisical credentials
  sops.secrets."infisical/client-id".sopsFile = ./secrets.yaml;
  sops.secrets."infisical/client-secret".sopsFile = ./secrets.yaml;
}
```

## Complete automation script

```bash
#!/usr/bin/env bash
# Create Infisical project and import secrets - fully automated

set -euo pipefail

PROJECT_NAME="${1:-my-project}"
ENV_FILE="${2:-.env}"

# Get user token and org ID
TOKEN=$(infisical user get token --silent 2>/dev/null | grep "Token:" | cut -d' ' -f2)
# Decode JWT to get org ID (middle part, base64 decoded)
ORG_ID=$(echo "$TOKEN" | cut -d'.' -f2 | base64 -d 2>/dev/null | jq -r '.organizationId')

echo "Creating project: $PROJECT_NAME"

# Create project
PROJECT=$(curl -sf -X POST "https://app.infisical.com/api/v2/workspace" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"projectName\": \"$PROJECT_NAME\", \"organizationId\": \"$ORG_ID\"}")

PROJECT_ID=$(echo "$PROJECT" | jq -r '.project.id')
echo "Project ID: $PROJECT_ID"

# Link local directory
cat > .infisical.json << EOF
{"workspaceId": "$PROJECT_ID", "defaultEnvironment": "prod"}
EOF

# Import secrets
echo "Importing secrets from $ENV_FILE"
infisical secrets set --file "$ENV_FILE" --env prod

# Create machine identity
echo "Creating machine identity"
IDENTITY=$(curl -sf -X POST "https://app.infisical.com/api/v1/identities" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"$PROJECT_NAME-server\", \"organizationId\": \"$ORG_ID\", \"role\": \"member\"}")

IDENTITY_ID=$(echo "$IDENTITY" | jq -r '.identity.id')

# Attach Universal Auth
AUTH=$(curl -sf -X POST "https://app.infisical.com/api/v1/auth/universal-auth/identities/$IDENTITY_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"accessTokenTTL": 7200, "accessTokenMaxTTL": 86400}')

CLIENT_ID=$(echo "$AUTH" | jq -r '.identityUniversalAuth.clientId')

# Create client secret
SECRET=$(curl -sf -X POST "https://app.infisical.com/api/v1/auth/universal-auth/identities/$IDENTITY_ID/client-secrets" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"description": "automated setup", "ttl": 0}')

CLIENT_SECRET=$(echo "$SECRET" | jq -r '.clientSecret')

# Add identity to project
curl -sf -X POST "https://app.infisical.com/api/v2/workspace/$PROJECT_ID/identity-memberships/$IDENTITY_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"role": "viewer"}' > /dev/null

echo ""
echo "Setup complete!"
echo "Client ID: $CLIENT_ID"
echo "Client Secret: $CLIENT_SECRET"
echo ""
echo "Add these to your SOPS secrets file for server authentication."
```

## API reference

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Create project | POST | `/api/v2/workspace` |
| List secrets | GET | `/api/v3/secrets/raw?workspaceId=ID&environment=ENV` |
| Set secrets | POST | `/api/v3/secrets/raw/SECRET_NAME` |
| Create identity | POST | `/api/v1/identities` |
| Attach Universal Auth | POST | `/api/v1/auth/universal-auth/identities/{id}` |
| Create client secret | POST | `/api/v1/auth/universal-auth/identities/{id}/client-secrets` |
| Add to project | POST | `/api/v2/workspace/{id}/identity-memberships/{identityId}` |
| Login (machine) | POST | `/api/v1/auth/universal-auth/login` |

## Comparison with alternatives

| Feature | Infisical | Doppler | SOPS |
|---------|-----------|---------|------|
| Self-hosted | Yes (open source) | No | N/A (file-based) |
| Web UI | Yes | Yes | No |
| CLI project creation | Via API | Yes (`doppler projects create`) | N/A |
| .env import | Yes | Yes | Manual |
| Runtime injection | Via API | `doppler run` | File read |
| Audit logs | Yes | Yes | Git history |
| Free tier | Generous | Limited | Free |

## Troubleshooting

### Token error: "malformed token"
The user JWT from `infisical user get token` is valid for API calls. Make sure you're using the full token including "eyJ..." prefix.

### Identity not found
Ensure the identity has Universal Auth attached and a client secret created. The identity also needs to be added to the project with appropriate role.

### Secrets not fetching
Check that:
1. Access token is valid (not expired)
2. Identity has `viewer` or higher role on the project
3. Correct `workspaceId` and `environment` in the request

## References

- [Infisical Documentation](https://infisical.com/docs)
- [Universal Auth](https://infisical.com/docs/documentation/platform/identities/universal-auth)
- [Machine Identities](https://infisical.com/docs/documentation/platform/identities/machine-identities)
- [API Reference](https://infisical.com/docs/api-reference)
