# Discovery Workflow

`UTSP-12`

This document defines the first repository discovery workflow for the
`TypeScript -> Jest` acquisition layer.

## Goal

Find candidate public repositories that are likely to contain high-quality
`TypeScript` implementation files with corresponding `Jest` unit tests.

## Workflow Shape

The discovery workflow is intentionally narrow:

1. load machine-readable criteria from `config/repository_selection_criteria.json`
2. build one or more GitHub repository search queries from those criteria
3. call the GitHub search API
4. normalize the returned metadata into a stable manifest
5. compare later runs by diffing manifest files

## Current CLI

The workflow is exposed through:

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli discover \
  --criteria config/repository_selection_criteria.json \
  --output data/discovery/repositories.json
```

To compare two saved discovery runs:

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli compare-discovery \
  data/discovery/baseline.json \
  data/discovery/candidate.json
```

## Captured Metadata

Each normalized repository candidate captures:

- repository identity and URL
- default branch
- stars and forks
- primary language
- SPDX license identifier
- topics
- update timestamps

## Rerun And Comparison Strategy

The discovery manifest is intentionally deterministic:

- repositories are sorted by `full_name`
- captured fields are fixed by the criteria file
- comparison is done by repository identity rather than by raw JSON order

That makes it practical to rerun the same criteria and see what changed.

## Acceptance Mapping

This ticket is done when:

- repository discovery can identify `TypeScript/Jest` candidates
- metadata for each candidate is captured
- results can be rerun and compared
