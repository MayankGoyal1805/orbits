.PHONY: sync build-priors baseline baseline-save inference iterative-inference test serve smoke docker-build docker-run validate

ifdef ITERABLE_ROUNDS
ITERATIVE_ROUNDS := $(ITERABLE_ROUNDS)
else
ITERATIVE_ROUNDS ?= 3
endif
ITERATIVE_JSON_OUTPUT ?= iterative_inference_results.json
ITERATIVE_TEXT_OUTPUT ?= output.txt

sync:
	uv sync

build-priors:
	uv run python scripts/build_task_priors.py

baseline:
	uv run python scripts/run_baseline.py

baseline-save:
	uv run python scripts/run_baseline.py --output outputs/evals/baseline_scores.json

inference:
	uv run python inference.py

iterative-inference:
	uv run python scripts/run_iterative_inference.py --rounds $(ITERATIVE_ROUNDS) --output $(ITERATIVE_JSON_OUTPUT) --text-output $(ITERATIVE_TEXT_OUTPUT)

test:
	uv run pytest

serve:
	uv run uvicorn server.app:app --host 0.0.0.0 --port 7860

smoke:
	uv run python scripts/smoke_test_api.py

docker-build:
	docker build -t orbits-openenv .

docker-run:
	docker run --rm -p 7860:7860 orbits-openenv

validate:
	bash scripts/validate-submission.sh http://localhost:7860 .
