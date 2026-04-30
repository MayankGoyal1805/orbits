# Tutorial: Understanding `models.py`

This document provides a detailed, line-by-line walkthrough of the `src/orbits_env/models.py` file. This module defines the core data structures used by the Orbits Environment, leveraging `pydantic` to ensure robust validation and serialization of environment states, observations, configurations, and actions.

## Imports and Setup

```python
from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field
```
*   `from __future__ import annotations`: This line imports the `annotations` feature from `__future__`, allowing forward references in type hinting without needing to quote them. It ensures that type hints are stored as strings rather than evaluated at definition time.
*   ``: This is a blank line for readability and adherence to Python style guides for separating import blocks.
*   `from enum import Enum`: This line imports the `Enum` class from the built-in `enum` module, which is used to create enumerations representing sets of symbolic names (members) bound to unique, constant values.
*   `from typing import Literal`: This line imports the `Literal` type hint from the `typing` module, which is used to indicate that a variable or parameter has a specific, fixed value.
*   ``: This is another blank line to separate standard library imports from third-party library imports.
*   `from pydantic import BaseModel, Field`: This line imports `BaseModel` and `Field` from the `pydantic` library. `BaseModel` is the base class for defining data models with built-in validation, and `Field` is used to customize and add constraints to individual model fields.

## Action Types

```python

class ActionType(str, Enum):
    NOOP = "noop"
    REQUEST_TRACKING_UPDATE = "request_tracking_update"
    RADIAL_MANEUVER = "radial_maneuver"
    ALONG_TRACK_MANEUVER = "along_track_maneuver"
    NORMAL_MANEUVER = "normal_maneuver"
```
*   ``: This is a blank line separating the class definition from the previous imports.
*   `class ActionType(str, Enum):`: This line defines a new enumeration class named `ActionType` that inherits from both `str` and `Enum`. Inheriting from `str` makes the enumeration members behave like strings, ensuring JSON serialization compatibility out of the box.
*   `    NOOP = "noop"`: This line defines an enumeration member `NOOP` with the string value `"noop"`, representing an action where the agent chooses to do nothing in the current step.
*   `    REQUEST_TRACKING_UPDATE = "request_tracking_update"`: This line defines an enumeration member `REQUEST_TRACKING_UPDATE` with the value `"request_tracking_update"`, representing an action where the agent requests better tracking data for an object.
*   `    RADIAL_MANEUVER = "radial_maneuver"`: This line defines an enumeration member `RADIAL_MANEUVER` with the value `"radial_maneuver"`, representing a spacecraft maneuver along the radial axis (towards or away from the central body).
*   `    ALONG_TRACK_MANEUVER = "along_track_maneuver"`: This line defines an enumeration member `ALONG_TRACK_MANEUVER` with the value `"along_track_maneuver"`, representing a spacecraft maneuver along its direction of travel.
*   `    NORMAL_MANEUVER = "normal_maneuver"`: This line defines an enumeration member `NORMAL_MANEUVER` with the value `"normal_maneuver"`, representing a spacecraft maneuver perpendicular to its orbital plane.

## Geometry Tags

```python

class GeometryTag(str, Enum):
    RADIAL_DOMINANT = "radial_dominant"
    ALONG_TRACK_DOMINANT = "along_track_dominant"
    NORMAL_DOMINANT = "normal_dominant"
    MIXED = "mixed"
```
*   ``: This is a blank line for readability between class definitions.
*   `class GeometryTag(str, Enum):`: This line defines a new string-based enumeration class named `GeometryTag`. This enum categorizes the dominant relative geometry of a potential conjunction event.
*   `    RADIAL_DOMINANT = "radial_dominant"`: This line defines an enumeration member `RADIAL_DOMINANT` with the value `"radial_dominant"`, indicating a conjunction where the radial separation is the most significant factor.
*   `    ALONG_TRACK_DOMINANT = "along_track_dominant"`: This line defines an enumeration member `ALONG_TRACK_DOMINANT` with the value `"along_track_dominant"`, indicating a conjunction where the along-track separation dominates.
*   `    NORMAL_DOMINANT = "normal_dominant"`: This line defines an enumeration member `NORMAL_DOMINANT` with the value `"normal_dominant"`, indicating a conjunction where the out-of-plane (normal) separation is the most critical axis.
*   `    MIXED = "mixed"`: This line defines an enumeration member `MIXED` with the value `"mixed"`, indicating a complex conjunction geometry that does not have a single dominant axis.

## Mission Offsets

```python

class MissionOffsets(BaseModel):
    radial_km: float = Field(default=0.0, ge=0.0)
    along_track_km: float = Field(default=0.0, ge=0.0)
    normal_km: float = Field(default=0.0, ge=0.0)
```
*   ``: This is a blank line for spacing before the next class.
*   `class MissionOffsets(BaseModel):`: This line defines a Pydantic model named `MissionOffsets` inheriting from `BaseModel`, used to represent the current displacement of the spacecraft from its ideal mission orbit.
*   `    radial_km: float = Field(default=0.0, ge=0.0)`: This line defines a floating-point field `radial_km` representing the radial offset in kilometers. It defaults to `0.0` and must be greater than or equal to (`ge`) `0.0` via Pydantic validation.
*   `    along_track_km: float = Field(default=0.0, ge=0.0)`: This line defines a floating-point field `along_track_km` representing the along-track offset in kilometers. It defaults to `0.0` and must be greater than or equal to `0.0`.
*   `    normal_km: float = Field(default=0.0, ge=0.0)`: This line defines a floating-point field `normal_km` representing the normal (cross-track) offset in kilometers. It defaults to `0.0` and must be greater than or equal to `0.0`.

## Conjunction Events

```python

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
```
*   ``: This is a blank line for code organization.
*   `class ConjunctionEvent(BaseModel):`: This line defines a Pydantic model named `ConjunctionEvent` representing a single tracked potential collision between the spacecraft and another object (like debris).
*   `    object_id: str`: This line defines a required string field `object_id` which acts as a unique identifier for the secondary object involved in the conjunction.
*   `    geometry_tag: GeometryTag`: This line defines a required field `geometry_tag` of type `GeometryTag` (the enum defined earlier) to describe the geometric nature of the event.
*   `    collision_probability: float = Field(ge=0.0, le=1.0)`: This line defines a float field for the estimated likelihood of a collision. It uses `Field` to ensure the value remains bounded between `0.0` (impossible) and `1.0` (certain).
*   `    predicted_miss_distance_km: float = Field(ge=0.0)`: This line defines a float field for the estimated distance between objects at their closest point, restricted to be non-negative.
*   `    time_to_closest_approach: int = Field(ge=0)`: This line defines an integer field representing the number of time steps until the closest approach occurs, restricted to non-negative values.
*   `    uncertainty: float = Field(ge=0.0, le=1.0)`: This line defines a float field representing the current confidence/uncertainty in the conjunction prediction, bounded between `0.0` and `1.0`.
*   `    radial_effectiveness: float = Field(ge=0.0, le=1.0)`: This line defines a float field that quantifies how effective a radial maneuver would be in mitigating this specific conjunction risk, bounded between `0.0` and `1.0`.
*   `    along_track_effectiveness: float = Field(ge=0.0, le=1.0)`: This line defines a float field quantifying the effectiveness of an along-track maneuver for this event, bounded between `0.0` and `1.0`.
*   `    normal_effectiveness: float = Field(ge=0.0, le=1.0)`: This line defines a float field quantifying the effectiveness of a normal maneuver for this event, bounded between `0.0` and `1.0`.
*   `    risk_growth_rate: float = Field(ge=0.0, le=0.3)`: This line defines a float field representing how quickly the collision probability might increase over time without intervention, bounded between `0.0` and `0.3`.
*   `    tracking_sensitivity: float = Field(ge=0.0, le=1.0)`: This line defines a float field representing how much requesting a tracking update would reduce uncertainty for this specific event, bounded between `0.0` and `1.0`.

## Environment Actions and Requests

```python

class EnvironmentAction(BaseModel):
    action_type: ActionType
    magnitude: float = Field(default=0.0, ge=0.0, le=1.0)


class ResetRequest(BaseModel):
    task_id: str = "collision_avoidance_easy"
```
*   ``: This is a blank line separating classes.
*   `class EnvironmentAction(BaseModel):`: This line defines a Pydantic model named `EnvironmentAction` to represent a single discrete action taken by the agent at a given step.
*   `    action_type: ActionType`: This line defines a required field `action_type` using the `ActionType` enum, specifying the nature of the action (e.g., maneuver type or tracking request).
*   `    magnitude: float = Field(default=0.0, ge=0.0, le=1.0)`: This line defines a float field for the magnitude (strength or duration) of the action. It defaults to `0.0` and is clamped between `0.0` and `1.0`.
*   ``: This is a blank line for readability.
*   `class ResetRequest(BaseModel):`: This line defines a Pydantic model named `ResetRequest` which encapsulates the payload sent when requesting the environment to reset to a new initial state.
*   `    task_id: str = "collision_avoidance_easy"`: This line defines a string field `task_id` with a default value of `"collision_avoidance_easy"`, specifying which predefined scenario the environment should load upon reset.

## Environment Observations

```python

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
```
*   ``: This is a blank line before the class definition.
*   `class EnvironmentObservation(BaseModel):`: This line defines a Pydantic model named `EnvironmentObservation`, which represents the agent's partial view of the environment state at a given time step.
*   `    task_id: str`: This line defines a required string field indicating the active task configuration.
*   `    step_index: int = Field(ge=0)`: This line defines an integer field `step_index` representing the current turn number, which must be non-negative.
*   `    horizon_remaining: int = Field(ge=0)`: This line defines an integer field representing the number of steps left before the episode automatically terminates.
*   `    fuel_remaining: float = Field(ge=0.0)`: This line defines a float field representing the remaining fuel budget, ensuring it cannot drop below `0.0`.
*   `    tracking_quality: float = Field(ge=0.0, le=1.0)`: This line defines a float field for the overall quality of sensor data, bounded between `0.0` (no data) and `1.0` (perfect data).
*   `    tracking_budget_remaining: int = Field(ge=0)`: This line defines an integer field denoting how many times the agent can still request tracking updates, constrained to be non-negative.
*   `    mission_offsets: MissionOffsets`: This line defines a field holding a nested `MissionOffsets` model, detailing the spacecraft's current deviation from its nominal path.
*   `    total_collision_probability: float = Field(ge=0.0, le=1.0)`: This line defines an aggregated float field for the combined probability of colliding with any tracked object, bounded between `0.0` and `1.0`.
*   `    highest_collision_probability: float = Field(ge=0.0, le=1.0)`: This line defines a float field containing the single highest collision probability among all currently tracked events.
*   `    visible_events: list[ConjunctionEvent]`: This line defines a field as a list of `ConjunctionEvent` models, representing the specific collision risks currently detectable by the agent.
*   `    last_action: ActionType | None = None`: This line defines an optional field storing the `ActionType` executed in the previous step, defaulting to `None` at the start of an episode.
*   `    last_action_error: str | None = None`: This line defines an optional string field for recording error messages if the previous action was invalid, defaulting to `None`.
*   `    done: bool = False`: This line defines a boolean flag indicating whether the episode has ended from the observation's perspective, defaulting to `False`.

## Environment State (Part 1)

```python

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
```
*   ``: This is a blank line for logical separation.
*   `class EnvironmentState(BaseModel):`: This line defines a Pydantic model named `EnvironmentState`, representing the complete, internal source of truth for the simulation at a given step.
*   `    episode_id: str`: This line defines a required string field acting as a unique identifier for the current simulation run.
*   `    task_id: str`: This line defines a required string field indicating which specific scenario is being simulated.
*   `    seed: int`: This line defines a required integer field storing the random seed used to initialize the environment, ensuring reproducibility.
*   `    step_index: int = Field(ge=0)`: This line defines a non-negative integer field tracking the current step number of the simulation.
*   `    horizon: int = Field(ge=1)`: This line defines an integer field for the maximum number of steps allowed in the episode, which must be at least `1`.
*   `    fuel_remaining: float = Field(ge=0.0)`: This line defines a non-negative float field tracking the exact amount of fuel left in the spacecraft.
*   `    tracking_quality: float = Field(ge=0.0, le=1.0)`: This line defines a float field tracking the true, underlying quality of the tracking system, bounded between `0.0` and `1.0`.
*   `    tracking_budget_remaining: int = Field(ge=0)`: This line defines a non-negative integer field tracking the remaining number of tracking requests the agent is allowed to make.
*   `    mission_offsets: MissionOffsets`: This line embeds the `MissionOffsets` model, representing the true physical deviations of the spacecraft from its nominal orbit.

## Environment State (Part 2)

```python
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
```
*   `    true_events: list[ConjunctionEvent]`: This line defines a required field containing a list of `ConjunctionEvent` objects representing the ground-truth list of all conjunctions, irrespective of whether they are visible to the agent.
*   `    cumulative_reward: float = 0.0`: This line defines a float field tracking the total reward accumulated by the agent since the beginning of the episode, initialized to `0.0`.
*   `    last_action: ActionType | None = None`: This line defines an optional field storing the true action applied in the previous step, defaulting to `None`.
*   `    last_action_error: str | None = None`: This line defines an optional string field containing any internal error message generated by the previous action attempt, defaulting to `None`.
*   `    tracking_updates_used: int = 0`: This line defines an integer field counting the total number of tracking updates requested throughout the episode, starting at `0`.
*   `    maneuvers_used: int = 0`: This line defines an integer field counting the total number of physical maneuvers executed, starting at `0`.
*   `    done: bool = False`: This line defines a boolean flag indicating if the simulation episode has definitively concluded, defaulting to `False`.
*   `    termination_reason: str | None = None`: This line defines an optional string field providing the specific reason for episode termination (e.g., "collision", "horizon_reached"), defaulting to `None`.
*   `    collision_occurred: bool = False`: This line defines a boolean flag specifically noting whether a physical collision occurred during the episode, defaulting to `False`.
*   `    success: bool = False`: This line defines a boolean flag indicating whether the agent successfully completed the mission objectives without incident, defaulting to `False`.

## Step Results

```python

class StepResult(BaseModel):
    observation: EnvironmentObservation
    reward: float = Field(ge=0.0, le=1.0)
    done: bool
    info: dict[str, float | int | str | bool]
```
*   ``: This is a blank line separating the class definition.
*   `class StepResult(BaseModel):`: This line defines a Pydantic model named `StepResult`, detailing the payload returned to the agent after taking an action, following the standard Reinforcement Learning interface format.
*   `    observation: EnvironmentObservation`: This line defines a required field embedding the newly computed `EnvironmentObservation` for the next time step.
*   `    reward: float = Field(ge=0.0, le=1.0)`: This line defines a float field for the scalar reward earned specifically from the last action, bounded between `0.0` and `1.0`.
*   `    done: bool`: This line defines a required boolean field signaling whether the episode has ended as a result of the step.
*   `    info: dict[str, float | int | str | bool]`: This line defines a required dictionary field intended to carry arbitrary diagnostic information or auxiliary metrics; the values can be floats, integers, strings, or booleans.

## Task Configuration (Part 1)

```python

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
```
*   ``: This is a blank line separating class definitions.
*   `class TaskConfig(BaseModel):`: This line defines a Pydantic model named `TaskConfig`, used to comprehensively define the static parameters and initial conditions for a specific scenario or difficulty level.
*   `    task_id: str`: This line defines a required string field containing the unique identifier for this specific task configuration.
*   `    difficulty: Literal["easy", "medium", "hard"]`: This line defines a required field constrained by a `Literal` type hint, meaning it must exactly match one of the string values `"easy"`, `"medium"`, or `"hard"`.
*   `    description: str`: This line defines a required string field containing human-readable documentation describing the task's context and objectives.
*   `    horizon: int = Field(ge=1)`: This line defines an integer field specifying the total number of time steps available in the episode, which must be at least `1`.
*   `    initial_fuel: float = Field(gt=0.0)`: This line defines a float field specifying the starting amount of fuel provided to the spacecraft, which must be strictly greater than (`gt`) `0.0`.
*   `    initial_tracking_quality: float = Field(ge=0.0, le=1.0)`: This line defines a float field specifying the tracking quality at the beginning of the episode, bounded between `0.0` and `1.0`.
*   `    tracking_budget: int = Field(ge=0)`: This line defines a non-negative integer field specifying the total number of tracking updates the agent is allowed to make throughout the task.
*   `    visible_event_limit: int = Field(ge=1, default=3)`: This line defines an integer field limiting the number of conjunction events exposed in the observation at any given time, defaulting to `3` and requiring at least `1`.
*   `    fuel_cost_tracking: float = Field(ge=0.0)`: This line defines a non-negative float field specifying the amount of fuel or generic resource consumed by requesting a tracking update.
*   `    maneuver_base_cost: float = Field(ge=0.0)`: This line defines a non-negative float field representing the fixed fuel cost incurred merely by initiating any maneuver, regardless of its magnitude.
*   `    maneuver_variable_cost: float = Field(ge=0.0)`: This line defines a non-negative float field representing the proportional fuel cost scaled by the magnitude of the executed maneuver.
*   `    tracking_improvement: float = Field(ge=0.0, le=1.0)`: This line defines a float field detailing how much tracking quality improves when an update is successfully requested, bounded between `0.0` and `1.0`.

## Task Configuration (Part 2)

```python
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
```
*   `    tracking_decay: float = Field(ge=0.0, le=1.0)`: This line defines a float field representing the rate at which tracking quality naturally degrades each step without an update, bounded between `0.0` and `1.0`.
*   `    uncertainty_reduction_factor: float = Field(ge=0.0, le=1.0)`: This line defines a float field used as a multiplier to reduce event uncertainty when a tracking update is applied, bounded between `0.0` and `1.0`.
*   `    passive_offset_recovery: float = Field(ge=0.0, le=1.0)`: This line defines a float field specifying the fractional amount of mission offset that naturally recovers back to zero per step, bounded between `0.0` and `1.0`.
*   `    mission_offset_penalty_weight: float = Field(ge=0.0)`: This line defines a non-negative float field serving as a scaling weight to penalize the reward function for straying from the ideal mission orbit.
*   `    fuel_penalty_weight: float = Field(ge=0.0)`: This line defines a non-negative float field serving as a scaling weight to penalize the reward function based on fuel consumption.
*   `    risk_reduction_reward_weight: float = Field(ge=0.0)`: This line defines a non-negative float field serving as a scaling weight for rewarding the agent when it successfully decreases collision probabilities.
*   `    tracking_reward_weight: float = Field(ge=0.0)`: This line defines a non-negative float field serving as a scaling weight for rewarding the agent for maintaining high tracking quality.
*   `    unsafe_probability_threshold: float = Field(ge=0.0, le=1.0)`: This line defines a float field setting the collision probability threshold at which the environment considers the situation critically unsafe, bounded between `0.0` and `1.0`.
*   `    success_probability_threshold: float = Field(ge=0.0, le=1.0)`: This line defines a float field setting the maximum allowed collision probability to successfully complete an episode, bounded between `0.0` and `1.0`.
*   `    max_total_offset_km: float = Field(gt=0.0)`: This line defines a positive float field setting the absolute limit on mission drift; exceeding this causes episode failure.
*   `    completion_bonus: float = Field(ge=0.0)`: This line defines a non-negative float field specifying a flat reward added to the score when the agent successfully survives the full horizon.
*   `    collision_penalty: float = Field(ge=0.0)`: This line defines a non-negative float field specifying a large flat penalty deducted from the score if a collision occurs.
*   `    max_magnitude: float = Field(default=1.0, gt=0.0, le=1.0)`: This line defines a float field setting the maximum allowed magnitude for any maneuver action, defaulting to `1.0` and clamped between `0.0` (exclusive) and `1.0` (inclusive).
*   `    conjunctions: list[ConjunctionEvent]`: This line defines a required field as a list of `ConjunctionEvent` objects, representing the initial set of conjunctions that populate the environment at the start of the task.