# Evaluation Runbook

`UTSP-31`

## Inputs

- generated result manifest for a benchmark run

## Steps

1. Run `evaluate-syntax`.
2. Run `evaluate-compile`.
3. Run `evaluate-jest`.
4. Run `evaluate-robustness`.
5. Build a standard report with `build-report`.
6. Compare the report against a prior run with `compare-reports`.

## Outputs

- syntax report
- compile report
- execution report
- robustness report
- standard run report
- baseline versus candidate comparison report
