# Tutorial: scoring.py

This document provides a detailed, line-by-line explanation of `scoring.py`. This tutorial is essential for understanding the core concepts and setup of the file.

```python
from __future__ import annotations

from orbits_env.models import EnvironmentState, TaskConfig


def grade_episode(state: EnvironmentState, task: TaskConfig) -> float:
    if state.collision_occurred:
        return 0.0

    highest_probability = max((event.collision_probability for event in state.true_events), default=0.0)
    total_probability = min(1.0, sum(event.collision_probability for event in state.true_events))
    total_offset = (
```

### Explanation

- **Line 1** (`from __future__ import annotations`): This line imports necessary modules or classes required for the functionality in this file. It ensures all dependencies are available in the current namespace.
- **Line 2** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 3** (`from orbits_env.models import EnvironmentState, TaskConfig`): This line imports necessary modules or classes required for the functionality in this file. It ensures all dependencies are available in the current namespace.
- **Line 4** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 5** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 6** (`def grade_episode(state: EnvironmentState, task: TaskConfig) -> float:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 7** (`if state.collision_occurred:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 8** (`return 0.0`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 9** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 10** (`highest_probability = max((event.collision_probability for event in state.true_events), default=0.0)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 11** (`total_probability = min(1.0, sum(event.collision_probability for event in state.true_events))`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 12** (`total_offset = (`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
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
```

### Explanation

- **Line 13** (`state.mission_offsets.radial_km`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 14** (`+ state.mission_offsets.along_track_km`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 15** (`+ state.mission_offsets.normal_km`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 16** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 17** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 18** (`safety = max(0.0, 1.0 - (0.65 * highest_probability + 0.35 * total_probability))`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 19** (`fuel_efficiency = min(1.0, state.fuel_remaining / task.initial_fuel)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 20** (`mission_preservation = max(0.0, 1.0 - (total_offset / task.max_total_offset_km))`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 21** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 22** (`tracking_budget_total = max(1, task.tracking_budget)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 23** (`tracking_efficiency = max(0.0, 1.0 - (state.tracking_updates_used / tracking_budget_total))`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 24** (`if highest_probability > task.success_probability_threshold:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.

```python
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
```

### Explanation

- **Line 25** (`tracking_efficiency *= 0.7`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 26** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 27** (`completion = 1.0 if state.success else 0.35`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 28** (`score = (`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 29** (`0.45 * safety`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 30** (`+ 0.2 * fuel_efficiency`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 31** (`+ 0.2 * mission_preservation`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 32** (`+ 0.05 * tracking_efficiency`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 33** (`+ 0.1 * completion`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 34** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 35** (`return round(max(0.0, min(1.0, score)), 4)`): This line returns a value or object from the current function to its caller, concluding the function's execution.

