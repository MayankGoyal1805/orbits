# Tutorial: `/home/mayank/repos/orbits/scripts/run_baseline.py`

## Concepts and Setup
This document provides a comprehensive line-by-line breakdown and tutorial for the script. It explores the concepts of operations, setup phases, environment configuration, and specific syntactical elements involved. Ensure you have the required dependencies installed and your Python environment appropriately activated before running this script.

## Code Explanation

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path

from orbits_env.baseline import choose_action
from orbits_env.env import SpaceDebrisEnv


```

* `from __future__ import annotations
`: Enables forward compatibility for language features, ensuring modern syntax like postponed evaluation of annotations.
* `
`: Empty line or whitespace.
* `import argparse
`: Imports dependencies required for the script: import argparse.
* `import json
`: Imports dependencies required for the script: import json.
* `from pathlib import Path
`: Imports dependencies required for the script: from pathlib import Path.
* `
`: Empty line or whitespace.
* `from orbits_env.baseline import choose_action
`: Imports dependencies required for the script: from orbits_env.baseline import choose_action.
* `from orbits_env.env import SpaceDebrisEnv
`: Imports dependencies required for the script: from orbits_env.env import SpaceDebrisEnv.
* `
`: Empty line or whitespace.
* `
`: Empty line or whitespace.

```python
def run_task(task_id: str, seed: int = 0) -> dict[str, float | str | int | bool]:
    env = SpaceDebrisEnv(task_id=task_id, seed=seed)
    observation = env.reset()
    total_reward = 0.0
    steps = 0

    while not observation.done:
        action = choose_action(observation)
        result = env.step(action)
        total_reward += result.reward
```

* `def run_task(task_id: str, seed: int = 0) -> dict[str, float | str | int | bool]:
`: Defines a function or method signature: def run_task(task_id: str, seed: int = 0) -> dict[str, float | str | int | bool]:.
* `    env = SpaceDebrisEnv(task_id=task_id, seed=seed)
`: Assigns a evaluated value to a variable or state property.
* `    observation = env.reset()
`: Assigns a evaluated value to a variable or state property.
* `    total_reward = 0.0
`: Assigns a evaluated value to a variable or state property.
* `    steps = 0
`: Assigns a evaluated value to a variable or state property.
* `
`: Empty line or whitespace.
* `    while not observation.done:
`: Starts a loop over an iterable, condition, or generation step.
* `        action = choose_action(observation)
`: Assigns a evaluated value to a variable or state property.
* `        result = env.step(action)
`: Assigns a evaluated value to a variable or state property.
* `        total_reward += result.reward
`: Assigns a evaluated value to a variable or state property.

```python
        steps += 1
        observation = result.observation

    state = env.state()
    total_offset_km = (
        state.mission_offsets.radial_km
        + state.mission_offsets.along_track_km
        + state.mission_offsets.normal_km
    )
    highest_probability = max((event.collision_probability for event in state.true_events), default=0.0)
```

* `        steps += 1
`: Assigns a evaluated value to a variable or state property.
* `        observation = result.observation
`: Assigns a evaluated value to a variable or state property.
* `
`: Empty line or whitespace.
* `    state = env.state()
`: Assigns a evaluated value to a variable or state property.
* `    total_offset_km = (
`: Assigns a evaluated value to a variable or state property.
* `        state.mission_offsets.radial_km
`: Executes the statement, evaluates an expression, or continues a multi-line block: state.mission_offsets.radial_km.
* `        + state.mission_offsets.along_track_km
`: Executes the statement, evaluates an expression, or continues a multi-line block: + state.mission_offsets.along_track_km.
* `        + state.mission_offsets.normal_km
`: Executes the statement, evaluates an expression, or continues a multi-line block: + state.mission_offsets.normal_km.
* `    )
`: Executes the statement, evaluates an expression, or continues a multi-line block: ).
* `    highest_probability = max((event.collision_probability for event in state.true_events), default=0.0)
`: Assigns a evaluated value to a variable or state property.

```python
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
```

* `    return {
`: Returns a computed value or state from the function: return {.
* `        "task_id": task_id,
`: Executes the statement, evaluates an expression, or continues a multi-line block: "task_id": task_id,.
* `        "steps": steps,
`: Executes the statement, evaluates an expression, or continues a multi-line block: "steps": steps,.
* `        "total_reward": round(total_reward, 4),
`: Executes the statement, evaluates an expression, or continues a multi-line block: "total_reward": round(total_reward, 4),.
* `        "score": env.grade(),
`: Executes the statement, evaluates an expression, or continues a multi-line block: "score": env.grade(),.
* `        "collision_occurred": state.collision_occurred,
`: Executes the statement, evaluates an expression, or continues a multi-line block: "collision_occurred": state.collision_occurred,.
* `        "success": state.success,
`: Executes the statement, evaluates an expression, or continues a multi-line block: "success": state.success,.
* `        "fuel_remaining": round(state.fuel_remaining, 4),
`: Executes the statement, evaluates an expression, or continues a multi-line block: "fuel_remaining": round(state.fuel_remaining, 4),.
* `        "tracking_updates_used": state.tracking_updates_used,
`: Executes the statement, evaluates an expression, or continues a multi-line block: "tracking_updates_used": state.tracking_updates_used,.
* `        "maneuvers_used": state.maneuvers_used,
`: Executes the statement, evaluates an expression, or continues a multi-line block: "maneuvers_used": state.maneuvers_used,.

```python
        "total_offset_km": round(total_offset_km, 4),
        "highest_collision_probability": round(highest_probability, 4),
        "termination_reason": state.termination_reason or "",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the reproducible baseline policy.")
    parser.add_argument(
        "--output",
```

* `        "total_offset_km": round(total_offset_km, 4),
`: Executes the statement, evaluates an expression, or continues a multi-line block: "total_offset_km": round(total_offset_km, 4),.
* `        "highest_collision_probability": round(highest_probability, 4),
`: Executes the statement, evaluates an expression, or continues a multi-line block: "highest_collision_probability": round(highest_probability, 4),.
* `        "termination_reason": state.termination_reason or "",
`: Executes the statement, evaluates an expression, or continues a multi-line block: "termination_reason": state.termination_reason or "",.
* `    }
`: Executes the statement, evaluates an expression, or continues a multi-line block: }.
* `
`: Empty line or whitespace.
* `
`: Empty line or whitespace.
* `def main() -> None:
`: Defines a function or method signature: def main() -> None:.
* `    parser = argparse.ArgumentParser(description="Run the reproducible baseline policy.")
`: Assigns a evaluated value to a variable or state property.
* `    parser.add_argument(
`: Executes the statement, evaluates an expression, or continues a multi-line block: parser.add_argument(.
* `        "--output",
`: Executes the statement, evaluates an expression, or continues a multi-line block: "--output",.

```python
        type=Path,
        default=None,
        help="Optional path to save the baseline results as JSON.",
    )
    args = parser.parse_args()

    task_ids = [
        "collision_avoidance_easy",
        "collision_avoidance_medium",
        "collision_avoidance_hard",
```

* `        type=Path,
`: Assigns a evaluated value to a variable or state property.
* `        default=None,
`: Assigns a evaluated value to a variable or state property.
* `        help="Optional path to save the baseline results as JSON.",
`: Assigns a evaluated value to a variable or state property.
* `    )
`: Executes the statement, evaluates an expression, or continues a multi-line block: ).
* `    args = parser.parse_args()
`: Assigns a evaluated value to a variable or state property.
* `
`: Empty line or whitespace.
* `    task_ids = [
`: Assigns a evaluated value to a variable or state property.
* `        "collision_avoidance_easy",
`: Executes the statement, evaluates an expression, or continues a multi-line block: "collision_avoidance_easy",.
* `        "collision_avoidance_medium",
`: Executes the statement, evaluates an expression, or continues a multi-line block: "collision_avoidance_medium",.
* `        "collision_avoidance_hard",
`: Executes the statement, evaluates an expression, or continues a multi-line block: "collision_avoidance_hard",.

```python
    ]
    results = [run_task(task_id) for task_id in task_ids]
    payload = json.dumps(results, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__":
```

* `    ]
`: Executes the statement, evaluates an expression, or continues a multi-line block: ].
* `    results = [run_task(task_id) for task_id in task_ids]
`: Assigns a evaluated value to a variable or state property.
* `    payload = json.dumps(results, indent=2)
`: Assigns a evaluated value to a variable or state property.
* `    if args.output is not None:
`: Starts a conditional branching block to control the execution flow.
* `        args.output.parent.mkdir(parents=True, exist_ok=True)
`: Assigns a evaluated value to a variable or state property.
* `        args.output.write_text(payload + "\n", encoding="utf-8")
`: Assigns a evaluated value to a variable or state property.
* `    print(payload)
`: Prints a message or value to the console output for logging or monitoring.
* `
`: Empty line or whitespace.
* `
`: Empty line or whitespace.
* `if __name__ == "__main__":
`: Checks if the script is executed directly (not imported as a module).

```python
    main()
```

* `    main()
`: Executes the statement, evaluates an expression, or continues a multi-line block: main().

