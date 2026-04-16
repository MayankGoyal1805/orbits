# File-By-File Reference

This section explains every non-`.git` file currently in the repository.

## Repository Root

`README.md`
- Project overview, setup commands, action/observation summary, baseline scores, and deployment notes.

`pyproject.toml`
- Python package metadata, runtime dependencies, dev dependencies, build backend, and tool config (`uv`, `pytest`, `ruff`).

`openenv.yaml`
- OpenEnv benchmark metadata: environment class/models, tasks, and API endpoint mapping.

`Makefile`
- Primary developer command entrypoints (`sync`, `baseline`, `inference`, `test`, `serve`, `docker-*`, `validate`).

`Dockerfile`
- Container image definition for running API on port `7860`.

`inference.py`
- Required inference runner using OpenAI-compatible API with fallback heuristic policy and strict logging output.

`.gitignore`
- Git exclusions for virtual envs, caches, local outputs, and local env files.

`.dockerignore`
- Docker build-context exclusions for speed and smaller image transfer.

## Server Package

`server/app.py`
- FastAPI application and all REST endpoints for reset/step/state/grade lifecycle.

`server/__init__.py`
- Empty package marker file.

## Environment Package (`src/orbits_env`)

`src/orbits_env/__init__.py`
- Public package exports for environment and model classes.

`src/orbits_env/models.py`
- All pydantic schemas and enums for actions, observations, state, conjunction events, and task configuration.

`src/orbits_env/env.py`
- Thin facade around simulator with methods: `reset`, `step`, `state`, `close`, `available_tasks`, `grade`.

`src/orbits_env/simulator.py`
- Core transition engine: observation synthesis, action effects, passive dynamics, reward shaping, and termination logic.

`src/orbits_env/baseline.py`
- Deterministic heuristic agent used for baseline scoring and inference fallback.

`src/orbits_env/graders/scoring.py`
- Final episode scoring function combining safety, fuel efficiency, mission preservation, tracking efficiency, and completion status.

`src/orbits_env/tasks/catalog.py`
- Built-in tasks (`easy`, `medium`, `hard`) and `get_task` helper.
- Also loads optional dataset-driven task overrides from `task_priors.json`.

`src/orbits_env/tasks/task_priors.json`
- Auto-generated, dataset-driven task override values derived from EDA processed outputs.

## Scripts

`scripts/run_baseline.py`
- Runs baseline policy over all tasks and optionally writes JSON output.

`scripts/smoke_test_api.py`
- Lightweight API sanity script by calling handlers directly.

`scripts/validate-submission.sh`
- End-to-end local validation: health ping, Docker build, tests, baseline run, inference run.

`scripts/build_task_priors.py`
- Reads processed EDA datasets and writes data-informed task priors JSON used by task catalog.

`scripts/run_iterative_inference.py`
- Runs Option 1 iterative self-improvement inference rounds with strategy-memory feedback.

## Tests

`tests/test_api.py`
- API lifecycle tests for reset/step/state/grade and task metadata.

`tests/test_env.py`
- Environment behavior tests for initialization, stepping, and rollout completion.

`tests/test_inference.py`
- Contract test for inference logging format.

`tests/test_task_priors.py`
- Verifies that priors JSON task overrides are applied correctly by catalog loader.

## Docs

`docs/README.md`
- Index and recommended reading order for docs.

`docs/00-learning-path.md`
- Guided learning order and system mental model.

`docs/01-quickstart.md`
- Setup instructions and practical local commands.

`docs/02-openenv-and-config.md`
- Explanation of `openenv.yaml`, `pyproject.toml`, Makefile, and ignore files.

`docs/03-architecture.md`
- Layered architecture and runtime flow.

`docs/04-environment-dynamics.md`
- Simulator internals: observation model, action effects, reward, termination.

`docs/05-api-and-inference.md`
- Endpoint behavior and inference/fallback mechanics.

`docs/06-tests-and-validation.md`
- Test suite and validation script explanation.

`docs/07-docker-and-deployment.md`
- Docker build/run/deploy explanation.

`docs/12-dataset-priors-and-iterative-option1.md`
- Detailed explanation of dataset-prior generation and iterative Option 1 implementation.
