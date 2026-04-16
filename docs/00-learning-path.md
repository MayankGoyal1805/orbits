# Learning Path

This project is a custom OpenEnv benchmark called `orbits-openenv` for satellite conjunction management.

The central idea: an agent observes conjunction risk and picks one action per step to reduce collision probability while preserving fuel and mission orbit quality.

## What You Are Looking At

- A Python package under `src/orbits_env` implementing environment models, tasks, simulator dynamics, and grading.
- A FastAPI server under `server` exposing OpenEnv-compatible endpoints.
- Local scripts under `scripts` for baseline evaluation, smoke checks, and submission validation.
- A required inference entry script in `inference.py` using an OpenAI-compatible client and fallback heuristic behavior.

## Recommended Study Flow

1. Read `README.md` once to understand goals and commands.
2. Read `openenv.yaml` to see the formal benchmark contract.
3. Read `src/orbits_env/models.py` to learn the domain data schema.
4. Read `src/orbits_env/tasks/catalog.py` to see difficulty design.
5. Read `src/orbits_env/simulator.py` to understand environment transition logic.
6. Read `src/orbits_env/graders/scoring.py` for final scoring logic.
7. Read `server/app.py` to connect simulator to HTTP endpoints.
8. Read `src/orbits_env/baseline.py` and `inference.py` to see policy execution patterns.
9. Read `tests` and `scripts` to see how behavior is verified.

## Mental Model

Each episode is a constrained resource-management problem:

- Safety objective: keep risk low.
- Cost objective: use as little fuel and mission offset as needed.
- Information objective: optionally spend tracking budget to reduce uncertainty.

The environment gives dense reward each step, and a separate final grade summarizes overall run quality.
