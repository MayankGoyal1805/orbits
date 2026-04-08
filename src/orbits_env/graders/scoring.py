from __future__ import annotations

from orbits_env.models import EnvironmentState, TaskConfig


def grade_episode(state: EnvironmentState, task: TaskConfig) -> float:
    if state.collision_occurred:
        return 0.0

    highest_probability = max((event.collision_probability for event in state.true_events), default=0.0)
    total_probability = min(1.0, sum(event.collision_probability for event in state.true_events))
    total_offset = (
        state.mission_offsets.radial_km
        + state.mission_offsets.along_track_km
        + state.mission_offsets.normal_km
    )

    safety = max(0.0, 1.0 - (0.65 * highest_probability + 0.35 * total_probability))
    fuel_efficiency = min(1.0, state.fuel_remaining / task.initial_fuel)
    mission_preservation = max(0.0, 1.0 - (total_offset / task.max_total_offset_km))

    tracking_budget_total = max(1, task.tracking_budget)
    tracking_efficiency = max(0.0, 1.0 - (state.tracking_updates_used / tracking_budget_total))
    if highest_probability > task.success_probability_threshold:
        tracking_efficiency *= 0.7

    completion = 1.0 if state.success else 0.35
    score = (
        0.45 * safety
        + 0.2 * fuel_efficiency
        + 0.2 * mission_preservation
        + 0.05 * tracking_efficiency
        + 0.1 * completion
    )
    return round(max(0.0, min(1.0, score)), 4)
