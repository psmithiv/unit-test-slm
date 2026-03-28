# Dataset Manifest Schema

`UTSP-16`

This document defines the first stable curated dataset manifest for the
`TypeScript -> Jest` pipeline.

## Goal

Every curated example should be reproducible and traceable after acquisition,
even after later normalization, deduplication, and split assignment stages.

## Current CLI

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli build-dataset-manifest \
  --raw-manifest data/raw/source_test_pairs.json \
  --output data/curated/dataset_manifest.json
```

## Schema

Top-level fields:

- `schema_version`
- `generated_at`
- `example_count`
- `examples`

Each example currently includes:

- `example_id`
- `split`
- `repository.name`
- `repository.url`
- `repository.revision`
- `repository.license_spdx_id`
- `source.path`
- `source.language`
- `source.code`
- `test.path`
- `test.framework`
- `test.code`
- `provenance`

## Notes

- `split` is initialized to `unassigned` and will be frozen later in the
  benchmark split ticket.
- source and test code are copied into the manifest so later stages can run
  without reopening the original repository checkout.
- when the raw manifest includes multiple candidate tests for one source file,
  the current dataset manifest keeps the highest-ranked test path and preserves
  the full candidate list in provenance.

## Acceptance Mapping

This ticket is done when:

- the schema includes source path, test path, repository metadata, and split
  assignment
- the schema is documented in the repo
