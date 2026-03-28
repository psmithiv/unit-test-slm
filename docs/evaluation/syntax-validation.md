# Syntax Validation

`UTSP-26`

This document defines the fast syntax and parse validation stage used before
deeper evaluation.

## Goal

Obviously invalid outputs should fail fast before compile, execution, or
robustness checks run.

## Current CLI

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli evaluate-syntax \
  --results data/results/direct.json \
  --output data/evaluation/direct.syntax.json
```

## Current Behavior

- direct Jest outputs are checked for balanced delimiters and basic test
  structure
- `TEST_SPEC` outputs are parsed as JSON and validated against the schema
- parse pass count and parse pass rate are reported per run

## Acceptance Mapping

This ticket is done when:

- invalid output can be detected automatically
- parse metrics are reported
