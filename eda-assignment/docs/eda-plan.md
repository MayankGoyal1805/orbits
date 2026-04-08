# EDA Start Plan (Option 4: Space Debris Collision Avoidance)

## Current Dataset Status
- SATCAT: present (`satcat.csv`), ~68k rows, 17 clear columns.
- UCS satellites: present (`satellites.csv`), ~7.5k rows, but export/header formatting is inconsistent and needs cleaning.
- Kelvins debris-origin: present (`space-debris-the-origin/`), train labels + orbital element files.

## Phase 1 - Dataset Audit (Do This First)

### 1) SATCAT audit
- Verify data types for:
  - `NORAD_CAT_ID`
  - `LAUNCH_DATE`, `DECAY_DATE`
  - `PERIOD`, `INCLINATION`, `APOGEE`, `PERIGEE`, `RCS`
- Check missing-value rates by column.
- Count objects by:
  - `OBJECT_TYPE`
  - `OPS_STATUS_CODE`
  - `OWNER`

### 2) UCS cleanup + audit
- Detect true delimiter/encoding and normalize to a clean table.
- Keep key fields (at minimum):
  - satellite name
  - NORAD/COSPAR
  - purpose/users/operator
  - orbit class/type
  - perigee/apogee/inclination
  - launch date
- Standardize decimal commas to decimal points in numeric fields.
- Validate row count and uniqueness by NORAD where available.

### 3) Kelvins audit
- Parse `labels_train.dat` columns as:
  - originator satellite id
  - area-to-mass ratio
  - epoch and orbital elements fields
- Count train/test debris trajectories.
- Summarize per-originator class frequency (class imbalance check).

## Phase 2 - EDA Outputs You Should Produce

### Required tables
1. Dataset inventory table:
- source
- local file path
- row count
- key columns
- known issues

2. Data quality table:
- missingness per column
- duplicated IDs
- parse failures

### Required plots
1. SATCAT object type distribution.
2. SATCAT launches by year.
3. SATCAT decays by year.
4. SATCAT apogee vs perigee scatter (sampled if needed).
5. UCS active satellites by purpose.
6. UCS active satellites by orbit class.
7. UCS launch trend over time.
8. Kelvins originator label frequency.
9. Kelvins inclination distribution.
10. Kelvins eccentricity distribution.

## Phase 3 - Integration Readiness (for OpenEnv)

### Build these reusable outputs
1. `data/processed/satcat_clean.csv`
2. `data/processed/ucs_clean.csv`
3. `data/processed/kelvins_train_flat.csv`
4. `data/processed/kelvins_test_flat.csv`

### Why this matters
These processed files become direct inputs for:
- scenario design decisions
- state feature selection
- later orbit/risk simulation modules

## Immediate Next Step
Start with UCS cleanup first, because it is currently the highest-risk file for downstream joins and analysis consistency.
