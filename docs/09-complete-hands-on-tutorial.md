# Complete Hands-On Tutorial

This is a detailed, end-to-end tutorial for learning the project by running it.

It assumes:

- You are in repository root.
- You already ran `uv sync`.

## 1. Understand The Project In One Minute

This repository implements an OpenEnv benchmark for satellite conjunction management.

Your agent receives uncertain conjunction observations and chooses one action each step:

- do nothing (`noop`)
- request better tracking (`request_tracking_update`)
- execute one of three maneuver axes (`radial`, `along_track`, `normal`)

Goal tradeoff:

- reduce collision risk
- preserve fuel
- avoid excessive mission offset

## 2. Confirm Local Environment

Run:

```bash
pwd
uv --version
```

Expected:

- You are in project root.
- `uv` prints version successfully.

## 3. Run The Test Suite

Run:

```bash
make test
```

What this verifies:

- API lifecycle methods work.
- Environment reset/step logic works.
- Inference output format contract works.

Expected from a healthy setup:

- all tests pass.

## 4. Run Baseline Policy

Run:

```bash
make baseline
```

What it does:

- runs deterministic heuristic on easy/medium/hard tasks
- prints per-task metrics

Main output fields to read:

- `score`: final grade in `0.0..1.0`
- `success`: whether safe completion criteria were met
- `fuel_remaining`: leftover fuel
- `total_offset_km`: mission orbit deviation proxy
- `highest_collision_probability`: residual worst-case risk

If you want saved artifact:

```bash
make baseline-save
```

Output file:

- `outputs/evals/baseline_scores.json`

## 5. Run Inference Script

Run:

```bash
make inference
```

Important behavior:

- if `HF_TOKEN` is unset, script uses deterministic heuristic fallback.
- if `HF_TOKEN` is set and API endpoint/model are valid, script calls the LLM.

Expected log format only:

- `[START] ...`
- `[STEP] ...`
- `[END] ...`

This strict format is intentional and tested.

## 6. Run API Server

Run:

```bash
make serve
```

Server URL:

- `http://127.0.0.1:7860`

In another terminal, check health:

```bash
curl -fsSL http://127.0.0.1:7860/health
```

Expected response:

```json
{"status":"ok"}
```

## 7. Exercise Core API Endpoints

Reset episode:

```bash
curl -fsSL -X POST http://127.0.0.1:7860/reset/collision_avoidance_easy
```

Step once:

```bash
curl -fsSL -X POST http://127.0.0.1:7860/step \
  -H 'content-type: application/json' \
  -d '{"action_type":"request_tracking_update","magnitude":0.0}'
```

Read grade:

```bash
curl -fsSL http://127.0.0.1:7860/grade
```

Close episode:

```bash
curl -fsSL -X POST http://127.0.0.1:7860/close
```

## 8. Understand How One Step Works Internally

For each step in simulator:

1. action cost/effect is applied
2. passive dynamics advance (risk growth, uncertainty drift, time decrement)
3. termination conditions are checked
4. shaped reward is computed
5. next observation is built

Files to read while this mental model is fresh:

- `src/orbits_env/simulator.py`
- `src/orbits_env/models.py`
- `src/orbits_env/tasks/catalog.py`

## 9. Learn Reward vs Grade (Critical)

Two related but distinct metrics exist:

- step reward: dense learning signal from simulator
- final grade: benchmark score from grader

Reward is useful for policy shaping.
Grade is used for final evaluation quality.

Read:

- `src/orbits_env/simulator.py` (reward components)
- `src/orbits_env/graders/scoring.py` (final weighted score)

## 10. Docker Path

Build image:

```bash
make docker-build
```

Run image:

```bash
make docker-run
```

If build fails with daemon/socket error, Docker engine is not running yet. Start Docker service first, then rerun.

## 11. Submission-Style Validation

Run:

```bash
make validate
```

What it runs:

1. health ping
2. docker build
3. tests
4. baseline
5. inference

## 12. Suggested Learning Exercises

1. Change one task parameter in `tasks/catalog.py` and rerun baseline to observe score shifts.
2. Modify heuristic thresholds in `baseline.py` and compare results.
3. Add logging in `simulator.py` for reward components and inspect step-by-step policy behavior.
4. Compare trajectories with and without tracking updates.
