# EDA Section 03: SATCAT Preparation

## Goal
Create a cleaned SATCAT table with usable date and numeric columns for downstream analysis.

## Inputs
- `input_data/raw/satcat.csv`

## Processing Steps
- Parse date fields:
  - `LAUNCH_DATE`
  - `DECAY_DATE`
- Convert orbital numeric fields to numeric dtypes where possible:
  - `PERIOD`, `INCLINATION`, `APOGEE`, `PERIGEE`, `RCS`
- Preserve all rows and columns unless conversion fails for specific cells.

## Output
- `input_data/processed/satcat_clean.csv`

## Notes
- This stage intentionally avoids aggressive filtering so later analyses can decide dataset-specific cutoffs.
- Coercion to numeric/date introduces missing values for malformed entries; these are expected and tracked in the data quality section.
