# OpenEnv And Config

This file explains how project configuration pieces fit together.

## openenv.yaml

`openenv.yaml` is the benchmark metadata contract. It declares:

- Benchmark identity: `name`, `version`, `benchmark`.
- Runtime app entrypoint: `module` and `app` (`server.app:app`).
- Environment implementation: package/class (`orbits_env.SpaceDebrisEnv`) and model types.
- Task list and difficulty metadata.
- API endpoint mapping (`/reset`, `/step`, `/state`, `/grade`, `/close`, `/health`).

Think of this as the canonical machine-readable description of the environment.

## pyproject.toml

Defines package metadata and dependencies.

Important sections:

- `[project]`: package name, version, Python requirement, runtime dependencies.
- `[project.optional-dependencies].dev`: test/lint tooling (`pytest`, `ruff`, `httpx`).
- `[tool.uv] package = true`: tells `uv` this is a package project.
- `[tool.pytest.ini_options]`: test discovery (`tests`) and python path (`src`, `.`).
- `[project.scripts]`: `server` command points to `server.app:main`.

## Makefile

The Makefile standardizes local workflows and ensures commands run through `uv`.

Patterns to notice:

- Every Python command uses `uv run ...` so the selected environment is consistent.
- Single command names (`baseline`, `inference`, `serve`) reduce cognitive load.

## .gitignore and .dockerignore

`.gitignore` excludes virtual envs, caches, local outputs, and local env files.

`.dockerignore` trims build context to keep images smaller/faster and avoid shipping unnecessary local artifacts.

## README Frontmatter

The top YAML block in `README.md` includes:

- `sdk: docker`
- `app_port: 7860`

This supports Docker-based Space deployment conventions.
