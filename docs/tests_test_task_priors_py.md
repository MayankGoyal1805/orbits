# Tutorial: `tests/test_task_priors.py`

This document provides a line-by-line explanation of `tests/test_task_priors.py`, detailing its concepts and setup.

```python
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
```
- `from __future__ import annotations`: Enables postponed evaluation of type hints for compatibility.
- ``: An empty line for spacing.
- `import importlib`: Imports the standard module used for reloading Python modules.
- `import json`: Imports the module used to encode data into JSON format.
- ``: An empty line for spacing.
- ``: An empty line for spacing.
- `def test_task_priors_override_applied(tmp_path, monkeypatch) -> None:`: Declares a test function utilizing Pytest fixtures for temporary files and mocking environment variables.
- `    priors_path = tmp_path / "task_priors.json"`: Determines a temporary path for the overrides JSON file.
- `    priors_payload = {`: Initiates the creation of a dictionary payload representing the file's content.
- `        "task_overrides": {`: Sets the root schema key required by the application to process task overrides.
- `            "collision_avoidance_easy": {`: Targets the specific ID of the task to apply modifications.
- `                "initial_tracking_quality": 0.79,`: Overrides the default `initial_tracking_quality` attribute to test parsing.
- `                "conjunctions": [`: Starts a list of configurations to override specific conjunction events.

```python
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
```
- `                    {`: Begins the dictionary for the first conjunction's override settings.
- `                        "risk_growth_rate": 0.061,`: Overrides the risk growth rate specifically for this conjunction.
- `                    }`: Closes the dictionary for the first conjunction override.
- `                ],`: Closes the list of conjunction overrides.
- `            }`: Closes the overrides configuration for the targeted task.
- `        }`: Closes the "task_overrides" mapping.
- `    }`: Concludes the definition of the `priors_payload` dictionary.
- `    priors_path.write_text(json.dumps(priors_payload), encoding="utf-8")`: Serializes the payload into a formatted JSON string and writes it to the temporary file path.
- ``: An empty line for spacing.
- `    monkeypatch.setenv("ORBITS_TASK_PRIORS_PATH", str(priors_path))`: Modifies the process environment variables to mock the `ORBITS_TASK_PRIORS_PATH` to point to our newly created temporary file.
- ``: An empty line for spacing.
- `    import orbits_env.tasks.catalog as catalog`: Imports the main task catalog module which accesses the environment variable to configure tasks.

```python
    reloaded = importlib.reload(catalog)
    task = reloaded.get_task("collision_avoidance_easy")

    assert task.initial_tracking_quality == 0.79
    assert task.conjunctions[0].risk_growth_rate == 0.061
```
- `    reloaded = importlib.reload(catalog)`: Forcefully reloads the imported `catalog` module, ensuring it reads the freshly injected environment variable on startup.
- `    task = reloaded.get_task("collision_avoidance_easy")`: Fetches the instantiated task object from the reloaded catalog to examine its properties.
- ``: An empty line for spacing.
- `    assert task.initial_tracking_quality == 0.79`: Verifies the task's base properties reflect the overridden `initial_tracking_quality` configuration.
- `    assert task.conjunctions[0].risk_growth_rate == 0.061`: Confirms the nested conjunction configuration correctly parsed and applied the overridden `risk_growth_rate`.
