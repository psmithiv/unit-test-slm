# Direct Versus TEST_SPEC

`UTSP-25`

This document defines how the pipeline compares direct test generation with the
structured `TEST_SPEC` path.

## Goal

Both paths should be benchmarked side by side when feasible so the project can
pick the more reliable V1 strategy for small models.

## Current CLI

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli compare-training-paths \
  --direct data/results/direct.json \
  --test-spec data/results/test_spec.json \
  --output data/results/direct_vs_test_spec.json
```

## Comparison Shape

The current comparison manifest records:

- side-by-side primary metrics
- the preferred V1 path
- the rationale for that choice

## Current V1 Preference

The current default V1 preference remains `TEST_SPEC`.

Reason:

- ties fall back to the structured path
- the project has already decided that smaller models benefit from a narrower
  prediction target and deterministic rendering

## Acceptance Mapping

This ticket is done when:

- both paths are benchmarked when feasible
- results are documented side by side
- the preferred V1 path is recorded
