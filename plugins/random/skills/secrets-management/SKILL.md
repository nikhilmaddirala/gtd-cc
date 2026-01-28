---
name: secrets-management
description: Manage secrets with 1Password CLI, Infisical, and other tools for development and automation workflows
version: 2.0.0
author: gtd-cc

# Skill metadata
domain: security
category: secrets-management
tags: [1password, infisical, secrets, cli, automation, devops, op]

# Skill classification
type: domain-expertise
complexity: intermediate
scope: comprehensive

# Usage information
prerequisites:
  - "1Password CLI (op) or Infisical CLI installed"
  - "Account with respective secrets provider"
  - "curl and jq for API operations (Infisical)"

provides:
  - "Secret retrieval with op read"
  - "Environment injection with op run"
  - "Config file templating with op inject"
  - "Infisical project creation and automation"
  - "Machine identity setup for CI/CD"
  - "Runtime secret fetching for containers"

# Integration notes
compatible_tools:
  - op (1Password CLI)
  - infisical (CLI)
  - curl
  - jq
  - NixOS/systemd
  - podman/docker
---

# Secrets management skill

Manage secrets programmatically using 1Password CLI or Infisical. This skill covers CLI-based secrets management for development, scripting, and automation workflows.

## Quick comparison

| Feature | 1Password CLI | Infisical |
|---------|---------------|-----------|
| Best for | Personal/team secrets, existing 1Password users | Project-based secrets, self-hosted option |
| Auth | Biometric, service accounts | JWT, machine identities |
| Secret refs | `op://vault/item/field` | API-based |
| Env injection | `op run` | API fetch + export |
| Config templating | `op inject` | Manual |
| Self-hosted | No (Connect Server) | Yes (open source) |


## 1Password CLI

### Installation

```bash
# macOS
brew install 1password-cli

# NixOS
nix-shell -p _1password

# Linux (manual)
curl -sS https://downloads.1password.com/linux/keys/1password.asc | gpg --dearmor -o /usr/share/keyrings/1password-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/1password-archive-keyring.gpg] https://downloads.1password.com/linux/debian/amd64 stable main" | sudo tee /etc/apt/sources.list.d/1password.list
sudo apt update && sudo apt install 1password-cli
```

### Authentication

```bash
# Interactive sign-in (opens browser or prompts for credentials)
op signin

# Check current session
op account list

# Sign out
op signout
```

### Secret reference syntax

1Password uses URI-style references to identify secrets:

```
op://vault/item/field
op://vault/item/section/field
```

Examples:
- `op://Private/GitHub Token/credential` - field named "credential" in item "GitHub Token"
- `op://Development/Database/prod/password` - field in section "prod"
- `op://Shared/AWS/Access Key ID` - spaces are supported (quote the reference)

### op read - retrieve single secrets

Read a specific field value from 1Password:

```bash
# Basic read
op read "op://Private/GitHub Token/credential"

# Read password field (common pattern)
op read "op://vault/item/password"

# Read with query parameters
op read "op://vault/item/one-time password?attribute=otp"  # Get TOTP code

# Save SSH key to file
op read "op://Private/SSH Key/private key" > ~/.ssh/id_rsa

# Use in scripts
export API_KEY=$(op read "op://Development/API Keys/production")
```

### op run - inject into environment

Run a command with secrets injected into environment variables:

```bash
# Define env vars with secret references, then run command
export DATABASE_URL="op://Production/Database/connection-string"
op run -- ./my-script.sh

# Use .env file with secret references
# .env.tpl:
# DATABASE_URL=op://Production/Database/url
# API_KEY=op://Production/API/key
op run --env-file=.env.tpl -- docker-compose up

# Show values (for debugging only!)
op run --no-masking -- printenv DATABASE_URL
```

### op inject - template config files

Replace secret references in files with actual values:

```bash
# Inject from stdin to stdout
cat config.tpl | op inject

# Inject from file to file
op inject --in-file config.tpl --out-file config.json

# Example template (config.tpl):
# {
#   "database": {
#     "host": "db.example.com",
#     "password": "op://Production/Database/password"
#   },
#   "api_key": "op://Production/API/key"
# }
```

### op item - manage items

```bash
# List items in a vault
op item list --vault=Private

# Get full item details
op item get "GitHub Token" --vault=Private

# Get specific fields
op item get "Database" --fields label=password,label=username

# Create new item
op item create --category=login \
  --title="New Service" \
  --vault=Private \
  username=admin \
  password=secret123

# Edit existing item
op item edit "Database" password=newsecret --vault=Production
```

### Service accounts for automation

For CI/CD and servers, use service accounts instead of user authentication:

```bash
# Set service account token (from 1Password dashboard)
export OP_SERVICE_ACCOUNT_TOKEN="ops_..."

# Now op commands work without interactive auth
op read "op://vault/item/field"
```

Service accounts:
- Created in 1Password web dashboard
- Scoped to specific vaults (principle of least privilege)
- No biometric/interactive auth required
- Token stored as single environment variable

### Common patterns

**Load database credentials:**
```bash
export DB_HOST=$(op read "op://Production/Database/host")
export DB_USER=$(op read "op://Production/Database/username")
export DB_PASS=$(op read "op://Production/Database/password")
psql -h "$DB_HOST" -U "$DB_USER" -W
```

**Docker with secrets:**
```bash
# docker-compose.yml uses env vars
op run --env-file=.env.secrets -- docker-compose up -d
```

**SSH with 1Password agent:**
```bash
# 1Password can act as SSH agent
# Enable in 1Password app settings, then:
export SSH_AUTH_SOCK=~/Library/Group\ Containers/2BUA8C4S2C.com.1password/t/agent.sock
ssh user@server
```

**Generate .env file:**
```bash
# .env.tpl with secret refs
cat > .env.tpl << 'EOF'
API_KEY=op://Production/API/key
DATABASE_URL=op://Production/Database/url
SECRET_KEY=op://Production/App/secret
EOF

# Generate actual .env
op inject --in-file .env.tpl --out-file .env
```


## Infisical

### Why Infisical

Infisical provides centralized secrets management with:
- Web UI for easy viewing and editing
- CLI for local development
- REST API for automation
- Machine identities for server authentication
- Audit logs and versioning
- Multiple environments (dev, staging, prod)
- Self-hosted option (open source)

### Authentication overview

| Mode | Use Case | Token Type |
|------|----------|------------|
| User login | Local development, API automation | JWT from browser OAuth |
| Machine identity | Servers, CI/CD, containers | Client ID + Secret |

### Quick start: CLI login

```bash
# Interactive browser-based login
infisical login

# Get your JWT token (for API calls)
infisical user get token
# Output: Token: eyJhbGciOiJIUzI1NiIs...
```

### API authentication

After `infisical login`, extract your JWT for API calls:

```bash
# Get token programmatically
TOKEN=$(infisical user get token --silent 2>/dev/null | grep "Token:" | cut -d' ' -f2)

# Use in API calls
curl -H "Authorization: Bearer $TOKEN" "https://app.infisical.com/api/..."
```

### Creating projects via API

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

### Linking local directory to project

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

### Importing secrets from .env

```bash
# Import all secrets from .env file
infisical secrets set --file .env --env prod

# Or set individual secrets
infisical secrets set "API_KEY=secret-value" --env prod
```

### Creating machine identities

Machine identities allow servers and containers to authenticate with Infisical.

**Step 1: Create the identity**

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

**Step 2: Attach Universal Auth**

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

**Step 3: Create client secret**

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

**Step 4: Add identity to project**

```bash
PROJECT_ID="your-project-id"

curl -s -X POST "https://app.infisical.com/api/v2/workspace/$PROJECT_ID/identity-memberships/$IDENTITY_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"role\": \"viewer\"}" | jq '.'
```

### Fetching secrets at runtime

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

# Generate .env file
curl -sf "https://app.infisical.com/api/v3/secrets/raw?workspaceId=$PROJECT_ID&environment=prod" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  | jq -r '.secrets[] | "\(.secretKey)=\(.secretValue)"' \
  > /path/to/env/file
```

### Infisical API reference

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


## NixOS integration

### 1Password with systemd

```nix
{ config, pkgs, ... }:
{
  # Install 1Password CLI
  environment.systemPackages = [ pkgs._1password ];

  # Service that uses 1Password secrets
  systemd.services."myapp" = {
    serviceConfig = {
      # Service account token from SOPS
      EnvironmentFile = config.sops.secrets."1password-token".path;
    };
    script = ''
      export DB_PASS=$(${pkgs._1password}/bin/op read "op://Production/Database/password")
      exec /path/to/myapp
    '';
  };

  sops.secrets."1password-token" = {
    sopsFile = ./secrets.yaml;
    # Contains: OP_SERVICE_ACCOUNT_TOKEN=ops_...
  };
}
```

### Infisical with systemd

```nix
{ config, pkgs, ... }:
{
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
      CLIENT_ID=$(cat ${config.sops.secrets."infisical/client-id".path})
      CLIENT_SECRET=$(cat ${config.sops.secrets."infisical/client-secret".path})

      ACCESS_TOKEN=$(curl -sf -X POST "https://app.infisical.com/api/v1/auth/universal-auth/login" \
        -H "Content-Type: application/json" \
        -d "{\"clientId\": \"$CLIENT_ID\", \"clientSecret\": \"$CLIENT_SECRET\"}" | jq -r '.accessToken')

      curl -sf "https://app.infisical.com/api/v3/secrets/raw?workspaceId=PROJECT_ID&environment=prod" \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        | jq -r '.secrets[] | "\(.secretKey)=\(.secretValue)"' \
        > /var/lib/myapp/env

      chmod 0400 /var/lib/myapp/env
    '';
  };

  virtualisation.oci-containers.containers."myapp" = {
    image = "myapp:latest";
    environmentFiles = [ "/var/lib/myapp/env" ];
  };
}
```


## Troubleshooting

### 1Password CLI

**"You are not signed in"**
Run `op signin` to authenticate. For service accounts, ensure `OP_SERVICE_ACCOUNT_TOKEN` is set.

**"Item not found"**
Check vault name and item title are correct. Use `op item list --vault=VaultName` to verify.

**"No session found"**
Session expired. Re-run `op signin` or use service account for automation.

### Infisical

**Token error: "malformed token"**
Ensure you're using the full JWT including "eyJ..." prefix from `infisical user get token`.

**Identity not found**
Ensure the identity has Universal Auth attached and a client secret created. The identity also needs to be added to the project.

**Secrets not fetching**
Check: access token is valid, identity has `viewer` role, correct `workspaceId` and `environment`.


## References

### 1Password
- [1Password CLI Documentation](https://developer.1password.com/docs/cli/)
- [Secret References](https://developer.1password.com/docs/cli/secret-references/)
- [op read Command](https://developer.1password.com/docs/cli/reference/commands/read/)
- [Service Accounts](https://developer.1password.com/docs/service-accounts/)

### Infisical
- [Infisical Documentation](https://infisical.com/docs)
- [Universal Auth](https://infisical.com/docs/documentation/platform/identities/universal-auth)
- [Machine Identities](https://infisical.com/docs/documentation/platform/identities/machine-identities)
- [API Reference](https://infisical.com/docs/api-reference)
