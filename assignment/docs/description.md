# Orbits Project Description (Presentation Ready)

## 1. What The Project Is

This project implements an OpenEnv-compatible collision-avoidance environment where an agent controls satellite actions under uncertainty.

The environment is exposed through an API and can be run in local Python mode or Docker mode.

Core implementation files:

- [src/orbits_env/env.py](src/orbits_env/env.py)
- [src/orbits_env/simulator.py](src/orbits_env/simulator.py)
- [src/orbits_env/tasks/catalog.py](src/orbits_env/tasks/catalog.py)
- [src/orbits_env/graders/scoring.py](src/orbits_env/graders/scoring.py)
- [server/app.py](server/app.py)

## 2. How Inference Works Right Now

The current system is LLM-first (strict mode by default):

1. load environment variables (optionally from local `.env`)
2. call model for action at each step
3. environment advances with that action
4. log step rewards and final score

Main file:

- [inference.py](inference.py)

Important: this is not gradient-based RL training. It is iterative decision-making using model calls and environment feedback.

## 3. Option 1 Implemented (Iterative Self-Improvement)

Implemented script:

- [scripts/run_iterative_inference.py](scripts/run_iterative_inference.py)

Loop behavior:

1. run all three tasks for Round 1
2. compute round metrics
3. generate reflection notes from failures/risk/offset behavior
4. rerun with updated strategy memory
5. select best round by `(success_rate, avg_score)`

Outputs:

- JSON metrics file (round summaries): typically [iterative_inference_results.json](iterative_inference_results.json)
- human-readable detailed log: [output.txt](output.txt)

## 4. Exact Success-Rate Calculation

Success rate in iterative runs is computed per round as:

$$
\text{success\_rate} = \frac{\text{number of task results where success=True}}{\text{total tasks in round}}
$$

In this project each round runs 3 tasks (easy/medium/hard), so:

- `1.00` means `3/3` successful tasks
- `0.67` means `2/3`
- `0.00` means `0/3`

Where this is implemented:

- [scripts/run_iterative_inference.py](scripts/run_iterative_inference.py)

And each task’s `success` field comes from final environment state:

- [inference.py](inference.py)
- [src/orbits_env/simulator.py](src/orbits_env/simulator.py)

## 5. How Datasets Are Used (Current Implementation)

Dataset artifacts used for priors:

- [assignment/eda/input_data/processed/satcat_clean.csv](assignment/eda/input_data/processed/satcat_clean.csv)
- [assignment/eda/input_data/processed/ucs_clean.csv](assignment/eda/input_data/processed/ucs_clean.csv)
- [assignment/eda/input_data/processed/kelvins_labels_clean.csv](assignment/eda/input_data/processed/kelvins_labels_clean.csv)

Priors builder:

- [scripts/build_task_priors.py](scripts/build_task_priors.py)

Generated priors file:

- [src/orbits_env/tasks/task_priors.json](src/orbits_env/tasks/task_priors.json)

Priors loaded into task config here:

- [src/orbits_env/tasks/catalog.py](src/orbits_env/tasks/catalog.py)

### 5.1 SATCAT contribution

- `OBJECT_TYPE` distribution -> debris ratio / payload ratio
- debris ratio contributes to `risk_scale`

### 5.2 UCS contribution

- `Class of Orbit` -> LEO/GEO ratio
- LEO ratio contributes to tracking and scenario pressure scaling

### 5.3 Kelvins labels contribution

- uses bounded eccentricity-like feature for uncertainty scaling
- uses inclination spread for tracking scaling context
- uses area-to-mass median as descriptive dataset statistic

### 5.4 What gets overridden in tasks

From priors, current overrides include:

- `initial_tracking_quality`
- `success_probability_threshold`
- per-conjunction:
  - `uncertainty`
  - `risk_growth_rate`
  - `tracking_sensitivity`

This means datasets already influence episode difficulty and dynamics indirectly through task parameters.

## 6. Why Only Kelvins Labels Are Used Right Now (Not Full Trajectories)

Yes, currently priors builder uses `kelvins_labels_clean.csv` and does not yet consume the long trajectory files directly.

Trajectory files exist and are processed in EDA:

- [assignment/eda/input_data/processed/kelvins_deb_train_long.csv](assignment/eda/input_data/processed/kelvins_deb_train_long.csv)
- [assignment/eda/input_data/processed/kelvins_deb_test_long.csv](assignment/eda/input_data/processed/kelvins_deb_test_long.csv)
- [assignment/eda/input_data/processed/kelvins_sat_long.csv](assignment/eda/input_data/processed/kelvins_sat_long.csv)

Why labels-first was chosen:

1. labels are compact and stable for first priors integration
2. trajectory tables are high-volume temporal data requiring additional feature engineering
3. this keeps runtime/task generation deterministic and lightweight while still data-informed

Planned next step:

- add trajectory-derived features (volatility, temporal drift, dispersion) into priors generation in [scripts/build_task_priors.py](scripts/build_task_priors.py)

## 7. Why Rounds Can Look Identical Sometimes

If you run in fallback-heuristic mode, policy is deterministic, so rounds can be identical.

For true iterative LLM variation:

1. keep fallback disabled (default strict mode)
2. ensure valid `HF_TOKEN`, `API_BASE_URL`, `MODEL_NAME`
3. control rate limits via pacing variables

## 8. What To Run Before Iterative Inference

Recommended sequence:

1. sync env and dependencies:

```bash
make sync
```

2. rebuild data-driven priors (especially after EDA changes):

```bash
make build-priors
```

3. run iterative inference with desired rounds:

```bash
make iterative-inference ITERATIVE_ROUNDS=3
```

Outputs to present:

- [iterative_inference_results.json](iterative_inference_results.json)
- [output.txt](output.txt)

## 9. Presentation One-Liner

We integrated SATCAT/UCS/Kelvins EDA into data-driven task priors, then used iterative LLM strategy refinement across rounds, evaluated by per-round success-rate and score on easy/medium/hard tasks.