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

echo "[2/4] Building Docker image"
docker build -t orbits-openenv-validate .

echo "[3/4] Running tests"
UV_CACHE_DIR=${UV_CACHE_DIR:-/tmp/orbits-uv-cache} uv run pytest -q

echo "[4/4] Running baseline and inference fallback"
UV_CACHE_DIR=${UV_CACHE_DIR:-/tmp/orbits-uv-cache} uv run python scripts/run_baseline.py --output outputs/evals/baseline_scores.json >/dev/null
UV_CACHE_DIR=${UV_CACHE_DIR:-/tmp/orbits-uv-cache} uv run python inference.py >/dev/null

echo "Validation passed."
