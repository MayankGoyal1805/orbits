# Tutorial: baseline.py

This document provides a detailed, line-by-line explanation of `baseline.py`. This tutorial is essential for understanding the core concepts and setup of the file.

```python
from __future__ import annotations

from orbits_env.models import ActionType, EnvironmentAction, EnvironmentObservation


def choose_action(observation: EnvironmentObservation) -> EnvironmentAction:
    if not observation.visible_events:
        return EnvironmentAction(action_type=ActionType.NOOP)

    highest_risk = max(observation.visible_events, key=lambda event: event.collision_probability)
    if (
        observation.tracking_budget_remaining > 0
```

### Explanation

- **Line 1** (`from __future__ import annotations`): This line imports necessary modules or classes required for the functionality in this file. It ensures all dependencies are available in the current namespace.
- **Line 2** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 3** (`from orbits_env.models import ActionType, EnvironmentAction, EnvironmentObservation`): This line imports necessary modules or classes required for the functionality in this file. It ensures all dependencies are available in the current namespace.
- **Line 4** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 5** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 6** (`def choose_action(observation: EnvironmentObservation) -> EnvironmentAction:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 7** (`if not observation.visible_events:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 8** (`return EnvironmentAction(action_type=ActionType.NOOP)`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 9** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 10** (`highest_risk = max(observation.visible_events, key=lambda event: event.collision_probability)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 11** (`if (`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 12** (`observation.tracking_budget_remaining > 0`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.

```python
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
```

### Explanation

- **Line 13** (`and observation.tracking_quality < 0.72`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 14** (`and highest_risk.uncertainty > 0.18`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 15** (`and highest_risk.time_to_closest_approach >= 2`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 16** (`):`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 17** (`return EnvironmentAction(action_type=ActionType.REQUEST_TRACKING_UPDATE)`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 18** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 19** (`if highest_risk.collision_probability < 0.14:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 20** (`return EnvironmentAction(action_type=ActionType.NOOP)`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 21** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 22** (`weighted_axes = {`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 23** (`ActionType.RADIAL_MANEUVER: 0.0,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 24** (`ActionType.ALONG_TRACK_MANEUVER: 0.0,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.

```python
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
```

### Explanation

- **Line 25** (`ActionType.NORMAL_MANEUVER: 0.0,`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 26** (`}`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 27** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 28** (`for event in observation.visible_events:`): This line initiates a loop, iterating over a sequence or repeatedly executing a block of code as long as a condition is met.
- **Line 29** (`urgency = 1.15 if event.time_to_closest_approach <= 2 else 1.0`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 30** (`weighted_axes[ActionType.RADIAL_MANEUVER] += (`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 31** (`event.collision_probability * urgency * event.radial_effectiveness`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 32** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 33** (`weighted_axes[ActionType.ALONG_TRACK_MANEUVER] += (`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 34** (`event.collision_probability * urgency * event.along_track_effectiveness`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 35** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 36** (`weighted_axes[ActionType.NORMAL_MANEUVER] += (`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
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

```

### Explanation

- **Line 37** (`event.collision_probability * urgency * event.normal_effectiveness`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 38** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 39** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 40** (`best_action = max(weighted_axes, key=weighted_axes.get)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 41** (`total_offset = (`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 42** (`observation.mission_offsets.radial_km`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 43** (`+ observation.mission_offsets.along_track_km`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 44** (`+ observation.mission_offsets.normal_km`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 45** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 46** (`if total_offset > 1.5 and highest_risk.collision_probability < 0.24:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 47** (`return EnvironmentAction(action_type=ActionType.NOOP)`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 48** (Blank line): This is a blank line, used to separate logical sections of code for better readability.

```python
    magnitude = 0.85 if highest_risk.collision_probability > 0.28 else 0.5
    return EnvironmentAction(action_type=best_action, magnitude=magnitude)
```

### Explanation

- **Line 49** (`magnitude = 0.85 if highest_risk.collision_probability > 0.28 else 0.5`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 50** (`return EnvironmentAction(action_type=best_action, magnitude=magnitude)`): This line returns a value or object from the current function to its caller, concluding the function's execution.

