# Robustness Evaluation

`UTSP-29`

This document defines the stronger quality signal used beyond syntax, compile,
and execution success.

## Goal

Weak tests should not be mistaken for strong tests just because they parse and
execute.

## Current Choice

The current implementation uses an equivalent robustness signal rather than full
mutation testing.

Rationale:

- it stays lightweight enough for the current local pipeline
- it still rewards assertion density and matcher strength
- it penalizes snapshot-only outputs

## Current CLI

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli evaluate-robustness \
  --results data/results/direct.json \
  --output data/evaluation/direct.robustness.json
```

## Acceptance Mapping

This ticket is done when:

- a mutation-testing or equivalent robustness signal is implemented with
  rationale
- the metric is included in benchmark reporting when enabled
