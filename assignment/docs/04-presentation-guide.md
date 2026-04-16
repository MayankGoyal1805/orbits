# Presentation Guide

Use this as a concise speaking plan for your assignment presentation.

## 1) Opening (30-45 sec)

"I executed the EDA pipeline end-to-end across SATCAT, UCS, and ESA Kelvins data. The objective was to produce cleaned, reproducible artifacts and extract modeling-relevant insights for a collision-avoidance simulation environment."

## 2) Data Sources (45 sec)

- SATCAT: global object catalog with object types and orbital metadata.
- UCS: operational satellite context (purpose, owner, orbit class, mass/power).
- Kelvins: labeled orbital/trajectory dataset for debris/satellite dynamics.

## 3) Data Engineering Pipeline (60-90 sec)

Explain your notebook stages:

1. Path checks and schema inspection.
2. UCS cleaning (delimiter handling, unnamed-column removal, numeric/date parsing).
3. SATCAT cleaning (date + numeric standardization).
4. Kelvins parsing into analysis-ready long tables.
5. Data quality summary and missingness profiling.
6. Domain analyses (composition, launch trends, orbit class, feature distributions).

## 4) Key Findings (60 sec)

Use concrete findings from your outputs:

- Debris objects are highly prevalent in SATCAT.
- LEO dominates UCS orbit class distribution.
- Launch activity rises sharply in recent years.
- Some UCS engineering fields have high missingness.
- Kelvins trajectories provide usable temporal structure.

## 5) Why This Matters For Simulation (60 sec)

- supports realistic threat-density assumptions
- supports LEO-focused scenario design
- informs uncertainty and risk-growth calibration
- motivates excluding highly sparse fields from core logic

## 6) Address The Common Question (45 sec)

Q: "Did you actually use these datasets in the project environment?"

A:

- Current environment is synthetic for reproducibility.
- EDA is used to justify and calibrate design parameters.
- Next step is offline prior generation from cleaned artifacts to inject real-data statistics into task configuration.

## 7) Demo Checklist

Before presentation:

1. Run notebook top-to-bottom once.
2. Ensure processed files exist under `assignment/eda/input_data/processed`.
3. Keep 3-4 key charts ready:
   - SATCAT object type distribution
   - SATCAT launch trend
   - UCS purpose distribution
   - UCS orbit class distribution
4. Keep one quality table screenshot ready.

## 8) Risk/Limitations Slide

Mention clearly:

- some fields are sparse/noisy (especially UCS source/power/mass subfields)
- challenge-label semantics for some Kelvins columns need source-doc confirmation
- current environment still uses synthetic event generation

This improves credibility.

## 9) Closing (20 sec)

"The EDA pipeline is reproducible, cleaned outputs are generated, and insights are directly usable for benchmark calibration. The next iteration will formalize data-driven task priors while preserving reproducible runtime behavior."
