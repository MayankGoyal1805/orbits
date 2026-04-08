from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class ActionType(str, Enum):
    NOOP = "noop"
    REQUEST_TRACKING_UPDATE = "request_tracking_update"
    RADIAL_MANEUVER = "radial_maneuver"
    ALONG_TRACK_MANEUVER = "along_track_maneuver"
    NORMAL_MANEUVER = "normal_maneuver"


class GeometryTag(str, Enum):
    RADIAL_DOMINANT = "radial_dominant"
    ALONG_TRACK_DOMINANT = "along_track_dominant"
    NORMAL_DOMINANT = "normal_dominant"
    MIXED = "mixed"


class MissionOffsets(BaseModel):
    radial_km: float = Field(default=0.0, ge=0.0)
    along_track_km: float = Field(default=0.0, ge=0.0)
    normal_km: float = Field(default=0.0, ge=0.0)


class ConjunctionEvent(BaseModel):
    object_id: str
    geometry_tag: GeometryTag
    collision_probability: float = Field(ge=0.0, le=1.0)
    predicted_miss_distance_km: float = Field(ge=0.0)
    time_to_closest_approach: int = Field(ge=0)
    uncertainty: float = Field(ge=0.0, le=1.0)
    radial_effectiveness: float = Field(ge=0.0, le=1.0)
    along_track_effectiveness: float = Field(ge=0.0, le=1.0)
    normal_effectiveness: float = Field(ge=0.0, le=1.0)
    risk_growth_rate: float = Field(ge=0.0, le=0.3)
    tracking_sensitivity: float = Field(ge=0.0, le=1.0)


class EnvironmentAction(BaseModel):
    action_type: ActionType
    magnitude: float = Field(default=0.0, ge=0.0, le=1.0)


class ResetRequest(BaseModel):
    task_id: str = "collision_avoidance_easy"


class EnvironmentObservation(BaseModel):
    task_id: str
    step_index: int = Field(ge=0)
    horizon_remaining: int = Field(ge=0)
    fuel_remaining: float = Field(ge=0.0)
    tracking_quality: float = Field(ge=0.0, le=1.0)
    tracking_budget_remaining: int = Field(ge=0)
    mission_offsets: MissionOffsets
    total_collision_probability: float = Field(ge=0.0, le=1.0)
    highest_collision_probability: float = Field(ge=0.0, le=1.0)
    visible_events: list[ConjunctionEvent]
    last_action: ActionType | None = None
    last_action_error: str | None = None
    done: bool = False


class EnvironmentState(BaseModel):
    episode_id: str
    task_id: str
    seed: int
    step_index: int = Field(ge=0)
    horizon: int = Field(ge=1)
    fuel_remaining: float = Field(ge=0.0)
    tracking_quality: float = Field(ge=0.0, le=1.0)
    tracking_budget_remaining: int = Field(ge=0)
    mission_offsets: MissionOffsets
    true_events: list[ConjunctionEvent]
    cumulative_reward: float = 0.0
    last_action: ActionType | None = None
    last_action_error: str | None = None
    tracking_updates_used: int = 0
    maneuvers_used: int = 0
    done: bool = False
    termination_reason: str | None = None
    collision_occurred: bool = False
    success: bool = False


class StepResult(BaseModel):
    observation: EnvironmentObservation
    reward: float = Field(ge=0.0, le=1.0)
    done: bool
    info: dict[str, float | int | str | bool]


class TaskConfig(BaseModel):
    task_id: str
    difficulty: Literal["easy", "medium", "hard"]
    description: str
    horizon: int = Field(ge=1)
    initial_fuel: float = Field(gt=0.0)
    initial_tracking_quality: float = Field(ge=0.0, le=1.0)
    tracking_budget: int = Field(ge=0)
    visible_event_limit: int = Field(ge=1, default=3)
    fuel_cost_tracking: float = Field(ge=0.0)
    maneuver_base_cost: float = Field(ge=0.0)
    maneuver_variable_cost: float = Field(ge=0.0)
    tracking_improvement: float = Field(ge=0.0, le=1.0)
    tracking_decay: float = Field(ge=0.0, le=1.0)
    uncertainty_reduction_factor: float = Field(ge=0.0, le=1.0)
    passive_offset_recovery: float = Field(ge=0.0, le=1.0)
    mission_offset_penalty_weight: float = Field(ge=0.0)
    fuel_penalty_weight: float = Field(ge=0.0)
    risk_reduction_reward_weight: float = Field(ge=0.0)
    tracking_reward_weight: float = Field(ge=0.0)
    unsafe_probability_threshold: float = Field(ge=0.0, le=1.0)
    success_probability_threshold: float = Field(ge=0.0, le=1.0)
    max_total_offset_km: float = Field(gt=0.0)
    completion_bonus: float = Field(ge=0.0)
    collision_penalty: float = Field(ge=0.0)
    max_magnitude: float = Field(default=1.0, gt=0.0, le=1.0)
    conjunctions: list[ConjunctionEvent]
