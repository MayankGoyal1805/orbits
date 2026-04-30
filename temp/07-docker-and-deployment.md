# Docker And Deployment

## Dockerfile Explained

`Dockerfile` builds from `python:3.11-slim` and installs the package with `pip install .`.

Key steps:

1. Set workdir to `/app`.
2. Copy project metadata and source directories.
3. Install package and dependencies into container environment.
4. Expose port `7860`.
5. Start Uvicorn serving `server.app:app`.

## Local Docker Usage

Build:

```bash
make docker-build
```

Run:

```bash
make docker-run
```

Check health:

```bash
curl -fsSL http://localhost:7860/health
```

## Hugging Face Space Notes

The README frontmatter includes `sdk: docker` and `app_port: 7860`.

That aligns with this repository's Docker serving model.

## Why Keep Docker In This Repo

- reproducible environment for reviewers
- easier parity between local and remote runtime
- clear packaging boundary for OpenEnv-compatible service
