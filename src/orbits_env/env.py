from __future__ import annotations

from orbits_env.graders.scoring import grade_episode
from orbits_env.models import EnvironmentAction, EnvironmentObservation, EnvironmentState, StepResult
from orbits_env.simulator import ConjunctionSimulator
from orbits_env.tasks.catalog import TASKS, get_task


class SpaceDebrisEnv:
    def __init__(self, task_id: str = "collision_avoidance_easy", seed: int = 0):
        self.task = get_task(task_id)
        self.simulator = ConjunctionSimulator(task=self.task, seed=seed)

    def reset(self) -> EnvironmentObservation:
        return self.simulator.reset()

    def step(self, action: EnvironmentAction) -> StepResult:
        return self.simulator.step(action)

    def state(self) -> EnvironmentState:
        if self.simulator.state is None:
            raise RuntimeError("Environment has not been reset yet.")
        return self.simulator.state.model_copy(deep=True)

    def close(self) -> None:
        self.simulator.state = None

    def available_tasks(self) -> list[str]:
        return list(TASKS.keys())

    def grade(self) -> float:
        return grade_episode(self.state(), self.task)
