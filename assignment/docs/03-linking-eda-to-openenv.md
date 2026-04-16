# Linking EDA To The OpenEnv Project

Short answer: yes, you can absolutely use this dataset work in the actual project.

Right now, the environment in `src/orbits_env/tasks/catalog.py` is hand-crafted and synthetic. Your EDA can be used to calibrate, justify, and optionally generate data-driven task parameters.

## 1) Current Situation

Current environment design:

- task definitions are manually specified (`easy/medium/hard`)
- conjunction event probabilities/effectiveness/risk growth are synthetic values
- no direct external dataset ingestion in runtime simulator

This is normal for a benchmark starter.

## 2) Practical Ways To Use EDA Outputs

### Option A: Calibration-Only (Fastest, safest)

Use EDA findings to tune static task parameters:

- set realistic initial risk ranges from observed distributions
- tune event counts per task using debris prevalence
- tune uncertainty/tracking-sensitivity ranges using data quality insight
- tune orbit/mission constraints based on UCS orbit distribution (LEO-heavy)

What changes in code:

- only `src/orbits_env/tasks/catalog.py`
- no runtime data dependency added

### Option B: Offline Parameter Build Step (Recommended)

Create an offline script that reads `assignment/eda/input_data/processed/*.csv` and writes:

- `src/orbits_env/tasks/task_priors.json`

Then have `catalog.py` load priors and construct tasks from those priors.

Pros:

- reproducible and data-driven
- runtime remains lightweight
- easy to explain in reports

### Option C: Runtime Data-Driven Sampling (Advanced)

Load processed data at environment init and sample conjunction events per episode.

Pros:

- highest realism potential

Cons:

- more runtime complexity
- larger coupling between benchmark and data artifacts
- harder reproducibility unless versioned carefully

## 3) Suggested Integration Plan For Your Deadline

For assignment/presentation, use Option A + Option B narrative:

1. Keep current environment runnable.
2. Show where EDA evidence maps to task design.
3. Add a simple offline prior-extraction script later (post-presentation if needed).

## 4) Example Mapping (EDA -> Environment)

1. Debris prevalence in SATCAT (`DEB` dominant)
- increase multi-threat scenarios in medium/hard tasks.

2. LEO dominance in UCS
- bias conjunction geometry and timing assumptions toward LEO-like crowded operations.

3. Temporal launch growth
- justify increasing risk-growth pressure in hard scenarios.

4. Missingness in certain metadata
- avoid over-reliance on sparse fields (power, dry mass) for core risk logic.

5. Kelvins trajectory density
- use trajectory-derived variability for uncertainty/risk-growth priors.

## 5) What To Say If Asked “Why Not Directly Use Raw Data Now?”

Use this answer:

- The benchmark currently prioritizes deterministic reproducibility and low runtime complexity.
- We first used real data for calibration and justification.
- The next iteration introduces an offline prior-generation step so task values are data-derived while runtime remains stable.

This is a strong engineering answer.

## 6) Minimal Concrete Next Step You Can Implement

Create a script (example path):

- `assignment/eda/build_task_priors.py`

Script output:

- JSON with percentiles/ranges for risk proxies and orbital distributions.

Then in `src/orbits_env/tasks/catalog.py`:

- optionally load JSON if present
- fallback to hardcoded defaults if absent

This gives you backward compatibility and a clear migration story.
