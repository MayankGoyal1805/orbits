from __future__ import annotations

import importlib
import json


def test_task_priors_override_applied(tmp_path, monkeypatch) -> None:
    priors_path = tmp_path / "task_priors.json"
    priors_payload = {
        "task_overrides": {
            "collision_avoidance_easy": {
                "initial_tracking_quality": 0.79,
                "conjunctions": [
                    {
                        "risk_growth_rate": 0.061,
                    }
                ],
            }
        }
    }
    priors_path.write_text(json.dumps(priors_payload), encoding="utf-8")

    monkeypatch.setenv("ORBITS_TASK_PRIORS_PATH", str(priors_path))

    import orbits_env.tasks.catalog as catalog

    reloaded = importlib.reload(catalog)
    task = reloaded.get_task("collision_avoidance_easy")

    assert task.initial_tracking_quality == 0.79
    assert task.conjunctions[0].risk_growth_rate == 0.061
