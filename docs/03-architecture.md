# Architecture

This section explains how data and control flow through the system.

## High-Level Layers

1. Domain models (`src/orbits_env/models.py`)
2. Task definitions (`src/orbits_env/tasks/catalog.py`)
3. Simulator and transition function (`src/orbits_env/simulator.py`)
4. Environment facade (`src/orbits_env/env.py`)
5. Grading (`src/orbits_env/graders/scoring.py`)
6. API serving (`server/app.py`)
7. Agent runners (`src/orbits_env/baseline.py`, `inference.py`)

## Main Runtime Loop

The runtime loop is standard environment interaction:

1. `reset()` initializes state and returns first observation.
2. Agent chooses `EnvironmentAction`.
3. `step(action)` mutates hidden state and returns `StepResult`.
4. Repeat until `done`.
5. `grade()` computes normalized episode score.

## Separation Of Concerns

- `models.py` only defines typed schema and constraints.
- `catalog.py` only defines task parameters and conjunction seeds.
- `simulator.py` does all state transitions, rewards, and termination checks.
- `env.py` keeps public API minimal and stable.
- `server/app.py` wraps environment methods in HTTP routes.
- `scoring.py` keeps final evaluation independent from reward shaping.

This split is useful for experimentation because each concern can evolve without rewriting everything else.

## Determinism And Episode Identity

- Environment constructor accepts `seed` and `task_id`.
- Episode IDs are generated from `task_id` plus UUID suffix.
- Task definitions are copied deeply (`model_copy(deep=True)`) to avoid accidental global mutation.
