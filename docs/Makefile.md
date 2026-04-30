# Understanding the `Makefile`

Welcome to the documentation for the `Makefile`. 

## What is a Makefile?
A `Makefile` is used by the `make` utility to automate running repetitive shell commands. Think of it as a table of contents for scripts. Instead of typing long commands like `uv run python scripts/run_iterative_inference.py --rounds 3`, a developer can simply type `make iterative-inference`.

---

## File Breakdown

### 1. Phony Targets
```makefile
.PHONY: sync build-priors baseline baseline-save inference iterative-inference test serve smoke docker-build docker-run validate
```
- Normally, Make expects a "target" to represent a physical file it needs to build.
- `.PHONY` tells Make: "These names are just command shortcuts, don't look for files named 'sync' or 'test' on the hard drive."

### 2. Variables and Conditionals
```makefile
ifdef ITERABLE_ROUNDS
ITERATIVE_ROUNDS := $(ITERABLE_ROUNDS)
else
ITERATIVE_ROUNDS ?= 3
endif
ITERATIVE_JSON_OUTPUT ?= iterative_inference_results.json
ITERATIVE_TEXT_OUTPUT ?= output.txt
```
- `ifdef / else / endif`: A conditional block. It checks if the environment variable `ITERABLE_ROUNDS` was passed in.
- `?=`: Conditional assignment. It assigns the value (e.g., `3`) ONLY if the variable (`ITERATIVE_ROUNDS`) isn't already set. This makes it easy for a user to override these variables in the terminal (e.g., `make iterative-inference ITERATIVE_ROUNDS=10`).

### 3. Setup and Environment
```makefile
sync:
	uv sync
```
- **Target `sync`:** Runs `uv sync`. `uv` is a modern, fast Python package manager. This command synchronizes the virtual environment, ensuring all dependencies listed in `pyproject.toml` are installed exactly as required.

### 4. Running Scripts
```makefile
build-priors:
	uv run python scripts/build_task_priors.py

baseline:
	uv run python scripts/run_baseline.py

baseline-save:
	uv run python scripts/run_baseline.py --output outputs/evals/baseline_scores.json
```
- These targets run various Python scripts located in the `scripts/` folder using `uv run` (which ensures the script runs inside the project's specific virtual environment).
- `baseline` runs hardcoded heuristics to test the environment without AI.

### 5. Running AI Inference
```makefile
inference:
	uv run python inference.py

iterative-inference:
	@echo "[MAKE-CONFIG] ITERATIVE_ROUNDS=$(ITERATIVE_ROUNDS) MODEL_NAME=$${MODEL_NAME:-<unset>} MAX_STEPS=$${MAX_STEPS:-<unset>}"
	uv run python scripts/run_iterative_inference.py --rounds $(ITERATIVE_ROUNDS) --output $(ITERATIVE_JSON_OUTPUT) --text-output $(ITERATIVE_TEXT_OUTPUT)
```
- `inference`: Executes the basic agent loop we explored in `inference.py`.
- `iterative-inference`: 
  - The `@echo` command prints configuration details to the terminal for debugging purposes. The `@` symbol hides the actual `echo` command itself from being printed.
  - It runs an iterative loop passing our Make variables (like `$(ITERATIVE_ROUNDS)`) dynamically into the python script as arguments.

### 6. Development and Testing
```makefile
test:
	uv run pytest

serve:
	uv run uvicorn server.app:app --host 0.0.0.0 --port 7860

smoke:
	uv run python scripts/smoke_test_api.py
```
- `test`: Triggers `pytest` to run all unit tests in the project.
- `serve`: Boots up the local API server using `uvicorn`, mimicking what the Docker container does.
- `smoke`: Runs a "smoke test". A smoke test is a quick, superficial test to make sure the core API endpoints respond and haven't catastrophically broken.

### 7. Docker and Validation
```makefile
docker-build:
	docker build -t orbits-openenv .

docker-run:
	docker run --rm -p 7860:7860 orbits-openenv

validate:
	bash scripts/validate-submission.sh http://localhost:7860 .
```
- `docker-build`: Tells Docker to build an image named `orbits-openenv` using the `Dockerfile` in the current directory (`.`).
- `docker-run`: Runs the container, linking port `7860` on your machine to port `7860` inside the container. `--rm` ensures the container deletes itself when you stop it, keeping your system clean.
- `validate`: Runs a bash script, likely used to evaluate or grade a submission based on the local running server.