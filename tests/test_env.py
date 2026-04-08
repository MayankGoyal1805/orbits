from __future__ import annotations

from orbits_env.env import SpaceDebrisEnv
from orbits_env.models import ActionType, EnvironmentAction


def test_reset_returns_first_observation() -> None:
    env = SpaceDebrisEnv(task_id="collision_avoidance_easy", seed=0)
    observation = env.reset()

    assert observation.task_id == "collision_avoidance_easy"
    assert observation.step_index == 0
    assert observation.horizon_remaining == 6
    assert observation.done is False
    assert len(observation.visible_events) == 1
    assert observation.tracking_budget_remaining == 2


def test_step_advances_state() -> None:
    env = SpaceDebrisEnv(task_id="collision_avoidance_easy", seed=0)
    env.reset()
    result = env.step(
        EnvironmentAction(action_type=ActionType.REQUEST_TRACKING_UPDATE, magnitude=0.0)
    )

    assert result.done is False
    assert result.observation.step_index == 1
    assert result.info["tracking_update"] is True
    assert result.observation.tracking_budget_remaining == 1


def test_baseline_like_rollout_completes() -> None:
    env = SpaceDebrisEnv(task_id="collision_avoidance_medium", seed=0)
    observation = env.reset()

    while not observation.done:
        highest_risk = max(
            observation.visible_events, key=lambda event: event.collision_probability
        )
        action_type = (
            ActionType.ALONG_TRACK_MANEUVER
            if highest_risk.along_track_effectiveness >= highest_risk.radial_effectiveness
            else ActionType.RADIAL_MANEUVER
        )
        observation = env.step(EnvironmentAction(action_type=action_type, magnitude=0.4)).observation

    state = env.state()
    assert state.done is True
    assert state.termination_reason is not None
    assert state.mission_offsets.radial_km >= 0.0
