from __future__ import annotations

import argparse
import json
from pathlib import Path

from orbits_env.baseline import choose_action
from orbits_env.env import SpaceDebrisEnv


def run_task(task_id: str, seed: int = 0) -> dict[str, float | str | int | bool]:
    env = SpaceDebrisEnv(task_id=task_id, seed=seed)
    observation = env.reset()
    total_reward = 0.0
    steps = 0

    while not observation.done:
        action = choose_action(observation)
        result = env.step(action)
        total_reward += result.reward
        steps += 1
        observation = result.observation

    state = env.state()
    total_offset_km = (
        state.mission_offsets.radial_km
        + state.mission_offsets.along_track_km
        + state.mission_offsets.normal_km
    )
    highest_probability = max((event.collision_probability for event in state.true_events), default=0.0)
    return {
        "task_id": task_id,
        "steps": steps,
        "total_reward": round(total_reward, 4),
        "score": env.grade(),
        "collision_occurred": state.collision_occurred,
        "success": state.success,
        "fuel_remaining": round(state.fuel_remaining, 4),
        "tracking_updates_used": state.tracking_updates_used,
        "maneuvers_used": state.maneuvers_used,
        "total_offset_km": round(total_offset_km, 4),
        "highest_collision_probability": round(highest_probability, 4),
        "termination_reason": state.termination_reason or "",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the reproducible baseline policy.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path to save the baseline results as JSON.",
    )
    args = parser.parse_args()

    task_ids = [
        "collision_avoidance_easy",
        "collision_avoidance_medium",
        "collision_avoidance_hard",
    ]
    results = [run_task(task_id) for task_id in task_ids]
    payload = json.dumps(results, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
