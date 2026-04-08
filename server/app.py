from __future__ import annotations

from fastapi import FastAPI, HTTPException

from orbits_env.env import SpaceDebrisEnv
from orbits_env.models import EnvironmentAction
from orbits_env.tasks.catalog import TASKS

app = FastAPI(title="Orbits OpenEnv", version="0.1.0")

ENVIRONMENTS: dict[str, SpaceDebrisEnv] = {}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str | list[str]]:
    env = SpaceDebrisEnv()
    return {
        "name": "orbits-openenv",
        "version": "0.1.0",
        "tasks": env.available_tasks(),
    }


@app.get("/tasks")
def tasks() -> dict[str, list[str]]:
    env = SpaceDebrisEnv()
    return {"tasks": env.available_tasks()}


@app.get("/tasks/{task_id}")
def task_detail(task_id: str) -> dict:
    task = TASKS.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Unknown task.")
    return task.model_dump()


@app.post("/reset/{task_id}")
def reset(task_id: str) -> dict:
    env = SpaceDebrisEnv(task_id=task_id)
    observation = env.reset()
    ENVIRONMENTS["default"] = env
    return observation.model_dump()


@app.post("/step")
def step(action: EnvironmentAction) -> dict:
    env = ENVIRONMENTS.get("default")
    if env is None:
        raise HTTPException(status_code=400, detail="Call reset before step.")
    result = env.step(action)
    return result.model_dump()


@app.get("/state")
def state() -> dict:
    env = ENVIRONMENTS.get("default")
    if env is None:
        raise HTTPException(status_code=400, detail="Call reset before state.")
    return env.state().model_dump()


@app.get("/grade")
def grade() -> dict[str, float]:
    env = ENVIRONMENTS.get("default")
    if env is None:
        raise HTTPException(status_code=400, detail="Call reset before grade.")
    return {"score": env.grade()}


@app.post("/close")
def close() -> dict[str, bool]:
    env = ENVIRONMENTS.pop("default", None)
    if env is not None:
        env.close()
    return {"closed": True}
