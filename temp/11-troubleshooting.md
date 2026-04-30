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

## Problems While Switching LLM Models

Symptom:

- switching `MODEL_NAME` sometimes fails even though another model works.

Common causes:

- selected model is not available for your current provider/key.
- API key variable name changed between providers.
- provider/model has stricter JSON-format behavior.

What this repo now does:

- accepts API keys from any of: `HF_TOKEN`, `OPENAI_API_KEY`, `GROQ_API_KEY`, `API_KEY`.
- validates model availability on startup (best effort) and fails early with a clear message.
- retries without provider JSON mode when strict JSON generation fails, then validates JSON locally.

Quick checks:

```bash
echo "$API_BASE_URL"
echo "$MODEL_NAME"
```

Minimal smoke run:

```bash
MODEL_NAME="openai/gpt-oss-20b" MAX_STEPS=1 make inference
```

If your provider says `model_not_found`, use one of the listed available model IDs in the error.

If startup model validation gets in your way temporarily:

```bash
export VALIDATE_MODEL_ON_START=0
```

## Changing .env But Model Does Not Change

Symptom:

- you edit `.env` `MODEL_NAME` but `make iterative-inference` still appears to use an old model.

Cause:

- `.env` loading uses `os.environ.setdefault(...)`, so already-exported shell vars take precedence over `.env`.

Fix in fish shell before rerun:

```bash
set -e MODEL_NAME API_BASE_URL HF_TOKEN OPENAI_API_KEY GROQ_API_KEY API_KEY REASONING_EFFORT
make iterative-inference
```

This clears override variables so values from `.env` are used.

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
