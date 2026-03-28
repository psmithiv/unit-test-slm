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
- `docs/dataset/test-spec-schema.md`: structured TEST_SPEC schema
- `docs/dataset/jest-renderer.md`: deterministic rendering from TEST_SPEC to Jest
- `docs/dataset/benchmark-splits.md`: reproducible train/validation/held-out splits

## Training

- `docs/training/baseline-inference.md`: untuned model benchmarking harness
- `docs/training/adapter-finetuning.md`: reproducible adapter-based training path
- `docs/training/artifact-versioning.md`: artifact storage and metadata convention
- `docs/training/direct-vs-test-spec.md`: side-by-side comparison and V1 decision

## Evaluation

- `docs/evaluation/syntax-validation.md`: fast syntax and parse validation
- `docs/evaluation/typescript-compile-evaluation.md`: compile success evaluation
