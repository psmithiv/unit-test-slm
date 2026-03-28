# Jest Renderer

`UTSP-20`

This document defines the deterministic renderer from `TEST_SPEC` to normalized
Jest code.

## Goal

The structured generation path should keep code-style decisions out of the
model. The model predicts `TEST_SPEC`; the renderer handles Jest formatting.

## Current CLI

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli render-test-spec \
  --spec data/test_specs/example.json \
  --output data/rendered/example.test.ts
```

## Renderer Rules

The current renderer:

- validates the incoming `TEST_SPEC` before rendering
- renders stable import ordering
- renders `jest.mock(...)` calls before the test suite
- renders `describe(...)` and `it(...)` blocks deterministically
- normalizes the final output with the same Jest normalization pass used for
  curated examples

## Supported Case Types

- `returns`
- `throws`
- `resolves`
- `rejects`
- `side_effect`

## Acceptance Mapping

This ticket is done when:

- the renderer produces valid normalized Jest code
- renderer output is deterministic for the same input
