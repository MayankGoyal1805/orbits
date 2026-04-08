# Data Inventory and Column Reference

## Datasets in Scope

1. SATCAT (CelesTrak)
- File: `input_data/raw/satcat.csv`
- Purpose: catalog-level object metadata and orbital summary fields.

2. UCS Satellite Database
- File: `input_data/raw/satellites.csv`
- Purpose: operational satellite metadata (owner, purpose, mass/power, orbit class).
- Note: raw export contains delimiter/format inconsistencies; columns below describe the canonical intended fields.

3. ESA Kelvins "Space Debris: the origin"
- Files:
  - `input_data/raw/space-debris-the-origin/labels_train.dat`
  - `input_data/raw/space-debris-the-origin/deb_train/*.dat`
  - `input_data/raw/space-debris-the-origin/deb_test/*.dat`
  - `input_data/raw/space-debris-the-origin/sat/*.dat`
- Purpose: labeled debris-origin learning dataset with orbital elements.

---

## 1) SATCAT Column Dictionary

- `OBJECT_NAME`: Human-readable object name.
- `OBJECT_ID`: International designator (COSPAR-style launch/object id).
- `NORAD_CAT_ID`: NORAD catalog number (unique object identifier in public catalogs).
- `OBJECT_TYPE`: Object class (e.g., payload, rocket body, debris).
- `OPS_STATUS_CODE`: Operational status code.
- `OWNER`: Owning/launching country or organization code.
- `LAUNCH_DATE`: Launch date.
- `LAUNCH_SITE`: Launch site code.
- `DECAY_DATE`: Date object decayed/re-entered (if applicable).
- `PERIOD`: Orbital period (minutes).
- `INCLINATION`: Orbital inclination (degrees).
- `APOGEE`: Apogee altitude (km).
- `PERIGEE`: Perigee altitude (km).
- `RCS`: Radar cross section (size proxy used in tracking context).
- `DATA_STATUS_CODE`: Data quality/status indicator.
- `ORBIT_CENTER`: Orbit center body code (typically Earth).
- `ORBIT_TYPE`: Orbit type code.

---

## 2) UCS Satellite Database Column Dictionary (Canonical Fields)

- `Name of Satellite`: Common satellite name.
- `Alternate Names`: Other known names.
- `Current Official Name of Satellite`: Current official designation.
- `Country/Org of UN Registry`: UN registration country/org.
- `Country of Operator/Owner`: Operator/owner country.
- `Operator/Owner`: Operating entity.
- `Users`: User category (civil, commercial, military, etc.).
- `Purpose`: Primary mission category.
- `Detailed Purpose`: More specific mission description.
- `Class of Orbit`: Broad orbit class (LEO, MEO, GEO, HEO).
- `Type of Orbit`: Subtype (e.g., sun-synchronous, non-polar inclined).
- `Longitude of GEO (degrees)`: Nominal GEO longitude (if applicable).
- `Perigee (km)`: Perigee altitude (km).
- `Apogee (km)`: Apogee altitude (km).
- `Eccentricity`: Orbital eccentricity.
- `Inclination (degrees)`: Orbital inclination.
- `Period (minutes)`: Orbital period.
- `Launch Mass (kg.)`: Total launch mass.
- `Dry Mass (kg.)`: Dry mass.
- `Power (watts)`: Nominal onboard power.
- `Date of Launch`: Launch date.
- `Expected Lifetime (yrs.)`: Planned lifetime in years.
- `Contractor`: Prime builder/manufacturer.
- `Country of Contractor`: Contractor country.
- `Launch Site`: Launch site.
- `Launch Vehicle`: Launcher name.
- `COSPAR Number`: International designator.
- `NORAD Number`: NORAD catalog id.
- `Comments`: Free-text notes.
- `Source Used for Orbital Data`: Source note for orbit fields.
- `Source` (repeated): Citation/source links in raw export.

Notes on UCS raw file:
- The delivered export may include repeated `Source` fields and many empty trailing columns.
- Numeric values may use decimal commas (e.g., `36,9`) and require normalization.

---

## 3) Kelvins Labels and Orbital Elements Dictionary

### `labels_train.dat` (9 columns)
- `col_0_originator_id`: Originator satellite id/class label.
- `col_1_area_to_mass_ratio`: Area-to-mass ratio target.
- `col_2`: Numeric feature from challenge state vector (epoch/derived term).
- `col_3`: Numeric feature from challenge state vector.
- `col_4`: Semimajor axis (km).
- `col_5`: Eccentricity.
- `col_6`: Inclination (deg).
- `col_7`: Mean anomaly (deg).
- `col_8`: Argument/RAAN-related angular element (deg, per challenge convention).

### Debris/Satellite trajectory files (`*.dat`)
Per challenge description, records use orbital elements in this order:
- Epoch (JD2000)
- Semimajor axis (km)
- Eccentricity
- Inclination (deg)
- Mean anomaly (deg)
- Argument of perigee (deg)
- RAAN (deg)

Note:
- Exact column naming for each `.dat` file will be enforced during parsing in processing scripts/notebook cells.

---

## Intended Usage in This Project

- SATCAT: primary catalog backbone for global object composition and trends.
- UCS: active-satellite operational context for mission/orbit/owner breakdowns.
- Kelvins: labeled orbital-element dataset for debris-origin and feature-behavior analysis.
