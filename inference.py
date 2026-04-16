from __future__ import annotations

import json
import os
import sys
import textwrap
import time
from typing import Optional

from openai import OpenAI

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from orbits_env.baseline import choose_action as choose_heuristic_action
from orbits_env.env import SpaceDebrisEnv
from orbits_env.models import ActionType, EnvironmentAction, EnvironmentObservation


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

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key:
                    os.environ.setdefault(key, value)
    except OSError:
        # .env loading is best-effort only.
        return


_load_dotenv_if_present()

API_BASE_URL = os.getenv("API_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
API_KEY = os.getenv("HF_TOKEN")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")
BENCHMARK = "orbits-openenv"
MAX_STEPS = int(os.getenv("MAX_STEPS", "12"))
REQUESTS_PER_MINUTE = max(1, int(os.getenv("REQUESTS_PER_MINUTE", "30")))
REQUEST_GAP_SECONDS = max(0.0, float(os.getenv("REQUEST_GAP_SECONDS", "2.5")))
MAX_LLM_RETRIES = max(0, int(os.getenv("MAX_LLM_RETRIES", "2")))
RETRY_BACKOFF_SECONDS = max(0.0, float(os.getenv("RETRY_BACKOFF_SECONDS", "1.5")))
MAX_RESPONSE_TOKENS = max(32, int(os.getenv("MAX_RESPONSE_TOKENS", "120")))
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


def _sanitize_error(error: str) -> str:
    return error.replace("\n", " ").replace("\r", " ").strip() or "null"


def _action_to_string(action: EnvironmentAction) -> str:
    if action.action_type in {ActionType.NOOP, ActionType.REQUEST_TRACKING_UPDATE}:
        return action.action_type.value
    return f"{action.action_type.value}({action.magnitude:.2f})"


def _parse_action(raw_text: str) -> EnvironmentAction:
    payload = json.loads(raw_text)
    action_type = payload.get("action_type", ActionType.NOOP)
    magnitude = payload.get("magnitude", 0.0)
    return EnvironmentAction(action_type=action_type, magnitude=magnitude)


def _build_basic_prompt(observation: EnvironmentObservation) -> str:
    return textwrap.dedent(
        f"""
        Current observation:
        {json.dumps(_observation_payload(observation), indent=2)}

        Return the next action as strict JSON only.
        """
    ).strip()


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
            if elapsed < min_interval_seconds:
                time.sleep(min_interval_seconds - elapsed)
        _LAST_REQUEST_TS = time.monotonic()

        try:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": (
                            _build_feedback_prompt(observation, history, strategy_memory)
                            if ENABLE_HISTORY
                            else _build_basic_prompt(observation)
                        ),
                    },
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_RESPONSE_TOKENS,
                response_format={"type": "json_object"},
            )
            content = (completion.choices[0].message.content or "").strip()
            return _parse_action(content)
        except Exception as exc:
            message = str(exc).lower()
            is_rate_limited = "rate limit" in message or "429" in message
            if not is_rate_limited or attempt >= MAX_LLM_RETRIES:
                raise
            time.sleep(RETRY_BACKOFF_SECONDS * (attempt + 1))

    raise RuntimeError("Failed to get action from LLM after retries.")


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
        return choose_heuristic_action(observation), None

    try:
        return _llm_action(client, observation, history, strategy_memory), None
    except Exception as exc:
        if not ALLOW_HEURISTIC_FALLBACK:
            raise
        fallback = choose_heuristic_action(observation)
        return fallback, _sanitize_error(str(exc))


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
    finally:
        env.close()
        if emit_logs:
            log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

    return {
        "task_id": task_id,
        "success": success,
        "score": round(score, 4),
        "steps": steps_taken,
        "total_reward": round(sum(rewards), 4),
        "rewards": [round(reward, 4) for reward in rewards],
        "termination_reason": termination_reason,
        "highest_collision_probability": round(highest_collision_probability, 4),
        "total_offset_km": round(total_offset_km, 4),
        "fuel_remaining": round(fuel_remaining, 4),
        "tracking_updates_used": tracking_updates_used,
    }


def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY) if API_KEY else None
    if client is None and not ALLOW_HEURISTIC_FALLBACK:
        raise RuntimeError(
            "Missing HF_TOKEN/API configuration for LLM mode. "
            "Set env vars (HF_TOKEN, API_BASE_URL, MODEL_NAME) or set ALLOW_HEURISTIC_FALLBACK=1 explicitly."
        )
    for task_id in TASK_IDS:
        run_task(task_id, client, emit_logs=True)


if __name__ == "__main__":
    main()
