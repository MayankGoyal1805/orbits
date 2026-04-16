# Environment Variables And API Keys

This file tells you exactly what variables exist, which ones are required, and when.

## Quick Summary

Variables you will use most:

- `API_BASE_URL`
- `MODEL_NAME`
- `HF_TOKEN`
- `LOCAL_IMAGE_NAME` (optional compatibility variable)

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

- if unset: script runs fallback heuristic mode (no external LLM calls)
- if set: script attempts remote model calls

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

## Recommended Local Setup Snippet

Add to your local shell env file (not committed):

```bash
export API_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
export MODEL_NAME="gemini-2.5-flash"
export HF_TOKEN="<your_provider_api_key>"
```

Then reload shell and run:

```bash
make inference
```

## Minimal Required Variables By Scenario

### Scenario A: Local learning without remote model

Required:

- none (script falls back automatically)

Optional:
- none

### Scenario B: Remote model inference

Required:

- `HF_TOKEN`

Recommended:

- `API_BASE_URL`
- `MODEL_NAME`
