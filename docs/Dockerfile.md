# Understanding `Dockerfile`

Welcome to this step-by-step tutorial on the project's `Dockerfile`.

## What is Docker?
Docker is a tool that allows developers to package an application along with all of its dependencies, libraries, and configurations into a single, standardized unit called a **Container**. This ensures that the application will run exactly the same way on your laptop, a coworker's laptop, or a cloud server.

A `Dockerfile` is simply a recipe containing a list of instructions on how to build this container image.

---

## Line-by-Line Breakdown

### 1. The Base Image
```dockerfile
FROM python:3.11-slim
```
- `FROM`: Every Dockerfile must start with a base image. We are inheriting a pre-made operating system that already has Python installed.
- `python:3.11-slim`: We are using Python 3.11. The `-slim` variant means it's a lightweight version of Linux (usually Debian-based) with only the bare minimum tools installed. This keeps the final container size small.

### 2. Setting the Working Directory
```dockerfile
WORKDIR /app
```
- `WORKDIR`: Sets the working directory inside the container. 
- From this line forward, any files we copy or commands we run will happen inside the `/app` folder inside the virtual container's filesystem.

### 3. Copying Files into the Container
```dockerfile
COPY pyproject.toml README.md openenv.yaml /app/
COPY src /app/src
COPY server /app/server
COPY scripts /app/scripts
```
- `COPY`: This instruction copies files from your host machine (your actual laptop/server) into the container environment.
- First, we copy essential configuration files (`pyproject.toml` for dependencies, `openenv.yaml` for environment configs) to the root `/app/`.
- Next, we copy over all of our code directories: the core logic (`src`), the API logic (`server`), and utility scripts (`scripts`).

### 4. Installing Dependencies
```dockerfile
RUN pip install .
```
- `RUN`: Executes a shell command inside the container during the build phase.
- `pip install .`: This tells pip (Python's package installer) to install the package located in the current directory (`.`). Because we copied `pyproject.toml` over, pip reads it, downloads all necessary dependencies (like FastAPI and Pydantic), and installs them globally inside the container.

### 5. Exposing Ports
```dockerfile
EXPOSE 7860
```
- `EXPOSE`: This acts as documentation for anyone using this container. It states that the application inside is going to be listening for network traffic on port `7860`.
- Note: This doesn't actually publish the port to the outside world; you still have to map it when running the container (e.g., `docker run -p 7860:7860`).

### 6. The Default Command
```dockerfile
CMD ["python", "-m", "uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
```
- `CMD`: Specifies the default command that will run when a container starts up from this image.
- `python -m uvicorn`: We are launching the uvicorn web server.
- `server.app:app`: We are pointing it to the FastAPI application instance named `app` located inside the `server/app.py` file.
- `--host 0.0.0.0`: **Crucial inside Docker.** This tells the server to bind to all network interfaces. If it bound to localhost (`127.0.0.1`), you wouldn't be able to access the server from outside the container.
- `--port 7860`: Instructs the server to listen on port 7860, matching our EXPOSE directive above.