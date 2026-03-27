# License And Provenance Enforcement

`UTSP-14`

This document defines how the acquisition pipeline enforces license rules and
preserves provenance for every extracted example.

## Goals

- block repositories that do not satisfy the configured license policy
- preserve repository identity on every downstream example
- preserve file-level provenance on every extracted source/test pair

## Current CLI

Filter a discovery manifest by license policy:

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli enforce-license-policy \
  --criteria config/repository_selection_criteria.json \
  --manifest data/discovery/repositories.json \
  --output data/discovery/repositories.filtered.json
```

Capture repository and file provenance during scraping:

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli scrape-repo \
  --repo-root path/to/repository \
  --repository-name owner/repo \
  --repository-url https://github.com/owner/repo \
  --revision <commit-sha> \
  --license-spdx-id MIT \
  --output data/raw/source_test_pairs.json
```

## Enforcement Rules

The current implementation:

- admits repositories only if their SPDX license is allowlisted
- rejects repositories with missing or blocked license metadata
- records rejected repositories with an explicit rejection reason

## Provenance Rules

Each raw source/test pair now carries:

- repository name
- repository URL
- repository revision
- repository license SPDX identifier
- source file path
- matched test file paths

## Acceptance Mapping

This ticket is done when:

- every example carries repository and file provenance
- license metadata is stored with each repository snapshot
- unapproved repositories can be excluded automatically
