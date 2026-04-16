# Quickstart

This guide focuses on practical setup and day-to-day commands.

## Prerequisites

- Python 3.11+
- `uv` installed
- Docker (optional, for container run)

## Why This Project Uses uv

`uv` is the environment and package manager used by this repository.

- It reads `pyproject.toml` dependencies.
- It creates and manages a virtual environment.
- It runs commands in that environment through `uv run ...`.
- It can be faster and more reproducible than ad-hoc `pip` workflows.

## Install Dependencies

```bash
uv sync
```

Equivalent Make target:

```bash
make sync
```

## Common Commands

Run baseline policy:

```bash
make baseline
```

Save baseline results to JSON:

```bash
make baseline-save
```

Run inference entrypoint:

```bash
make inference
```

Build task priors from processed EDA datasets:

```bash
make build-priors
```

Run iterative self-improvement inference rounds:

```bash
make iterative-inference
```

Run tests:

```bash
make test
```

Run local API server:

```bash
make serve
```

Run smoke test against direct Python API functions:

```bash
make smoke
```

Build and run Docker container:

```bash
make docker-build
make docker-run
```

Submission-style validation:

```bash
make validate
```

## Inference Credentials

`inference.py` reads:

- `API_BASE_URL` (default Google GenAI OpenAI-compatible endpoint)
- `MODEL_NAME`
- `HF_TOKEN`

When `HF_TOKEN` is missing, inference automatically falls back to deterministic heuristic behavior (`orbits_env.baseline.choose_action`). This is useful for local debugging without external API calls.
