# Learning Path: How to Navigate This Project

Welcome to the **Orbits OpenEnv** project! If you are a beginner to Python, Reinforcement Learning (RL), or Space Physics, this codebase might seem overwhelming at first. Don't worry! This guide is designed to take you step-by-step from a complete novice to understanding every line of code.

## Where to Start?

Do not jump straight into the code. Follow this exact reading order to build your understanding layer by layer.

### Phase 1: High-Level Concepts (Start Here)
Before looking at Python files, read these overviews to understand *what* we are building and *why*:
1. **`03_PHYSICS_AND_DOMAIN.md`**: Learn about Space Debris, Collision Probability, and the simplified orbital mechanics used in this game.
2. **`02_ARCHITECTURE_OVERVIEW.md`**: Understand how the different pieces of software (the Simulation, the Web Server, the AI Agent) talk to each other.
3. **`01_SETUP_GUIDE.md`**: Learn how to install the tools (Python, Docker, `uv`) needed to run this project on your own computer.

### Phase 2: The Core Rules (Data Models)
In modern Python, we define the "shape" of our data before we write the logic. 
* **Read: `src_orbits_env_models_py.md`** 
  * *Why?* This file defines the dictionary and lists used everywhere else. You'll learn what an `EnvironmentAction` looks like and what data is inside a `ConjunctionEvent`.

### Phase 3: The Physics Engine & Environment
Now we look at the game itself. How does time move forward? How do we calculate the score?
1. **Read: `src_orbits_env_simulator_py.md`**: The hardest file! This handles the math of moving the satellite and calculating risk.
2. **Read: `src_orbits_env_env_py.md`**: The "controller". It wraps the complex simulator into simple `reset()` and `step()` functions for the AI to use.
3. **Read: `src_orbits_env_tasks_catalog_py.md`**: See how different difficulty levels (easy, medium, hard) are defined.
4. **Read: `src_orbits_env_graders_scoring_py.md`**: Learn how the final grade (from 0.0 to 1.0) is mathematically calculated at the end of the game.

### Phase 4: The Web Server
We need a way for our AI (which might be running on a different computer) to play the game over the internet.
* **Read: `server_app_py.md`**: Learn how FastAPI is used to turn our Python environment into a web server that accepts HTTP requests.

### Phase 5: The AI Agents (Inference)
Now we build the AI that plays the game!
1. **Read: `src_orbits_env_baseline_py.md`**: Look at a "dumb" AI. It just uses `if/else` statements to decide what to do. It's a great baseline.
2. **Read: `inference_py.md`**: Look at the "smart" AI. Learn how we connect to Large Language Models (like OpenAI or Gemini) and ask them to choose our next move.

### Phase 6: Scripts and Automation
Learn how we run these files automatically from the terminal.
* **Read: `Makefile.md` & `pyproject_toml.md`**: Understand how project commands and dependencies are organized.
* **Read: `scripts_run_iterative_inference_py.md`**: Learn how we run the AI in a loop so it can learn from its mistakes.

### Phase 7: Testing
Professional code is always tested.
* **Read: `tests_test_env_py.md` & `tests_test_api_py.md`**: Learn how `pytest` is used to automatically check if our code is broken.

Take your time, read line-by-line, and welcome to Orbits!