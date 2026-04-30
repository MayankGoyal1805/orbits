# Understanding `openenv.yaml`

Welcome to the documentation for `openenv.yaml`. This file is the central configuration manifesto for our Orbits OpenEnv project. 

## What is YAML?
YAML (YAML Ain't Markup Language) is a human-readable data serialization format. It is widely used for configuration files because it relies on simple indentation to define structures (like lists and dictionaries) rather than complex brackets or tags.

## What is OpenEnv?
OpenEnv is a framework concept used to standardize how Reinforcement Learning (RL) and AI agents interact with custom environments. This YAML file describes everything an external server, evaluator, or user needs to know about the environment without reading the Python code.

---

## File Breakdown

### 1. General Metadata
```yaml
name: orbits-openenv
description: OpenEnv environment for space debris collision avoidance and conjunction management.
version: 0.1.0
benchmark: orbits-openenv
```
- These top-level keys provide human and machine-readable context about the project.
- It specifies the project's name, purpose, and versioning.

### 2. Entrypoint
```yaml
entrypoint:
  module: server.app
  app: app
```
- **Entrypoint:** This tells external tools how to launch the web server for this environment.
- It points to the `app` instance (likely a FastAPI app) residing inside the `server.app` python module (`server/app.py`).

### 3. Environment Definition
```yaml
environment:
  package: orbits_env
  class: SpaceDebrisEnv
  observation_model: EnvironmentObservation
  action_model: EnvironmentAction
  state_model: EnvironmentState
  reward_type: float
```
- **Code Mapping:** This section links the concepts of the environment to actual Python classes and files.
- The core logic lives in `orbits_env.SpaceDebrisEnv`.
- It defines what "Shapes" the data will take, using Pydantic models (like `EnvironmentObservation` for what the agent sees, and `EnvironmentAction` for what it can do).
- It states that the "Reward" for taking actions will be a decimal number (`float`).

### 4. Tasks Setup
```yaml
tasks:
  - id: collision_avoidance_easy
    difficulty: easy
    description: Single debris threat with high tracking quality and generous fuel.
  - id: collision_avoidance_medium
    difficulty: medium
    description: Two threats with mixed maneuver geometry and tighter fuel.
  - id: collision_avoidance_hard
    difficulty: hard
    description: Three competing threats with poor certainty and tight offset limits.
```
- A list of available tasks in the environment. 
- A hyphen `-` in YAML denotes an item in a list (array).
- We have 3 distinct tasks that a model must solve, ranging from `easy` to `hard`. This setup is typical in RL benchmarks to evaluate how well an agent scales with difficulty.

### 5. API Endpoints
```yaml
api:
  reset: /reset
  step: /step
  state: /state
  grade: /grade
  close: /close
  health: /health
```
- To make this environment easily accessible to AI agents written in any language (or running over the internet), the environment is wrapped in a REST API.
- These endpoints dictate how users interact with the environment over HTTP:
  - `/reset`: Starts a new task.
  - `/step`: Submits an action and receives the next observation.
  - `/health`: A standard endpoint used to check if the server is alive and running.