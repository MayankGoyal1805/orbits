# Project Context: Option 4 - Space Debris Collision Avoidance OpenEnv

## Project Idea
Build an OpenEnv environment where an autonomous spacecraft agent learns to avoid collisions with space debris while preserving fuel and respecting operational constraints.

This project is realistic, strongly aligned with sequential decision-making, and suitable for both:
- a practical OpenEnv benchmark environment
- an EDA + methods report

## Why This Option
- Strong OpenEnv fit: clear step/reset dynamics, measurable outcomes, and multi-task grading.
- Good novelty/feasibility balance: less saturated than urban heat island ML while still data-rich.
- Real-world relevance: conjunction events and maneuver planning are active aerospace problems.

## Environment Goal
At each decision step, the agent chooses whether and how to maneuver in order to:
- reduce collision risk
- maintain safe miss distance
- minimize total delta-v (fuel use)
- avoid unnecessary or unstable maneuver patterns

## Core OpenEnv Design

### State (example features)
- Relative geometry: range, relative velocity, estimated miss distance.
- Orbit context: propagated object states from TLE/GP data.
- Risk context: conjunction risk proxy (and uncertainty proxies when available).
- Vehicle status: remaining fuel, max burn, mission constraints.
- Time context: time-to-closest-approach and decision horizon.

### Actions
- Discrete MVP action space:
  - no-op
  - small/medium/large burns in standard maneuver directions
- Optional advanced action space:
  - continuous burn vector + timing

### Reward
- Positive reward for reducing risk and improving final safety.
- Penalty for fuel expenditure and excessive maneuvers.
- Large penalty for unsafe terminal outcomes.
- Optional shaping for monotonic risk reduction.

## Suggested Tasks and Graders
Use multiple tasks with normalized scores in [0.0, 1.0]:

1. Single-threat avoidance
- One debris object, moderate warning time.
- Grader emphasizes safe separation and low fuel.

2. Multi-threat avoidance
- Several debris objects in a shared horizon.
- Grader emphasizes robust decision quality under complexity.

3. Fuel-constrained avoidance
- Tight delta-v budget.
- Grader emphasizes safety with efficient control.

4. Late-warning scenario
- Short decision horizon before closest approach.
- Grader emphasizes urgency handling and graceful degradation.

## Baselines
- Rule-based threshold policy (deterministic).
- One-step maneuver heuristic baseline.
- Optional RL baseline (e.g., PPO) for comparison.

## Primary Evaluation Metrics
- Collision rate / unsafe event rate.
- Final miss distance.
- Total delta-v consumed.
- Number of maneuvers per episode.
- Task success score (grader output).

## Datasets

### 1) CelesTrak GP/TLE Catalog (primary)
- Use: initialize and propagate object orbits.
- Role: foundational orbital state data for scenario generation.

### 2) CelesTrak SOCRATES / Conjunction Screening (primary)
- Use: candidate close-approach events and risk-relevant context.
- Role: build realistic episodes and threat windows.

### 3) ESA DISCOSweb (secondary)
- Use: object metadata (type, size, status, etc.).
- Role: enrich state features and filter realistic subsets.
- Note: API registration may be required.

### 4) ESA Kelvins Collision-Avoidance Challenge Resources (reference)
- Use: benchmark-style framing and scenario design inspiration.
- Role: improve task realism and reporting comparability.

### 5) Space-Track/CDM-style Data (advanced)
- Use: higher-fidelity conjunction workflows.
- Role: post-MVP realism upgrade.
- Note: access is typically more restrictive.

## Recommended MVP Data Stack
Start with:
- CelesTrak GP/TLE
- CelesTrak conjunction outputs

Then add:
- ESA DISCOSweb metadata

Finally (optional):
- CDM-like uncertainty-rich inputs

## EDA Plan (for the report)
- Distribution of conjunction distances, relative speeds, and warning times.
- Frequency trends by orbit region and object category.
- Relationship between maneuver magnitude/timing and post-maneuver risk proxy.
- Scenario difficulty clusters for task construction.

## Deliverable Outline
1. OpenEnv environment with typed models and deterministic reset/step behavior.
2. Multi-task graders with normalized scoring.
3. Reproducible baseline script and metrics table.
4. EDA section connecting data characteristics to environment design decisions.
5. Deployment-ready packaging (Docker + reproducibility notes).
