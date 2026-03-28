# TypeScript Compile Evaluation

`UTSP-27`

This document defines the compile evaluation stage for generated outputs.

## Goal

Generated tests should be judged on actual TypeScript compatibility rather than
surface formatting alone.

## Current CLI

```bash
PYTHONPATH=src python3 -m unit_test_slm.cli evaluate-compile \
  --results data/results/direct.json \
  --backend mock \
  --output data/evaluation/direct.compile.json
```

The evaluator also supports a `subprocess` backend for real local compile
checks, for example a `tsc --noEmit` wrapper.

## Acceptance Mapping

This ticket is done when:

- benchmark outputs can be checked for compile success
- compile rate is reported per run
