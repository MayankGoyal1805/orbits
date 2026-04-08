# EDA Section 08: Kelvins Analysis

## Goal
Assess feature distributions and trajectory volume characteristics in Kelvins processed data.

## Analyses
- Numeric summary statistics of cleaned label features.
- Histograms for selected features:
  - `area_to_mass_ratio`
  - `semi_major_axis_km`
  - `eccentricity`
  - `inclination_deg`
- Trajectory subset summary:
  - Total rows
  - Number of unique trajectories
  - Average points per trajectory

## Practical Outcome
- Confirms the label table is numerically usable.
- Shows split-level trajectory density differences (short debris sequences vs long sat tracks).
- Identifies which features are immediately usable for baseline classifiers or reward shaping heuristics.
