# EDA Chunk 01 - Setup and Dataset Inventory

## Objective
In this chunk, we validate that all core files exist and can be loaded into pandas.

## Datasets covered
1. SATCAT (`input_data/raw/satcat.csv`)
2. UCS satellites (`input_data/raw/satellites.csv`)
3. Kelvins labels (`input_data/raw/space-debris-the-origin/labels_train.dat`)

## What we do
1. Define consistent project paths.
2. Run existence checks for each required dataset path.
3. Load SATCAT and inspect shape/columns/sample rows.
4. Load UCS using semicolon separator and inspect shape/columns/sample rows.
5. Load Kelvins labels as whitespace-delimited and inspect shape/sample rows.

## Why this chunk is important
- Prevents silent path mistakes.
- Confirms parser assumptions before deep analysis.
- Establishes repeatable structure for later chunks.

## Notes
- UCS is loaded with `sep=';'` for now. We will clean and standardize its fields in Chunk 02.
- Kelvins labels have no header; we will assign explicit column names in Chunk 02.
