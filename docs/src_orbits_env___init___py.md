# Documentation for `src/orbits_env/__init__.py`

Welcome to this beginner-friendly guide! We are going to explore the code in `src/orbits_env/__init__.py`.

Unlike the empty `__init__.py` we saw in the `server` folder, this file actually contains code. Let's see how developers use `__init__.py` to create clean, easy-to-use interfaces for their Python packages.

## Understanding the Code Line-by-Line

### 1. Relative Imports

```python
from .env import SpaceDebrisEnv
from .models import (
    ActionType,
    ConjunctionEvent,
    EnvironmentAction,
    EnvironmentObservation,
    EnvironmentState,
    GeometryTag,
    MissionOffsets,
    ResetRequest,
    StepResult,
    TaskConfig,
)
```
- **What is a relative import?** Notice the dots `.env` and `.models`. This tells Python: "Look in the exact same folder as this `__init__.py` file for a file named `env.py` and `models.py`."
- **Why do this?** The `orbits_env` package is built out of many different files to keep the codebase organized. However, for a user trying to use this package, it is annoying to remember exactly which file contains which class. 
    - E.g., The user doesn't want to type `from orbits_env.models import ActionType`.
- By importing these classes into the `__init__.py` file, we are "bubbling them up" to the top level of the package. Now, users can simply type:
    ```python
    from orbits_env import SpaceDebrisEnv, ActionType
    ```
    This creates a clean, unified "Public API" for the package.

### 2. Defining `__all__`

```python
__all__ = [
    "ActionType",
    "ConjunctionEvent",
    "EnvironmentAction",
    "EnvironmentObservation",
    "EnvironmentState",
    "GeometryTag",
    "MissionOffsets",
    "ResetRequest",
    "SpaceDebrisEnv",
    "StepResult",
    "TaskConfig",
]
```

- **What is `__all__`?** In Python, `__all__` is a special list of strings. It tells Python exactly which names should be exported when someone uses a wildcard import.
- **Wildcard Imports:** If a user writes `from orbits_env import *` in their script, Python will look at the `__all__` list to decide what to give them. It will *only* import the 11 classes listed above.
- **Security & Cleanliness:** If we had imported some standard libraries at the top of this file (like `import os` or `import json`), we wouldn't want `import *` to accidentally give the user `os` and `json`. Defining `__all__` explicitly prevents internal variables and hidden helper functions from leaking out into the user's codebase, keeping their environment clean.