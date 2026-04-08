# EDA Section 05: Data Quality Summary

## Goal
Produce a compact, cross-dataset quality snapshot for cleaned SATCAT, cleaned UCS, and cleaned Kelvins labels.

## Metrics
- Row count
- Column count
- Duplicate row count
- Total missing cells
- Missing percentage

## Additional Checks
- Top missing columns per dataset (head of missing-value rankings).

## Why It Matters
- Confirms basic integrity before modeling.
- Highlights fields requiring imputation, exclusion, or robust handling.
- Establishes a reproducible baseline quality report for subsequent iterations.
