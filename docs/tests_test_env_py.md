# Understanding `tests/test_env.py`

Welcome to this tutorial on `test_env.py`! This guide breaks down how the core simulation environment works in the Orbits OpenEnv project. 

If you're new to Reinforcement Learning (RL), the "environment" is the simulated world where the AI agent lives. The agent observes the world, takes an action, and the environment moves one "step" forward in time, providing a new observation and a reward. This file tests that simulation engine locally without the API layer.

## Key Libraries and Concepts

1. **Reinforcement Learning (RL) Gyms**: While we don't see `gym` or `gymnasium` imported, `SpaceDebrisEnv` clearly follows standard RL environment interfaces containing `reset()` and `step()` functions.
2. **Action Space**: The types of actions an agent can take. Here, an agent can perform orbital maneuvers like "Radial" or "Along-Track".
3. **Horizon**: The maximum number of steps or days allowed in a single episode.
4. **Observation State**: The data returned to the agent so it can make a decision (e.g., how many days are left, the risk of collision, tracking budget).

---

## Line-by-Line Walkthrough

### 1. Imports

```python
from __future__ import annotations
```
* **What it does**: Allows type hints to be evaluated as strings, preventing errors when referencing classes that haven't been fully loaded yet (PEP 563).

```python
from orbits_env.env import SpaceDebrisEnv
from orbits_env.models import ActionType, EnvironmentAction
```
* **What it does**: 
  * `SpaceDebrisEnv`: Imports the main simulation environment class for the space debris scenario.
  * `ActionType`: An Enumeration (Enum) defining the distinct kinds of actions an agent can make (e.g., maneuvering, requesting tracking).
  * `EnvironmentAction`: A data class or Pydantic model combining the `ActionType` with numerical values like `magnitude`.

### 2. Testing the Reset Function

```python
def test_reset_returns_first_observation() -> None:
```
* **What it does**: Defines a test to ensure that when the environment starts (resets), it gives the correct initial state.

```python
    env = SpaceDebrisEnv(task_id="collision_avoidance_easy", seed=0)
    observation = env.reset()
```
* **What it does**: Instantiates the environment for an easy task. Setting `seed=0` is crucial in machine learning and testing; it ensures the random number generator produces the exact same sequence of events every time, making the test predictable and reproducible. `env.reset()` starts the simulation and returns the very first observation.

```python
    assert observation.task_id == "collision_avoidance_easy"
    assert observation.step_index == 0
    assert observation.horizon_remaining == 6
    assert observation.done is False
    assert len(observation.visible_events) == 1
    assert observation.tracking_budget_remaining == 2
```
* **What it does**: Verifies the initial snapshot of the world:
  * The task ID matches what we requested.
  * `step_index == 0`: We are at the very beginning of time (Day 0).
  * `horizon_remaining == 6`: The episode will last for 6 steps before it automatically ends.
  * `done is False`: The episode is actively running; it hasn't finished yet.
  * `len(observation.visible_events) == 1`: There is exactly 1 detected collision risk (conjunction event) currently visible to our satellite radar.
  * `tracking_budget_remaining == 2`: The agent has the ability to request highly accurate tracking data exactly 2 times during this episode.

### 3. Testing the Step Function

```python
def test_step_advances_state() -> None:
    env = SpaceDebrisEnv(task_id="collision_avoidance_easy", seed=0)
    env.reset()
```
* **What it does**: Initializes and resets the environment just like the previous test.

```python
    result = env.step(
        EnvironmentAction(action_type=ActionType.REQUEST_TRACKING_UPDATE, magnitude=0.0)
    )
```
* **What it does**: The agent takes a specific action: `REQUEST_TRACKING_UPDATE`. This tells the environment the agent wants better sensor data on the debris instead of dodging. The magnitude is `0.0` because requesting data doesn't require thrust power. The environment processes this and returns a `result`.

```python
    assert result.done is False
    assert result.observation.step_index == 1
    assert result.info["tracking_update"] is True
    assert result.observation.tracking_budget_remaining == 1
```
* **What it does**: Checks the state of the world *after* the action:
  * We are still not done.
  * The simulation has advanced to `step_index == 1`.
  * The `info` dictionary (a common RL pattern for extra diagnostic info) confirms a tracking update happened.
  * Because we used one of our tracking requests, the budget drops from `2` down to `1`.

### 4. Testing a Full Episode (Rollout)

```python
def test_baseline_like_rollout_completes() -> None:
    env = SpaceDebrisEnv(task_id="collision_avoidance_medium", seed=0)
    observation = env.reset()
```
* **What it does**: Starts a complete "rollout" (a full episode from start to finish) on "medium" difficulty.

```python
    while not observation.done:
```
* **What it does**: Starts a loop that will run continuously as long as the episode is active (`observation.done` is False).

```python
        highest_risk = max(
            observation.visible_events, key=lambda event: event.collision_probability
        )
```
* **What it does**: 
  * Looks at all incoming debris (`visible_events`).
  * Uses the built-in `max()` function with a custom `key`. The `lambda` (an anonymous, inline function) tells Python to find the event that has the absolute highest `collision_probability`.

```python
        action_type = (
            ActionType.ALONG_TRACK_MANEUVER
            if highest_risk.along_track_effectiveness >= highest_risk.radial_effectiveness
            else ActionType.RADIAL_MANEUVER
        )
```
* **What it does**: This is a simple heuristic algorithm (a basic AI). It checks the properties of the `highest_risk` event. If moving forward/backward in the orbit (`ALONG_TRACK`) is more effective than moving up/down (`RADIAL`), it chooses the along-track maneuver. Otherwise, it picks radial.

```python
        observation = env.step(EnvironmentAction(action_type=action_type, magnitude=0.4)).observation
```
* **What it does**: Executes the chosen action with a thrust magnitude of `0.4`. It then immediately overwrites the `observation` variable with the *new* observation returned by the environment. The loop then goes back to the top to see if the episode is done.

```python
    state = env.state()
    assert state.done is True
    assert state.termination_reason is not None
    assert state.mission_offsets.radial_km >= 0.0
```
* **What it does**: Once the `while` loop breaks (meaning `observation.done` became `True`), it fetches the final state of the environment. It verifies that the simulation officially ended, that it recorded a reason for ending, and that the total radial movement offset (how far the satellite was pushed off its original path) is physically valid (greater than or equal to 0).

---

## Summary
This file ensures the physical rules of the space simulation work perfectly. It proves that time moves forward when actions are taken, budgets deplete correctly, and an automated agent can successfully interact with the simulation from start to finish.