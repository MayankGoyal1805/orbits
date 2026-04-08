# EDA Section 04: Kelvins Preparation

## Goal
Standardize Kelvins metadata and flatten trajectory files into tabular CSV artifacts.

## Inputs
- `input_data/raw/space-debris-the-origin/labels.dat`
- `input_data/raw/space-debris-the-origin/deb_train/*.dat`
- `input_data/raw/space-debris-the-origin/deb_test/*.dat`
- `input_data/raw/space-debris-the-origin/sat/*.dat`

## Processing Steps
- Copy label table and assign consistent column names.
- Read each trajectory folder file-by-file using whitespace parsing.
- Add trajectory metadata columns:
  - `trajectory_file`
  - `trajectory_id`
- Concatenate per-folder records into long-form tables.

## Outputs
- `input_data/processed/kelvins_labels_clean.csv`
- `input_data/processed/kelvins_deb_train_long.csv`
- `input_data/processed/kelvins_deb_test_long.csv`
- `input_data/processed/kelvins_sat_long.csv`

## Notes
- Long-form trajectory tables are easier to aggregate by track length, cadence, and split-level statistics.
