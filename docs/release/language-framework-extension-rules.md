# Language And Framework Extension Rules

`UTSP-33`

This document defines the checklist for extending the pipeline from
`TypeScript -> Jest` to a new language/framework pair.

## Reusable Components

The following parts are intended to stay reusable across pairs:

- repository discovery and license gating
- quality scoring and acquisition traceability
- dataset manifest structure and split freezing
- artifact versioning and standard benchmark reporting
- regression comparison and release gates

## Pair-Specific Adaptation Points

The following parts must be reviewed or replaced for a new pair:

- repository selection criteria and dependency markers
- raw source/test pairing heuristics
- normalization rules
- structured intermediate schema if `TEST_SPEC` stays in scope
- deterministic renderer
- compile and execution harnesses
- robustness heuristics if matcher ecosystems differ materially

## Extension Checklist

For a new pair, complete these steps:

1. Define the new task contract and update repository selection criteria.
2. Replace language-specific acquisition and normalization rules.
3. Decide whether to reuse or redesign the structured intermediate form.
4. Replace the renderer and evaluation harnesses.
5. Freeze new benchmark splits and update the V1 thresholds if needed.
6. Publish updated runbooks and release gates for the new pair.

## Acceptance Mapping

This ticket is done when:

- required adaptation points are documented
- reusable and pair-specific components are distinguished
