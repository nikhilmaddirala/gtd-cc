#!/usr/bin/env bash
set -euo pipefail

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || true)
if [ -z "$ROOT" ]; then
  echo "Not in a git repository"
  exit 1
fi

cd "$ROOT"

if ! git subrepo version >/dev/null 2>&1; then
  echo "git-subrepo is not installed or not enabled in PATH"
  exit 1
fi

echo ""
echo "SUBREPO STATUS"
echo ""

# Use git-subrepo's native status with --fetch to show remote divergence
git subrepo status --all --fetch
