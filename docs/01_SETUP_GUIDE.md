# Setup & Quickstart Guide

This guide explains the tools required to run the Orbits OpenEnv project and the exact commands to get it working on your local machine.

## Prerequisites: The Tools We Use

Before we run the code, you need a few standard software development tools installed on your computer:

1. **Python (3.10+)**: The programming language used for the entire project.
2. **`uv`**: A modern, extremely fast Python package manager written in Rust. It replaces older tools like `pip` or `poetry`. It manages our "virtual environment" (a sandbox for our code so its dependencies don't mess up your computer).
3. **Docker (Optional but recommended)**: A tool that packages our code into a "container", ensuring it runs exactly the same way on your computer as it does on a cloud server.
4. **Make**: A classic terminal tool that uses the `Makefile` to run long, complex commands using short shortcuts.

## Step 1: Install Dependencies

Open your terminal, navigate to the `orbits` project folder, and run:

```bash
uv sync
```

**What this does:** `uv` looks at the `pyproject.toml` and `uv.lock` files, downloads all the required libraries (like `fastapi`, `pydantic`, `openai`, `pytest`), and installs them in a hidden folder called `.venv`.

## Step 2: Run the Tests

To make sure everything downloaded correctly and the code isn't fundamentally broken, run the automated tests:

```bash
make test
```

**What this does:** It runs `pytest`, which executes all the files in the `tests/` folder. You should see a lot of green checkmarks indicating success.

## Step 3: Run the Hardcoded AI (Baseline)

Let's watch a simple, hardcoded AI play the game.

```bash
make baseline
```

**What this does:** It runs `scripts/run_baseline.py`. The simulation will start, and the basic `if/else` AI will make decisions. It will print out a final score at the end.

## Step 4: Run the Web Server Locally

If you want to interact with the environment via HTTP (like a website), start the server:

```bash
make serve
```

**What this does:** It boots up the FastAPI application (`server/app.py`) on your local machine (usually at `http://127.0.0.1:8000`). You can visit `http://127.0.0.1:8000/docs` in your browser to see the interactive API documentation!

## Step 5: Run the LLM Agent (Inference)

To run the "smart" AI that uses a Large Language Model, you must provide it with API keys.

First, set up your terminal with the required keys (replace the placeholder with your actual key):
```bash
export API_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
export MODEL_NAME="gemini-2.5-flash"
export HF_TOKEN="your_actual_api_key_here"
```

Then run:
```bash
make inference
```

**What this does:** It runs `inference.py`, which will send the game state to the LLM, ask the LLM for a decision, execute that decision in the game, and repeat until the game is over.