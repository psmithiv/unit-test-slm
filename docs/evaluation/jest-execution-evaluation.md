# Jest Execution Evaluation

`UTSP-28`

This document defines the Jest execution evaluation stage.

## Goal

Generated tests should be measured behaviorally where feasible, not just by
static appearance.

## Current CLI

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli evaluate-jest \
  --results data/results/direct.json \
  --backend mock \
  --output data/evaluation/direct.jest.json
```

The evaluator also supports a `subprocess` backend for a real Jest harness.

## Acceptance Mapping

This ticket is done when:

- benchmark outputs can be run in a Jest harness
- execution pass rate is reported
