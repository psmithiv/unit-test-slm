# Repository Selection Criteria

`UTSP-11`

This document defines how the pipeline should decide whether a public repository
is worth considering for the first `TypeScript -> Jest` acquisition pass.

The objective is simple: prefer quality and traceability over raw corpus size.

## Required Match Criteria

A repository is a V1 candidate only if it satisfies all of the following:

- the repository contains `TypeScript` source files
- the repository contains `Jest` test files or a clear `Jest` dependency signal
- the repository structure is legible enough to pair source modules with tests
- the repository license is allowed or explicitly reviewable

## Positive Quality Signals

The acquisition workflow should prefer repositories with signals such as:

- recent maintenance activity
- meaningful test density rather than token test directories
- assertion-heavy tests instead of snapshots-only coverage
- clear separation between implementation files and unit-test files
- consistent naming conventions such as `*.test.ts` or `*.spec.ts`
- dependency declarations that clearly indicate `Jest`

## Repository Metadata To Capture

The discovery workflow should capture, at minimum:

- repository owner and name
- repository URL
- default branch
- stars and forks
- last pushed timestamp
- primary language reported by GitHub
- license metadata
- topics or labels when available

## Exclusion Rules

The first acquisition pass should exclude repositories that are obviously poor
fits, including:

- repositories without `TypeScript`
- repositories without a clear `Jest` signal
- repositories whose tests are mostly fixtures, snapshots, or generated output
- repositories whose structure prevents reproducible source/test pairing
- archived, empty, or placeholder repositories
- repositories under blocked licenses

## License Handling

V1 should only admit repositories under allowlisted licenses by default.

The initial allowlist is:

- `MIT`
- `Apache-2.0`
- `BSD-2-Clause`
- `BSD-3-Clause`
- `ISC`

The initial denylist is:

- unknown or missing license metadata
- copyleft or review-required licenses unless explicitly approved later

## V1 Bias

The first pass should bias toward:

- utility libraries
- SDK-style modules
- service/helper packages with mockable dependencies
- codebases where unit-test intent is easy to read

The first pass should avoid:

- large monorepos where pairing logic is ambiguous
- browser-first end-to-end heavy repositories
- frameworks whose tests mostly exercise rendering or integration behavior

## Acceptance Mapping

This ticket is done when the repository documents:

- framework match criteria
- language match criteria
- quality signals
- license handling
- explicit exclusion rules
