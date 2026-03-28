# Deduplication Strategy

`UTSP-18`

This document defines how the dataset curation stage removes exact duplicates
and near-duplicates.

## Goal

Training and benchmark quality should not be inflated by repeated or nearly
identical examples.

## Current CLI

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli dedupe-dataset \
  --manifest data/curated/dataset_manifest.normalized.json \
  --output data/curated/dataset_manifest.deduped.json
```

## Exact Duplicates

The pipeline computes a stable SHA-256 signature over normalized source and test
code. If a later example has the same signature, it is rejected as a duplicate.

## Near-Duplicate Strategy

The current near-duplicate pass computes a similarity ratio across the combined
normalized source and test payload. Examples above the configured threshold are
rejected as near-duplicates.

This strategy is intentionally conservative and traceable. It is not trying to
solve semantic equivalence yet.

## Traceability

Rejected items are preserved with:

- `example_id`
- rejection reason
- matched retained example
- similarity score

## Acceptance Mapping

This ticket is done when:

- duplicate detection exists
- the near-duplicate strategy is documented
- filtered examples remain traceable
