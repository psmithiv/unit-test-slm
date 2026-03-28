# Adapter Fine-Tuning

`UTSP-23`

This document defines the parameter-efficient fine-tuning path for local small
models.

## Goal

Fine-tuning should stay practical on local hardware by using adapter-based
updates instead of full-model retraining.

## Current CLI

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli prepare-finetune-run \
  --config config/training/adapter_v1.json \
  --dataset-version dataset-v1 \
  --output-root artifacts \
  --output data/training/adapter_run_plan.json
```

## Current Strategy

The current plan generator builds a versioned MLX LoRA-style run manifest that
records:

- `model_id`
- `dataset_version`
- `adapter_strategy`
- `training_config_id`
- `run_id`
- `seed`
- output directory convention
- generated command line

## Reproducibility

- training configs are versioned as JSON files under `config/training/`
- `training_config_id` is derived from canonicalized config content
- `run_id` is derived from model, dataset version, config id, and seed

## Acceptance Mapping

This ticket is done when:

- a documented adapter-based training path exists
- training configs are versioned
- outputs are reproducible
