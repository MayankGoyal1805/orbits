from __future__ import annotations

from orbits_env.models import EnvironmentAction
from server.app import close, grade, health, reset, reset_default, state, step, task_detail


def test_health() -> None:
    assert health() == {"status": "ok"}


def test_reset_step_state_cycle() -> None:
    reset_payload = reset_default()
    assert reset_payload["task_id"] == "collision_avoidance_easy"

    medium_reset = reset("collision_avoidance_medium")
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
