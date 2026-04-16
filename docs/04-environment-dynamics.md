# Environment Dynamics

This is the core of the benchmark behavior.

## State And Observation

Hidden simulator state (`EnvironmentState`) tracks:

- fuel, tracking quality, tracking budget
- mission offsets by axis
- true conjunction events
- cumulative reward and counters

Observation (`EnvironmentObservation`) is what the agent sees:

- top-risk events (limited by `visible_event_limit`)
- aggregate risk summaries
- resource levels
- last action metadata

Observed event values are intentionally conservative when tracking quality is low:

- observed collision probability is inflated
- observed miss distance is reduced
- observed uncertainty is increased

This models imperfect situational awareness.

## Actions

Action types:

- `noop`
- `request_tracking_update`
- `radial_maneuver`
- `along_track_maneuver`
- `normal_maneuver`

`magnitude` is clamped to task `max_magnitude`.

## Step Transition Breakdown

Within one `step(action)`:

1. Validate state and done flag.
2. Record pre-action total probability and uncertainty.
3. Apply action effects:
   - tracking update: consumes budget/fuel, improves tracking quality, reduces uncertainty.
   - maneuver: consumes fuel, changes offsets, reduces risk based on geometry effectiveness and timing.
   - noop: can incur waste penalty under high risk.
4. Advance passive dynamics:
   - tracking quality decays.
   - mission offsets recover partially.
   - conjunction time-to-closest-approach decreases.
   - risk can grow with urgency/uncertainty/miss-distance pressure.
5. Increment `step_index` and evaluate termination.
6. Compute shaped reward components and final step reward.
7. Emit new observation and info dictionary.

## Reward Components

Reward starts from a base and adjusts with bonuses/penalties:

- positive: risk reduction, tracking gain, completion bonus
- negative: fuel penalty, mission offset penalty, waste penalty

If collision occurs, reward is forced to `0.0`.

Important: this shaped reward is for learning signal; final benchmark score comes from `grade_episode`.

## Termination Conditions

Episode ends on any of:

- fuel exhausted
- mission deviation too high
- imminent collision at threshold when event reaches closest approach
- horizon reached or all events reached closest approach

On normal completion, success requires:

- residual highest probability under task threshold
- mission offset within allowed maximum
