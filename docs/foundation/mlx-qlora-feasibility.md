# MLX And QLoRA Feasibility Spike

`UTSP-9`

This document records the current feasibility findings for using `MLX` as the
V1 fine-tuning path for the `TypeScript -> Jest` project.

The official `mlx-lm` sources referenced here were checked on March 27, 2026.

## Short Answer

The V1 training path is feasible on Apple Silicon with `mlx-lm`, but the safest
interpretation is:

- use `mlx_lm.lora` as the standard training entrypoint
- treat `QLoRA` as the quantized-model variant of that same workflow
- keep the first implementation on a model family explicitly listed by the
  `mlx-lm` LoRA docs

## What The Official MLX Sources Support

According to the `mlx-lm` README, the package supports:

- text generation and fine-tuning on Apple Silicon
- low-rank and full-model fine-tuning
- fine-tuning with quantized models

According to the official `mlx_lm/LORA.md` guide:

- the main training command is `mlx_lm.lora`
- supported fine-tune types are `lora`, `dora`, and `full`
- if `--model` points to a quantized model, training uses `QLoRA`
- otherwise the same command path uses regular `LoRA`
- training data is expected as `train.jsonl`, with optional `valid.jsonl` and
  `test.jsonl`
- learned adapters are saved to `adapters/` by default and can be redirected
  with `--adapter-path`

## Officially Documented Fine-Tuning Families

The current `mlx_lm` LoRA guide explicitly lists these fine-tunable families:

- `Mistral`
- `Llama`
- `Phi2`
- `Mixtral`
- `Qwen2`
- `Gemma`
- `OLMo`
- `MiniCPM`
- `InternLM2`

This matters because the `mlx-lm` README says inference supports thousands of
models, but the LoRA guide is narrower about the families it explicitly
documents for adapter training.

## Supported And Unsupported Interpretation

Supported today:

- adapter-based training on Apple Silicon with `mlx_lm.lora`
- a quantized-model path that the official docs call `QLoRA`
- reproducible adapter output directories and resumable adapter training

Not safe to assume today:

- that every Hugging Face model runnable in `mlx-lm` is equally safe to
  fine-tune with LoRA or QLoRA
- that every small model in the shortlist is first-class in the current LoRA
  docs

## Impact On The Current Shortlist

The current shortlist is still directionally useful, but its training risk is
not uniform.

### Lower-Risk MLX Training Path

`Qwen/Qwen2.5-Coder-0.5B-Instruct` remains the stronger V1 training candidate.

This is an inference from the official MLX docs, not a direct guarantee:

- the LoRA guide explicitly lists the `Qwen2` family
- the shortlisted direct-generation model is a small Qwen-family code model
- the direct generation use case benefits from a code-specialized prior

### Higher-Risk MLX Training Path

`HuggingFaceTB/SmolLM2-360M-Instruct` remains attractive conceptually for a
bounded structured-output task, but it is not explicitly listed in the current
official `mlx-lm` LoRA family list.

That does not prove it is impossible. It does mean V1 should not depend on it
as the first guaranteed MLX fine-tuning path.

## Required Workarounds And Guardrails

The official docs imply the following practical guardrails for V1:

- prefer a model from an explicitly documented LoRA family first
- keep the first dataset in the `jsonl` shapes that `mlx_lm.lora` already
  expects
- convert and quantize the base checkpoint before training when `QLoRA` is
  required
- lower memory pressure with smaller batch size, fewer tuned layers, gradient
  accumulation, or gradient checkpointing when needed

The memory section of `LORA.md` also explicitly recommends quantization,
smaller batch size, fewer tuned layers, and gradient checkpointing as the main
ways to fit training to local hardware.

## Recommended V1 Training Path

The recommended V1 path is:

1. start with `mlx_lm.lora` on a supported Qwen-family checkpoint
2. get the dataset into the expected `train.jsonl` / `valid.jsonl` / `test.jsonl`
   structure
3. prove regular `LoRA` first on the unquantized checkpoint
4. switch the same workflow to `QLoRA` by pointing training at a quantized
   model if memory pressure justifies it
5. save adapters under an explicit versioned `--adapter-path` convention

This keeps the workflow aligned with what the official docs already describe,
instead of making the project depend on a less-certain model/conversion path on
day one.

## V1 Recommendation

Recommended V1 training path:

- `MLX`: yes
- adapter-based fine-tuning: yes
- `QLoRA`: yes, but as the quantized variant of the same `mlx_lm.lora`
  pipeline
- first guaranteed model family: `Qwen`-family over the current `SmolLM2`
  option

## Acceptance Mapping

This ticket is done when the repository documents:

- supported workflow details
- unsupported or not-safe-to-assume workflow details
- required workarounds
- the recommended V1 training path

## Sources

- Official `mlx-lm` README: `https://github.com/ml-explore/mlx-lm`
- Official LoRA guide: `https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md`
