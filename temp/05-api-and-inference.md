# API And Inference

## FastAPI Endpoints

`server/app.py` exposes the environment over HTTP and function-callable handlers.

Routes:

- `GET /health`: readiness check.
- `GET /`: environment metadata and available tasks.
- `GET /tasks`: task IDs.
- `GET /tasks/{task_id}`: full task config.
- `POST /reset` and `POST /reset/{task_id}`: start new episode.
- `POST /step`: apply one action.
- `GET /state`: full state snapshot.
- `GET /grade`: normalized episode score.
- `POST /close`: close active environment.

The server stores one default active environment in process memory (`ENVIRONMENTS["default"]`).

## Inference Script Contract

`inference.py` is the required script for model-based action selection.

Behavior:

1. Build OpenAI-compatible client when `HF_TOKEN` exists.
2. Iterate all three task IDs.
3. For each step, request model JSON action or fallback to heuristic.
4. Log strict machine-parseable lines:
   - `[START] ...`
   - `[STEP] ...`
   - `[END] ...`

Fallback behavior:

- Any model call failure triggers safe fallback to baseline heuristic for that step.
- Missing token means full heuristic run.

## Prompting Strategy

The system prompt enforces strict action schema.

User prompt includes:

- current observation payload
- optional recent action/reward history
- strategy notes for risk-vs-resource tradeoff

`response_format={"type": "json_object"}` encourages valid machine output.

## Baseline Policy

`src/orbits_env/baseline.py` is a deterministic heuristic:

- requests tracking updates only under uncertainty/timing conditions
- otherwise picks axis with best risk-weighted effectiveness
- scales maneuver magnitude by current risk
- chooses `noop` when risk low or offset already high

This baseline is both a benchmark reference and a robust fallback policy.
