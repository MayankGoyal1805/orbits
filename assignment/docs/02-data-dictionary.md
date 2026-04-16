# Data Dictionary (Detailed)

This guide explains the fields used in your EDA sources.

Important note:

- Some providers use source-specific conventions and codebooks.
- Field meanings below are practical analysis interpretations suitable for EDA and presentation.

## A) SATCAT (`satcat.csv`)

Columns observed:

1. `OBJECT_NAME`: object name in catalog.
2. `OBJECT_ID`: international designator style identifier (launch year + piece).
3. `NORAD_CAT_ID`: NORAD catalog integer ID.
4. `OBJECT_TYPE`: object class, commonly:
   - `PAY` (payload)
   - `DEB` (debris)
   - `R/B` (rocket body)
   - `UNK` (unknown)
5. `OPS_STATUS_CODE`: operational status code (provider-specific coded category).
6. `OWNER`: owning state/entity label.
7. `LAUNCH_DATE`: launch date.
8. `LAUNCH_SITE`: launch location code/name.
9. `DECAY_DATE`: reentry/decay date when known.
10. `PERIOD`: orbital period (minutes).
11. `INCLINATION`: orbital inclination (degrees).
12. `APOGEE`: apogee altitude (km).
13. `PERIGEE`: perigee altitude (km).
14. `RCS`: radar cross section proxy (size/detectability related).
15. `DATA_STATUS_CODE`: data quality/completeness code (provider-specific).
16. `ORBIT_CENTER`: orbit center body (usually Earth).
17. `ORBIT_TYPE`: orbit regime/type code.

How these fields support modeling:

- Risk context: `OBJECT_TYPE`, `RCS`, `OPS_STATUS_CODE`
- Orbital geometry: `INCLINATION`, `APOGEE`, `PERIGEE`, `PERIOD`
- Temporal dynamics: `LAUNCH_DATE`, `DECAY_DATE`

## B) UCS (`satellites.csv`)

### Raw columns (as loaded)

Key analytical columns:

1. `Name of Satellite, Alternate Names`
2. `Current Official Name of Satellite`
3. `Country/Org of UN Registry`
4. `Country of Operator/Owner`
5. `Operator/Owner`
6. `Users`
7. `Purpose`
8. `Detailed Purpose`
9. `Class of Orbit`
10. `Type of Orbit`
11. `Longitude of GEO (degrees)`
12. `Perigee (km)`
13. `Apogee (km)`
14. `Eccentricity`
15. `Inclination (degrees)`
16. `Period (minutes)`
17. `Launch Mass (kg.)`
18. `Dry Mass (kg.)`
19. `Power (watts)`
20. `Date of Launch`
21. `Expected Lifetime (yrs.)`
22. `Contractor`
23. `Country of Contractor`
24. `Launch Site`
25. `Launch Vehicle`
26. `COSPAR Number`
27. `NORAD Number`
28. `Comments`
29. `Source Used for Orbital Data`
30. `Source`
31. `Source.1`
32. `Source.2`
33. `Source.3`
34. `Source.4`
35. `Source.5`
36. `Source.6`

Low-information placeholder columns from parsing artifact:

- `Unnamed: 28`
- `Unnamed: 37` through `Unnamed: 67`

### Cleaned UCS columns (in `ucs_clean.csv`)

After cleaning, placeholders are removed and split fields are added:

- Added `Name of Satellite`
- Added `Alternate Names (raw)`
- Numeric columns cast to numeric where possible
- `Date of Launch` parsed to datetime

Field meaning highlights for presentation:

- Mission profile: `Purpose`, `Detailed Purpose`, `Users`
- Operational context: operator/owner + country fields
- Orbital profile: orbit class/type + geometry (`Perigee/Apogee/Eccentricity/Inclination/Period`)
- Engineering profile: mass and power fields
- Traceability: `Source*`, `Comments`

## C) Kelvins Labels (`labels_train.dat`)

Renamed columns in notebook:

1. `originator_id`: source object/satellite identifier for generated sample.
2. `area_to_mass_ratio`: area-to-mass ratio (important for perturbation behavior).
3. `feature_2`: unlabeled feature from challenge file (kept as raw feature).
4. `feature_3`: unlabeled feature from challenge file (kept as raw feature).
5. `semi_major_axis_km`: semi-major axis related value (units per challenge context).
6. `eccentricity`: orbit eccentricity.
7. `inclination_deg`: inclination (degrees).
8. `mean_anomaly_deg`: mean anomaly angle (degrees).
9. `raan_or_arg_deg`: RAAN or argument-like angular feature per challenge format.

Important caveat:

- For `feature_2`, `feature_3`, and `raan_or_arg_deg`, final semantic labeling should be confirmed from challenge documentation before physics-sensitive interpretation.

## D) Kelvins Trajectory Long Tables

Generated files:

- `kelvins_deb_train_long.csv`
- `kelvins_deb_test_long.csv`
- `kelvins_sat_long.csv`

Common structure:

- unnamed numeric columns from original `.dat` trajectory rows
- `trajectory_file`: original source filename
- `trajectory_id`: filename stem used as trajectory key

These long tables are useful for:

- temporal trajectory statistics
- sequence feature engineering
- generating synthetic conjunction profiles

## E) Missingness Context (Observed)

From your current run:

- SATCAT has moderate missingness concentrated in status/decay/RCS fields.
- UCS has substantial missingness in power, dry mass, detailed purpose, and many source metadata columns.
- Kelvins labels are complete in current subset.

Presentation tip:

- Emphasize that high missingness does not invalidate EDA; it guides which fields are trustworthy for downstream simulation calibration.
