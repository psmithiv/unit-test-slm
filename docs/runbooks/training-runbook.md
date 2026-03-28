# Training Runbook

`UTSP-31`

## Inputs

- benchmark prompt manifest
- dataset version identifier
- training config JSON

## Steps

1. Measure untuned candidates with `run-baseline`.
2. Prepare an adapter-based run manifest with `prepare-finetune-run`.
3. Execute the generated MLX command outside the repo as needed.
4. Register produced adapters and metadata with `register-artifacts`.
5. Compare direct versus `TEST_SPEC` paths with `compare-training-paths`.

## Outputs

- baseline result manifest
- fine-tuning run plan
- artifact manifest
- direct versus `TEST_SPEC` comparison manifest
