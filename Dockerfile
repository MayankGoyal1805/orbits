FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md openenv.yaml /app/
COPY src /app/src
COPY server /app/server
COPY scripts /app/scripts

RUN pip install .

EXPOSE 7860

CMD ["python", "-m", "uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
