# EDA Section 02 - UCS Data Preparation

## Objective
Prepare the UCS satellite dataset for consistent analysis.

## Why preparation is required
The raw UCS export includes:
- multiple placeholder columns (`Unnamed:*`)
- mixed numeric formats (e.g., decimal commas)
- a combined first field (`Name of Satellite, Alternate Names`)

These issues can produce incorrect summaries if not standardized first.

## Transformations applied
1. Header cleanup
- Trimmed whitespace from all column names.

2. Placeholder column removal
- Dropped columns that start with `Unnamed:`.

3. Name field normalization
- Split `Name of Satellite, Alternate Names` into:
  - `Name of Satellite`
  - `Alternate Names (raw)`

4. Numeric coercion (selected fields)
- Standardized decimal commas to decimal points.
- Converted to numeric with invalid entries set to missing.
- Fields:
  - `Perigee (km)`
  - `Apogee (km)`
  - `Eccentricity`
  - `Inclination (degrees)`
  - `Period (minutes)`
  - `Launch Mass (kg.)`
  - `Dry Mass (kg.)`
  - `Power (watts)`

5. Date parsing
- Parsed `Date of Launch` into datetime.

## Result snapshot
- Original shape: `(7561, 68)`
- Cleaned shape: `(7561, 38)`
- Removed placeholder columns: `32`

## Interpretation note for report
Large missingness remains in some columns (e.g., power, dry mass, repeated source fields). This is expected in public satellite registries and should be explicitly reported in the data quality section before model/environment assumptions are made.
