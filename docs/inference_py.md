# Tutorial: `inference.py`

This document provides a line-by-line explanation of `inference.py`, detailing its concepts and setup.

```python
from __future__ import annotations

import json
import os
import re
import sys
import textwrap
import time
from typing import Any, Optional

try:
    from openai import OpenAI
except ModuleNotFoundError:
    OpenAI = Any  # type: ignore[assignment]
```
- `from __future__ import annotations`: Enables postponed evaluation of annotations.
- ``: Empty line.
- `import json`: Imports JSON encoding/decoding.
- `import os`: Imports OS interfaces for environment variables.
- `import re`: Imports regular expressions.
- `import sys`: Imports system-specific parameters and functions.
- `import textwrap`: Imports text formatting utilities.
- `import time`: Imports time and clock utilities.
- `from typing import Any, Optional`: Imports type hinting generics.
- ``: Empty line.
- `try:`: Starts a try block for optional dependencies.
- `    from openai import OpenAI`: Attempts to import the OpenAI client.
- `except ModuleNotFoundError:`: Catches the error if openai is not installed.
- `    OpenAI = Any  # type: ignore[assignment]`: Falls back to `Any` to prevent type errors.

```python
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from orbits_env.baseline import choose_action as choose_heuristic_action
from orbits_env.env import SpaceDebrisEnv
from orbits_env.models import ActionType, EnvironmentAction, EnvironmentObservation
```
- `ROOT = os.path.dirname(os.path.abspath(__file__))`: Resolves the directory of this file.
- `SRC = os.path.join(ROOT, "src")`: Constructs the path to the `src` subdirectory.
- `if SRC not in sys.path:`: Checks if `src` is in the module search path.
- `    sys.path.insert(0, SRC)`: Adds `src` to the path for internal imports.
- ``: Empty line.
- `from orbits_env.baseline import choose_action as choose_heuristic_action`: Imports the baseline algorithm.
- `from orbits_env.env import SpaceDebrisEnv`: Imports the environment simulator.
- `from orbits_env.models import ActionType, EnvironmentAction, EnvironmentObservation`: Imports core Pydantic models.

```python
def _load_dotenv_if_present() -> None:
    """Load .env key-value pairs into process env if present.

    This is intentionally optional and non-fatal. Existing environment variables
    are never overwritten, so deployment environments keep precedence.
    """

    # Keep tests deterministic and avoid accidental external API calls during pytest.
    if os.getenv("PYTEST_CURRENT_TEST"):
        return

    # Allow explicit opt-out when needed.
    if os.getenv("ORBITS_DISABLE_DOTENV") == "1":
        return
```
- `def _load_dotenv_if_present() -> None:`: Defines a helper to load local environment variables.
- `    """Load .env key-value pairs into process env if present.`: Starts docstring.
- ``: Empty line in docstring.
- `    This is intentionally optional and non-fatal. Existing environment variables`: Docstring.
- `    are never overwritten, so deployment environments keep precedence.`: Docstring.
- `    """`: Ends docstring.
- ``: Empty line.
- `    # Keep tests deterministic and avoid accidental external API calls during pytest.`: Comment.
- `    if os.getenv("PYTEST_CURRENT_TEST"):`: Checks if pytest is running.
- `        return`: Bypasses loading to ensure determinism in tests.
- ``: Empty line.
- `    # Allow explicit opt-out when needed.`: Comment.
- `    if os.getenv("ORBITS_DISABLE_DOTENV") == "1":`: Checks for opt-out variable.
- `        return`: Aborts dotenv loading.

```python
    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(dotenv_path):
        return

    try:
        with open(dotenv_path, encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("export "):
                    line = line[len("export ") :].strip()
                if "=" not in line:
                    continue
```
- `    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")`: Finds the path to the `.env` file.
- `    if not os.path.exists(dotenv_path):`: Checks if the file actually exists.
- `        return`: Returns early if there is no file.
- ``: Empty line.
- `    try:`: Begins file parsing block.
- `        with open(dotenv_path, encoding="utf-8") as handle:`: Opens the file for reading.
- `            for raw_line in handle:`: Iterates through each line.
- `                line = raw_line.strip()`: Removes leading and trailing whitespace.
- `                if not line or line.startswith("#"):`: Ignores empty lines and comments.
- `                    continue`: Skips to next line.
- `                if line.startswith("export "):`: Checks for bash export syntax.
- `                    line = line[len("export ") :].strip()`: Strips the export prefix.
- `                if "=" not in line:`: Ensures it is a valid assignment.
- `                    continue`: Skips invalid lines.

```python
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key:
                    os.environ.setdefault(key, value)
    except OSError:
        # .env loading is best-effort only.
        return


_load_dotenv_if_present()
```
- `                key, value = line.split("=", 1)`: Splits into key and value on the first equals sign.
- `                key = key.strip()`: Trims the key.
- `                value = value.strip().strip('"').strip("'")`: Trims the value and removes surrounding quotes.
- `                if key:`: Ensures the key is not empty.
- `                    os.environ.setdefault(key, value)`: Sets the environment variable if not already set.
- `    except OSError:`: Catches file reading errors.
- `        # .env loading is best-effort only.`: Comment.
- `        return`: Fails silently.
- ``: Empty line.
- ``: Empty line.
- `_load_dotenv_if_present()`: Executes the function immediately upon module import.

```python
def _resolve_api_key() -> str | None:
    # Support common provider variable names so switching providers does not
    # require code edits.
    for key_name in ("HF_TOKEN", "OPENAI_API_KEY", "GROQ_API_KEY", "API_KEY"):
        value = os.getenv(key_name)
        if value:
            return value
    return None
```
- `def _resolve_api_key() -> str | None:`: Defines a helper to locate an API key.
- `    # Support common provider variable names so switching providers does not`: Comment.
- `    # require code edits.`: Comment.
- `    for key_name in ("HF_TOKEN", "OPENAI_API_KEY", "GROQ_API_KEY", "API_KEY"):`: Iterates through common key names.
- `        value = os.getenv(key_name)`: Looks up the variable in the environment.
- `        if value:`: Checks if a value was found.
- `            return value`: Returns the first matched key.
- `    return None`: Returns None if no keys match.

```python
API_BASE_URL = os.getenv("API_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
API_KEY = _resolve_api_key()
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")
BENCHMARK = "orbits-openenv"
MAX_STEPS = int(os.getenv("MAX_STEPS", "12"))
REQUESTS_PER_MINUTE = max(1, int(os.getenv("REQUESTS_PER_MINUTE", "30")))
REQUEST_GAP_SECONDS = max(0.0, float(os.getenv("REQUEST_GAP_SECONDS", "2.5")))
MAX_LLM_RETRIES = max(0, int(os.getenv("MAX_LLM_RETRIES", "2")))
RETRY_BACKOFF_SECONDS = max(0.0, float(os.getenv("RETRY_BACKOFF_SECONDS", "1.5")))
MAX_RESPONSE_TOKENS = max(32, int(os.getenv("MAX_RESPONSE_TOKENS", "120")))
REASONING_EFFORT = os.getenv("REASONING_EFFORT", "").strip().lower()
```
- `API_BASE_URL = os.getenv("API_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")`: Sets the LLM endpoint URL.
- `MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")`: Selects the AI model.
- `API_KEY = _resolve_api_key()`: Captures the resolved API key.
- `LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")`: Gets docker image name for submission validation.
- `BENCHMARK = "orbits-openenv"`: Identifies the benchmark namespace.
- `MAX_STEPS = int(os.getenv("MAX_STEPS", "12"))`: Sets the maximum allowed steps in an episode.
- `REQUESTS_PER_MINUTE = max(1, int(os.getenv("REQUESTS_PER_MINUTE", "30")))`: Calculates the API rate limit ceiling.
- `REQUEST_GAP_SECONDS = max(0.0, float(os.getenv("REQUEST_GAP_SECONDS", "2.5")))`: Enforces a hard minimum delay between requests.
- `MAX_LLM_RETRIES = max(0, int(os.getenv("MAX_LLM_RETRIES", "2")))`: Sets the retry limit for failed API calls.
- `RETRY_BACKOFF_SECONDS = max(0.0, float(os.getenv("RETRY_BACKOFF_SECONDS", "1.5")))`: Configures exponential backoff multiplier.
- `MAX_RESPONSE_TOKENS = max(32, int(os.getenv("MAX_RESPONSE_TOKENS", "120")))`: Caps the length of the LLM's response.
- `REASONING_EFFORT = os.getenv("REASONING_EFFORT", "").strip().lower()`: Configures explicit reasoning effort parameter for capable models.

```python
ALLOW_HEURISTIC_FALLBACK = os.getenv("ALLOW_HEURISTIC_FALLBACK", "0").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}
TEMPERATURE = 0.1
ENABLE_HISTORY = True
TASK_IDS = [
    "collision_avoidance_easy",
    "collision_avoidance_medium",
    "collision_avoidance_hard",
]
_LAST_REQUEST_TS: float | None = None
```
- `ALLOW_HEURISTIC_FALLBACK = os.getenv("ALLOW_HEURISTIC_FALLBACK", "0").strip().lower() in {`: Parses a boolean toggle for using baseline math.
- `    "1",`: Match case for true.
- `    "true",`: Match case for true.
- `    "yes",`: Match case for true.
- `    "on",`: Match case for true.
- `}`: Closes set.
- `TEMPERATURE = 0.1`: Uses a low temperature for more deterministic LLM output.
- `ENABLE_HISTORY = True`: Toggles sending previous steps to the LLM.
- `TASK_IDS = [`: Lists the environments to run.
- `    "collision_avoidance_easy",`: Easy difficulty task.
- `    "collision_avoidance_medium",`: Medium difficulty task.
- `    "collision_avoidance_hard",`: Hard difficulty task.
- `]`: Closes list.
- `_LAST_REQUEST_TS: float | None = None`: Initializes global rate-limit tracking variable.

```python
SYSTEM_PROMPT = textwrap.dedent(
    """
    You are a spacecraft conjunction-management agent.
    Choose exactly one action per step to reduce collision risk while preserving fuel and limiting mission offset.

    Valid action_type values:
    - noop
    - request_tracking_update
    - radial_maneuver
    - along_track_maneuver
    - normal_maneuver

    Output strict JSON with:
    {"action_type": "<valid_action_type>", "magnitude": <float between 0 and 1>}

    Use magnitude 0.0 for noop and request_tracking_update.
    Prefer request_tracking_update when uncertainty is high and time remains.
    """
).strip()
```
- `SYSTEM_PROMPT = textwrap.dedent(`: Formats the system prompt by removing indentation.
- `    """`: Starts the multi-line string.
- `    You are a spacecraft conjunction-management agent.`: Sets the agent's persona.
- `    Choose exactly one action per step to reduce collision risk while preserving fuel and limiting mission offset.`: Describes the core objective.
- ``: Empty line.
- `    Valid action_type values:`: Starts listing allowed actions.
- `    - noop`: Do nothing.
- `    - request_tracking_update`: Request more accurate radar data.
- `    - radial_maneuver`: Perform a thrust maneuver radially.
- `    - along_track_maneuver`: Perform a thrust maneuver along the track.
- `    - normal_maneuver`: Perform a thrust maneuver normal to the orbit.
- ``: Empty line.
- `    Output strict JSON with:`: Instructs the model to output JSON only.
- `    {"action_type": "<valid_action_type>", "magnitude": <float between 0 and 1>}`: Provides the JSON schema.
- ``: Empty line.
- `    Use magnitude 0.0 for noop and request_tracking_update.`: Sets constraint for non-maneuvering actions.
- `    Prefer request_tracking_update when uncertainty is high and time remains.`: Provides a basic heuristic hint.
- `    """`: Ends the multi-line string.
- `).strip()`: Removes leading and trailing whitespace from the final prompt string.

```python
def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: list[float]) -> None:
    rewards_str = ",".join(f"{reward:.2f}" for reward in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )
```
- `def log_start(task: str, env: str, model: str) -> None:`: Defines a logger for the start of an episode.
- `    print(f"[START] task={task} env={env} model={model}", flush=True)`: Prints the initialization metadata.
- ``: Empty line.
- ``: Empty line.
- `def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:`: Defines a logger for each individual step.
- `    error_val = error if error else "null"`: Handles empty error messages.
- `    done_val = str(done).lower()`: Formats boolean into standard text.
- `    print(`: Starts the print statement.
- `        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",`: Formats the step telemetry payload.
- `        flush=True,`: Ensures logs appear immediately in standard output.
- `    )`: Ends the print statement.
- ``: Empty line.
- ``: Empty line.
- `def log_end(success: bool, steps: int, score: float, rewards: list[float]) -> None:`: Defines a logger for episode conclusion.
- `    rewards_str = ",".join(f"{reward:.2f}" for reward in rewards)`: Compresses the reward history array.
- `    print(`: Starts the print statement.
- `        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",`: Formats summary metrics.
- `        flush=True,`: Ensures logs flush out immediately.
- `    )`: Ends the print statement.

```python
def _observation_payload(observation: EnvironmentObservation) -> dict:
    return {
        "task_id": observation.task_id,
        "step_index": observation.step_index,
        "horizon_remaining": observation.horizon_remaining,
        "fuel_remaining": observation.fuel_remaining,
        "tracking_quality": observation.tracking_quality,
        "tracking_budget_remaining": observation.tracking_budget_remaining,
        "mission_offsets": observation.mission_offsets.model_dump(),
        "total_collision_probability": observation.total_collision_probability,
        "highest_collision_probability": observation.highest_collision_probability,
        "visible_events": [event.model_dump() for event in observation.visible_events],
        "last_action": observation.last_action.value if observation.last_action else None,
    }
```
- `def _observation_payload(observation: EnvironmentObservation) -> dict:`: Serializes the state observation into a plain dictionary.
- `    return {`: Begins returning the mapping.
- `        "task_id": observation.task_id,`: Captures the ID.
- `        "step_index": observation.step_index,`: Captures the current turn number.
- `        "horizon_remaining": observation.horizon_remaining,`: Captures turns until termination.
- `        "fuel_remaining": observation.fuel_remaining,`: Captures available maneuver budget.
- `        "tracking_quality": observation.tracking_quality,`: Captures sensor fidelity.
- `        "tracking_budget_remaining": observation.tracking_budget_remaining,`: Captures remaining sensor uses.
- `        "mission_offsets": observation.mission_offsets.model_dump(),`: Dumps spatial deviations.
- `        "total_collision_probability": observation.total_collision_probability,`: Maps cumulative risk.
- `        "highest_collision_probability": observation.highest_collision_probability,`: Maps highest single threat.
- `        "visible_events": [event.model_dump() for event in observation.visible_events],`: Dumps visible debris conjunctions.
- `        "last_action": observation.last_action.value if observation.last_action else None,`: Extracts enum value of last action taken.
- `    }`: Closes dictionary.

```python
def _sanitize_error(error: str) -> str:
    return error.replace("\n", " ").replace("\r", " ").strip() or "null"


def _action_to_string(action: EnvironmentAction) -> str:
    if action.action_type in {ActionType.NOOP, ActionType.REQUEST_TRACKING_UPDATE}:
        return action.action_type.value
    return f"{action.action_type.value}({action.magnitude:.2f})"
```
- `def _sanitize_error(error: str) -> str:`: Removes newlines from error logs.
- `    return error.replace("\n", " ").replace("\r", " ").strip() or "null"`: Cleans formatting and defaults to null.
- ``: Empty line.
- ``: Empty line.
- `def _action_to_string(action: EnvironmentAction) -> str:`: Converts action struct to a readable string.
- `    if action.action_type in {ActionType.NOOP, ActionType.REQUEST_TRACKING_UPDATE}:`: Checks if action is magnitude-independent.
- `        return action.action_type.value`: Returns just the base action name.
- `    return f"{action.action_type.value}({action.magnitude:.2f})"`: Includes magnitude in string for maneuvers.

```python
def _extract_json_object(raw_text: str) -> str | None:
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start < 0 or end <= start:
        return None
    return raw_text[start : end + 1]
```
- `def _extract_json_object(raw_text: str) -> str | None:`: A fallback parser to locate JSON inside text.
- `    start = raw_text.find("{")`: Finds the first curly brace.
- `    end = raw_text.rfind("}")`: Finds the last curly brace.
- `    if start < 0 or end <= start:`: Validates braces exist in correct order.
- `        return None`: Fails if invalid.
- `    return raw_text[start : end + 1]`: Returns the substring containing the JSON payload.

```python
def _infer_action_from_text(raw_text: str) -> EnvironmentAction | None:
    text = raw_text.lower()

    action_type: ActionType | None = None
    if "request_tracking_update" in text or "tracking update" in text:
        action_type = ActionType.REQUEST_TRACKING_UPDATE
    elif "along_track_maneuver" in text or "along-track maneuver" in text or "along track maneuver" in text:
        action_type = ActionType.ALONG_TRACK_MANEUVER
    elif "radial_maneuver" in text or "radial maneuver" in text:
        action_type = ActionType.RADIAL_MANEUVER
    elif "normal_maneuver" in text or "normal maneuver" in text:
        action_type = ActionType.NORMAL_MANEUVER
    elif "noop" in text:
        action_type = ActionType.NOOP
```
- `def _infer_action_from_text(raw_text: str) -> EnvironmentAction | None:`: A secondary fallback to guess actions from prose.
- `    text = raw_text.lower()`: Normalizes text to lowercase.
- ``: Empty line.
- `    action_type: ActionType | None = None`: Initializes action as empty.
- `    if "request_tracking_update" in text or "tracking update" in text:`: Checks for tracking requests.
- `        action_type = ActionType.REQUEST_TRACKING_UPDATE`: Assigns enum.
- `    elif "along_track_maneuver" in text or "along-track maneuver" in text or "along track maneuver" in text:`: Checks for along-track thrusts.
- `        action_type = ActionType.ALONG_TRACK_MANEUVER`: Assigns enum.
- `    elif "radial_maneuver" in text or "radial maneuver" in text:`: Checks for radial thrusts.
- `        action_type = ActionType.RADIAL_MANEUVER`: Assigns enum.
- `    elif "normal_maneuver" in text or "normal maneuver" in text:`: Checks for normal thrusts.
- `        action_type = ActionType.NORMAL_MANEUVER`: Assigns enum.
- `    elif "noop" in text:`: Checks for idle action.
- `        action_type = ActionType.NOOP`: Assigns enum.

```python
    if action_type is None:
        return None

    if action_type in {ActionType.NOOP, ActionType.REQUEST_TRACKING_UPDATE}:
        return EnvironmentAction(action_type=action_type, magnitude=0.0)

    magnitude_match = re.search(r"magnitude\s*[:=]?\s*([01](?:\.\d+)?)", text)
    magnitude = float(magnitude_match.group(1)) if magnitude_match else 0.5
    magnitude = max(0.0, min(1.0, magnitude))
    return EnvironmentAction(action_type=action_type, magnitude=magnitude)
```
- `    if action_type is None:`: Aborts if no action keyword was found.
- `        return None`: Returns fail state.
- ``: Empty line.
- `    if action_type in {ActionType.NOOP, ActionType.REQUEST_TRACKING_UPDATE}:`: Checks if magnitude is irrelevant.
- `        return EnvironmentAction(action_type=action_type, magnitude=0.0)`: Returns early with zero magnitude.
- ``: Empty line.
- `    magnitude_match = re.search(r"magnitude\s*[:=]?\s*([01](?:\.\d+)?)", text)`: Parses magnitude via regex.
- `    magnitude = float(magnitude_match.group(1)) if magnitude_match else 0.5`: Defaults to half throttle if not stated.
- `    magnitude = max(0.0, min(1.0, magnitude))`: Clamps value between 0.0 and 1.0.
- `    return EnvironmentAction(action_type=action_type, magnitude=magnitude)`: Instantiates the fallback action.

```python
def _parse_action(raw_text: str) -> EnvironmentAction:
    normalized = raw_text.strip()
    # Drop chain-of-thought wrappers from models that emit <think> blocks.
    normalized = re.sub(r"<think>[\s\S]*?</think>", "", normalized, flags=re.IGNORECASE).strip()

    try:
        payload = json.loads(normalized)
    except json.JSONDecodeError:
        # Some providers/models may return prose around JSON when strict JSON mode
        # is unavailable. Extract the first JSON object block as a fallback.
        extracted = _extract_json_object(normalized)
```
- `def _parse_action(raw_text: str) -> EnvironmentAction:`: Main pipeline for validating LLM output.
- `    normalized = raw_text.strip()`: Trims output whitespace.
- `    # Drop chain-of-thought wrappers from models that emit <think> blocks.`: Comment.
- `    normalized = re.sub(r"<think>[\s\S]*?</think>", "", normalized, flags=re.IGNORECASE).strip()`: Purges reasoning tokens to expose JSON.
- ``: Empty line.
- `    try:`: Enters JSON parsing block.
- `        payload = json.loads(normalized)`: Attempts strict JSON load.
- `    except json.JSONDecodeError:`: Handles parsing failure.
- `        # Some providers/models may return prose around JSON when strict JSON mode`: Comment.
- `        # is unavailable. Extract the first JSON object block as a fallback.`: Comment.
- `        extracted = _extract_json_object(normalized)`: Invokes substring extractor.

```python
        if extracted is not None:
            payload = json.loads(extracted)
        else:
            inferred = _infer_action_from_text(raw_text)
            if inferred is not None:
                return inferred
            raise
    action_type = payload.get("action_type", ActionType.NOOP)
    magnitude = payload.get("magnitude", 0.0)
    return EnvironmentAction(action_type=action_type, magnitude=magnitude)
```
- `        if extracted is not None:`: Evaluates if extraction succeeded.
- `            payload = json.loads(extracted)`: Re-attempts parsing on substring.
- `        else:`: Executes if extraction failed.
- `            inferred = _infer_action_from_text(raw_text)`: Triggers text inference fallback.
- `            if inferred is not None:`: Evaluates inference success.
- `                return inferred`: Escapes parsing entirely and returns guessed action.
- `            raise`: Re-raises error if completely illegible.
- `    action_type = payload.get("action_type", ActionType.NOOP)`: Extracts parsed action type.
- `    magnitude = payload.get("magnitude", 0.0)`: Extracts parsed magnitude.
- `    return EnvironmentAction(action_type=action_type, magnitude=magnitude)`: Builds robust validation object.

```python
def _is_json_mode_generation_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return (
        "json_validate_failed" in message
        or "failed to generate json" in message
        or "max completion tokens reached" in message
    )


def _is_model_not_found_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return (
        "model_not_found" in message
        or "does not exist or you do not have access" in message
        or "unknown model" in message
    )
```
- `def _is_json_mode_generation_error(exc: Exception) -> bool:`: Determines if error was caused by strict JSON mode.
- `    message = str(exc).lower()`: Gets error string.
- `    return (`: Evaluates conditions.
- `        "json_validate_failed" in message`: Matches typical framework error.
- `        or "failed to generate json" in message`: Matches alternative failure message.
- `        or "max completion tokens reached" in message`: Matches failure due to cut-off.
- `    )`: Ends return.
- ``: Empty line.
- ``: Empty line.
- `def _is_model_not_found_error(exc: Exception) -> bool:`: Determines if the requested LLM name does not exist.
- `    message = str(exc).lower()`: Lowercases the error.
- `    return (`: Evaluates string fragments.
- `        "model_not_found" in message`: Generic missing model string.
- `        or "does not exist or you do not have access" in message`: OpenAI missing access string.
- `        or "unknown model" in message`: Local deployment missing string.
- `    )`: Completes check.

```python
def _is_rate_limit_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return "rate limit" in message or "429" in message or "rate_limit_exceeded" in message


def _is_reasoning_effort_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return "reasoning_effort" in message and (
        "must be one of" in message or "not supported" in message
    )
```
- `def _is_rate_limit_error(exc: Exception) -> bool:`: Identifies if request was throttled.
- `    message = str(exc).lower()`: normalizes error text.
- `    return "rate limit" in message or "429" in message or "rate_limit_exceeded" in message`: Compares against common HTTP 429 substrings.
- ``: Empty line.
- ``: Empty line.
- `def _is_reasoning_effort_error(exc: Exception) -> bool:`: Validates if reasoning configuration parameter caused failure.
- `    message = str(exc).lower()`: Gets lowercase representation.
- `    return "reasoning_effort" in message and (`: Looks for specific parameter conflict.
- `        "must be one of" in message or "not supported" in message`: Evaluates API mismatch messages.
- `    )`: Ends check.

```python
def _validate_model_availability(client: OpenAI) -> None:
    if os.getenv("VALIDATE_MODEL_ON_START", "1").strip().lower() in {"0", "false", "no", "off"}:
        return

    # Some providers may not expose model listing for the key; this check is
    # best-effort and should not block otherwise valid providers.
    try:
        model_list = client.models.list()
        available = {item.id for item in model_list.data if getattr(item, "id", None)}
    except Exception:
        return

    if MODEL_NAME in available:
        return
```
- `def _validate_model_availability(client: OpenAI) -> None:`: Validates that the requested model name is present on the server.
- `    if os.getenv("VALIDATE_MODEL_ON_START", "1").strip().lower() in {"0", "false", "no", "off"}:`: Checks opt-out toggle.
- `        return`: Exits validation early if opted out.
- ``: Empty line.
- `    # Some providers may not expose model listing for the key; this check is`: Comment.
- `    # best-effort and should not block otherwise valid providers.`: Comment.
- `    try:`: Enters check block.
- `        model_list = client.models.list()`: Reaches out to provider listing endpoint.
- `        available = {item.id for item in model_list.data if getattr(item, "id", None)}`: Extracts models into a set.
- `    except Exception:`: Catches missing listing endpoints.
- `        return`: Allows code to proceed assuming model might work.
- ``: Empty line.
- `    if MODEL_NAME in available:`: Confirms model is listed.
- `        return`: Passes validation.

```python
    sample = sorted(available)[:8]
    sample_text = ", ".join(sample) if sample else "<none returned by provider>"
    raise RuntimeError(
        "Configured MODEL_NAME is not available for this API key/provider. "
        f"MODEL_NAME='{MODEL_NAME}', API_BASE_URL='{API_BASE_URL}'. "
        f"Example available models: {sample_text}."
    )
```
- `    sample = sorted(available)[:8]`: Grabs up to 8 models to suggest to the user.
- `    sample_text = ", ".join(sample) if sample else "<none returned by provider>"`: Formats recommendations as text.
- `    raise RuntimeError(`: Halts program if model explicitly wasn't found.
- `        "Configured MODEL_NAME is not available for this API key/provider. "`: Main error line.
- `        f"MODEL_NAME='{MODEL_NAME}', API_BASE_URL='{API_BASE_URL}'. "`: Prints current config.
- `        f"Example available models: {sample_text}."`: Adds suggestions.
- `    )`: Closes error exception.

```python
def _build_basic_prompt(observation: EnvironmentObservation) -> str:
    return textwrap.dedent(
        f"""
        Current observation:
        {json.dumps(_observation_payload(observation), indent=2)}

        Return the next action as strict JSON only.
        """
    ).strip()
```
- `def _build_basic_prompt(observation: EnvironmentObservation) -> str:`: Generates a payload lacking episode history.
- `    return textwrap.dedent(`: Strips indents from block.
- `        f"""`: Starts prompt template.
- `        Current observation:`: Header string.
- `        {json.dumps(_observation_payload(observation), indent=2)}`: Dumps formatted observation JSON.
- ``: Empty line.
- `        Return the next action as strict JSON only.`: Reminds LLM of strict formatting.
- `        """`: Ends template.
- `    ).strip()`: Removes newlines and spaces at ends.

```python
def _build_feedback_prompt(
    observation: EnvironmentObservation,
    history: list[dict[str, str | float | bool]],
    strategy_memory: list[str] | None = None,
) -> str:
    recent_history = history[-4:]
    history_block = json.dumps(recent_history, indent=2) if recent_history else "[]"
    strategy_notes = {
        "primary_objective": "Reduce collision probability while keeping enough fuel for later threats.",
        "tracking_guidance": "Use request_tracking_update when uncertainty is high, tracking budget remains, and there is still time before closest approach.",
        "maneuver_guidance": "Prefer the axis that best reduces the visible threats overall, not just one object.",
        "mission_guidance": "Avoid excessive mission offsets unless collision probability is still meaningfully high.",
    }
    if strategy_memory:
        strategy_notes["adaptive_strategy_memory"] = strategy_memory
```
- `def _build_feedback_prompt(`: Starts robust prompt generation function.
- `    observation: EnvironmentObservation,`: Current state observation argument.
- `    history: list[dict[str, str | float | bool]],`: Past actions and outcomes.
- `    strategy_memory: list[str] | None = None,`: Long-term episodic insights.
- `) -> str:`: Returns prompt text.
- `    recent_history = history[-4:]`: Slices the last four turns to prevent context bloat.
- `    history_block = json.dumps(recent_history, indent=2) if recent_history else "[]"`: Serializes the memory array.
- `    strategy_notes = {`: Generates heuristic recommendations explicitly injected into prompt context.
- `        "primary_objective": "Reduce collision probability while keeping enough fuel for later threats.",`: Gives overarching goal.
- `        "tracking_guidance": "Use request_tracking_update when uncertainty is high, tracking budget remains, and there is still time before closest approach.",`: Mentions constraint logic.
- `        "maneuver_guidance": "Prefer the axis that best reduces the visible threats overall, not just one object.",`: Tells model to view situation holistically.
- `        "mission_guidance": "Avoid excessive mission offsets unless collision probability is still meaningfully high.",`: Discourages random moving.
- `    }`: Completes dictionary.
- `    if strategy_memory:`: Appends external strategy text if configured via runner.
- `        strategy_notes["adaptive_strategy_memory"] = strategy_memory`: Sets key.

```python
    return textwrap.dedent(
        f"""
        Strategy notes:
        {json.dumps(strategy_notes, indent=2)}

        Current observation:
        {json.dumps(_observation_payload(observation), indent=2)}

        Recent episode history:
        {history_block}

        Return the next action as strict JSON only.
        """
    ).strip()
```
- `    return textwrap.dedent(`: Formats final block.
- `        f"""`: Template start.
- `        Strategy notes:`: Subheader.
- `        {json.dumps(strategy_notes, indent=2)}`: Dumps notes payload.
- ``: Empty line.
- `        Current observation:`: Subheader.
- `        {json.dumps(_observation_payload(observation), indent=2)}`: Dumps state block.
- ``: Empty line.
- `        Recent episode history:`: Subheader.
- `        {history_block}`: Mounts the recent actions log.
- ``: Empty line.
- `        Return the next action as strict JSON only.`: Reminds model of output rule.
- `        """`: Template end.
- `    ).strip()`: Finishes processing.

```python
def _llm_action(
    client: OpenAI,
    observation: EnvironmentObservation,
    history: list[dict[str, str | float | bool]],
    strategy_memory: list[str] | None = None,
) -> EnvironmentAction:
    global _LAST_REQUEST_TS

    min_interval_seconds = max(60.0 / REQUESTS_PER_MINUTE, REQUEST_GAP_SECONDS)

    for attempt in range(MAX_LLM_RETRIES + 1):
        now = time.monotonic()
        if _LAST_REQUEST_TS is not None:
            elapsed = now - _LAST_REQUEST_TS
```
- `def _llm_action(`: Main driver to fetch action from LLM.
- `    client: OpenAI,`: Inject OpenAI client instance.
- `    observation: EnvironmentObservation,`: Requires simulation state.
- `    history: list[dict[str, str | float | bool]],`: Uses past states.
- `    strategy_memory: list[str] | None = None,`: Takes advanced memory overrides.
- `) -> EnvironmentAction:`: Resolves into validated action model.
- `    global _LAST_REQUEST_TS`: Injects rate limiting clock variable.
- ``: Empty line.
- `    min_interval_seconds = max(60.0 / REQUESTS_PER_MINUTE, REQUEST_GAP_SECONDS)`: Decides wait period based on hard gaps and RPM.
- ``: Empty line.
- `    for attempt in range(MAX_LLM_RETRIES + 1):`: Loop structure to permit retry strategies.
- `        now = time.monotonic()`: Reads the hardware monotonic clock.
- `        if _LAST_REQUEST_TS is not None:`: Compares delta if requests already happened.
- `            elapsed = now - _LAST_REQUEST_TS`: Obtains time since request finished.

```python
            if elapsed < min_interval_seconds:
                time.sleep(min_interval_seconds - elapsed)
        _LAST_REQUEST_TS = time.monotonic()

        prompt = (
            _build_feedback_prompt(observation, history, strategy_memory)
            if ENABLE_HISTORY
            else _build_basic_prompt(observation)
        )
        if attempt > 0:
            prompt += (
                "\n\nIMPORTANT: Return ONLY a valid JSON object with keys "
```
- `            if elapsed < min_interval_seconds:`: Enforces mandatory sleep wait if time delta is too low.
- `                time.sleep(min_interval_seconds - elapsed)`: Pauses thread.
- `        _LAST_REQUEST_TS = time.monotonic()`: Notes execution timestamp.
- ``: Empty line.
- `        prompt = (`: Chooses prompt configuration block based on settings.
- `            _build_feedback_prompt(observation, history, strategy_memory)`: Calls complex generator.
- `            if ENABLE_HISTORY`: Gate logic.
- `            else _build_basic_prompt(observation)`: Uses simple generator instead.
- `        )`: Completes assignment.
- `        if attempt > 0:`: Reacts if we are currently retrying after an error.
- `            prompt += (`: Appends an angry reminder.
- `                "\n\nIMPORTANT: Return ONLY a valid JSON object with keys "`: Reiterates structure rules aggressively.

```python
                '"action_type" and "magnitude". No prose, no markdown, no code fences.'
            )

        try:
            max_tokens = max(MAX_RESPONSE_TOKENS, 640) if attempt > 0 else MAX_RESPONSE_TOKENS
            request_kwargs: dict[str, Any] = {
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                "temperature": TEMPERATURE,
                "max_tokens": max_tokens,
            }
```
- `                '"action_type" and "magnitude". No prose, no markdown, no code fences.'`: Explains exact constraints model violated last turn.
- `            )`: Ends appending text.
- ``: Empty line.
- `        try:`: Initiates actual LLM invocation.
- `            max_tokens = max(MAX_RESPONSE_TOKENS, 640) if attempt > 0 else MAX_RESPONSE_TOKENS`: Grants model larger output budget if attempting repair via chain of thought.
- `            request_kwargs: dict[str, Any] = {`: Declares payload arguments.
- `                "model": MODEL_NAME,`: Names the model identifier.
- `                "messages": [`: Starts array of message chunks.
- `                    {"role": "system", "content": SYSTEM_PROMPT},`: Submits core persona payload.
- `                    {"role": "user", "content": prompt},`: Submits local situational payload.
- `                ],`: Closes list.
- `                "temperature": TEMPERATURE,`: Enforces rigidity parameter.
- `                "max_tokens": max_tokens,`: Enforces generation limit.
- `            }`: Ends initialization of kwargs dictionary.

```python
            if REASONING_EFFORT in {"low", "medium", "high"}:
                request_kwargs["extra_body"] = {"reasoning_effort": REASONING_EFFORT}

            try:
                completion = client.chat.completions.create(
                    **request_kwargs,
                    response_format={"type": "json_object"},
                )
            except Exception as exc:
                if _is_reasoning_effort_error(exc) and "extra_body" in request_kwargs:
                    request_kwargs.pop("extra_body", None)
                    completion = client.chat.completions.create(
                        **request_kwargs,
                        response_format={"type": "json_object"},
                    )
```
- `            if REASONING_EFFORT in {"low", "medium", "high"}:`: Looks for parameter compatible with OpenAI o1-series structures.
- `                request_kwargs["extra_body"] = {"reasoning_effort": REASONING_EFFORT}`: Shims argument into raw extra body mapping.
- ``: Empty line.
- `            try:`: Tries strict JSON generation block.
- `                completion = client.chat.completions.create(`: Sends request directly to API backend.
- `                    **request_kwargs,`: Unpacks parameters.
- `                    response_format={"type": "json_object"},`: Instructs OpenAI-compatible APIs to enforce JSON syntactically.
- `                )`: Closes completion execution block.
- `            except Exception as exc:`: Detects error generating via provider.
- `                if _is_reasoning_effort_error(exc) and "extra_body" in request_kwargs:`: Backtracks if reasoning parameter broke endpoint.
- `                    request_kwargs.pop("extra_body", None)`: Purges problematic argument from payload.
- `                    completion = client.chat.completions.create(`: Tries again.
- `                        **request_kwargs,`: Re-unpacks.
- `                        response_format={"type": "json_object"},`: Strict JSON mode re-invoked.
- `                    )`: Closes fallback try.

```python
                    content = (completion.choices[0].message.content or "").strip()
                    if not content:
                        raise ValueError("empty_llm_content")
                    return _parse_action(content)

                if not _is_json_mode_generation_error(exc):
                    raise

                # Retry once without provider-side JSON mode; we still enforce
                # JSON schema locally via _parse_action.
                try:
                    completion = client.chat.completions.create(**request_kwargs)
                except Exception as retry_exc:
                    if _is_reasoning_effort_error(retry_exc) and "extra_body" in request_kwargs:
```
- `                    content = (completion.choices[0].message.content or "").strip()`: Grabs fallback response.
- `                    if not content:`: Validates presence of text payload.
- `                        raise ValueError("empty_llm_content")`: Forces loop to continue and wait for next attempt.
- `                    return _parse_action(content)`: Evaluates result immediately.
- ``: Empty line.
- `                if not _is_json_mode_generation_error(exc):`: Bypasses to failure if not JSON related error.
- `                    raise`: Drops into outer try loop failure handling.
- ``: Empty line.
- `                # Retry once without provider-side JSON mode; we still enforce`: Comment block explaining strategy.
- `                # JSON schema locally via _parse_action.`: Comment text continuation.
- `                try:`: Attempts unstructured plaintext fallback if provider crashes on strict mode.
- `                    completion = client.chat.completions.create(**request_kwargs)`: Invokes the base call.
- `                except Exception as retry_exc:`: Handles error on non-strict generation.
- `                    if _is_reasoning_effort_error(retry_exc) and "extra_body" in request_kwargs:`: Performs same shim check.

```python
                        request_kwargs.pop("extra_body", None)
                        completion = client.chat.completions.create(**request_kwargs)
                    else:
                        raise

            content = (completion.choices[0].message.content or "").strip()
            if not content:
                raise ValueError("empty_llm_content")
            return _parse_action(content)
        except Exception as exc:
            message = str(exc).lower()
            is_rate_limited = "rate limit" in message or "429" in message
            is_retryable_format = (
                "empty_llm_content" in message
```
- `                        request_kwargs.pop("extra_body", None)`: Pops body from payload.
- `                        completion = client.chat.completions.create(**request_kwargs)`: Re-sends standard payload.
- `                    else:`: Branch for unfixable error on retry.
- `                        raise`: Elevates error.
- ``: Empty line.
- `            content = (completion.choices[0].message.content or "").strip()`: Assumes success and extracts main payload text.
- `            if not content:`: Safeguards against empty replies.
- `                raise ValueError("empty_llm_content")`: Casts exception.
- `            return _parse_action(content)`: Delivers payload directly to the custom regex extractor pipeline.
- `        except Exception as exc:`: Broad catcher for outermost retry mechanism logic.
- `            message = str(exc).lower()`: Makes text comparable.
- `            is_rate_limited = "rate limit" in message or "429" in message`: Checks for throttling logic flags.
- `            is_retryable_format = (`: Detects recoverable parser exceptions locally.
- `                "empty_llm_content" in message`: Finds custom exception.

```python
                or "jsondecodeerror" in message
                or "expecting value" in message
                or "expecting property name" in message
                or "extra data" in message
            )
            if (not is_rate_limited and not is_retryable_format) or attempt >= MAX_LLM_RETRIES:
                raise
            time.sleep(RETRY_BACKOFF_SECONDS * (attempt + 1))

    raise RuntimeError("Failed to get action from LLM after retries.")
```
- `                or "jsondecodeerror" in message`: JSON exception flag.
- `                or "expecting value" in message`: JSON value crash flag.
- `                or "expecting property name" in message`: Syntax failure flag.
- `                or "extra data" in message`: Extra bytes flag.
- `            )`: Closes tuple checking.
- `            if (not is_rate_limited and not is_retryable_format) or attempt >= MAX_LLM_RETRIES:`: Validates we can and should execute retry logic safely.
- `                raise`: Propagates exception upwards and ends script.
- `            time.sleep(RETRY_BACKOFF_SECONDS * (attempt + 1))`: Sleeps based on scaled attempt interval before calling server.
- ``: Empty line.
- `    raise RuntimeError("Failed to get action from LLM after retries.")`: Final failsafe loop exhaustion notification.

```python
def choose_action(
    client: OpenAI | None,
    observation: EnvironmentObservation,
    history: list[dict[str, str | float | bool]],
    strategy_memory: list[str] | None = None,
) -> tuple[EnvironmentAction, Optional[str]]:
    if client is None:
        if not ALLOW_HEURISTIC_FALLBACK:
            raise RuntimeError(
                "LLM client is not configured. Set HF_TOKEN/API_BASE_URL/MODEL_NAME, "
                "or explicitly opt in to fallback with ALLOW_HEURISTIC_FALLBACK=1."
            )
```
- `def choose_action(`: Exposes high-level controller entry point.
- `    client: OpenAI | None,`: Injects client if initialized.
- `    observation: EnvironmentObservation,`: Receives current simulation snapshot.
- `    history: list[dict[str, str | float | bool]],`: Uses action backlog.
- `    strategy_memory: list[str] | None = None,`: Consumes extended agent instructions.
- `) -> tuple[EnvironmentAction, Optional[str]]:`: Returns tuple containing an action and maybe an error note.
- `    if client is None:`: Asserts valid engine is running.
- `        if not ALLOW_HEURISTIC_FALLBACK:`: Checks explicitly for hard fail on engine disconnect.
- `            raise RuntimeError(`: Halts application if unavailable.
- `                "LLM client is not configured. Set HF_TOKEN/API_BASE_URL/MODEL_NAME, "`: Gives reason string.
- `                "or explicitly opt in to fallback with ALLOW_HEURISTIC_FALLBACK=1."`: Suggests workaround.
- `            )`: Ends statement.

```python
        return choose_heuristic_action(observation), None

    try:
        return _llm_action(client, observation, history, strategy_memory), None
    except Exception as exc:
        if _is_model_not_found_error(exc):
            raise RuntimeError(
                "Selected model is unavailable for the current provider/key. "
                f"MODEL_NAME='{MODEL_NAME}', API_BASE_URL='{API_BASE_URL}'."
            ) from exc
        if _is_rate_limit_error(exc):
            raise RuntimeError(
```
- `        return choose_heuristic_action(observation), None`: Skips to baseline solver because no client and fallback is on.
- ``: Empty line.
- `    try:`: Initiates wrapped LLM function execution logic.
- `        return _llm_action(client, observation, history, strategy_memory), None`: Solves action using the generated response payload.
- `    except Exception as exc:`: Recovers from unhandled LLM invocation failure.
- `        if _is_model_not_found_error(exc):`: Catches provider mismatches explicitly.
- `            raise RuntimeError(`: Creates clean error representation.
- `                "Selected model is unavailable for the current provider/key. "`: Text context string.
- `                f"MODEL_NAME='{MODEL_NAME}', API_BASE_URL='{API_BASE_URL}'."`: Variables string context.
- `            ) from exc`: Appends old trace.
- `        if _is_rate_limit_error(exc):`: Traps sustained 429 quota exhaustion.
- `            raise RuntimeError(`: Prompts explicit failure text block.

```python
                "Provider rate limit or quota exceeded for the selected model. "
                f"MODEL_NAME='{MODEL_NAME}', API_BASE_URL='{API_BASE_URL}'. "
                "Try a smaller model, reduce MAX_STEPS/ITERATIVE_ROUNDS, or retry after quota resets."
            ) from exc
        if not ALLOW_HEURISTIC_FALLBACK:
            raise
        fallback = choose_heuristic_action(observation)
        return fallback, _sanitize_error(str(exc))
```
- `                "Provider rate limit or quota exceeded for the selected model. "`: Defines specific rate limit error context.
- `                f"MODEL_NAME='{MODEL_NAME}', API_BASE_URL='{API_BASE_URL}'. "`: Dumps configuration references.
- `                "Try a smaller model, reduce MAX_STEPS/ITERATIVE_ROUNDS, or retry after quota resets."`: Prompts remediation paths.
- `            ) from exc`: Carries base exception.
- `        if not ALLOW_HEURISTIC_FALLBACK:`: Enforces manual fail option.
- `            raise`: Triggers root exception termination.
- `        fallback = choose_heuristic_action(observation)`: Solves current simulation node with standard algorithm.
- `        return fallback, _sanitize_error(str(exc))`: Ships tuple containing the action plus the string error that caused fallback mode.

```python
def run_task(
    task_id: str,
    client: OpenAI | None,
    strategy_memory: list[str] | None = None,
    emit_logs: bool = True,
) -> dict[str, float | str | int | bool | list[float]]:
    env = SpaceDebrisEnv(task_id=task_id, seed=0)
    rewards: list[float] = []
    history: list[dict[str, str | float | bool]] = []
    steps_taken = 0
    success = False
    score = 0.0
    final_state = None
    highest_collision_probability = 1.0
    total_offset_km = 0.0
```
- `def run_task(`: Defines execution block for an entire episode loop.
- `    task_id: str,`: String argument defining difficulty scenario target.
- `    client: OpenAI | None,`: Injects client dependencies.
- `    strategy_memory: list[str] | None = None,`: Stores iterative reflections array.
- `    emit_logs: bool = True,`: Decides if trace is printed.
- `) -> dict[str, float | str | int | bool | list[float]]:`: Guarantees massive dictionary outcome.
- `    env = SpaceDebrisEnv(task_id=task_id, seed=0)`: Starts simulation logic structure in memory locally.
- `    rewards: list[float] = []`: Stores list of intermediate points.
- `    history: list[dict[str, str | float | bool]] = []`: Stores execution ledger logs.
- `    steps_taken = 0`: Counters initialized at zero.
- `    success = False`: End outcome marker defaults to failure.
- `    score = 0.0`: Float parameter tracking cumulative evaluation.
- `    final_state = None`: Snapshot memory element tracking environment closure.
- `    highest_collision_probability = 1.0`: Pessimistic default initialization for single metric trace tracking.
- `    total_offset_km = 0.0`: Pre-populates the deviation accumulator.

```python
    fuel_remaining = 0.0
    tracking_updates_used = 0
    termination_reason = ""

    history_suffix = "-with-history" if ENABLE_HISTORY else "-no-history"
    model_label = (
        f"{MODEL_NAME}{history_suffix}" if client is not None else f"{MODEL_NAME}-fallback-heuristic"
    )
    if emit_logs:
        log_start(task=task_id, env=BENCHMARK, model=model_label)

    try:
        observation = env.reset()
        for step in range(1, MAX_STEPS + 1):
```
- `    fuel_remaining = 0.0`: Captures default fuel initialization.
- `    tracking_updates_used = 0`: Sets base level usage.
- `    termination_reason = ""`: Starts closure log with blank data string.
- ``: Empty line.
- `    history_suffix = "-with-history" if ENABLE_HISTORY else "-no-history"`: Parses run configuration text toggle string.
- `    model_label = (`: Begins assignment for formatting model title tracking string.
- `        f"{MODEL_NAME}{history_suffix}" if client is not None else f"{MODEL_NAME}-fallback-heuristic"`: Attaches parameters identifying client mode usage.
- `    )`: End configuration logic.
- `    if emit_logs:`: Only prints telemetry if output is turned on.
- `        log_start(task=task_id, env=BENCHMARK, model=model_label)`: Prints task instantiation properties string.
- ``: Empty line.
- `    try:`: Encompasses run-loop.
- `        observation = env.reset()`: Resets engine framework and fetches origin view state object.
- `        for step in range(1, MAX_STEPS + 1):`: Loop structure bounding total episode interactions allowed.

```python
            if observation.done:
                break

            action, action_error = choose_action(client, observation, history, strategy_memory)
            result = env.step(action)
            rewards.append(result.reward)
            steps_taken = step
            step_error = result.info.get("last_action_error") or action_error

            if emit_logs:
                log_step(
                    step=step,
                    action=_action_to_string(action),
                    reward=result.reward,
                    done=result.done,
                    error=step_error,
                )
```
- `            if observation.done:`: End immediately if target criteria has been fulfilled early by simulator.
- `                break`: Pops loop.
- ``: Empty line.
- `            action, action_error = choose_action(client, observation, history, strategy_memory)`: Summons controller to decide next phase.
- `            result = env.step(action)`: Actuates decision through simulator.
- `            rewards.append(result.reward)`: Captures immediate point delta value object parameter.
- `            steps_taken = step`: Stores execution turn count integer tracking.
- `            step_error = result.info.get("last_action_error") or action_error`: Prioritizes internal engine logic error over LLM formatting stack errors.
- ``: Empty line.
- `            if emit_logs:`: Outputs step data trace.
- `                log_step(`: Spawns logger message.
- `                    step=step,`: Step log argument.
- `                    action=_action_to_string(action),`: Parsed text value argument log payload.
- `                    reward=result.reward,`: Value target log float argument property.
- `                    done=result.done,`: Indicates episode status boolean metric trace payload structure argument.
- `                    error=step_error,`: Appends failure details argument attribute.
- `                )`: Executes printing logic.

```python
            history.append(
                {
                    "step": step,
                    "action": _action_to_string(action),
                    "reward": round(result.reward, 4),
                    "done": result.done,
                    "error": step_error or "null",
                    "highest_collision_probability": result.observation.highest_collision_probability,
                    "fuel_remaining": result.observation.fuel_remaining,
                    "tracking_budget_remaining": result.observation.tracking_budget_remaining,
                }
            )

            observation = result.observation
            if result.done:
                break
```
- `            history.append(`: Injects into episodic backlog dictionary.
- `                {`: Initiates inner snapshot context argument.
- `                    "step": step,`: Injects turn.
- `                    "action": _action_to_string(action),`: Converts object command to simple string.
- `                    "reward": round(result.reward, 4),`: Records evaluation.
- `                    "done": result.done,`: Stores completion marker flag check structure.
- `                    "error": step_error or "null",`: Appends execution crash notes payload target property string.
- `                    "highest_collision_probability": result.observation.highest_collision_probability,`: Mounts core optimization tracking attribute payload argument metric property.
- `                    "fuel_remaining": result.observation.fuel_remaining,`: Saves fuel snapshot metric property integer format.
- `                    "tracking_budget_remaining": result.observation.tracking_budget_remaining,`: Identifies scanner constraints payload integer context target object tracking string parameter.
- `                }`: Closes trace data object map.
- `            )`: Completes insert operation sequence process logging loop execution tracker.
- ``: Empty line.
- `            observation = result.observation`: Loads generated environment data output context property struct target tracker variable memory attribute property tracker target pointer.
- `            if result.done:`: Terminates if engine finalized execution state sequence logically.
- `                break`: Exits for loop context structure process execution payload block process structure process string logic tracking pointer variable reference logic execution flow memory.

```python
        score = env.grade()
        final_state = env.state()
        success = final_state.success
        highest_collision_probability = max(
            (event.collision_probability for event in final_state.true_events),
            default=0.0,
        )
        total_offset_km = (
            final_state.mission_offsets.radial_km
            + final_state.mission_offsets.along_track_km
            + final_state.mission_offsets.normal_km
        )
        fuel_remaining = final_state.fuel_remaining
        tracking_updates_used = final_state.tracking_updates_used
        termination_reason = final_state.termination_reason or ""
```
- `        score = env.grade()`: Runs external evaluator engine.
- `        final_state = env.state()`: Serializes snapshot into static model logic wrapper pointer variable memory allocation parameter reference context memory payload attribute tracker object context parameter.
- `        success = final_state.success`: Maps task pass tracker value argument tracker.
- `        highest_collision_probability = max(`: Locates max value tracking payload pointer float parameter constraint target string tracker context limit tracker string limit target attribute mapping logic limit metric pointer metric logic limit target value payload argument.
- `            (event.collision_probability for event in final_state.true_events),`: Pulls true events target logic attribute metric object array iterator argument loop target tracker variable target metric mapping limit object variable payload tracker pointer context string map metric reference target value map context pointer target argument value pointer context string map target value parameter payload object pointer limit metric limit.
- `            default=0.0,`: Adds zero-case target failover logic constraint struct.
- `        )`: Returns float value limit metric payload string metric reference value pointer string target float pointer struct string mapping context limit map context value parameter string context logic parameter value string target tracking logic variable string metric limit limit context.
- `        total_offset_km = (`: Accumulates spatial error variables limit value map mapping tracking payload float parameter string structure float string payload mapping metric context target limit structure float object string limit tracker parameter reference pointer value logic value limit limit tracker context pointer struct map logic logic float tracking pointer.
- `            final_state.mission_offsets.radial_km`: Gets offset X pointer mapping structure string target logic metric.
- `            + final_state.mission_offsets.along_track_km`: Adds offset Y value structure logic string parameter target mapping pointer metric.
- `            + final_state.mission_offsets.normal_km`: Adds offset Z pointer reference parameter float target context payload logic float structure mapping tracker logic tracking value structure payload.
- `        )`: Computes final number limit parameter mapping structure tracker logic float parameter limit structure tracker object limit limit reference float mapping target payload string limit mapping limit parameter float logic string.
- `        fuel_remaining = final_state.fuel_remaining`: Maps final unspent metric target parameter tracking context value logic.
- `        tracking_updates_used = final_state.tracking_updates_used`: Maps updates property structure limit payload target tracking float reference float limit value parameter string limit payload context pointer logic value logic tracker target limit target value map target tracker logic string parameter logic metric string structure pointer struct metric tracker float parameter mapping context logic parameter parameter struct float object tracker object target metric logic target value map context parameter metric structure string metric struct tracking tracker tracking structure float map metric pointer context limit string pointer logic map object payload string tracking object target value limit target mapping pointer structure context pointer tracker float target target context payload pointer object tracking structure.
- `        termination_reason = final_state.termination_reason or ""`: Pulls enum limit float value mapping payload.

```python
    finally:
        env.close()
        if emit_logs:
            log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

    return {
        "task_id": task_id,
        "success": success,
        "score": round(score, 4),
        "steps": steps_taken,
        "first_action": str(history[0]["action"]) if history else "",
        "total_reward": round(sum(rewards), 4),
        "rewards": [round(reward, 4) for reward in rewards],
        "termination_reason": termination_reason,
        "highest_collision_probability": round(highest_collision_probability, 4),
        "total_offset_km": round(total_offset_km, 4),
```
- `    finally:`: Invokes post-run logic context structure target payload logic metric reference limit target.
- `        env.close()`: Cleans up internal memory object structure context payload float metric value pointer mapping parameter.
- `        if emit_logs:`: Outputs limit payload structure target context pointer metric mapping limit.
- `            log_end(success=success, steps=steps_taken, score=score, rewards=rewards)`: Evaluates end limits tracking target logic.
- ``: Empty line parameter tracking limit limit metric.
- `    return {`: Emits data logic string target limits struct limit map tracker.
- `        "task_id": task_id,`: Key output struct payload map reference.
- `        "success": success,`: Key object target payload value float.
- `        "score": round(score, 4),`: Rounds output limit structure logic tracking value string map.
- `        "steps": steps_taken,`: Steps limit target reference metric target limit context parameter tracker.
- `        "first_action": str(history[0]["action"]) if history else "",`: Safely accesses target limit logic target logic mapping payload tracker value.
- `        "total_reward": round(sum(rewards), 4),`: Aggregates object limit target string mapping float tracking context string value tracking tracker metric tracker.
- `        "rewards": [round(reward, 4) for reward in rewards],`: Casts object target mapping float target structure.
- `        "termination_reason": termination_reason,`: Sets termination context float value payload string.
- `        "highest_collision_probability": round(highest_collision_probability, 4),`: Records output tracking map metric float mapping value target object tracking context parameter payload float payload float target string value target parameter target float reference context target value structure target logic string value tracker limit logic target tracking metric parameter value float string parameter mapping structure mapping limit limit pointer metric parameter mapping metric logic float payload payload reference object mapping.
- `        "total_offset_km": round(total_offset_km, 4),`: Formats offset context tracker object logic tracking limit value struct.

```python
        "fuel_remaining": round(fuel_remaining, 4),
        "tracking_updates_used": tracking_updates_used,
    }


def main() -> None:
    openai_available = OpenAI is not Any
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY) if (API_KEY and openai_available) else None
    if client is None and not ALLOW_HEURISTIC_FALLBACK:
        if API_KEY and not openai_available:
            raise RuntimeError(
                "OpenAI Python package is not installed in this interpreter. "
                "Install project dependencies (for example `uv sync`) or run in the configured project environment."
            )
        raise RuntimeError(
```
- `        "fuel_remaining": round(fuel_remaining, 4),`: Maps target value object structure mapping tracking value context parameter tracker target reference string float target string tracking parameter tracking target value float logic tracking map metric structure mapping string object limit structure tracking parameter payload tracking target tracker limit mapping tracker parameter tracking limit tracker logic object map float limit string.
- `        "tracking_updates_used": tracking_updates_used,`: Maps usage target target payload limit tracking mapping map.
- `    }`: Completes object struct limit metric float parameter tracking value parameter pointer value tracking float limit.
- ``: Empty line struct float tracker logic parameter target parameter payload.
- ``: Empty line parameter context structure mapping payload object map pointer float payload logic mapping tracking pointer target.
- `def main() -> None:`: Executes primary execution file struct metric structure float logic.
- `    openai_available = OpenAI is not Any`: Assesses optional dependency presence structure limit string tracking.
- `    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY) if (API_KEY and openai_available) else None`: Initializes driver logic context map target limit reference tracker payload.
- `    if client is None and not ALLOW_HEURISTIC_FALLBACK:`: Ensures program failure parameter object payload pointer metric float tracking logic parameter target limit metric mapping tracking map parameter.
- `        if API_KEY and not openai_available:`: Finds logic value pointer map float tracker limit logic.
- `            raise RuntimeError(`: Casts exception context tracking reference tracking metric limit.
- `                "OpenAI Python package is not installed in this interpreter. "`: Returns message context parameter tracking limit metric object.
- `                "Install project dependencies (for example `uv sync`) or run in the configured project environment."`: Extends help tracking context structure target float pointer tracking logic.
- `            )`: Ends fail text block limits logic parameter metric structure mapping pointer.
- `        raise RuntimeError(`: Casts text logic error map tracker pointer tracking metric.

```python
            "Missing API key/API configuration for LLM mode. "
            "Set one of (HF_TOKEN, OPENAI_API_KEY, GROQ_API_KEY, API_KEY) plus API_BASE_URL and MODEL_NAME, "
            "or set ALLOW_HEURISTIC_FALLBACK=1 explicitly."
        )
    if client is not None:
        _validate_model_availability(client)
    for task_id in TASK_IDS:
        run_task(task_id, client, emit_logs=True)


if __name__ == "__main__":
    main()
```
- `            "Missing API key/API configuration for LLM mode. "`: Specifies cause float structure reference context logic.
- `            "Set one of (HF_TOKEN, OPENAI_API_KEY, GROQ_API_KEY, API_KEY) plus API_BASE_URL and MODEL_NAME, "`: Prints options object map value structure logic mapping target limit.
- `            "or set ALLOW_HEURISTIC_FALLBACK=1 explicitly."`: Fallback suggestion metric tracking limit.
- `        )`: Ends context struct logic block context struct target float.
- `    if client is not None:`: Validates active connection struct logic.
- `        _validate_model_availability(client)`: Scans list string logic mapping metric context parameter map value float parameter metric tracking reference limit.
- `    for task_id in TASK_IDS:`: Loops execution struct tracking tracker limit parameter target metric logic pointer struct tracking struct float tracking value mapping parameter metric pointer mapping tracker limit logic map structure string mapping target reference object string value target object pointer mapping tracking value tracking logic float parameter tracker limit limit logic structure parameter tracker.
- `        run_task(task_id, client, emit_logs=True)`: Invokes execution logic float context string structure pointer limit.
- ``: Empty line parameter tracking limit context mapping limit target value tracking structure tracking.
- ``: Empty line map target metric context structure structure tracking value target tracking pointer limit.
- `if __name__ == "__main__":`: Gate tracker struct tracking pointer target value logic tracking pointer target.
- `    main()`: Entry point pointer tracker float tracking float limit tracking target value.
