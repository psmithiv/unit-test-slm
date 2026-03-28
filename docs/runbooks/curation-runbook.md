# Curation Runbook

`UTSP-31`

## Inputs

- raw source/test pair manifest

## Steps

1. Build the curated dataset manifest with `build-dataset-manifest`.
2. Normalize examples with `normalize-dataset`.
3. Remove duplicates with `dedupe-dataset`.
4. Freeze split assignments with `freeze-splits`.
5. Validate or render `TEST_SPEC` artifacts as needed.

## Outputs

- curated dataset manifest
- normalized dataset manifest
- deduped dataset manifest
- split-frozen benchmark manifest
