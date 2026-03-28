# Artifact Versioning

`UTSP-24`

This document defines the storage and metadata convention for training outputs.

## Goal

Adapters, checkpoints, and related metadata should be comparable later without
guessing which model, dataset, or config produced them.

## Current CLI

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli register-artifacts \
  --training-plan data/training/adapter_run_plan.json \
  --artifact-file adapters/adapter_model.safetensors \
  --artifact-file metrics.json \
  --output data/training/artifact_manifest.json
```

## Convention

Training outputs are expected under:

`artifacts/<model-id>/<dataset-version>/<training-config-id>/<run-id>/`

The artifact manifest records:

- `model_id`
- `dataset_version`
- `training_config_id`
- `run_id`
- `output_dir`
- artifact paths

## Acceptance Mapping

This ticket is done when:

- checkpoints or adapters are stored under a documented convention
- metadata includes model, dataset version, and training config identifiers
