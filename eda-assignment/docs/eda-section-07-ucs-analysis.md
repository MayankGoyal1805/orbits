# EDA Section 07: UCS Analysis

## Goal
Profile active satellite context from UCS data, including mission purpose, orbit class, and launch cadence.

## Analyses
- Purpose distribution (top categories).
- Orbit class distribution after light normalization:
  - Upper-case normalization
  - Mapping known classes (`LEO`, `MEO`, `GEO`, `ELLIPTICAL`)
  - Grouping anomalies into `OTHER/UNKNOWN`
- Launch counts by year with practical range filtering (`1957` to `2035`).

## Key Observations
- Communications dominates active mission purpose counts.
- LEO is the primary operational orbit class by a large margin.
- Recent years show sharp launch growth, consistent with mega-constellation expansion.

## Relevance to OpenEnv
- Provides realistic traffic priors and orbit-regime composition for collision-avoidance simulations.
