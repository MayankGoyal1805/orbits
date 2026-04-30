# Tutorial: env.py

This document provides a detailed, line-by-line explanation of `env.py`. This tutorial is essential for understanding the core concepts and setup of the file.

```python
from __future__ import annotations

from orbits_env.graders.scoring import grade_episode
from orbits_env.models import EnvironmentAction, EnvironmentObservation, EnvironmentState, StepResult
from orbits_env.simulator import ConjunctionSimulator
from orbits_env.tasks.catalog import TASKS, get_task


class SpaceDebrisEnv:
    def __init__(self, task_id: str = "collision_avoidance_easy", seed: int = 0):
        self.task = get_task(task_id)
        self.simulator = ConjunctionSimulator(task=self.task, seed=seed)
```

### Explanation

- **Line 1** (`from __future__ import annotations`): This line imports necessary modules or classes required for the functionality in this file. It ensures all dependencies are available in the current namespace.
- **Line 2** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 3** (`from orbits_env.graders.scoring import grade_episode`): This line imports necessary modules or classes required for the functionality in this file. It ensures all dependencies are available in the current namespace.
- **Line 4** (`from orbits_env.models import EnvironmentAction, EnvironmentObservation, EnvironmentState, StepResult`): This line imports necessary modules or classes required for the functionality in this file. It ensures all dependencies are available in the current namespace.
- **Line 5** (`from orbits_env.simulator import ConjunctionSimulator`): This line imports necessary modules or classes required for the functionality in this file. It ensures all dependencies are available in the current namespace.
- **Line 6** (`from orbits_env.tasks.catalog import TASKS, get_task`): This line imports necessary modules or classes required for the functionality in this file. It ensures all dependencies are available in the current namespace.
- **Line 7** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 8** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 9** (`class SpaceDebrisEnv:`): This line defines a new class. This class encapsulates related state and behavior into a single, reusable object-oriented construct.
- **Line 10** (`def __init__(self, task_id: str = "collision_avoidance_easy", seed: int = 0):`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 11** (`self.task = get_task(task_id)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 12** (`self.simulator = ConjunctionSimulator(task=self.task, seed=seed)`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.

```python

    def reset(self) -> EnvironmentObservation:
        return self.simulator.reset()

    def step(self, action: EnvironmentAction) -> StepResult:
        return self.simulator.step(action)

    def state(self) -> EnvironmentState:
        if self.simulator.state is None:
            raise RuntimeError("Environment has not been reset yet.")
        return self.simulator.state.model_copy(deep=True)

```

### Explanation

- **Line 13** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 14** (`def reset(self) -> EnvironmentObservation:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 15** (`return self.simulator.reset()`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 16** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 17** (`def step(self, action: EnvironmentAction) -> StepResult:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 18** (`return self.simulator.step(action)`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 19** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 20** (`def state(self) -> EnvironmentState:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 21** (`if self.simulator.state is None:`): This line starts a conditional statement, checking a specific boolean condition to control the flow of execution.
- **Line 22** (`raise RuntimeError("Environment has not been reset yet.")`): This line raises an exception, explicitly signaling an error or invalid state that requires special handling.
- **Line 23** (`return self.simulator.state.model_copy(deep=True)`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 24** (Blank line): This is a blank line, used to separate logical sections of code for better readability.

```python
    def close(self) -> None:
        self.simulator.state = None

    def available_tasks(self) -> list[str]:
        return list(TASKS.keys())

    def grade(self) -> float:
        return grade_episode(self.state(), self.task)
```

### Explanation

- **Line 25** (`def close(self) -> None:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 26** (`self.simulator.state = None`): This line assigns a value to a variable or attribute. This operation updates the state or stores a computation for later use.
- **Line 27** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 28** (`def available_tasks(self) -> list[str]:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 29** (`return list(TASKS.keys())`): This line returns a value or object from the current function to its caller, concluding the function's execution.
- **Line 30** (Blank line): This is a blank line, used to separate logical sections of code for better readability.
- **Line 31** (`def grade(self) -> float:`): This line defines a new function or method. It specifies the name of the function and its expected parameters, forming the basic building block of logic.
- **Line 32** (`return grade_episode(self.state(), self.task)`): This line returns a value or object from the current function to its caller, concluding the function's execution.

