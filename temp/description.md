# Orbits Environment Description

This document is a detailed presentation-ready reference for how the simulator works, what parameters are used, what the model is allowed to output, what metrics are evaluated, and how datasets are integrated.

## 1. System Architecture

Main runtime components:

- Environment and wrapper: [src/orbits_env/env.py](src/orbits_env/env.py)
- Simulator state transition engine: [src/orbits_env/simulator.py](src/orbits_env/simulator.py)
- Data models and constraints: [src/orbits_env/models.py](src/orbits_env/models.py)
- Task catalog and priors loading: [src/orbits_env/tasks/catalog.py](src/orbits_env/tasks/catalog.py)
- Final scoring function: [src/orbits_env/graders/scoring.py](src/orbits_env/graders/scoring.py)
- Inference runner and model calls: [inference.py](inference.py)
- Iterative Option 1 loop: [scripts/run_iterative_inference.py](scripts/run_iterative_inference.py)
- Dataset-to-priors builder: [scripts/build_task_priors.py](scripts/build_task_priors.py)

## 1.5 Exact Difficulty Levels (What We Put In Easy, Medium, Hard)

Source of truth for baseline task definitions:

- [src/orbits_env/tasks/catalog.py](src/orbits_env/tasks/catalog.py)

These baseline values can later be adjusted by priors in [src/orbits_env/tasks/task_priors.json](src/orbits_env/tasks/task_priors.json), but the default setup is:

| Parameter | easy | medium | hard |
|---|---:|---:|---:|
| horizon | 6 | 8 | 10 |
| initial_fuel | 9.5 | 8.0 | 7.2 |
| initial_tracking_quality | 0.82 | 0.68 | 0.57 |
| tracking_budget | 2 | 2 | 3 |
| visible_event_limit | 2 | 3 | 3 |
| fuel_cost_tracking | 0.10 | 0.14 | 0.16 |
| maneuver_base_cost | 0.35 | 0.42 | 0.44 |
| maneuver_variable_cost | 0.55 | 0.62 | 0.70 |
| tracking_improvement | 0.16 | 0.18 | 0.20 |
| tracking_decay | 0.04 | 0.055 | 0.07 |
| uncertainty_reduction_factor | 0.55 | 0.50 | 0.45 |
| passive_offset_recovery | 0.10 | 0.08 | 0.06 |
| mission_offset_penalty_weight | 0.18 | 0.22 | 0.26 |
| fuel_penalty_weight | 0.16 | 0.20 | 0.22 |
| risk_reduction_reward_weight | 0.95 | 1.00 | 1.04 |
| tracking_reward_weight | 0.18 | 0.22 | 0.25 |
| unsafe_probability_threshold | 0.62 | 0.58 | 0.54 |
| success_probability_threshold | 0.18 | 0.24 | 0.28 |
| max_total_offset_km | 2.4 | 2.1 | 1.9 |
| completion_bonus | 0.25 | 0.28 | 0.30 |

Conjunction setup by difficulty:

- easy: 1 conjunction, radial-dominant, relatively high initial confidence.
- medium: 2 conjunctions with mixed dominant maneuver axes.
- hard: 3 conjunctions, poorer certainty, tighter mission-offset constraint, higher risk-growth pressure.

Difficulty intuition:

- easy gives more fuel and better initial tracking quality.
- medium increases combinatorial planning pressure (multiple threats) with tighter resources.
- hard adds more threat interactions and stricter mission-preservation tolerance.

## 2. What Input The Model Gets

The model is called once per step with:

1. System prompt containing allowed action schema and mission objective.
2. User content containing:
- current observation payload
- strategy notes
- recent step history (last 4 entries)
- optional adaptive strategy memory from prior rounds in iterative mode

Observation payload fields passed to model are from [inference.py](inference.py):

- task_id
- step_index
- horizon_remaining
- fuel_remaining
- tracking_quality
- tracking_budget_remaining
- mission_offsets
- total_collision_probability
- highest_collision_probability
- visible_events (list)
- last_action

Exact observation payload shape sent to model each step:

```json
{
	"task_id": "collision_avoidance_medium",
	"step_index": 2,
	"horizon_remaining": 6,
	"fuel_remaining": 7.15,
	"tracking_quality": 0.71,
	"tracking_budget_remaining": 1,
	"mission_offsets": {
		"radial_km": 0.22,
		"along_track_km": 0.09,
		"normal_km": 0.0
	},
	"total_collision_probability": 0.51,
	"highest_collision_probability": 0.29,
	"visible_events": [
		{
			"object_id": "deb-101",
			"geometry_tag": "along_track_dominant",
			"collision_probability": 0.29,
			"predicted_miss_distance_km": 1.42,
			"time_to_closest_approach": 3,
			"uncertainty": 0.23,
			"radial_effectiveness": 0.36,
			"along_track_effectiveness": 0.82,
			"normal_effectiveness": 0.48,
			"risk_growth_rate": 0.055,
			"tracking_sensitivity": 0.55
		}
	],
	"last_action": "request_tracking_update"
}
```

Additional context also sent to the LLM in the same request:

- strategy notes (safety/fuel/offset guidance)
- recent episode history (up to 4 latest steps)
- optional adaptive strategy memory from previous rounds in [scripts/run_iterative_inference.py](scripts/run_iterative_inference.py)

Important distinction:

- model sees observed events (tracking-quality-adjusted), not raw true internal event state.

## 3. What Output The Model Is Allowed To Give

Allowed action types are defined in [src/orbits_env/models.py](src/orbits_env/models.py):

- noop
- request_tracking_update
- radial_maneuver
- along_track_maneuver
- normal_maneuver

Action schema is:

- action_type: one of the above values
- magnitude: float between 0 and 1

Validation constraints are enforced by pydantic model EnvironmentAction.

Expected output format from the LLM:

```json
{"action_type": "radial_maneuver", "magnitude": 0.52}
```

Rules:

- magnitude should be 0 for noop and request_tracking_update.
- for maneuvers, magnitude is bounded to [0, 1] by validation and simulator clamping.

Model output robustness handling in [inference.py](inference.py):

- first tries provider-side json_object response format.
- if provider JSON mode fails, retries without that mode and parses JSON locally.
- if model emits prose or <think> blocks, parser attempts JSON extraction.
- if no valid JSON object is found, parser attempts best-effort action inference from text keywords.

Exact model call parameters in [inference.py](inference.py):

- model: MODEL_NAME (default gemini-2.5-flash)
- temperature: 0.1
- max_tokens: MAX_RESPONSE_TOKENS (default 120)
- response_format: json_object
- messages:
	- system: simulator action contract and policy guidance
	- user: current observation + recent history + strategy notes (+ optional adaptive memory)

Relevant runtime environment parameters:

- API_BASE_URL (default https://generativelanguage.googleapis.com/v1beta/openai/)
- HF_TOKEN (API key source)
- MODEL_NAME (default gemini-2.5-flash)
- MAX_STEPS (default 12)
- REQUESTS_PER_MINUTE (default 30)
- REQUEST_GAP_SECONDS (default 2.5)
- MAX_LLM_RETRIES (default 2)
- RETRY_BACKOFF_SECONDS (default 1.5)
- MAX_RESPONSE_TOKENS (default 120)
- REASONING_EFFORT (optional: low, medium, high)
- ALLOW_HEURISTIC_FALLBACK (default off)

## 4. What The Simulator Tracks Internally

Core mutable state is EnvironmentState in [src/orbits_env/models.py](src/orbits_env/models.py), including:

- step index and horizon
- fuel remaining
- tracking quality and tracking budget remaining
- mission offsets by axis
- true conjunction events
- counters: tracking updates used, maneuvers used
- done flag, termination reason, collision flag, success flag
- cumulative reward

Task configuration parameters (full TaskConfig surface in [src/orbits_env/models.py](src/orbits_env/models.py)):

- task_id, difficulty, description
- horizon
- initial_fuel
- initial_tracking_quality
- tracking_budget
- visible_event_limit
- fuel_cost_tracking
- maneuver_base_cost
- maneuver_variable_cost
- tracking_improvement
- tracking_decay
- uncertainty_reduction_factor
- passive_offset_recovery
- mission_offset_penalty_weight
- fuel_penalty_weight
- risk_reduction_reward_weight
- tracking_reward_weight
- unsafe_probability_threshold
- success_probability_threshold
- max_total_offset_km
- completion_bonus
- collision_penalty
- max_magnitude
- conjunctions

Current baseline task values are defined in [src/orbits_env/tasks/catalog.py](src/orbits_env/tasks/catalog.py) for easy, medium, and hard tasks, and may be overridden by priors from [src/orbits_env/tasks/task_priors.json](src/orbits_env/tasks/task_priors.json).

## 5. Step Transition Logic (Exact Flow)

Per call to step(action) in [src/orbits_env/simulator.py](src/orbits_env/simulator.py):

1. Validate state and done flag.
2. Clamp action magnitude to task max_magnitude.
3. Apply action branch:
- request_tracking_update
- maneuver by axis
- noop
4. Advance passive dynamics:
- tracking decays
- offsets passively recover
- conjunction time-to-closest-approach decrements
- probability and uncertainty update with urgency and pressure terms
5. Increment step index and run termination checks.
6. Compute reward components and final step reward.
7. Return StepResult with observation, reward, done, info.

## 6. Reward Calculation

Reward components in [src/orbits_env/simulator.py](src/orbits_env/simulator.py):

- base
- risk_reduction
- tracking_gain
- completion_bonus
- fuel_penalty
- mission_penalty
- waste_penalty

Final reward is clamped to 0..1.

Special rule:

- if collision occurs, step reward is forced to 0.

## 7. Success, Done, And Termination

Termination checks in [src/orbits_env/simulator.py](src/orbits_env/simulator.py):

- fuel_exhausted
- mission_deviation_limit_exceeded
- collision
- all events resolved or horizon reached

Success at episode end requires both:

1. residual highest collision probability less than or equal to task success_probability_threshold
2. total mission offset less than or equal to task max_total_offset_km

If true, termination reason is safe_completion.

## 8. What Is Evaluated And Tracked For Reporting

Per task reporting returned by run_task in [inference.py](inference.py):

- success
- score
- steps
- total_reward
- reward sequence
- termination_reason
- highest_collision_probability
- total_offset_km
- fuel_remaining
- tracking_updates_used

Iterative per-round summary in [scripts/run_iterative_inference.py](scripts/run_iterative_inference.py):

- avg_score
- avg_total_reward
- success_rate
- full task-level results

Success rate formula:

success_rate = successful_tasks / total_tasks_in_round

With 3 tasks per round, 1.00 means 3 out of 3 successful tasks.

## 9. Final Grading Formula

Final score is separate from step reward and computed in [src/orbits_env/graders/scoring.py](src/orbits_env/graders/scoring.py):

- safety term from highest and total collision probability
- fuel efficiency term
- mission preservation term
- tracking efficiency term
- completion term

Weighted combination is clamped to 0..1 and rounded.

## 10. How Datasets Are Used Today

Priors builder input files:

- [assignment/eda/input_data/processed/satcat_clean.csv](assignment/eda/input_data/processed/satcat_clean.csv)
- [assignment/eda/input_data/processed/ucs_clean.csv](assignment/eda/input_data/processed/ucs_clean.csv)
- [assignment/eda/input_data/processed/kelvins_labels_clean.csv](assignment/eda/input_data/processed/kelvins_labels_clean.csv)

Builder script:

- [scripts/build_task_priors.py](scripts/build_task_priors.py)

Generated priors file:

- [src/orbits_env/tasks/task_priors.json](src/orbits_env/tasks/task_priors.json)

Catalog consumes priors here:

- [src/orbits_env/tasks/catalog.py](src/orbits_env/tasks/catalog.py)

Current overrides applied from priors:

- initial_tracking_quality
- success_probability_threshold
- conjunction uncertainty
- conjunction risk_growth_rate
- conjunction tracking_sensitivity

## 11. Why Kelvins Labels Are Used But Not Full Trajectories Yet

You are correct that current priors integration uses labels file and not the long trajectory files.

Used now:

- [assignment/eda/input_data/processed/kelvins_labels_clean.csv](assignment/eda/input_data/processed/kelvins_labels_clean.csv)

Not yet used in priors computation:

- [assignment/eda/input_data/processed/kelvins_deb_train_long.csv](assignment/eda/input_data/processed/kelvins_deb_train_long.csv)
- [assignment/eda/input_data/processed/kelvins_deb_test_long.csv](assignment/eda/input_data/processed/kelvins_deb_test_long.csv)
- [assignment/eda/input_data/processed/kelvins_sat_long.csv](assignment/eda/input_data/processed/kelvins_sat_long.csv)

Reason:

1. labels give compact stable statistics for first integration pass.
2. trajectory tables are high-volume sequence data requiring dedicated feature engineering.
3. labels-first kept implementation deterministic and low-risk while still making tasks data-informed.

Planned extension:

- add trajectory-derived volatility and temporal dispersion features into priors generation in [scripts/build_task_priors.py](scripts/build_task_priors.py).

## 12. LLM Mode And Fallback

Current default behavior in [inference.py](inference.py):

- strict LLM mode
- if credentials are missing, run fails with explicit error
- fallback heuristic is only enabled when ALLOW_HEURISTIC_FALLBACK is explicitly set

Supported key variable names for provider switching:

- HF_TOKEN
- OPENAI_API_KEY
- GROQ_API_KEY
- API_KEY

Provider/model preflight behavior:

- if model list API is available, code validates that MODEL_NAME exists before running.
- if not available from provider, run continues and first generation call becomes the source of truth.

Environment precedence behavior:

- values already exported in shell override values in .env.
- .env is loaded with setdefault behavior for safety in deployed environments.

Rate-limit controls already implemented:

- requests per minute pacing
- hard per-request gap
- retry/backoff for rate-limit errors
- response token cap

## 13. Execution Sequence To Reproduce Current Pipeline

1. Build priors from EDA processed data:

make build-priors

2. Run iterative inference:

make iterative-inference ITERATIVE_ROUNDS=3

3. Review outputs:

- [iterative_inference_results.json](iterative_inference_results.json)
- [output.txt](output.txt)

## 14. End-To-End Data Flow (Exactly What Is Passed Forward)

1. Task config loaded from catalog (+ optional priors override).
2. Reset creates EnvironmentState with conjunction list and resource budgets.
3. Observation is derived from true events using tracking-quality-dependent conservatism.
4. Inference layer sends observation/history/strategy memory to model.
5. Model returns strict JSON action.
6. Simulator validates and applies action, updates dynamics, computes reward, checks done/success.
7. Episode-level metrics are graded into score and reported.
8. Iterative runner aggregates round metrics and builds next-round strategy memory.
