# Baseline Inference

`UTSP-22`

This document defines the baseline inference harness for candidate base models.

## Goal

Untuned models should be measured on the same benchmark prompts before any
adapter training is attempted.

## Current CLI

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli run-baseline \
  --model-id qwen2.5-0.5b-instruct \
  --prompts data/benchmarks/prompts.json \
  --backend mock \
  --output data/results/qwen2.5-0.5b-instruct.baseline.json
```

The harness also supports a `subprocess` backend for real local model commands.

## Comparable Output Format

Each result record currently includes:

- `example_id`
- `mode`
- `prompt`
- `output`

The result manifest records:

- `model_id`
- `backend`
- `prompt_manifest_version`
- `generated_at`

## Acceptance Mapping

This ticket is done when:

- candidate base models can run against benchmark prompts
- outputs are saved in a comparable format
