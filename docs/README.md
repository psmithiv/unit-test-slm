# Unit Test SLM Docs

This directory captures the project's local source-of-truth documents as the
pipeline is implemented ticket by ticket.

## Foundation

- `docs/foundation/v1-task-contract.md`: V1 task boundary for `TypeScript -> Jest`
- `docs/foundation/base-model-shortlist.md`: initial small-model candidates for V1
- `docs/foundation/mlx-qlora-feasibility.md`: official MLX training-path findings
- `docs/foundation/generation-strategy-decision.md`: direct output vs `TEST_SPEC`

## Acquisition

- `docs/acquisition/repository-selection-criteria.md`: repository inclusion and exclusion rules
- `docs/acquisition/discovery-workflow.md`: GitHub discovery workflow and manifest shape
- `docs/acquisition/license-and-provenance.md`: license gating and provenance rules
- `docs/acquisition/quality-scoring-and-filtering.md`: repository quality scoring rules
- `docs/acquisition/source-test-pair-scraper.md`: raw pairing manifest and scraper behavior
- `config/repository_selection_criteria.json`: machine-readable acquisition criteria

## Dataset

- `docs/dataset/dataset-manifest-schema.md`: stable curated example manifest
- `docs/dataset/normalization-rules.md`: deterministic source and test normalization
- `docs/dataset/deduplication-strategy.md`: exact and near-duplicate handling
