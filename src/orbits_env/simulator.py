from __future__ import annotations

from uuid import uuid4

from orbits_env.models import (
    ActionType,
    ConjunctionEvent,
    EnvironmentAction,
    EnvironmentObservation,
    EnvironmentState,
    MissionOffsets,
    StepResult,
    TaskConfig,
)


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _total_collision_probability(events: list[ConjunctionEvent]) -> float:
    return _clamp(sum(event.collision_probability for event in events))


def _highest_collision_probability(events: list[ConjunctionEvent]) -> float:
    return max((event.collision_probability for event in events), default=0.0)


def _total_offset_km(offsets: MissionOffsets) -> float:
    return offsets.radial_km + offsets.along_track_km + offsets.normal_km


def _axis_effectiveness(event: ConjunctionEvent, action_type: ActionType) -> float:
    if action_type == ActionType.RADIAL_MANEUVER:
        return event.radial_effectiveness
    if action_type == ActionType.ALONG_TRACK_MANEUVER:
        return event.along_track_effectiveness
    if action_type == ActionType.NORMAL_MANEUVER:
        return event.normal_effectiveness
    return 0.0


class ConjunctionSimulator:
    def __init__(self, task: TaskConfig, seed: int = 0):
        self.task = task
        self.seed = seed
        self.state: EnvironmentState | None = None

    def reset(self) -> EnvironmentObservation:
        self.state = EnvironmentState(
            episode_id=f"{self.task.task_id}-{uuid4().hex[:8]}",
            task_id=self.task.task_id,
            seed=self.seed,
            step_index=0,
            horizon=self.task.horizon,
            fuel_remaining=self.task.initial_fuel,
            tracking_quality=self.task.initial_tracking_quality,
            tracking_budget_remaining=self.task.tracking_budget,
            mission_offsets=MissionOffsets(),
            true_events=[event.model_copy(deep=True) for event in self.task.conjunctions],
        )
        return self.observation()

    def observation(self) -> EnvironmentObservation:
        if self.state is None:
            raise RuntimeError("Environment must be reset before requesting observation.")

        visible_events = sorted(
            [self._observe_event(event) for event in self.state.true_events],
            key=lambda event: event.collision_probability,
            reverse=True,
        )[: self.task.visible_event_limit]

        return EnvironmentObservation(
            task_id=self.state.task_id,
            step_index=self.state.step_index,
            horizon_remaining=max(0, self.state.horizon - self.state.step_index),
            fuel_remaining=round(self.state.fuel_remaining, 4),
            tracking_quality=round(self.state.tracking_quality, 4),
            tracking_budget_remaining=self.state.tracking_budget_remaining,
            mission_offsets=self.state.mission_offsets.model_copy(deep=True),
            total_collision_probability=round(_total_collision_probability(self.state.true_events), 4),
            highest_collision_probability=round(_highest_collision_probability(self.state.true_events), 4),
            visible_events=visible_events,
            last_action=self.state.last_action,
            last_action_error=self.state.last_action_error,
            done=self.state.done,
        )

    def step(self, action: EnvironmentAction) -> StepResult:
        if self.state is None:
            raise RuntimeError("Environment must be reset before stepping.")
        if self.state.done:
            raise RuntimeError("Episode is done. Call reset() to start a new episode.")

        magnitude = min(action.magnitude, self.task.max_magnitude)
        previous_total_probability = _total_collision_probability(self.state.true_events)
        previous_uncertainty = sum(event.uncertainty for event in self.state.true_events)

        reward_components = {
            "base": 0.38,
            "risk_reduction": 0.0,
            "tracking_gain": 0.0,
            "fuel_penalty": 0.0,
            "mission_penalty": 0.0,
            "waste_penalty": 0.0,
            "completion_bonus": 0.0,
        }
        info: dict[str, float | int | str | bool] = {"task_id": self.task.task_id}
        self.state.last_action_error = None

        if action.action_type == ActionType.REQUEST_TRACKING_UPDATE:
            self._apply_tracking_update(reward_components, info)
        elif action.action_type in {
            ActionType.RADIAL_MANEUVER,
            ActionType.ALONG_TRACK_MANEUVER,
            ActionType.NORMAL_MANEUVER,
        }:
            self._apply_maneuver(action.action_type, magnitude, reward_components, info)
        else:
            info["noop"] = True
            if _highest_collision_probability(self.state.true_events) > 0.28:
                reward_components["waste_penalty"] += 0.08

        self._advance_dynamics()

        self.state.step_index += 1
        self.state.last_action = action.action_type
        self._check_termination()

        new_total_probability = _total_collision_probability(self.state.true_events)
        risk_reduction = max(0.0, previous_total_probability - new_total_probability)
        reward_components["risk_reduction"] = min(
            0.35, risk_reduction * self.task.risk_reduction_reward_weight
        )

        new_uncertainty = sum(event.uncertainty for event in self.state.true_events)
        if action.action_type == ActionType.REQUEST_TRACKING_UPDATE:
            uncertainty_reduction = max(0.0, previous_uncertainty - new_uncertainty)
            reward_components["tracking_gain"] = min(
                0.14, uncertainty_reduction * self.task.tracking_reward_weight
            )

        if self.state.collision_occurred:
            reward = 0.0
        else:
            if self.state.success:
                reward_components["completion_bonus"] = self.task.completion_bonus
            reward = _clamp(
                reward_components["base"]
                + reward_components["risk_reduction"]
                + reward_components["tracking_gain"]
                + reward_components["completion_bonus"]
                - reward_components["fuel_penalty"]
                - reward_components["mission_penalty"]
                - reward_components["waste_penalty"]
            )

        self.state.cumulative_reward += reward

        info.update(
            {
                "fuel_remaining": round(self.state.fuel_remaining, 4),
                "tracking_quality": round(self.state.tracking_quality, 4),
                "tracking_budget_remaining": self.state.tracking_budget_remaining,
                "total_collision_probability": round(new_total_probability, 4),
                "highest_collision_probability": round(_highest_collision_probability(self.state.true_events), 4),
                "total_offset_km": round(_total_offset_km(self.state.mission_offsets), 4),
                "collision_occurred": self.state.collision_occurred,
                "success": self.state.success,
                "termination_reason": self.state.termination_reason or "",
                "last_action_error": self.state.last_action_error or "",
            }
        )
        observation = self.observation()
        return StepResult(observation=observation, reward=round(reward, 4), done=self.state.done, info=info)

    def _observe_event(self, event: ConjunctionEvent) -> ConjunctionEvent:
        if self.state is None:
            raise RuntimeError("Environment must be reset before requesting observation.")

        conservatism = (1.0 - self.state.tracking_quality) * event.uncertainty * event.tracking_sensitivity
        observed_probability = _clamp(event.collision_probability + 0.35 * conservatism)
        observed_miss_distance = max(0.1, event.predicted_miss_distance_km - 0.6 * conservatism)
        observed_uncertainty = _clamp(event.uncertainty + 0.45 * (1.0 - self.state.tracking_quality))
        return event.model_copy(
            update={
                "collision_probability": round(observed_probability, 4),
                "predicted_miss_distance_km": round(observed_miss_distance, 4),
                "uncertainty": round(observed_uncertainty, 4),
            }
        )

    def _apply_tracking_update(
        self,
        reward_components: dict[str, float],
        info: dict[str, float | int | str | bool],
    ) -> None:
        if self.state is None:
            return

        if self.state.tracking_budget_remaining <= 0:
            reward_components["waste_penalty"] += 0.12
            info["tracking_update"] = False
            info["tracking_budget_exhausted"] = True
            self.state.last_action_error = "tracking_budget_exhausted"
            return

        self.state.tracking_budget_remaining -= 1
        self.state.tracking_updates_used += 1
        self.state.fuel_remaining = max(0.0, self.state.fuel_remaining - self.task.fuel_cost_tracking)
        self.state.tracking_quality = _clamp(
            self.state.tracking_quality + self.task.tracking_improvement
        )

        for event in self.state.true_events:
            event.uncertainty = _clamp(event.uncertainty * self.task.uncertainty_reduction_factor)

        reward_components["fuel_penalty"] += self.task.fuel_penalty_weight * self.task.fuel_cost_tracking
        info["tracking_update"] = True

    def _apply_maneuver(
        self,
        action_type: ActionType,
        magnitude: float,
        reward_components: dict[str, float],
        info: dict[str, float | int | str | bool],
    ) -> None:
        if self.state is None:
            return

        maneuver_cost = self.task.maneuver_base_cost + self.task.maneuver_variable_cost * max(0.2, magnitude)
        self.state.fuel_remaining = max(0.0, self.state.fuel_remaining - maneuver_cost)
        self.state.maneuvers_used += 1
        self._apply_offsets(action_type, magnitude)

        for event in self.state.true_events:
            effectiveness = _axis_effectiveness(event, action_type)
            tracking_factor = 0.7 + 0.3 * self.state.tracking_quality
            timing_factor = 0.92 if event.time_to_closest_approach <= 1 else 1.0
            probability_reduction = magnitude * effectiveness * 0.22 * tracking_factor * timing_factor
            miss_distance_gain = magnitude * effectiveness * 0.85
            uncertainty_reduction = 0.03 * magnitude * effectiveness * self.state.tracking_quality

            event.collision_probability = _clamp(event.collision_probability - probability_reduction)
            event.predicted_miss_distance_km += miss_distance_gain
            event.uncertainty = _clamp(event.uncertainty - uncertainty_reduction)

        reward_components["fuel_penalty"] += self.task.fuel_penalty_weight * maneuver_cost
        reward_components["mission_penalty"] += self.task.mission_offset_penalty_weight * min(
            1.0, _total_offset_km(self.state.mission_offsets) / self.task.max_total_offset_km
        )
        info["maneuver_cost"] = round(maneuver_cost, 4)

    def _apply_offsets(self, action_type: ActionType, magnitude: float) -> None:
        if self.state is None:
            return

        delta = 0.55 * max(0.2, magnitude)
        if action_type == ActionType.RADIAL_MANEUVER:
            self.state.mission_offsets.radial_km += delta
            self.state.mission_offsets.along_track_km += 0.15 * delta
        elif action_type == ActionType.ALONG_TRACK_MANEUVER:
            self.state.mission_offsets.along_track_km += delta
            self.state.mission_offsets.radial_km += 0.12 * delta
        elif action_type == ActionType.NORMAL_MANEUVER:
            self.state.mission_offsets.normal_km += delta
            self.state.mission_offsets.along_track_km += 0.08 * delta

    def _advance_dynamics(self) -> None:
        if self.state is None:
            return

        self.state.tracking_quality = _clamp(self.state.tracking_quality - self.task.tracking_decay)
        self.state.mission_offsets.radial_km *= 1.0 - self.task.passive_offset_recovery
        self.state.mission_offsets.along_track_km *= 1.0 - self.task.passive_offset_recovery
        self.state.mission_offsets.normal_km *= 1.0 - self.task.passive_offset_recovery

        for event in self.state.true_events:
            event.time_to_closest_approach = max(0, event.time_to_closest_approach - 1)
            urgency = 0.12 if event.time_to_closest_approach <= 1 else 0.06 if event.time_to_closest_approach <= 3 else 0.02
            uncertainty_pressure = event.uncertainty * (0.08 + 0.05 * (1.0 - self.state.tracking_quality))
            miss_distance_pressure = 0.02 if event.predicted_miss_distance_km < 1.2 else 0.0

            event.collision_probability = _clamp(
                event.collision_probability
                + event.risk_growth_rate * (0.35 + urgency)
                + uncertainty_pressure
                + miss_distance_pressure
            )
            event.uncertainty = _clamp(
                event.uncertainty + (1.0 - self.state.tracking_quality) * 0.05 * event.tracking_sensitivity
            )
            event.predicted_miss_distance_km = max(0.1, event.predicted_miss_distance_km - 0.11)

    def _check_termination(self) -> None:
        if self.state is None:
            return

        if self.state.fuel_remaining <= 0.0:
            self.state.done = True
            self.state.termination_reason = "fuel_exhausted"
            return

        if _total_offset_km(self.state.mission_offsets) > self.task.max_total_offset_km * 1.35:
            self.state.done = True
            self.state.termination_reason = "mission_deviation_limit_exceeded"
            return

        imminent_collision = next(
            (
                event
                for event in self.state.true_events
                if event.time_to_closest_approach == 0
                and event.collision_probability >= self.task.unsafe_probability_threshold
            ),
            None,
        )
        if imminent_collision is not None:
            self.state.done = True
            self.state.collision_occurred = True
            self.state.termination_reason = "collision"
            return

        all_events_resolved = all(event.time_to_closest_approach == 0 for event in self.state.true_events)
        reached_horizon = self.state.step_index >= self.state.horizon
        if not (all_events_resolved or reached_horizon):
            return

        self.state.done = True
        residual_probability = _highest_collision_probability(self.state.true_events)
        offset_ok = _total_offset_km(self.state.mission_offsets) <= self.task.max_total_offset_km
        self.state.success = residual_probability <= self.task.success_probability_threshold and offset_ok
        self.state.termination_reason = "safe_completion" if self.state.success else "horizon_reached"
