# TEST_SPEC Schema

`UTSP-19`

This document defines the bounded `TEST_SPEC` representation used as the
structured alternative to direct test-file generation.

## Goal

Smaller models should solve a narrower prediction task by producing a structured
specification that can later be rendered into normalized Jest code.

## Current Shape

Top-level fields:

- `schema_version`
- `suite`
- `target`
- `setup`
- `mocks`
- `cases`

`target` currently includes:

- `module_path`
- `export_name`

`cases` are bounded to these types:

- `returns`
- `throws`
- `resolves`
- `rejects`
- `side_effect`

## Coverage

The schema explicitly covers:

- setup imports and before-each behavior
- explicit mocks
- bounded case definitions with names, types, inputs, and assertions

## Validation

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli validate-test-spec \
  --spec data/test_specs/example.json
```

## Acceptance Mapping

This ticket is done when:

- `TEST_SPEC` fields are documented
- bounded case types are defined
- the schema covers setup, mocks, and cases
