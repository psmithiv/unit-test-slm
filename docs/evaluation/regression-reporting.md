# Regression Reporting

`UTSP-30`

This document defines the standard benchmark report format and the baseline
versus candidate comparison flow.

## Goal

Improvements and regressions should be visible immediately across benchmark
runs.

## Current CLI

Build a standard report:

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli build-report \
  --run-label baseline \
  --syntax data/evaluation/direct.syntax.json \
  --compile data/evaluation/direct.compile.json \
  --jest data/evaluation/direct.jest.json \
  --robustness data/evaluation/direct.robustness.json \
  --output data/evaluation/direct.report.json
```

Compare two reports:

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli compare-reports \
  --baseline data/evaluation/baseline.report.json \
  --candidate data/evaluation/tuned.report.json \
  --output data/evaluation/baseline_vs_tuned.json
```

## Acceptance Mapping

This ticket is done when:

- a standard report format exists
- baseline versus tuned comparisons are captured
