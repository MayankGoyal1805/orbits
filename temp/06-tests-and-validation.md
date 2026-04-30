# Tests And Validation

This repository validates behavior at multiple levels.

## Unit And Integration Tests

`tests/test_env.py` checks environment mechanics:

- reset returns expected first observation
- step advances state correctly
- full rollout reaches valid termination

`tests/test_api.py` checks API handler cycle:

- health
- reset/step/state/grade/close paths
- task detail lookup

`tests/test_inference.py` checks inference output contract:

- script runs successfully
- output lines include only `[START]`, `[STEP]`, `[END]`

Run all tests:

```bash
make test
```

## Smoke Script

`scripts/smoke_test_api.py` directly imports and calls API handlers as a quick sanity check.

This is lighter than full external HTTP validation.

## Submission Validation Script

`scripts/validate-submission.sh` performs:

1. health endpoint ping
2. Docker image build
3. test run
4. baseline and inference fallback run

This approximates a practical CI gate for packaging and runtime compatibility.
