# Tutorial: `/home/mayank/repos/orbits/server/app.py`

## Concepts and Setup
This document provides a comprehensive line-by-line breakdown and tutorial for the script. It explores the concepts of operations, setup phases, environment configuration, and specific syntactical elements involved. Ensure you have the required dependencies installed and your Python environment appropriately activated before running this script.

## Code Explanation

```python
from __future__ import annotations

from fastapi import FastAPI, HTTPException
import uvicorn

from orbits_env.env import SpaceDebrisEnv
from orbits_env.models import EnvironmentAction, ResetRequest
from orbits_env.tasks.catalog import TASKS

app = FastAPI(title="Orbits OpenEnv", version="0.1.0")
```

* `from __future__ import annotations
`: Enables forward compatibility for language features, ensuring modern syntax like postponed evaluation of annotations.
* `
`: Empty line or whitespace.
* `from fastapi import FastAPI, HTTPException
`: Imports dependencies required for the script: from fastapi import FastAPI, HTTPException.
* `import uvicorn
`: Imports dependencies required for the script: import uvicorn.
* `
`: Empty line or whitespace.
* `from orbits_env.env import SpaceDebrisEnv
`: Imports dependencies required for the script: from orbits_env.env import SpaceDebrisEnv.
* `from orbits_env.models import EnvironmentAction, ResetRequest
`: Imports dependencies required for the script: from orbits_env.models import EnvironmentAction, ResetRequest.
* `from orbits_env.tasks.catalog import TASKS
`: Imports dependencies required for the script: from orbits_env.tasks.catalog import TASKS.
* `
`: Empty line or whitespace.
* `app = FastAPI(title="Orbits OpenEnv", version="0.1.0")
`: Assigns a evaluated value to a variable or state property.

```python

ENVIRONMENTS: dict[str, SpaceDebrisEnv] = {}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
```

* `
`: Empty line or whitespace.
* `ENVIRONMENTS: dict[str, SpaceDebrisEnv] = {}
`: Assigns a evaluated value to a variable or state property.
* `
`: Empty line or whitespace.
* `
`: Empty line or whitespace.
* `@app.get("/health")
`: A decorator modifying the behavior or properties of the following function: @app.get("/health").
* `def health() -> dict[str, str]:
`: Defines a function or method signature: def health() -> dict[str, str]:.
* `    return {"status": "ok"}
`: Returns a computed value or state from the function: return {"status": "ok"}.
* `
`: Empty line or whitespace.
* `
`: Empty line or whitespace.
* `@app.get("/")
`: A decorator modifying the behavior or properties of the following function: @app.get("/").

```python
def root() -> dict[str, str | list[str]]:
    env = SpaceDebrisEnv()
    return {
        "name": "orbits-openenv",
        "version": "0.1.0",
        "tasks": env.available_tasks(),
    }


@app.get("/tasks")
```

* `def root() -> dict[str, str | list[str]]:
`: Defines a function or method signature: def root() -> dict[str, str | list[str]]:.
* `    env = SpaceDebrisEnv()
`: Assigns a evaluated value to a variable or state property.
* `    return {
`: Returns a computed value or state from the function: return {.
* `        "name": "orbits-openenv",
`: Executes the statement, evaluates an expression, or continues a multi-line block: "name": "orbits-openenv",.
* `        "version": "0.1.0",
`: Executes the statement, evaluates an expression, or continues a multi-line block: "version": "0.1.0",.
* `        "tasks": env.available_tasks(),
`: Executes the statement, evaluates an expression, or continues a multi-line block: "tasks": env.available_tasks(),.
* `    }
`: Executes the statement, evaluates an expression, or continues a multi-line block: }.
* `
`: Empty line or whitespace.
* `
`: Empty line or whitespace.
* `@app.get("/tasks")
`: A decorator modifying the behavior or properties of the following function: @app.get("/tasks").

```python
def tasks() -> dict[str, list[str]]:
    env = SpaceDebrisEnv()
    return {"tasks": env.available_tasks()}


@app.get("/tasks/{task_id}")
def task_detail(task_id: str) -> dict:
    task = TASKS.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Unknown task.")
```

* `def tasks() -> dict[str, list[str]]:
`: Defines a function or method signature: def tasks() -> dict[str, list[str]]:.
* `    env = SpaceDebrisEnv()
`: Assigns a evaluated value to a variable or state property.
* `    return {"tasks": env.available_tasks()}
`: Returns a computed value or state from the function: return {"tasks": env.available_tasks()}.
* `
`: Empty line or whitespace.
* `
`: Empty line or whitespace.
* `@app.get("/tasks/{task_id}")
`: A decorator modifying the behavior or properties of the following function: @app.get("/tasks/{task_id}").
* `def task_detail(task_id: str) -> dict:
`: Defines a function or method signature: def task_detail(task_id: str) -> dict:.
* `    task = TASKS.get(task_id)
`: Assigns a evaluated value to a variable or state property.
* `    if task is None:
`: Starts a conditional branching block to control the execution flow.
* `        raise HTTPException(status_code=404, detail="Unknown task.")
`: Assigns a evaluated value to a variable or state property.

```python
    return task.model_dump()


def _reset_env(task_id: str) -> dict:
    env = SpaceDebrisEnv(task_id=task_id)
    observation = env.reset()
    ENVIRONMENTS["default"] = env
    return observation.model_dump()


```

* `    return task.model_dump()
`: Returns a computed value or state from the function: return task.model_dump().
* `
`: Empty line or whitespace.
* `
`: Empty line or whitespace.
* `def _reset_env(task_id: str) -> dict:
`: Defines a function or method signature: def _reset_env(task_id: str) -> dict:.
* `    env = SpaceDebrisEnv(task_id=task_id)
`: Assigns a evaluated value to a variable or state property.
* `    observation = env.reset()
`: Assigns a evaluated value to a variable or state property.
* `    ENVIRONMENTS["default"] = env
`: Assigns a evaluated value to a variable or state property.
* `    return observation.model_dump()
`: Returns a computed value or state from the function: return observation.model_dump().
* `
`: Empty line or whitespace.
* `
`: Empty line or whitespace.

```python
@app.post("/reset")
def reset_default(request: ResetRequest | None = None) -> dict:
    task_id = request.task_id if request is not None else "collision_avoidance_easy"
    return _reset_env(task_id)


@app.post("/reset/{task_id}")
def reset(task_id: str) -> dict:
    return _reset_env(task_id)

```

* `@app.post("/reset")
`: A decorator modifying the behavior or properties of the following function: @app.post("/reset").
* `def reset_default(request: ResetRequest | None = None) -> dict:
`: Defines a function or method signature: def reset_default(request: ResetRequest | None = None) -> dict:.
* `    task_id = request.task_id if request is not None else "collision_avoidance_easy"
`: Assigns a evaluated value to a variable or state property.
* `    return _reset_env(task_id)
`: Returns a computed value or state from the function: return _reset_env(task_id).
* `
`: Empty line or whitespace.
* `
`: Empty line or whitespace.
* `@app.post("/reset/{task_id}")
`: A decorator modifying the behavior or properties of the following function: @app.post("/reset/{task_id}").
* `def reset(task_id: str) -> dict:
`: Defines a function or method signature: def reset(task_id: str) -> dict:.
* `    return _reset_env(task_id)
`: Returns a computed value or state from the function: return _reset_env(task_id).
* `
`: Empty line or whitespace.

```python

@app.post("/step")
def step(action: EnvironmentAction) -> dict:
    env = ENVIRONMENTS.get("default")
    if env is None:
        raise HTTPException(status_code=400, detail="Call reset before step.")
    result = env.step(action)
    return result.model_dump()


```

* `
`: Empty line or whitespace.
* `@app.post("/step")
`: A decorator modifying the behavior or properties of the following function: @app.post("/step").
* `def step(action: EnvironmentAction) -> dict:
`: Defines a function or method signature: def step(action: EnvironmentAction) -> dict:.
* `    env = ENVIRONMENTS.get("default")
`: Assigns a evaluated value to a variable or state property.
* `    if env is None:
`: Starts a conditional branching block to control the execution flow.
* `        raise HTTPException(status_code=400, detail="Call reset before step.")
`: Assigns a evaluated value to a variable or state property.
* `    result = env.step(action)
`: Assigns a evaluated value to a variable or state property.
* `    return result.model_dump()
`: Returns a computed value or state from the function: return result.model_dump().
* `
`: Empty line or whitespace.
* `
`: Empty line or whitespace.

```python
@app.get("/state")
def state() -> dict:
    env = ENVIRONMENTS.get("default")
    if env is None:
        raise HTTPException(status_code=400, detail="Call reset before state.")
    return env.state().model_dump()


@app.get("/grade")
def grade() -> dict[str, float]:
```

* `@app.get("/state")
`: A decorator modifying the behavior or properties of the following function: @app.get("/state").
* `def state() -> dict:
`: Defines a function or method signature: def state() -> dict:.
* `    env = ENVIRONMENTS.get("default")
`: Assigns a evaluated value to a variable or state property.
* `    if env is None:
`: Starts a conditional branching block to control the execution flow.
* `        raise HTTPException(status_code=400, detail="Call reset before state.")
`: Assigns a evaluated value to a variable or state property.
* `    return env.state().model_dump()
`: Returns a computed value or state from the function: return env.state().model_dump().
* `
`: Empty line or whitespace.
* `
`: Empty line or whitespace.
* `@app.get("/grade")
`: A decorator modifying the behavior or properties of the following function: @app.get("/grade").
* `def grade() -> dict[str, float]:
`: Defines a function or method signature: def grade() -> dict[str, float]:.

```python
    env = ENVIRONMENTS.get("default")
    if env is None:
        raise HTTPException(status_code=400, detail="Call reset before grade.")
    return {"score": env.grade()}


@app.post("/close")
def close() -> dict[str, bool]:
    env = ENVIRONMENTS.pop("default", None)
    if env is not None:
```

* `    env = ENVIRONMENTS.get("default")
`: Assigns a evaluated value to a variable or state property.
* `    if env is None:
`: Starts a conditional branching block to control the execution flow.
* `        raise HTTPException(status_code=400, detail="Call reset before grade.")
`: Assigns a evaluated value to a variable or state property.
* `    return {"score": env.grade()}
`: Returns a computed value or state from the function: return {"score": env.grade()}.
* `
`: Empty line or whitespace.
* `
`: Empty line or whitespace.
* `@app.post("/close")
`: A decorator modifying the behavior or properties of the following function: @app.post("/close").
* `def close() -> dict[str, bool]:
`: Defines a function or method signature: def close() -> dict[str, bool]:.
* `    env = ENVIRONMENTS.pop("default", None)
`: Assigns a evaluated value to a variable or state property.
* `    if env is not None:
`: Starts a conditional branching block to control the execution flow.

```python
        env.close()
    return {"closed": True}


def main() -> None:
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
```

* `        env.close()
`: Executes the statement, evaluates an expression, or continues a multi-line block: env.close().
* `    return {"closed": True}
`: Returns a computed value or state from the function: return {"closed": True}.
* `
`: Empty line or whitespace.
* `
`: Empty line or whitespace.
* `def main() -> None:
`: Defines a function or method signature: def main() -> None:.
* `    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)
`: Assigns a evaluated value to a variable or state property.
* `
`: Empty line or whitespace.
* `
`: Empty line or whitespace.
* `if __name__ == "__main__":
`: Checks if the script is executed directly (not imported as a module).
* `    main()
`: Executes the statement, evaluates an expression, or continues a multi-line block: main().

