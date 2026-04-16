# Notebook Walkthrough

Notebook: `assignment/eda/eda.ipynb`

This walkthrough explains what each section does, why it matters, and how to talk about it in evaluation/presentation.

## 1) Title And Scope

The opening markdown defines the EDA objective:

- understand debris/satellite populations
- clean and standardize heterogeneous sources
- produce evidence useful for collision-avoidance simulation design

This is good framing because it connects data work to modeling intent.

## 2) Data Loading And Inspection

What the code does:

- sets paths using `pathlib.Path`
- verifies required files exist
- loads three source families:
  - SATCAT (`satcat.csv`)
  - UCS (`satellites.csv`, semicolon-delimited)
  - Kelvins labels (`labels_train.dat`, whitespace-delimited)
- prints shape/columns and previews samples

Why this matters:

- catches missing data early
- confirms delimiter assumptions
- gives immediate schema visibility before cleaning

Execution result in your run:

- SATCAT shape: `(68568, 17)`
- UCS shape: `(7560, 68)`
- Kelvins labels shape: `(100, 9)`

## 3) UCS Preparation

What the code does:

- creates working copy `ucs_clean`
- normalizes column names via `.strip()`
- drops `Unnamed:*` placeholder columns from malformed/extra separators
- splits `Name of Satellite, Alternate Names` into:
  - `Name of Satellite`
  - `Alternate Names (raw)`
- standardizes numeric-like columns (comma decimal to dot, cast to numeric)
- parses `Date of Launch` to datetime
- writes output to `assignment/eda/input_data/processed/ucs_clean.csv`

Why this matters:

- UCS exports commonly include formatting noise and mixed numeric encodings
- robust numeric/date parsing is required before any trend analysis

## 4) SATCAT Preparation

What the code does:

- parses `LAUNCH_DATE` and `DECAY_DATE` as datetimes
- casts orbital numeric fields (`PERIOD`, `INCLINATION`, `APOGEE`, `PERIGEE`, `RCS`)
- saves `satcat_clean.csv`

Why this matters:

- ensures orbital and temporal features are numerically analyzable
- supports time-series and composition plots without repeated preprocessing

## 5) Kelvins Preparation

What the code does:

- renames label columns to semantic names where available
- loads trajectories from three folders (`deb_train`, `deb_test`, `sat`)
- stacks trajectories into long tables and adds:
  - `trajectory_file`
  - `trajectory_id`
- saves processed outputs:
  - `kelvins_labels_clean.csv`
  - `kelvins_deb_train_long.csv`
  - `kelvins_deb_test_long.csv`
  - `kelvins_sat_long.csv`

Why this matters:

- converts folder/file organization into analysis-ready tabular form
- creates reusable artifacts for later feature engineering

## 6) Data Quality Summary

What the code does:

- builds compact quality metrics per cleaned dataset:
  - rows
  - columns
  - duplicate rows
  - missing cells and percentage
- prints top missing columns for each source

Why this matters:

- tells you where confidence is high/low
- helps justify why some fields are excluded from model design

Observed highlights:

- `satcat_clean`: notable missingness in `DATA_STATUS_CODE`, `RCS`, `DECAY_DATE`
- `ucs_clean`: very high missingness in many `Source.*`, `Power (watts)`, `Dry Mass (kg.)`
- `kelvins_labels_clean`: no missing values in provided 9 columns

## 7) SATCAT Analysis

What the code does:

- plots object type distribution (`DEB`, `PAY`, `R/B`, `UNK`)
- plots launch count by year

Interpretation from your outputs:

- debris (`DEB`) is the largest category, larger than payloads
- launch/object creation activity increases sharply in recent years

Modeling implication:

- simulated environment should include frequent debris encounters and non-stationary risk pressure over time.

## 8) UCS Analysis

What the code does:

- plots top mission purposes
- normalizes orbit class labels and plots distribution
- plots launch trend

Interpretation from your outputs:

- communications dominates purpose distribution
- LEO dominates orbit class
- post-2020 launch growth is strong

Modeling implication:

- environment scenarios should heavily emphasize LEO operations and communications-like mission constraints.

## 9) Kelvins Analysis

What the code does:

- computes descriptive statistics for numeric labels
- plots distributions for key columns
- summarizes trajectory table sizes and average points per trajectory

Interpretation from your outputs:

- trajectory subsets are successfully parsed
- `sat` trajectories are much denser than debris train/test subsets

Modeling implication:

- dynamic risk generation can use richer temporal behavior from dense trajectory subsets.

## 10) Integrated Findings

What the code does:

- creates concise cross-dataset summary table
- verifies processed artifacts exist

Why this matters:

- confirms reproducible pipeline completion
- provides a project handoff checkpoint

## Validation Status

This notebook was executed successfully end-to-end in the current environment.

Also, two quality cleanups were applied for presentation quality:

- SATCAT launch-year derivation now uses consistent DataFrame assignment flow
- UCS orbit normalization logic simplified and made explicit

No runtime failures were observed in current environment.
