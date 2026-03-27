# unit-test-slm

Pipeline for training a small language model against one programming language
and one unit-test framework at a time.

The first supported pair is `TypeScript -> Jest`.

## Current Docs

The current in-repo project docs live under `docs/`.

- `docs/README.md`
- `docs/foundation/v1-task-contract.md`
- `docs/acquisition/repository-selection-criteria.md`

## Local Validation

Run the current Python test suite with:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```
