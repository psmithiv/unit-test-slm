# V1 Task Contract

`UTSP-7`

This document defines the first supported task boundary for the `Unit Test SLM`
pipeline. The goal is a stable V1 scope that later tickets can implement
without revisiting basic assumptions.

## Supported Pair

- source language: `TypeScript`
- target unit-test framework: `Jest`

V1 is intentionally single-pair. The pipeline may later be reused for other
language/framework combinations, but that is not part of the first delivery.

## Task Definition

The V1 task is:

> given a `TypeScript` source module and limited local context, produce a
> normalized `Jest` unit-test artifact suitable for automated evaluation.

For V1, the system is optimized for narrow unit-test generation rather than
general code synthesis.

## Input Contract

The canonical source input is:

- one `TypeScript` implementation file under test
- its relative file path within the repository snapshot
- optional nearby context needed to understand exported behavior

V1 does not require multi-file architectural reasoning across an entire codebase.
If a module cannot be understood from its local implementation boundary, it is a
poor V1 training candidate.

## Output Contract

The output must target `Jest` conventions and be suitable for deterministic
evaluation. The rendering strategy itself is finalized in `UTSP-10`, but the
V1 output assumptions are already fixed:

- the artifact must represent a `Jest` test file or a structure that renders
  directly into one
- the result must focus on unit-test behavior for the provided module
- the output should be normalized enough to compare across runs
- the output must be constrained enough to support syntax, compile, and
  execution checks

## Output Style Assumptions

Regardless of whether the model produces direct code or an intermediate
structure, the V1 pipeline assumes the final rendered `Jest` output should:

- use explicit `describe` and `it` / `test` blocks
- prefer readable arrange-act-assert flow
- keep imports and mocks explicit rather than implied
- focus on behaviorally meaningful cases such as happy-path, boundary, error,
  and dependency interaction coverage
- avoid project-specific stylistic flourishes that make normalization harder

The goal is not to reproduce every house style found on GitHub. The goal is a
consistent evaluable target.

## In-Scope Test Patterns

The V1 task should prioritize examples like:

- pure or mostly pure module functions
- utility modules with deterministic inputs and outputs
- service helpers with mockable dependencies
- async functions with explicit resolve and reject behavior

## V1 Non-Goals

The following are explicitly out of scope for V1:

- multi-language training
- multi-framework training
- end-to-end or browser-driven integration tests
- broad support for every Jest plugin or matcher ecosystem variant
- autonomous promotion of generated tests into production repositories
- full-repository reasoning across large architectural surfaces
- IDE integration, editor plugins, or developer-facing productization

## Acceptance Mapping

This ticket is done when the repository documents:

- `TypeScript` as the source language
- `Jest` as the target framework
- the expected output style assumptions
- the V1 non-goals
