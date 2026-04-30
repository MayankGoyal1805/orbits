# Understanding `pyproject.toml`

Welcome! In this tutorial, we will explore the `pyproject.toml` file.

## What is `pyproject.toml`?
TOML (Tom's Obvious, Minimal Language) is a simple configuration file format. In the Python ecosystem, `pyproject.toml` has become the absolute standard for defining how a Python project is built, packaged, and managed. It replaces older files like `setup.py` and `requirements.txt`.

---

## File Breakdown

### 1. Project Metadata
```toml
[project]
name = "orbits-openenv"
version = "0.1.0"
description = "OpenEnv environment for space debris collision avoidance."
readme = "README.md"
requires-python = ">=3.11"
```
- `[project]`: This header starts a specific "table" (section) in TOML.
- Here, we declare the basic information about our project.
- `requires-python`: Specifies that this project leverages modern Python features and won't run on anything older than Python 3.11.

### 2. Core Dependencies
```toml
dependencies = [
    "fastapi>=0.115.0",
    "openenv-core>=0.2.0",
    "openai>=1.79.0",
    "pydantic>=2.10.0",
    "pyyaml>=6.0.2",
    "uvicorn>=0.34.0",
    "matplotlib>=3.10.8",
    "seaborn>=0.13.2",
]
```
These are the exact libraries our app needs to run:
- **FastAPI / uvicorn:** High-performance web framework (FastAPI) and server (uvicorn) to host our environment API.
- **Pydantic:** Validates data and types (ensures JSON payloads match what we expect).
- **OpenAI:** Used in `inference.py` to communicate with Large Language Models.
- **Matplotlib / Seaborn:** Popular data visualization and plotting libraries, likely used for reports or analysis.

### 3. Executable Scripts
```toml
[project.scripts]
server = "server.app:main"
```
- This allows you to run a command line script. Typing `server` in the terminal will automatically execute the `main()` function inside `server/app.py`.

### 4. Optional Dependencies (Development)
```toml
[project.optional-dependencies]
dev = [
    "httpx>=0.28.0",
    "pytest>=8.3.0",
    "ruff>=0.12.0",
]
```
- These libraries are only installed if you specify that you are working on the code (developing), not just running it.
- **httpx:** An HTTP client used for making web requests (often used to test FastAPI endpoints).
- **pytest:** The industry-standard framework for writing and running automated tests.
- **ruff:** An incredibly fast Python linter and code formatter written in Rust. It checks your code for style errors.

### 5. Build System Configurations
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/orbits_env"]
```
- Defines how to turn our raw code into a distributable Python package (`.whl` file).
- We use **Hatchling** as our build backend.
- We specifically tell it to package the code found inside the `src/orbits_env` folder.

### 6. UV Package Manager Configuration
```toml
[tool.uv]
package = true
```
- **uv** is a blazing-fast Python package installer and resolver. This tells `uv` to treat our project directory as an installable package rather than just a folder of scripts.

### 7. Linter and Tester Configs
```toml
[tool.ruff]
line-length = 100

[tool.pytest.ini_options]
pythonpath = ["src", "."]
testpaths = ["tests"]
```
- **Ruff Configuration:** We tell Ruff to allow lines of code up to 100 characters long (the default is often 88).
- **Pytest Configuration:** Tells Pytest where to look for source code (`src` and the root `.`) and where to find the test files (`tests/` directory).