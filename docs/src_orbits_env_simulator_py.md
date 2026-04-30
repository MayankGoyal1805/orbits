# Tutorial: simulator.py

This document provides a detailed, line-by-line explanation of `simulator.py`. This tutorial is essential for understanding the core concepts and setup of the file.

```python
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
```

### Explanation

- **Line 1** (`from __future__ import annotations`): This line imports necessary modules or classes required for the functionality in this file. It ensures all dependencies are available in the current namespace.
- **Line 2** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 3** (`from uuid import uuid4`): This line imports necessary modules or classes required for the functionality in this file. It ensures all dependencies are available in the current namespace.
- **Line 4** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 5** (`from orbits_env.models import (`): This line imports necessary modules or classes required for the functionality in this file. It ensures all dependencies are available in the current namespace.
- **Line 6** (`ActionType,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 7** (`ConjunctionEvent,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 8** (`EnvironmentAction,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 9** (`EnvironmentObservation,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 10** (`EnvironmentState,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 11** (`MissionOffsets,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 12** (`StepResult,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.

```python
    TaskConfig,
)


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _total_collision_probability(events: list[ConjunctionEvent]) -> float:
    return _clamp(sum(event.collision_probability for event in events))


```

### Explanation

- **Line 13** (`TaskConfig,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 14** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 15** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 16** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 17** (`def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 18** (`return max(low, min(high, value))`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 19** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 20** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 21** (`def _total_collision_probability(events: list[ConjunctionEvent]) -> float:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 22** (`return _clamp(sum(event.collision_probability for event in events))`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 23** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 24** (Blank line): This is a blank line, used to separate logical sections of code for better readability.

```python
def _highest_collision_probability(events: list[ConjunctionEvent]) -> float:
    return max((event.collision_probability for event in events), default=0.0)


def _total_offset_km(offsets: MissionOffsets) -> float:
    return offsets.radial_km + offsets.along_track_km + offsets.normal_km


def _axis_effectiveness(event: ConjunctionEvent, action_type: ActionType) -> float:
    if action_type == ActionType.RADIAL_MANEUVER:
        return event.radial_effectiveness
    if action_type == ActionType.ALONG_TRACK_MANEUVER:
```

### Explanation

- **Line 25** (`def _highest_collision_probability(events: list[ConjunctionEvent]) -> float:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 26** (`return max((event.collision_probability for event in events), default=0.0)`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 27** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 28** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 29** (`def _total_offset_km(offsets: MissionOffsets) -> float:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 30** (`return offsets.radial_km + offsets.along_track_km + offsets.normal_km`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 31** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 32** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 33** (`def _axis_effectiveness(event: ConjunctionEvent, action_type: ActionType) -> float:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 34** (`if action_type == ActionType.RADIAL_MANEUVER:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 35** (`return event.radial_effectiveness`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 36** (`if action_type == ActionType.ALONG_TRACK_MANEUVER:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.

```python
        return event.along_track_effectiveness
    if action_type == ActionType.NORMAL_MANEUVER:
        return event.normal_effectiveness
    return 0.0


class ConjunctionSimulator:
    def __init__(self, task: TaskConfig, seed: int = 0):
        self.task = task
        self.seed = seed
        self.state: EnvironmentState | None = None

```

### Explanation

- **Line 37** (`return event.along_track_effectiveness`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 38** (`if action_type == ActionType.NORMAL_MANEUVER:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 39** (`return event.normal_effectiveness`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 40** (`return 0.0`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 41** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 42** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 43** (`class ConjunctionSimulator:`): This line defines a new class. This class encapsulates related state and behavior into a single, reusable object-oriented construct.
- **Line 44** (`def __init__(self, task: TaskConfig, seed: int = 0):`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 45** (`self.task = task`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 46** (`self.seed = seed`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 47** (`self.state: EnvironmentState | None = None`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 48** (Blank line): This is a blank line, used to separate logical sections of code for better readability.

```python
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
```

### Explanation

- **Line 49** (`def reset(self) -> EnvironmentObservation:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 50** (`self.state = EnvironmentState(`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 51** (`episode_id=f"{self.task.task_id}-{uuid4().hex[:8]}",`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 52** (`task_id=self.task.task_id,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 53** (`seed=self.seed,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 54** (`step_index=0,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 55** (`horizon=self.task.horizon,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 56** (`fuel_remaining=self.task.initial_fuel,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 57** (`tracking_quality=self.task.initial_tracking_quality,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 58** (`tracking_budget_remaining=self.task.tracking_budget,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 59** (`mission_offsets=MissionOffsets(),`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 60** (`true_events=[event.model_copy(deep=True) for event in self.task.conjunctions],`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
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
```

### Explanation

- **Line 61** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 62** (`return self.observation()`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 63** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 64** (`def observation(self) -> EnvironmentObservation:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 65** (`if self.state is None:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 66** (`raise RuntimeError("Environment must be reset before requesting observation.")`): This line raises an exception, explicitly signaling an error or invalid state that requires special handling.
- **Line 67** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 68** (`visible_events = sorted(`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 69** (`[self._observe_event(event) for event in self.state.true_events],`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 70** (`key=lambda event: event.collision_probability,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 71** (`reverse=True,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 72** (`)[: self.task.visible_event_limit]`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.

```python

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
```

### Explanation

- **Line 73** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 74** (`return EnvironmentObservation(`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 75** (`task_id=self.state.task_id,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 76** (`step_index=self.state.step_index,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 77** (`horizon_remaining=max(0, self.state.horizon - self.state.step_index),`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 78** (`fuel_remaining=round(self.state.fuel_remaining, 4),`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 79** (`tracking_quality=round(self.state.tracking_quality, 4),`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 80** (`tracking_budget_remaining=self.state.tracking_budget_remaining,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 81** (`mission_offsets=self.state.mission_offsets.model_copy(deep=True),`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 82** (`total_collision_probability=round(_total_collision_probability(self.state.true_events), 4),`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 83** (`highest_collision_probability=round(_highest_collision_probability(self.state.true_events), 4),`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 84** (`visible_events=visible_events,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
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
```

### Explanation

- **Line 85** (`last_action=self.state.last_action,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 86** (`last_action_error=self.state.last_action_error,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 87** (`done=self.state.done,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 88** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 89** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 90** (`def step(self, action: EnvironmentAction) -> StepResult:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 91** (`if self.state is None:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 92** (`raise RuntimeError("Environment must be reset before stepping.")`): This line raises an exception, explicitly signaling an error or invalid state that requires special handling.
- **Line 93** (`if self.state.done:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 94** (`raise RuntimeError("Episode is done. Call reset() to start a new episode.")`): This line raises an exception, explicitly signaling an error or invalid state that requires special handling.
- **Line 95** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 96** (`magnitude = min(action.magnitude, self.task.max_magnitude)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
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
```

### Explanation

- **Line 97** (`previous_total_probability = _total_collision_probability(self.state.true_events)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 98** (`previous_uncertainty = sum(event.uncertainty for event in self.state.true_events)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 99** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 100** (`reward_components = {`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 101** (`"base": 0.38,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 102** (`"risk_reduction": 0.0,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 103** (`"tracking_gain": 0.0,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 104** (`"fuel_penalty": 0.0,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 105** (`"mission_penalty": 0.0,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 106** (`"waste_penalty": 0.0,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 107** (`"completion_bonus": 0.0,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 108** (`}`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.

```python
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
```

### Explanation

- **Line 109** (`info: dict[str, float | int | str | bool] = {"task_id": self.task.task_id}`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 110** (`self.state.last_action_error = None`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 111** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 112** (`if action.action_type == ActionType.REQUEST_TRACKING_UPDATE:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 113** (`self._apply_tracking_update(reward_components, info)`): This line accesses or modifies an attribute or method on the current instance of the class (`self`), interacting with the object's internal state.
- **Line 114** (`elif action.action_type in {`): This line starts an alternative conditional statement, checked only if the preceding `if` condition was false.
- **Line 115** (`ActionType.RADIAL_MANEUVER,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 116** (`ActionType.ALONG_TRACK_MANEUVER,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 117** (`ActionType.NORMAL_MANEUVER,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 118** (`}:`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 119** (`self._apply_maneuver(action.action_type, magnitude, reward_components, info)`): This line accesses or modifies an attribute or method on the current instance of the class (`self`), interacting with the object's internal state.
- **Line 120** (`else:`): This line provides the fallback block of code, which executes if all preceding conditional checks evaluate to false.

```python
            info["noop"] = True
            if _highest_collision_probability(self.state.true_events) > 0.28:
                reward_components["waste_penalty"] += 0.08

        self._advance_dynamics()

        self.state.step_index += 1
        self.state.last_action = action.action_type
        self._check_termination()

        new_total_probability = _total_collision_probability(self.state.true_events)
        risk_reduction = max(0.0, previous_total_probability - new_total_probability)
```

### Explanation

- **Line 121** (`info["noop"] = True`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 122** (`if _highest_collision_probability(self.state.true_events) > 0.28:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 123** (`reward_components["waste_penalty"] += 0.08`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 124** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 125** (`self._advance_dynamics()`): This line accesses or modifies an attribute or method on the current instance of the class (`self`), interacting with the object's internal state.
- **Line 126** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 127** (`self.state.step_index += 1`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 128** (`self.state.last_action = action.action_type`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 129** (`self._check_termination()`): This line accesses or modifies an attribute or method on the current instance of the class (`self`), interacting with the object's internal state.
- **Line 130** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 131** (`new_total_probability = _total_collision_probability(self.state.true_events)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 132** (`risk_reduction = max(0.0, previous_total_probability - new_total_probability)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
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
```

### Explanation

- **Line 133** (`reward_components["risk_reduction"] = min(`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 134** (`0.35, risk_reduction * self.task.risk_reduction_reward_weight`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 135** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 136** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 137** (`new_uncertainty = sum(event.uncertainty for event in self.state.true_events)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 138** (`if action.action_type == ActionType.REQUEST_TRACKING_UPDATE:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 139** (`uncertainty_reduction = max(0.0, previous_uncertainty - new_uncertainty)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 140** (`reward_components["tracking_gain"] = min(`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 141** (`0.14, uncertainty_reduction * self.task.tracking_reward_weight`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 142** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 143** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 144** (`if self.state.collision_occurred:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.

```python
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
```

### Explanation

- **Line 145** (`reward = 0.0`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 146** (`else:`): This line provides the fallback block of code, which executes if all preceding conditional checks evaluate to false.
- **Line 147** (`if self.state.success:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 148** (`reward_components["completion_bonus"] = self.task.completion_bonus`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 149** (`reward = _clamp(`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 150** (`reward_components["base"]`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 151** (`+ reward_components["risk_reduction"]`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 152** (`+ reward_components["tracking_gain"]`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 153** (`+ reward_components["completion_bonus"]`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 154** (`- reward_components["fuel_penalty"]`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 155** (`- reward_components["mission_penalty"]`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 156** (`- reward_components["waste_penalty"]`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.

```python
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
```

### Explanation

- **Line 157** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 158** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 159** (`self.state.cumulative_reward += reward`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 160** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 161** (`info.update(`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 162** (`{`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 163** (`"fuel_remaining": round(self.state.fuel_remaining, 4),`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 164** (`"tracking_quality": round(self.state.tracking_quality, 4),`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 165** (`"tracking_budget_remaining": self.state.tracking_budget_remaining,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 166** (`"total_collision_probability": round(new_total_probability, 4),`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 167** (`"highest_collision_probability": round(_highest_collision_probability(self.state.true_events), 4),`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 168** (`"total_offset_km": round(_total_offset_km(self.state.mission_offsets), 4),`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.

```python
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
```

### Explanation

- **Line 169** (`"collision_occurred": self.state.collision_occurred,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 170** (`"success": self.state.success,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 171** (`"termination_reason": self.state.termination_reason or "",`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 172** (`"last_action_error": self.state.last_action_error or "",`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 173** (`}`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 174** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 175** (`observation = self.observation()`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 176** (`return StepResult(observation=observation, reward=round(reward, 4), done=self.state.done, info=info)`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 177** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 178** (`def _observe_event(self, event: ConjunctionEvent) -> ConjunctionEvent:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 179** (`if self.state is None:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 180** (`raise RuntimeError("Environment must be reset before requesting observation.")`): This line raises an exception, explicitly signaling an error or invalid state that requires special handling.

```python

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
```

### Explanation

- **Line 181** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 182** (`conservatism = (1.0 - self.state.tracking_quality) * event.uncertainty * event.tracking_sensitivity`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 183** (`observed_probability = _clamp(event.collision_probability + 0.35 * conservatism)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 184** (`observed_miss_distance = max(0.1, event.predicted_miss_distance_km - 0.6 * conservatism)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 185** (`observed_uncertainty = _clamp(event.uncertainty + 0.45 * (1.0 - self.state.tracking_quality))`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 186** (`return event.model_copy(`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 187** (`update={`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 188** (`"collision_probability": round(observed_probability, 4),`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 189** (`"predicted_miss_distance_km": round(observed_miss_distance, 4),`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 190** (`"uncertainty": round(observed_uncertainty, 4),`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 191** (`}`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 192** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.

```python

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
```

### Explanation

- **Line 193** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 194** (`def _apply_tracking_update(`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 195** (`self,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 196** (`reward_components: dict[str, float],`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 197** (`info: dict[str, float | int | str | bool],`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 198** (`) -> None:`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 199** (`if self.state is None:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 200** (`return`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 201** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 202** (`if self.state.tracking_budget_remaining <= 0:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 203** (`reward_components["waste_penalty"] += 0.12`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 204** (`info["tracking_update"] = False`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
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
```

### Explanation

- **Line 205** (`info["tracking_budget_exhausted"] = True`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 206** (`self.state.last_action_error = "tracking_budget_exhausted"`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 207** (`return`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 208** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 209** (`self.state.tracking_budget_remaining -= 1`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 210** (`self.state.tracking_updates_used += 1`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 211** (`self.state.fuel_remaining = max(0.0, self.state.fuel_remaining - self.task.fuel_cost_tracking)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 212** (`self.state.tracking_quality = _clamp(`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 213** (`self.state.tracking_quality + self.task.tracking_improvement`): This line accesses or modifies an attribute or method on the current instance of the class (`self`), interacting with the object's internal state.
- **Line 214** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 215** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 216** (`for event in self.state.true_events:`): This line initiates a loop, iterating over a sequence or repeatedly executing a block of code as long as a condition is met.

```python
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
```

### Explanation

- **Line 217** (`event.uncertainty = _clamp(event.uncertainty * self.task.uncertainty_reduction_factor)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 218** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 219** (`reward_components["fuel_penalty"] += self.task.fuel_penalty_weight * self.task.fuel_cost_tracking`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 220** (`info["tracking_update"] = True`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 221** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 222** (`def _apply_maneuver(`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 223** (`self,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 224** (`action_type: ActionType,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 225** (`magnitude: float,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 226** (`reward_components: dict[str, float],`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 227** (`info: dict[str, float | int | str | bool],`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 228** (`) -> None:`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.

```python
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
```

### Explanation

- **Line 229** (`if self.state is None:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 230** (`return`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 231** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 232** (`maneuver_cost = self.task.maneuver_base_cost + self.task.maneuver_variable_cost * max(0.2, magnitude)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 233** (`self.state.fuel_remaining = max(0.0, self.state.fuel_remaining - maneuver_cost)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 234** (`self.state.maneuvers_used += 1`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 235** (`self._apply_offsets(action_type, magnitude)`): This line accesses or modifies an attribute or method on the current instance of the class (`self`), interacting with the object's internal state.
- **Line 236** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 237** (`for event in self.state.true_events:`): This line initiates a loop, iterating over a sequence or repeatedly executing a block of code as long as a condition is met.
- **Line 238** (`effectiveness = _axis_effectiveness(event, action_type)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 239** (`tracking_factor = 0.7 + 0.3 * self.state.tracking_quality`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 240** (`timing_factor = 0.92 if event.time_to_closest_approach <= 1 else 1.0`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
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
```

### Explanation

- **Line 241** (`probability_reduction = magnitude * effectiveness * 0.22 * tracking_factor * timing_factor`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 242** (`miss_distance_gain = magnitude * effectiveness * 0.85`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 243** (`uncertainty_reduction = 0.03 * magnitude * effectiveness * self.state.tracking_quality`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 244** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 245** (`event.collision_probability = _clamp(event.collision_probability - probability_reduction)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 246** (`event.predicted_miss_distance_km += miss_distance_gain`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 247** (`event.uncertainty = _clamp(event.uncertainty - uncertainty_reduction)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 248** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 249** (`reward_components["fuel_penalty"] += self.task.fuel_penalty_weight * maneuver_cost`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 250** (`reward_components["mission_penalty"] += self.task.mission_offset_penalty_weight * min(`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 251** (`1.0, _total_offset_km(self.state.mission_offsets) / self.task.max_total_offset_km`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 252** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.

```python
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
```

### Explanation

- **Line 253** (`info["maneuver_cost"] = round(maneuver_cost, 4)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 254** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 255** (`def _apply_offsets(self, action_type: ActionType, magnitude: float) -> None:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 256** (`if self.state is None:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 257** (`return`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 258** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 259** (`delta = 0.55 * max(0.2, magnitude)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 260** (`if action_type == ActionType.RADIAL_MANEUVER:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 261** (`self.state.mission_offsets.radial_km += delta`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 262** (`self.state.mission_offsets.along_track_km += 0.15 * delta`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 263** (`elif action_type == ActionType.ALONG_TRACK_MANEUVER:`): This line starts an alternative conditional statement, checked only if the preceding `if` condition was false.
- **Line 264** (`self.state.mission_offsets.along_track_km += delta`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
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
```

### Explanation

- **Line 265** (`self.state.mission_offsets.radial_km += 0.12 * delta`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 266** (`elif action_type == ActionType.NORMAL_MANEUVER:`): This line starts an alternative conditional statement, checked only if the preceding `if` condition was false.
- **Line 267** (`self.state.mission_offsets.normal_km += delta`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 268** (`self.state.mission_offsets.along_track_km += 0.08 * delta`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 269** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 270** (`def _advance_dynamics(self) -> None:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 271** (`if self.state is None:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 272** (`return`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 273** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 274** (`self.state.tracking_quality = _clamp(self.state.tracking_quality - self.task.tracking_decay)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 275** (`self.state.mission_offsets.radial_km *= 1.0 - self.task.passive_offset_recovery`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 276** (`self.state.mission_offsets.along_track_km *= 1.0 - self.task.passive_offset_recovery`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
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
```

### Explanation

- **Line 277** (`self.state.mission_offsets.normal_km *= 1.0 - self.task.passive_offset_recovery`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 278** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 279** (`for event in self.state.true_events:`): This line initiates a loop, iterating over a sequence or repeatedly executing a block of code as long as a condition is met.
- **Line 280** (`event.time_to_closest_approach = max(0, event.time_to_closest_approach - 1)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 281** (`urgency = 0.12 if event.time_to_closest_approach <= 1 else 0.06 if event.time_to_closest_approach <= 3 else 0.02`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 282** (`uncertainty_pressure = event.uncertainty * (0.08 + 0.05 * (1.0 - self.state.tracking_quality))`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 283** (`miss_distance_pressure = 0.02 if event.predicted_miss_distance_km < 1.2 else 0.0`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 284** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 285** (`event.collision_probability = _clamp(`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 286** (`event.collision_probability`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 287** (`+ event.risk_growth_rate * (0.35 + urgency)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 288** (`+ uncertainty_pressure`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.

```python
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
```

### Explanation

- **Line 289** (`+ miss_distance_pressure`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 290** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 291** (`event.uncertainty = _clamp(`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 292** (`event.uncertainty + (1.0 - self.state.tracking_quality) * 0.05 * event.tracking_sensitivity`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 293** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 294** (`event.predicted_miss_distance_km = max(0.1, event.predicted_miss_distance_km - 0.11)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 295** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 296** (`def _check_termination(self) -> None:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 297** (`if self.state is None:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 298** (`return`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 299** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 300** (`if self.state.fuel_remaining <= 0.0:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.

```python
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
```

### Explanation

- **Line 301** (`self.state.done = True`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 302** (`self.state.termination_reason = "fuel_exhausted"`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 303** (`return`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 304** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 305** (`if _total_offset_km(self.state.mission_offsets) > self.task.max_total_offset_km * 1.35:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 306** (`self.state.done = True`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 307** (`self.state.termination_reason = "mission_deviation_limit_exceeded"`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 308** (`return`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 309** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 310** (`imminent_collision = next(`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 311** (`(`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 312** (`event`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.

```python
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

```

### Explanation

- **Line 313** (`for event in self.state.true_events`): This line initiates a loop, iterating over a sequence or repeatedly executing a block of code as long as a condition is met.
- **Line 314** (`if event.time_to_closest_approach == 0`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 315** (`and event.collision_probability >= self.task.unsafe_probability_threshold`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 316** (`),`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 317** (`None,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 318** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 319** (`if imminent_collision is not None:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 320** (`self.state.done = True`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 321** (`self.state.collision_occurred = True`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 322** (`self.state.termination_reason = "collision"`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 323** (`return`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 324** (Blank line): This is a blank line, used to separate logical sections of code for better readability.

```python
        all_events_resolved = all(event.time_to_closest_approach == 0 for event in self.state.true_events)
        reached_horizon = self.state.step_index >= self.state.horizon
        if not (all_events_resolved or reached_horizon):
            return

        self.state.done = True
        residual_probability = _highest_collision_probability(self.state.true_events)
        offset_ok = _total_offset_km(self.state.mission_offsets) <= self.task.max_total_offset_km
        self.state.success = residual_probability <= self.task.success_probability_threshold and offset_ok
        self.state.termination_reason = "safe_completion" if self.state.success else "horizon_reached"
```

### Explanation

- **Line 325** (`all_events_resolved = all(event.time_to_closest_approach == 0 for event in self.state.true_events)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 326** (`reached_horizon = self.state.step_index >= self.state.horizon`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 327** (`if not (all_events_resolved or reached_horizon):`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 328** (`return`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 329** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 330** (`self.state.done = True`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 331** (`residual_probability = _highest_collision_probability(self.state.true_events)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 332** (`offset_ok = _total_offset_km(self.state.mission_offsets) <= self.task.max_total_offset_km`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 333** (`self.state.success = residual_probability <= self.task.success_probability_threshold and offset_ok`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 334** (`self.state.termination_reason = "safe_completion" if self.state.success else "horizon_reached"`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

