# Environment Variables And API Keys

This file tells you exactly what variables exist, which ones are required, and when.

## Quick Summary

Variables you will use most:

- `API_BASE_URL`
- `MODEL_NAME`
- `HF_TOKEN`
- `LOCAL_IMAGE_NAME` (optional compatibility variable)
- `REQUESTS_PER_MINUTE` (optional throttling control)
- `REQUEST_GAP_SECONDS` (optional hard gap between requests)
- `MAX_LLM_RETRIES` and `RETRY_BACKOFF_SECONDS` (optional rate-limit retry controls)
- `MAX_RESPONSE_TOKENS` (optional response-size cap to reduce token pressure)

## 1) API_BASE_URL

Used by:

- `inference.py`

Purpose:

- OpenAI-compatible API base endpoint used by client.

Current script default:

- `https://generativelanguage.googleapis.com/v1beta/openai/`

When to override:

- using another OpenAI-compatible provider
- custom/self-hosted gateway

Example:

```bash
export API_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
```

## 2) MODEL_NAME

Used by:

- `inference.py`

Purpose:

- sets model identifier for chat completion requests.

Current script default:

- `gemini-2.5-flash`

Example:

```bash
export MODEL_NAME="gemini-2.5-flash"
```

## 3) HF_TOKEN

Used by:

- `inference.py` as API key for `OpenAI(...)` client.

Important behavior:

- if unset: script fails in strict LLM mode (default behavior)
- if set: script uses remote model calls

Example:

```bash
export HF_TOKEN="<your_provider_api_key>"
```

Security note:

- never commit this token to git
- keep it in your shell env file (ignored), secret manager, or CI secret store

## 4) LOCAL_IMAGE_NAME

Used by:

- declared in `inference.py`

Current behavior:

- present for checklist compatibility
- not actively used in current local inference flow

You can leave it unset for normal local runs.

## 4b) ALLOW_HEURISTIC_FALLBACK

Used by:

- `inference.py` and iterative inference runner.

Purpose:

- explicitly opt in to heuristic fallback when LLM config is unavailable or calls fail.

Default:

- disabled (`0`)

Example:

```bash
export ALLOW_HEURISTIC_FALLBACK=1
```

## 5) Request Pacing And Rate-Limit Controls

Used by:

- `inference.py` and iterative inference runner via imported inference settings.

Variables:

- `REQUESTS_PER_MINUTE`: soft pacing target (default `30`).
- `REQUEST_GAP_SECONDS`: hard minimum gap between requests (default `2.5`).
- `MAX_LLM_RETRIES`: retries for rate-limit errors (default `2`).
- `RETRY_BACKOFF_SECONDS`: base backoff seconds (default `1.5`).
- `MAX_RESPONSE_TOKENS`: cap model response tokens (default `120`).

Example conservative setup:

```bash
export REQUESTS_PER_MINUTE=20
export REQUEST_GAP_SECONDS=3
export MAX_LLM_RETRIES=3
export RETRY_BACKOFF_SECONDS=2
export MAX_RESPONSE_TOKENS=100
```

## Recommended Local Setup Snippet

Add to your local shell env file (not committed):

```bash
export API_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
export MODEL_NAME="gemini-2.5-flash"
export HF_TOKEN="<your_provider_api_key>"
export REQUESTS_PER_MINUTE=20
export REQUEST_GAP_SECONDS=3
```

Then reload shell and run:

```bash
make inference
```

## Minimal Required Variables By Scenario

### Scenario A: Local learning without remote model

Required:

- set `ALLOW_HEURISTIC_FALLBACK=1`

Optional:
- none

### Scenario B: Remote model inference

Required:

- `HF_TOKEN`

Recommended:

- `API_BASE_URL`
- `MODEL_NAME`

## Pre-Run Checklist For Iterative Inference

Run these when you want code/data changes reflected in iterative runs:

1. Sync environment after dependency/code changes:

```bash
make sync
```

2. Rebuild dataset priors after EDA data updates:

```bash
make build-priors
```

3. Run iterative inference with chosen rounds:

```bash
make iterative-inference ITERATIVE_ROUNDS=3
```

4. Check outputs:

- JSON summary: `iterative_inference_results.json`
- detailed text report: `output.txt`
