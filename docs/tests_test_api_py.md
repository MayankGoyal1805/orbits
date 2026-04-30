# Tutorial: `tests/test_api.py`

This document provides a line-by-line explanation of `tests/test_api.py`, detailing its concepts and setup.

```python
from __future__ import annotations

from orbits_env.models import EnvironmentAction
from server.app import close, grade, health, reset, reset_default, state, step, task_detail


def test_health() -> None:
    assert health() == {"status": "ok"}


def test_reset_step_state_cycle() -> None:
    reset_payload = reset_default()
    assert reset_payload["task_id"] == "collision_avoidance_easy"

    medium_reset = reset("collision_avoidance_medium")
```
- `from __future__ import annotations`: Employs modern type hint evaluation syntax.
- ``: An empty line for spacing.
- `from orbits_env.models import EnvironmentAction`: Imports the Pydantic type class to instantiate strictly validated action payloads.
- `from server.app import close, grade, health, reset, reset_default, state, step, task_detail`: Pulls in the core API endpoint methods defined in the server application to test them directly.
- ``: An empty line for spacing.
- ``: An empty line for spacing.
- `def test_health() -> None:`: Initiates a test function specifically validating the health-check capability.
- `    assert health() == {"status": "ok"}`: Executes the health endpoint and asserts it strictly returns the expected liveness dictionary.
- ``: An empty line for spacing.
- ``: An empty line for spacing.
- `def test_reset_step_state_cycle() -> None:`: Begins a comprehensive test method to simulate a full environment lifecycle.
- `    reset_payload = reset_default()`: Sends a request to the server to reset and start a new simulation with the default configuration.
- `    assert reset_payload["task_id"] == "collision_avoidance_easy"`: Affirms that the default configuration resolves to the "easy" difficulty task.
- ``: An empty line for spacing.
- `    medium_reset = reset("collision_avoidance_medium")`: Directly invokes a reset passing a specific task identifier to configure the environment.

```python
    assert medium_reset["task_id"] == "collision_avoidance_medium"

    reset_payload = reset("collision_avoidance_easy")
    assert reset_payload["task_id"] == "collision_avoidance_easy"

    step_payload = step(EnvironmentAction(action_type="radial_maneuver", magnitude=0.5))
    assert "reward" in step_payload

    state_payload = state()
    assert state_payload["task_id"] == "collision_avoidance_easy"
    assert "score" in grade()
    assert task_detail("collision_avoidance_easy")["difficulty"] == "easy"
    assert close() == {"closed": True}
```
- `    assert medium_reset["task_id"] == "collision_avoidance_medium"`: Confirms the environment correctly initialized the requested medium difficulty task.
- ``: An empty line for spacing.
- `    reset_payload = reset("collision_avoidance_easy")`: Resets the environment once more to return it to the easy difficulty baseline for further testing.
- `    assert reset_payload["task_id"] == "collision_avoidance_easy"`: Validates the reset successfully reverted the environment state to the desired task.
- ``: An empty line for spacing.
- `    step_payload = step(EnvironmentAction(action_type="radial_maneuver", magnitude=0.5))`: Invokes a single simulation step utilizing a created `EnvironmentAction` object containing a validated payload.
- `    assert "reward" in step_payload`: Verifies the simulation successfully processed the action and generated an observation dictionary containing a calculated reward value.
- ``: An empty line for spacing.
- `    state_payload = state()`: Requests the active, fully serialized state of the current environment session.
- `    assert state_payload["task_id"] == "collision_avoidance_easy"`: Asserts the fetched environment state maintains consistency with the ongoing initialized task.
- `    assert "score" in grade()`: Calls the grading endpoint to calculate performance and verifies the response includes the final metric string.
- `    assert task_detail("collision_avoidance_easy")["difficulty"] == "easy"`: Inspects the task metadata endpoint to confirm the static details associated with the specified task are accurate.
- `    assert close() == {"closed": True}`: Gracefully terminates the running environment and asserts the closure operation was reported as successful.
