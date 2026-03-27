# Quality Scoring And Filtering

`UTSP-15`

This document defines the quality scoring pass that runs after discovery and
license filtering.

## Goal

The acquisition pipeline should reject repositories that technically match the
language and license rules but are still poor defaults for V1 training data.

## Current CLI

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli score-discovery \
  --criteria config/repository_selection_criteria.json \
  --manifest data/discovery/repositories.filtered.json \
  --output data/discovery/repositories.scored.json
```

## Scoring Model

The current repository score is a weighted sum of:

- star count relative to the configured minimum
- fork count relative to the configured minimum
- recency of the latest push relative to the recency window
- topic alignment with `typescript` and `jest`

The score threshold and component weights are configured in
`config/repository_selection_criteria.json`.

## Traceability

Accepted repositories retain their quality breakdown under `quality`.

Rejected repositories are preserved under `rejected_repositories` with:

- the repository name
- the rejection reason
- the full quality breakdown used to make the decision

## Acceptance Mapping

This ticket is done when:

- scoring heuristics are implemented
- quality thresholds are configurable
- rejected repositories remain traceable
