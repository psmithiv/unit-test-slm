# Generation Strategy Decision

`UTSP-10`

This document records the V1 decision on whether the pipeline should train for
direct Jest file generation, a structured `TEST_SPEC` representation, or both.

## Decision

V1 will use a dual-track strategy:

- keep direct generation as a benchmark and comparison path
- retain `TEST_SPEC` as the preferred V1 operating mode

This means direct generation is not rejected outright, but the project should
optimize its first reusable pipeline around:

1. source module -> `TEST_SPEC`
2. deterministic renderer -> normalized Jest test file

## Decision Outcome

### Direct Generation

Decision: accepted as a comparison path, not as the default V1 delivery shape.

Why it stays:

- it gives the project a realistic benchmark against a code-specialized small
  model
- it avoids prematurely forcing all useful test behavior into a schema
- it helps measure whether the structured path is actually worth the extra
  system complexity

Why it is not the preferred V1 default:

- it asks the model to learn file structure, style, imports, mocks, and test
  semantics in one unconstrained output space
- it is more exposed to formatting drift and stylistic variance from scraped
  GitHub examples
- it increases evaluation noise because output normalization becomes harder

### `TEST_SPEC`

Decision: retained and preferred for V1.

Why it wins the V1 bias:

- it narrows the prediction task for very small models
- it moves formatting and style control into deterministic code
- it makes normalization easier across repositories and runs
- it keeps the system compatible with smaller constrained-task candidates
- it creates a cleaner comparison surface for automated evaluation

## Why This Decision Fits The Project

The project is not trying to build a general-purpose coding model. It is trying
to build a narrow reusable pipeline for one language/framework pair at a time.

That pushes the design toward:

- lower output entropy
- stronger normalization
- clearer provenance between model output and rendered code
- easier compile and execution evaluation

For this project, those are more important than maximizing raw free-form code
generation flexibility in V1.

## V1 `TEST_SPEC` Shape

The exact schema can evolve in later tickets, but the V1 structure should cover
at least:

- subject under test
- imports
- setup
- mocks
- cases

Each case should stay bounded to a small ontology such as:

- happy path
- boundary condition
- error path
- async resolve
- async reject
- dependency interaction

## Operational Meaning

The dual-track decision means the next phases should do both of the following:

- preserve enough dataset structure to benchmark direct source-to-Jest training
- design the primary curation and rendering pipeline around `TEST_SPEC`

The project should not spend V1 effort trying to support every possible shape of
free-form Jest authoring. It should bias toward the structured path and keep the
direct path as the benchmark that can overturn the assumption if results justify
it later.

## What Would Change This Decision

The project should revisit this decision only if later benchmarking shows one of
the following:

- the direct-generation path clearly beats the structured path on compile,
  execution, and robustness metrics
- the `TEST_SPEC` schema proves too lossy to express useful Jest behavior
- the renderer becomes the dominant source of complexity or failure

Until one of those conditions is observed, the preferred V1 direction remains
structured generation plus deterministic rendering.

## Acceptance Mapping

This ticket is done when the repository documents:

- direct generation as accepted, rejected, or dual-track
- the `TEST_SPEC` concept and why it remains
- rationale tied to small-model constraints
