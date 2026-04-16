#!/usr/bin/env bash
set -euo pipefail

PING_URL="${1:-}"
REPO_DIR="${2:-.}"

if [ -z "$PING_URL" ]; then
  echo "Usage: $0 <ping_url> [repo_dir]"
  exit 1
fi

cd "$REPO_DIR"

echo "[1/4] Checking Space health endpoint"
curl -fsSL "${PING_URL%/}/health" >/dev/null

echo "[2/4] Building Docker image (if Docker daemon is accessible)"
if docker info >/dev/null 2>&1; then
  docker build -t orbits-openenv-validate .
else
  echo "Skipping Docker build: Docker daemon is not accessible for the current user."
fi

echo "[3/4] Running tests"
uv run pytest -q

echo "[4/4] Running baseline and inference fallback"
uv run python scripts/run_baseline.py >/dev/null
uv run python inference.py >/dev/null

echo "Validation passed."
