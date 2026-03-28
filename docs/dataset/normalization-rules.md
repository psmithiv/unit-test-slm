# Normalization Rules

`UTSP-17`

This document defines the deterministic normalization pass for curated
`TypeScript -> Jest` examples.

## Goal

The model should see one consistent formatting and naming style regardless of
the conventions used by the original repository.

## Current CLI

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli normalize-dataset \
  --manifest data/curated/dataset_manifest.json \
  --output data/curated/dataset_manifest.normalized.json
```

## Current Rules

Common source and test normalization:

- normalize line endings to `LF`
- replace tabs with two spaces
- strip trailing whitespace
- collapse runs of more than two blank lines
- enforce a trailing newline

Jest-specific normalization:

- rename `test(...)` blocks to `it(...)`
- normalize `describe(...)` and `it(...)` string labels to single quotes when
  the label is a simple string literal

## Determinism

The pipeline records normalization metadata on each example so downstream
training and evaluation can verify which rules were applied.

## Acceptance Mapping

This ticket is done when:

- formatting and naming normalization rules are documented
- the pipeline can normalize examples deterministically
