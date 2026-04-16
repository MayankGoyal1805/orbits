# Troubleshooting

This page collects common issues and practical fixes.

## uv Hardlink Warning During Install

Symptom:

- warning about failed hardlink and fallback to full copy.

Meaning:

- cache and environment may be on different filesystems.

Fix (optional):

```bash
export UV_LINK_MODE=copy
```

This is not a functional failure; installs still work.

## Inference Uses Fallback Instead Of LLM

Symptom:

- model label in logs ends with `fallback-heuristic`.

Cause:

- `HF_TOKEN` missing or model request failed.

Checks:

```bash
echo "$HF_TOKEN"
echo "$API_BASE_URL"
echo "$MODEL_NAME"
```

Fix:

- set valid key and endpoint values.

## Docker Command Cannot Connect To Daemon

Symptom:

- `dial unix /var/run/docker.sock: connect: no such file or directory`

Cause:

- Docker daemon not running.

Fix:

- start Docker engine/service for your distro.
- rerun `make docker-build`.

## API Error: Call reset before step/state/grade

Symptom:

- 400 response with message to call reset first.

Cause:

- no active default environment session.

Fix:

```bash
curl -fsSL -X POST http://127.0.0.1:7860/reset/collision_avoidance_easy
```

Then call `/step`, `/state`, `/grade`.

## Unknown task_id Error

Symptom:

- task lookup failure.

Fix:

- use one of:
  - `collision_avoidance_easy`
  - `collision_avoidance_medium`
  - `collision_avoidance_hard`

List tasks live:

```bash
curl -fsSL http://127.0.0.1:7860/tasks
```
