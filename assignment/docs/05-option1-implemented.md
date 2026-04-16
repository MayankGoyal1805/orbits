# Option 1 Implemented (Dataset-Driven + Iterative)

This note is presentation-oriented and describes what is now actually implemented.

## What Was Added

1. Dataset-to-priors build step:
- command: `make build-priors`
- script: `scripts/build_task_priors.py`
- output: `src/orbits_env/tasks/task_priors.json`

2. Environment task loading now uses priors when available:
- file: `src/orbits_env/tasks/catalog.py`
- fallback to built-in defaults if priors are missing

3. Iterative self-improvement runner (Option 1):
- script: `scripts/run_iterative_inference.py`
- command: `make iterative-inference`
- performs multi-round run + reflection notes + best-round selection
- round count is configurable (`ITERATIVE_ROUNDS=<n>`)
- writes detailed step-by-step report to `output.txt`

## How Datasets Are Used Exactly

From your EDA processed outputs:

1. SATCAT (`satcat_clean.csv`)
- debris ratio computed from `OBJECT_TYPE`
- affects global risk scaling

2. UCS (`ucs_clean.csv`)
- LEO ratio from `Class of Orbit`
- affects tracking sensitivity and scenario pressure assumptions

3. Kelvins (`kelvins_labels_clean.csv`)
- eccentricity-like bounded feature used for uncertainty scaling
- inclination spread used in tracking scaling context

These statistics are converted into explicit task overrides:

- `initial_tracking_quality`
- `success_probability_threshold`
- conjunction `uncertainty`
- conjunction `risk_growth_rate`
- conjunction `tracking_sensitivity`

## What Improved In Actual Run

Example two-round Option 1 run:

- Round 1: avg score `0.5497`, success rate `0.00`
- Round 2: avg score `0.5874`, success rate `0.67`

So both average score and success rate improved.

## Important Clarification For Presentation

This is not gradient-based RL training.

It is iterative policy improvement via:

- data-informed scenario priors
- round-to-round strategy feedback in context
- best-round selection

## Suggested Slide Sentence

"We integrated SATCAT/UCS/Kelvins EDA outputs into task priors and implemented iterative self-improvement inference. In our run, this increased success rate from 0% to 67% and improved average score from 0.5497 to 0.5874."
