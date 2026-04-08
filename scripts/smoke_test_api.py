from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.app import close, grade, health, reset, reset_default, state, step, task_detail, tasks
from orbits_env.models import EnvironmentAction


def main() -> None:
    assert health() == {"status": "ok"}

    task_listing = tasks()
    assert "collision_avoidance_easy" in task_listing["tasks"]

    observation = reset_default()
    assert observation["task_id"] == "collision_avoidance_easy"

    result = step(EnvironmentAction(action_type="request_tracking_update", magnitude=0.0))
    assert "reward" in result

    current_state = state()
    assert current_state["task_id"] == "collision_avoidance_easy"
    assert "score" in grade()
    assert task_detail("collision_avoidance_easy")["difficulty"] == "easy"
    assert close() == {"closed": True}

    print("API smoke test passed.")


if __name__ == "__main__":
    main()
