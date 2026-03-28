# V1 Definition Of Done

`UTSP-32`

This document freezes the acceptance bar for the first release of the
`TypeScript -> Jest` unit-test SLM pipeline.

## V1 Delivery Criteria

V1 is done when all of the following are true:

- acquisition, curation, training, and evaluation flows are documented and
  runnable from the repo runbooks
- the pipeline can produce benchmark reports in the standard format
- the preferred V1 path is explicitly recorded
- training configs, dataset versions, and artifact manifests are versioned

## Required Benchmark Thresholds

The V1 candidate should meet these minimum thresholds on the held-out benchmark:

- `parse_pass_rate >= 0.95`
- `compile_pass_rate >= 0.90`
- `execution_pass_rate >= 0.75`
- `robustness_score >= 0.45`

## Review Gates

Before a V1 release is accepted:

- benchmark reports must show baseline versus candidate comparison
- rejected acquisitions and deduped examples must remain traceable
- a human review must confirm that at least a sample of generated tests are
  behaviorally useful and not merely well-formed

## Acceptance Mapping

This ticket is done when:

- V1 delivery criteria are documented
- required benchmark thresholds or review gates are listed
