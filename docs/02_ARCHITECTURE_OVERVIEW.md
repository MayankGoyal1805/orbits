# System Architecture Overview

To understand the codebase, you need to understand how the different components talk to each other. This project is divided into three main conceptual blocks: **The Core Environment**, **The Web Server**, and **The Agent**.

Here is a high-level map of the system:

```text
+-----------------------+         HTTP / JSON          +-----------------------+
|      THE AGENT        |  <========================>  |     THE WEB SERVER    |
|   (inference.py)      |                              |    (server/app.py)    |
|                       |  <========================>  |                       |
| 1. Reads Observation  |         REST API             | 1. Receives Actions   |
| 2. Asks LLM for move  |                              | 2. Validates Data     |
| 3. Sends Action       |                              | 3. Talks to Core Env  |
+-----------------------+                              +-----------+-----------+
                                                                   |
                                                                   | Internal Python Calls
                                                                   v
                                                       +-----------------------+
                                                       | THE CORE ENVIRONMENT  |
                                                       | (src/orbits_env/)     |
                                                       |                       |
                                                       | 1. env.py (Wrapper)   |
                                                       | 2. simulator.py       |
                                                       | 3. models.py (Types)  |
                                                       +-----------------------+
```

## 1. The Core Environment (`src/orbits_env/`)
This is the heart of the project. It contains all the rules of the universe, the physics math, and the scoring system.
- **It is completely independent.** The Core Environment does not know about the Internet, HTTP, or Large Language Models. It just takes in Python commands and outputs Python data.
- **The Loop:** It relies on two main functions:
  - `reset()`: Starts a new game and returns the initial state.
  - `step(action)`: Takes an action, advances the game by one "turn", and returns the new state, the score (reward), and whether the game is over (done).

## 2. The Web Server (`server/app.py`)
In the modern AI world, we want to evaluate agents remotely. We don't want the AI to run on the exact same computer as the simulation engine. 
- To solve this, we wrap the Core Environment in a **FastAPI Web Server**.
- The server creates "endpoints" (like URLs). When the Agent sends a packet of JSON data (an Action) to the `/step` endpoint, the server translates that JSON into a Python object, hands it to the Core Environment, gets the result back, turns the result back into JSON, and sends it to the Agent over the internet.
- **OpenEnv Standard:** This server follows a specific API standard called `OpenEnv`. This ensures that any Agent built for OpenEnv can talk to this server without knowing how the underlying code works.

## 3. The Agent (`inference.py` or `baseline.py`)
The Agent is the "Player". 
- It lives entirely outside the Environment.
- In this project, our primary agent (`inference.py`) acts as a translator between the Environment and a Large Language Model (LLM).
- **The Agent Loop:**
  1. It asks the Environment for the current state (Observation).
  2. It formats that state into a text prompt.
  3. It sends the prompt to the LLM (like OpenAI or Gemini).
  4. The LLM replies with a JSON string representing a decision.
  5. The Agent parses the JSON into an Action.
  6. The Agent sends the Action to the Environment's `step()` function.
  7. Repeat until the episode is `done`.

By separating these three layers, we make the code modular, testable, and highly scalable!