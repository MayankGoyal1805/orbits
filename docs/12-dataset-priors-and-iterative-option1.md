# Dataset Priors And Iterative Option 1

This document explains what was implemented for Option 1 and exactly how EDA datasets are used.

## What Was Implemented

1. Dataset-driven priors builder:
- `scripts/build_task_priors.py`
- reads processed EDA files and writes `src/orbits_env/tasks/task_priors.json`

2. Priors-aware task catalog:
- `src/orbits_env/tasks/catalog.py`
- loads task overrides from priors JSON if present
- falls back to original hardcoded defaults when priors are absent

3. Iterative self-improvement runner:
- `scripts/run_iterative_inference.py`
- runs multiple rounds
- carries strategy memory between rounds
- keeps best round by success-rate then average score

4. Inference enhancements for iterative mode:
- `inference.py` now supports optional strategy-memory injection per round
- per-task run returns structured metrics for iterative evaluation
- existing `uv run python inference.py` behavior remains unchanged

## Exact Dataset Inputs Used

From `assignment/eda/input_data/processed`:

1. `satcat_clean.csv`
- `OBJECT_TYPE` distribution used for debris/payload ratios
- debris ratio influences global risk scaling

2. `ucs_clean.csv`
- `Class of Orbit` used for LEO/GEO ratios
- LEO ratio influences tracking sensitivity and risk context scaling

3. `kelvins_labels_clean.csv`
- eccentricity-like bounded feature used to scale uncertainty priors
- inclination spread used to modulate tracking sensitivity scaling
- area-to-mass median captured in priors metadata

## How Priors Affect Environment Parameters

Generated file `src/orbits_env/tasks/task_priors.json` includes:

- `dataset_stats`: computed summary stats and scaling terms
- `task_overrides`: field-level updates for each difficulty

Per difficulty, current overrides include:

1. `initial_tracking_quality`
2. `success_probability_threshold`
3. conjunction-level values:
- `uncertainty`
- `risk_growth_rate`
- `tracking_sensitivity`

These values modify task setup before simulation begins, so the same simulator logic runs on data-informed task parameters.

## Option 1 Loop Details

`run_iterative_inference.py` performs:

1. Round 1:
- runs all tasks with dataset strategy notes from priors metadata

2. Reflection step:
- computes failures/successes and residual risk patterns
- builds adaptive notes (risk thresholds, tracking guidance, offset control)

3. Next round:
- reruns all tasks with updated strategy memory in prompt context

4. Selection:
- best round chosen by `(success_rate, avg_score)`

This is context-level adaptation, not weight-level RL.

## Observed Run Example

Two-round run produced:

- Round 1: `avg_score=0.5497`, `success_rate=0.00`
- Round 2: `avg_score=0.5874`, `success_rate=0.67`

So Option 1 achieved a meaningful practical improvement in this run.

## Commands

Build priors:

```bash
make build-priors
```

Single-pass inference:

```bash
make inference
```

Iterative Option 1 inference:

```bash
make iterative-inference
```

Custom rounds/output:

```bash
uv run python scripts/run_iterative_inference.py --rounds 2 --output iterative_inference_results.json
```

## Notes

- If priors JSON is missing or invalid, catalog falls back to default tasks.
- You can override priors path with `ORBITS_TASK_PRIORS_PATH`.
- Iterative output writing now falls back to a local file if target path is not writable.
