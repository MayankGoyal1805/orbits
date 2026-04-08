UV_CACHE_DIR ?= /tmp/orbits-uv-cache

.PHONY: sync baseline baseline-save inference test serve smoke docker-build docker-run validate

sync:
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv sync

baseline:
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run python scripts/run_baseline.py

baseline-save:
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run python scripts/run_baseline.py --output outputs/evals/baseline_scores.json

inference:
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run python inference.py

test:
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run pytest

serve:
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run uvicorn server.app:app --host 0.0.0.0 --port 7860

smoke:
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run python scripts/smoke_test_api.py

docker-build:
	docker build -t orbits-openenv .

docker-run:
	docker run --rm -p 7860:7860 orbits-openenv

validate:
	bash scripts/validate-submission.sh http://localhost:7860 .
