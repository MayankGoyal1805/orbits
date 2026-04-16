---
title: Orbits OpenEnv
sdk: docker
app_port: 7860
short_description: OpenEnv environment for space debris collision avoidance.
---

# Orbits OpenEnv

Orbits OpenEnv is a real-world OpenEnv environment for **space debris collision avoidance**. The agent plays the role of a satellite operator managing conjunction risk over a short planning horizon while preserving fuel, limiting mission-orbit deviation, and deciding when to request better tracking information.

## Environment Description

The environment exposes the standard interaction loop:

- `reset()` returns the first observation
- `step(action)` advances the simulator and returns observation, reward, done, and info
- `state()` returns the full current state for grading and inspection

The simulator uses a structured operational abstraction instead of high-fidelity orbital propagation:

- conjunction events have collision probability, miss distance, time-to-closest-approach, uncertainty, and maneuver geometry
- actions trade off safety, fuel, tracking budget, and mission offsets
- rewards provide partial progress signals across the full episode

## Action Space

Typed action model: [src/orbits_env/models.py](src/orbits_env/models.py)

- `noop`
- `request_tracking_update`
- `radial_maneuver`
- `along_track_maneuver`
- `normal_maneuver`

Actions include a bounded `magnitude` in `[0.0, 1.0]`.

## Observation Space

Observations include:

- `task_id`
- `step_index`
- `horizon_remaining`
- `fuel_remaining`
- `tracking_quality`
- `tracking_budget_remaining`
- `mission_offsets`
- `total_collision_probability`
- `highest_collision_probability`
- `visible_events`
- `last_action`
- `last_action_error`
- `done`

Each visible conjunction event includes:

- object identifier
- collision probability estimate
- miss distance
- time to closest approach
- uncertainty
- geometry tag
- maneuver effectiveness by axis

## Tasks

Three graded tasks are included:

- `collision_avoidance_easy`: one clear debris threat, strong initial tracking, generous fuel
- `collision_avoidance_medium`: two threats with different maneuver geometry and tighter resources
- `collision_avoidance_hard`: three competing threats with lower certainty and tighter offset limits

Task difficulty progresses from easy to hard, and each task is graded on a normalized `0.0–1.0` scale.

## Setup And Usage

Install dependencies:

```bash
uv sync
```

Run the reproducible heuristic baseline:

```bash
make baseline
```

Run the required submission inference script:

```bash
make inference
```

Build dataset-driven task priors from EDA artifacts:

```bash
make build-priors
```

Run iterative self-improvement inference (Option 1):

```bash
make iterative-inference
```

Required inference environment variables:

```bash
export API_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
export MODEL_NAME="gemini-2.5-flash"
export HF_TOKEN="<provider-api-key>"
```

`inference.py` now runs in strict LLM mode by default. If `HF_TOKEN` is missing (or API config is invalid), it raises an error.
Heuristic fallback is available only with explicit opt-in:

```bash
export ALLOW_HEURISTIC_FALLBACK=1
```

`LOCAL_IMAGE_NAME` is present in `inference.py` for checklist compatibility but is not used in the current local environment path.

`inference.py` optionally loads a local `.env` file for convenience, but production/submission environments with pre-set variables remain the primary source of truth.

Run tests:

```bash
make test
```

Start the local API server:

```bash
make serve
```

Build and run Docker locally:

```bash
make docker-build
make docker-run
```

## Baseline Scores

Reproducible heuristic baseline scores:

- easy: `0.8169`
- medium: `0.6588`
- hard: `0.5540`

These results are saved locally by:

```bash
make baseline-save
```

## Hugging Face Spaces

This repository is configured for a Docker-based Hugging Face Space through the YAML block at the top of this README. The container serves the environment on port `7860`.

## Repository Notes

- [openenv.yaml](openenv.yaml): environment metadata
- [Dockerfile](Dockerfile): container build
- [inference.py](inference.py): required OpenAI-client inference script
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md): deployment notes
- [docs/markd](docs/markd): learning notes
