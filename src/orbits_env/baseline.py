from __future__ import annotations

from orbits_env.models import ActionType, EnvironmentAction, EnvironmentObservation


def choose_action(observation: EnvironmentObservation) -> EnvironmentAction:
    if not observation.visible_events:
        return EnvironmentAction(action_type=ActionType.NOOP)

    highest_risk = max(observation.visible_events, key=lambda event: event.collision_probability)
    if (
        observation.tracking_budget_remaining > 0
        and observation.tracking_quality < 0.72
        and highest_risk.uncertainty > 0.18
        and highest_risk.time_to_closest_approach >= 2
    ):
        return EnvironmentAction(action_type=ActionType.REQUEST_TRACKING_UPDATE)

    if highest_risk.collision_probability < 0.14:
        return EnvironmentAction(action_type=ActionType.NOOP)

    weighted_axes = {
        ActionType.RADIAL_MANEUVER: 0.0,
        ActionType.ALONG_TRACK_MANEUVER: 0.0,
        ActionType.NORMAL_MANEUVER: 0.0,
    }

    for event in observation.visible_events:
        urgency = 1.15 if event.time_to_closest_approach <= 2 else 1.0
        weighted_axes[ActionType.RADIAL_MANEUVER] += (
            event.collision_probability * urgency * event.radial_effectiveness
        )
        weighted_axes[ActionType.ALONG_TRACK_MANEUVER] += (
            event.collision_probability * urgency * event.along_track_effectiveness
        )
        weighted_axes[ActionType.NORMAL_MANEUVER] += (
            event.collision_probability * urgency * event.normal_effectiveness
        )

    best_action = max(weighted_axes, key=weighted_axes.get)
    total_offset = (
        observation.mission_offsets.radial_km
        + observation.mission_offsets.along_track_km
        + observation.mission_offsets.normal_km
    )
    if total_offset > 1.5 and highest_risk.collision_probability < 0.24:
        return EnvironmentAction(action_type=ActionType.NOOP)

    magnitude = 0.85 if highest_risk.collision_probability > 0.28 else 0.5
    return EnvironmentAction(action_type=best_action, magnitude=magnitude)
