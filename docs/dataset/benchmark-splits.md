# Benchmark Splits

`UTSP-21`

This document defines how curated examples are assigned to train, validation,
and held-out benchmark splits.

## Goal

Model comparisons should use the same held-out benchmark set every time unless
the split version intentionally changes.

## Current CLI

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli freeze-splits \
  --manifest data/curated/dataset_manifest.deduped.json \
  --split-version v1 \
  --output data/curated/dataset_manifest.splits.json
```

## Split Strategy

The current implementation hashes `split_version` with `example_id` and assigns:

- `train` for the first 80 buckets
- `validation` for the next 10 buckets
- `held_out` for the last 10 buckets

## Versioning

The manifest records:

- `split_version`
- `split_counts`
- `benchmark.version`
- `benchmark.held_out_example_ids`

Changing the split version intentionally reshuffles the assignment while keeping
the process reproducible for that version.

## Acceptance Mapping

This ticket is done when:

- train, validation, and held-out splits exist
- the benchmark set is versioned
- split generation is reproducible
