# Tutorial: catalog.py

This document provides a detailed, line-by-line explanation of `catalog.py`. This tutorial is essential for understanding the core concepts and setup of the file.

```python
from __future__ import annotations

import json
import os
from pathlib import Path

from orbits_env.models import ConjunctionEvent, GeometryTag, TaskConfig


def _base_tasks() -> dict[str, TaskConfig]:
    return {
    "collision_avoidance_easy": TaskConfig(
```

### Explanation

- **Line 1** (`from __future__ import annotations`): This line imports necessary modules or classes required for the functionality in this file. It ensures all dependencies are available in the current namespace.
- **Line 2** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 3** (`import json`): This line imports necessary modules or classes required for the functionality in this file. It ensures all dependencies are available in the current namespace.
- **Line 4** (`import os`): This line imports necessary modules or classes required for the functionality in this file. It ensures all dependencies are available in the current namespace.
- **Line 5** (`from pathlib import Path`): This line imports necessary modules or classes required for the functionality in this file. It ensures all dependencies are available in the current namespace.
- **Line 6** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 7** (`from orbits_env.models import ConjunctionEvent, GeometryTag, TaskConfig`): This line imports necessary modules or classes required for the functionality in this file. It ensures all dependencies are available in the current namespace.
- **Line 8** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 9** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 10** (`def _base_tasks() -> dict[str, TaskConfig]:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 11** (`return {`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 12** (`"collision_avoidance_easy": TaskConfig(`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.

```python
        task_id="collision_avoidance_easy",
        difficulty="easy",
        description="Single high-confidence threat with enough fuel to maneuver conservatively.",
        horizon=6,
        initial_fuel=9.5,
        initial_tracking_quality=0.82,
        tracking_budget=2,
        visible_event_limit=2,
        fuel_cost_tracking=0.1,
        maneuver_base_cost=0.35,
        maneuver_variable_cost=0.55,
        tracking_improvement=0.16,
```

### Explanation

- **Line 13** (`task_id="collision_avoidance_easy",`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 14** (`difficulty="easy",`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 15** (`description="Single high-confidence threat with enough fuel to maneuver conservatively.",`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 16** (`horizon=6,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 17** (`initial_fuel=9.5,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 18** (`initial_tracking_quality=0.82,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 19** (`tracking_budget=2,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 20** (`visible_event_limit=2,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 21** (`fuel_cost_tracking=0.1,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 22** (`maneuver_base_cost=0.35,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 23** (`maneuver_variable_cost=0.55,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 24** (`tracking_improvement=0.16,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
        tracking_decay=0.04,
        uncertainty_reduction_factor=0.55,
        passive_offset_recovery=0.1,
        mission_offset_penalty_weight=0.18,
        fuel_penalty_weight=0.16,
        risk_reduction_reward_weight=0.95,
        tracking_reward_weight=0.18,
        unsafe_probability_threshold=0.62,
        success_probability_threshold=0.18,
        max_total_offset_km=2.4,
        completion_bonus=0.25,
        collision_penalty=0.0,
```

### Explanation

- **Line 25** (`tracking_decay=0.04,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 26** (`uncertainty_reduction_factor=0.55,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 27** (`passive_offset_recovery=0.1,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 28** (`mission_offset_penalty_weight=0.18,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 29** (`fuel_penalty_weight=0.16,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 30** (`risk_reduction_reward_weight=0.95,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 31** (`tracking_reward_weight=0.18,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 32** (`unsafe_probability_threshold=0.62,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 33** (`success_probability_threshold=0.18,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 34** (`max_total_offset_km=2.4,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 35** (`completion_bonus=0.25,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 36** (`collision_penalty=0.0,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
        conjunctions=[
            ConjunctionEvent(
                object_id="deb-001",
                geometry_tag=GeometryTag.RADIAL_DOMINANT,
                collision_probability=0.34,
                predicted_miss_distance_km=1.25,
                time_to_closest_approach=4,
                uncertainty=0.12,
                radial_effectiveness=0.86,
                along_track_effectiveness=0.38,
                normal_effectiveness=0.44,
                risk_growth_rate=0.06,
```

### Explanation

- **Line 37** (`conjunctions=[`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 38** (`ConjunctionEvent(`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 39** (`object_id="deb-001",`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 40** (`geometry_tag=GeometryTag.RADIAL_DOMINANT,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 41** (`collision_probability=0.34,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 42** (`predicted_miss_distance_km=1.25,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 43** (`time_to_closest_approach=4,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 44** (`uncertainty=0.12,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 45** (`radial_effectiveness=0.86,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 46** (`along_track_effectiveness=0.38,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 47** (`normal_effectiveness=0.44,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 48** (`risk_growth_rate=0.06,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
                tracking_sensitivity=0.45,
            )
        ],
    ),
    "collision_avoidance_medium": TaskConfig(
        task_id="collision_avoidance_medium",
        difficulty="medium",
        description="Two conjunctions with different maneuver geometry and a tighter fuel budget.",
        horizon=8,
        initial_fuel=8.0,
        initial_tracking_quality=0.68,
        tracking_budget=2,
```

### Explanation

- **Line 49** (`tracking_sensitivity=0.45,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 50** (`)`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 51** (`],`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 52** (`),`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 53** (`"collision_avoidance_medium": TaskConfig(`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 54** (`task_id="collision_avoidance_medium",`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 55** (`difficulty="medium",`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 56** (`description="Two conjunctions with different maneuver geometry and a tighter fuel budget.",`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 57** (`horizon=8,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 58** (`initial_fuel=8.0,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 59** (`initial_tracking_quality=0.68,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 60** (`tracking_budget=2,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
        visible_event_limit=3,
        fuel_cost_tracking=0.14,
        maneuver_base_cost=0.42,
        maneuver_variable_cost=0.62,
        tracking_improvement=0.18,
        tracking_decay=0.055,
        uncertainty_reduction_factor=0.5,
        passive_offset_recovery=0.08,
        mission_offset_penalty_weight=0.22,
        fuel_penalty_weight=0.2,
        risk_reduction_reward_weight=1.0,
        tracking_reward_weight=0.22,
```

### Explanation

- **Line 61** (`visible_event_limit=3,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 62** (`fuel_cost_tracking=0.14,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 63** (`maneuver_base_cost=0.42,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 64** (`maneuver_variable_cost=0.62,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 65** (`tracking_improvement=0.18,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 66** (`tracking_decay=0.055,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 67** (`uncertainty_reduction_factor=0.5,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 68** (`passive_offset_recovery=0.08,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 69** (`mission_offset_penalty_weight=0.22,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 70** (`fuel_penalty_weight=0.2,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 71** (`risk_reduction_reward_weight=1.0,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 72** (`tracking_reward_weight=0.22,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
        unsafe_probability_threshold=0.58,
        success_probability_threshold=0.24,
        max_total_offset_km=2.1,
        completion_bonus=0.28,
        collision_penalty=0.0,
        conjunctions=[
            ConjunctionEvent(
                object_id="deb-101",
                geometry_tag=GeometryTag.ALONG_TRACK_DOMINANT,
                collision_probability=0.27,
                predicted_miss_distance_km=1.55,
                time_to_closest_approach=5,
```

### Explanation

- **Line 73** (`unsafe_probability_threshold=0.58,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 74** (`success_probability_threshold=0.24,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 75** (`max_total_offset_km=2.1,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 76** (`completion_bonus=0.28,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 77** (`collision_penalty=0.0,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 78** (`conjunctions=[`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 79** (`ConjunctionEvent(`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 80** (`object_id="deb-101",`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 81** (`geometry_tag=GeometryTag.ALONG_TRACK_DOMINANT,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 82** (`collision_probability=0.27,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 83** (`predicted_miss_distance_km=1.55,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 84** (`time_to_closest_approach=5,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
                uncertainty=0.2,
                radial_effectiveness=0.36,
                along_track_effectiveness=0.82,
                normal_effectiveness=0.48,
                risk_growth_rate=0.055,
                tracking_sensitivity=0.55,
            ),
            ConjunctionEvent(
                object_id="deb-102",
                geometry_tag=GeometryTag.RADIAL_DOMINANT,
                collision_probability=0.23,
                predicted_miss_distance_km=1.7,
```

### Explanation

- **Line 85** (`uncertainty=0.2,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 86** (`radial_effectiveness=0.36,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 87** (`along_track_effectiveness=0.82,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 88** (`normal_effectiveness=0.48,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 89** (`risk_growth_rate=0.055,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 90** (`tracking_sensitivity=0.55,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 91** (`),`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 92** (`ConjunctionEvent(`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 93** (`object_id="deb-102",`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 94** (`geometry_tag=GeometryTag.RADIAL_DOMINANT,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 95** (`collision_probability=0.23,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 96** (`predicted_miss_distance_km=1.7,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
                time_to_closest_approach=6,
                uncertainty=0.24,
                radial_effectiveness=0.74,
                along_track_effectiveness=0.34,
                normal_effectiveness=0.42,
                risk_growth_rate=0.05,
                tracking_sensitivity=0.48,
            ),
        ],
    ),
    "collision_avoidance_hard": TaskConfig(
        task_id="collision_avoidance_hard",
```

### Explanation

- **Line 97** (`time_to_closest_approach=6,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 98** (`uncertainty=0.24,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 99** (`radial_effectiveness=0.74,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 100** (`along_track_effectiveness=0.34,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 101** (`normal_effectiveness=0.42,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 102** (`risk_growth_rate=0.05,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 103** (`tracking_sensitivity=0.48,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 104** (`),`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 105** (`],`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 106** (`),`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 107** (`"collision_avoidance_hard": TaskConfig(`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 108** (`task_id="collision_avoidance_hard",`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
        difficulty="hard",
        description="Three competing threats with poor initial certainty and tight mission-offset limits.",
        horizon=10,
        initial_fuel=7.2,
        initial_tracking_quality=0.57,
        tracking_budget=3,
        visible_event_limit=3,
        fuel_cost_tracking=0.16,
        maneuver_base_cost=0.44,
        maneuver_variable_cost=0.7,
        tracking_improvement=0.2,
        tracking_decay=0.07,
```

### Explanation

- **Line 109** (`difficulty="hard",`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 110** (`description="Three competing threats with poor initial certainty and tight mission-offset limits.",`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 111** (`horizon=10,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 112** (`initial_fuel=7.2,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 113** (`initial_tracking_quality=0.57,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 114** (`tracking_budget=3,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 115** (`visible_event_limit=3,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 116** (`fuel_cost_tracking=0.16,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 117** (`maneuver_base_cost=0.44,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 118** (`maneuver_variable_cost=0.7,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 119** (`tracking_improvement=0.2,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 120** (`tracking_decay=0.07,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
        uncertainty_reduction_factor=0.45,
        passive_offset_recovery=0.06,
        mission_offset_penalty_weight=0.26,
        fuel_penalty_weight=0.22,
        risk_reduction_reward_weight=1.04,
        tracking_reward_weight=0.25,
        unsafe_probability_threshold=0.54,
        success_probability_threshold=0.28,
        max_total_offset_km=1.9,
        completion_bonus=0.3,
        collision_penalty=0.0,
        conjunctions=[
```

### Explanation

- **Line 121** (`uncertainty_reduction_factor=0.45,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 122** (`passive_offset_recovery=0.06,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 123** (`mission_offset_penalty_weight=0.26,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 124** (`fuel_penalty_weight=0.22,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 125** (`risk_reduction_reward_weight=1.04,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 126** (`tracking_reward_weight=0.25,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 127** (`unsafe_probability_threshold=0.54,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 128** (`success_probability_threshold=0.28,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 129** (`max_total_offset_km=1.9,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 130** (`completion_bonus=0.3,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 131** (`collision_penalty=0.0,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 132** (`conjunctions=[`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
            ConjunctionEvent(
                object_id="deb-201",
                geometry_tag=GeometryTag.ALONG_TRACK_DOMINANT,
                collision_probability=0.24,
                predicted_miss_distance_km=1.45,
                time_to_closest_approach=4,
                uncertainty=0.3,
                radial_effectiveness=0.33,
                along_track_effectiveness=0.81,
                normal_effectiveness=0.4,
                risk_growth_rate=0.07,
                tracking_sensitivity=0.62,
```

### Explanation

- **Line 133** (`ConjunctionEvent(`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 134** (`object_id="deb-201",`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 135** (`geometry_tag=GeometryTag.ALONG_TRACK_DOMINANT,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 136** (`collision_probability=0.24,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 137** (`predicted_miss_distance_km=1.45,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 138** (`time_to_closest_approach=4,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 139** (`uncertainty=0.3,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 140** (`radial_effectiveness=0.33,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 141** (`along_track_effectiveness=0.81,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 142** (`normal_effectiveness=0.4,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 143** (`risk_growth_rate=0.07,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 144** (`tracking_sensitivity=0.62,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
            ),
            ConjunctionEvent(
                object_id="deb-202",
                geometry_tag=GeometryTag.NORMAL_DOMINANT,
                collision_probability=0.21,
                predicted_miss_distance_km=1.6,
                time_to_closest_approach=7,
                uncertainty=0.26,
                radial_effectiveness=0.38,
                along_track_effectiveness=0.29,
                normal_effectiveness=0.84,
                risk_growth_rate=0.055,
```

### Explanation

- **Line 145** (`),`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 146** (`ConjunctionEvent(`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 147** (`object_id="deb-202",`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 148** (`geometry_tag=GeometryTag.NORMAL_DOMINANT,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 149** (`collision_probability=0.21,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 150** (`predicted_miss_distance_km=1.6,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 151** (`time_to_closest_approach=7,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 152** (`uncertainty=0.26,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 153** (`radial_effectiveness=0.38,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 154** (`along_track_effectiveness=0.29,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 155** (`normal_effectiveness=0.84,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 156** (`risk_growth_rate=0.055,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
                tracking_sensitivity=0.5,
            ),
            ConjunctionEvent(
                object_id="deb-203",
                geometry_tag=GeometryTag.RADIAL_DOMINANT,
                collision_probability=0.19,
                predicted_miss_distance_km=1.8,
                time_to_closest_approach=5,
                uncertainty=0.32,
                radial_effectiveness=0.78,
                along_track_effectiveness=0.36,
                normal_effectiveness=0.41,
```

### Explanation

- **Line 157** (`tracking_sensitivity=0.5,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 158** (`),`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 159** (`ConjunctionEvent(`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 160** (`object_id="deb-203",`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 161** (`geometry_tag=GeometryTag.RADIAL_DOMINANT,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 162** (`collision_probability=0.19,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 163** (`predicted_miss_distance_km=1.8,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 164** (`time_to_closest_approach=5,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 165** (`uncertainty=0.32,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 166** (`radial_effectiveness=0.78,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 167** (`along_track_effectiveness=0.36,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 168** (`normal_effectiveness=0.41,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python
                risk_growth_rate=0.06,
                tracking_sensitivity=0.58,
            ),
        ],
    ),
    }


def _task_priors_path() -> Path:
    configured = os.getenv("ORBITS_TASK_PRIORS_PATH")
    if configured:
        return Path(configured)
```

### Explanation

- **Line 169** (`risk_growth_rate=0.06,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 170** (`tracking_sensitivity=0.58,`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 171** (`),`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 172** (`],`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 173** (`),`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 174** (`}`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 175** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 176** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 177** (`def _task_priors_path() -> Path:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 178** (`configured = os.getenv("ORBITS_TASK_PRIORS_PATH")`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 179** (`if configured:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 180** (`return Path(configured)`): This line returns a value or object from the current function to its caller, concluding the function's execution.

```python
    return Path(__file__).resolve().with_name("task_priors.json")


def _load_task_overrides() -> dict[str, dict]:
    path = _task_priors_path()
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

```

### Explanation

- **Line 181** (`return Path(__file__).resolve().with_name("task_priors.json")`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 182** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 183** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 184** (`def _load_task_overrides() -> dict[str, dict]:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 185** (`path = _task_priors_path()`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 186** (`if not path.exists():`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 187** (`return {}`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 188** (`try:`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 189** (`payload = json.loads(path.read_text(encoding="utf-8"))`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 190** (`except (OSError, json.JSONDecodeError):`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 191** (`return {}`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 192** (Blank line): This is a blank line, used to separate logical sections of code for better readability.

```python
    overrides = payload.get("task_overrides")
    if not isinstance(overrides, dict):
        return {}
    return overrides


def _apply_single_task_override(task: TaskConfig, override: dict) -> TaskConfig:
    task_data = task.model_dump()
    scalar_updates = {k: v for k, v in override.items() if k != "conjunctions"}
    for key, value in scalar_updates.items():
        if key in task_data:
            task_data[key] = value
```

### Explanation

- **Line 193** (`overrides = payload.get("task_overrides")`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 194** (`if not isinstance(overrides, dict):`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 195** (`return {}`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 196** (`return overrides`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 197** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 198** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 199** (`def _apply_single_task_override(task: TaskConfig, override: dict) -> TaskConfig:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 200** (`task_data = task.model_dump()`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 201** (`scalar_updates = {k: v for k, v in override.items() if k != "conjunctions"}`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 202** (`for key, value in scalar_updates.items():`): This line initiates a loop, iterating over a sequence or repeatedly executing a block of code as long as a condition is met.
- **Line 203** (`if key in task_data:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 204** (`task_data[key] = value`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python

    conjunction_overrides = override.get("conjunctions", [])
    if isinstance(conjunction_overrides, list):
        for idx, conjunction_override in enumerate(conjunction_overrides):
            if idx >= len(task_data["conjunctions"]) or not isinstance(conjunction_override, dict):
                continue
            for key, value in conjunction_override.items():
                if key in task_data["conjunctions"][idx]:
                    task_data["conjunctions"][idx][key] = value

    return TaskConfig(**task_data)

```

### Explanation

- **Line 205** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 206** (`conjunction_overrides = override.get("conjunctions", [])`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 207** (`if isinstance(conjunction_overrides, list):`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 208** (`for idx, conjunction_override in enumerate(conjunction_overrides):`): This line initiates a loop, iterating over a sequence or repeatedly executing a block of code as long as a condition is met.
- **Line 209** (`if idx >= len(task_data["conjunctions"]) or not isinstance(conjunction_override, dict):`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 210** (`continue`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 211** (`for key, value in conjunction_override.items():`): This line initiates a loop, iterating over a sequence or repeatedly executing a block of code as long as a condition is met.
- **Line 212** (`if key in task_data["conjunctions"][idx]:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 213** (`task_data["conjunctions"][idx][key] = value`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 214** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 215** (`return TaskConfig(**task_data)`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 216** (Blank line): This is a blank line, used to separate logical sections of code for better readability.

```python

def _build_tasks() -> dict[str, TaskConfig]:
    tasks = _base_tasks()
    overrides = _load_task_overrides()
    for task_id, override in overrides.items():
        task = tasks.get(task_id)
        if task is None or not isinstance(override, dict):
            continue
        tasks[task_id] = _apply_single_task_override(task, override)
    return tasks


```

### Explanation

- **Line 217** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 218** (`def _build_tasks() -> dict[str, TaskConfig]:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 219** (`tasks = _base_tasks()`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 220** (`overrides = _load_task_overrides()`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 221** (`for task_id, override in overrides.items():`): This line initiates a loop, iterating over a sequence or repeatedly executing a block of code as long as a condition is met.
- **Line 222** (`task = tasks.get(task_id)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 223** (`if task is None or not isinstance(override, dict):`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 224** (`continue`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 225** (`tasks[task_id] = _apply_single_task_override(task, override)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 226** (`return tasks`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 227** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 228** (Blank line): This is a blank line, used to separate logical sections of code for better readability.

```python
TASKS: dict[str, TaskConfig] = _build_tasks()


def get_task(task_id: str) -> TaskConfig:
    try:
        return TASKS[task_id].model_copy(deep=True)
    except KeyError as exc:
        raise ValueError(f"Unknown task_id: {task_id}") from exc
```

### Explanation

- **Line 229** (`TASKS: dict[str, TaskConfig] = _build_tasks()`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 230** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 231** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 232** (`def get_task(task_id: str) -> TaskConfig:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 233** (`try:`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 234** (`return TASKS[task_id].model_copy(deep=True)`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 235** (`except KeyError as exc:`): This line performs an operation, expression evaluation, or continues a multi-line statement, contributing to the broader logic of the surrounding block.
- **Line 236** (`raise ValueError(f"Unknown task_id: {task_id}") from exc`): This line raises an exception, explicitly signaling an error or invalid state that requires special handling.

