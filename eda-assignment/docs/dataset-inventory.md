# Dataset Inventory (Current)

Detailed column-by-column definitions are documented in `docs/data-inventory.md`.

## 1) SATCAT (CelesTrak)
- Path: `satcat.csv`
- Rows: 68,330 data rows (+ header)
- Columns: 17
- Core fields:
  - `NORAD_CAT_ID`
  - `OBJECT_TYPE`
  - `OWNER`
  - `LAUNCH_DATE`, `DECAY_DATE`
  - `PERIOD`, `INCLINATION`, `APOGEE`, `PERIGEE`
- Status: ready for EDA.

## 2) UCS Satellite Database
- Path: `satellites.csv`
- Rows: 7,561 data rows (+ header)
- Issue: appears exported with mixed separators in the header/content and needs normalization before analysis.
- Intended fields (after cleanup):
  - satellite name / aliases
  - NORAD/COSPAR
  - purpose/users/operator
  - orbit class/type
  - perigee/apogee/inclination
  - launch date
- Status: requires cleanup first.

## 3) ESA Kelvins "Space Debris: the origin"
- Path: `space-debris-the-origin/`
- Main files:
  - `labels_train.dat` (100 labeled training trajectories)
  - `deb_train/*.dat` (debris train trajectories)
  - `deb_test/*.dat` (debris test trajectories)
  - `sat/*.dat` (candidate originator satellite trajectories)
- Status: ready for parsing and EDA.

## Notes
- This is enough to begin EDA immediately.
- Additional CelesTrak GP/TLE and conjunction feeds can be added later for simulation-focused environment work.
