# Initial Base Model Shortlist

`UTSP-8`

This document narrows the initial model candidates for the first
`TypeScript -> Jest` experiments. The shortlist is intentionally small so the
project can compare a direct-code path against a more constrained structured
generation path without wasting cycles on a broad model bake-off.

The model cards below were checked on March 27, 2026.

## Selection Criteria

The V1 shortlist prefers models that are:

- small enough to be practical on Apple Silicon with parameter-efficient tuning
- available through standard Hugging Face model distribution
- instruction-tuned so they can support prompt-based baseline evaluation
- licensed in a way that does not immediately block internal experimentation

## Candidate 1: `Qwen/Qwen2.5-Coder-0.5B-Instruct`

### Why It Is On The List

This is the primary direct-generation candidate.

Based on the official model card, this model is:

- instruction tuned
- code specific
- approximately `0.49B` parameters
- Apache-2.0 licensed
- published with a `32,768` token context window

### Fit For This Project

This candidate is the best V1 fit when the task is framed as:

- source module in
- Jest test file out

The code specialization matters because the task includes imports, mocks,
assertions, and file-level structure rather than just natural-language
classification.

### Tradeoffs

- stronger code prior than a generic small instruct model
- more plausible for direct Jest test generation
- still small enough to keep local experiments practical
- likely weaker than larger code models on long-range reasoning and subtle
  cross-file behaviors
- may still be too weak for unconstrained full-file generation on noisy inputs

## Candidate 2: `HuggingFaceTB/SmolLM2-360M-Instruct`

### Why It Is On The List

This is the primary constrained-task candidate.

Based on the official model card, this model is:

- instruction tuned
- `360M` parameters
- Apache-2.0 licensed
- positioned for lightweight local or on-device style use

### Fit For This Project

This candidate is the better V1 fit when the task is framed as a narrower
prediction problem, such as:

- source module in
- bounded `TEST_SPEC` or equivalent structured test plan out

At this size, the project should not assume strong unconstrained code synthesis.
It is more realistic as a model that selects, structures, or fills bounded test
cases than as a model that authors arbitrary Jest files from scratch.

### Tradeoffs

- materially cheaper to fine-tune and iterate on
- good stress test for the structured-output strategy
- weaker raw coding prior than a code-specialized model
- likely unsuitable as the only direct-code candidate

## Recommended V1 Shortlist Outcome

Carry both candidates into the next phase, with distinct roles:

- direct-generation candidate: `Qwen/Qwen2.5-Coder-0.5B-Instruct`
- constrained-generation candidate: `HuggingFaceTB/SmolLM2-360M-Instruct`

This is a deliberate dual-track shortlist, not an attempt to pick one winner
before the structured-output decision and `MLX` feasibility work are complete.

## Deferred Questions

These questions are intentionally deferred to later tickets:

- exact `MLX` fine-tuning support and conversion path
- whether quantized fine-tuning introduces material workflow constraints
- whether the project should retain a third model as a stretch baseline

## Acceptance Mapping

This ticket is done when the repository documents:

- at least one `~0.5B` candidate
- at least one `~360M` candidate
- rationale and tradeoffs for each

## Sources

- Official model card: `https://huggingface.co/Qwen/Qwen2.5-Coder-0.5B-Instruct`
- Official model card: `https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct`
