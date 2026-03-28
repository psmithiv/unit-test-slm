"""Jest execution evaluation for generated outputs."""

from __future__ import annotations

import subprocess
from typing import Any


def run_jest_check(
    output: str, *, backend: str = "mock", harness_command: list[str] | None = None
) -> dict[str, Any]:
    if backend == "mock":
        passed = "expect(" in output and ("it(" in output or "test(" in output)
        return {"passed": passed, "backend": backend}

    if backend == "subprocess":
        if not harness_command:
            raise ValueError("subprocess Jest evaluation requires a harness command")
        result = subprocess.run(
            harness_command,
            input=output,
            text=True,
            capture_output=True,
        )
        return {
            "passed": result.returncode == 0,
            "backend": backend,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }

    raise ValueError(f"unsupported backend: {backend}")


def evaluate_jest_execution(
    result_manifest: dict[str, Any], *, backend: str = "mock", harness_command: list[str] | None = None
) -> dict[str, Any]:
    evaluated_results = []
    pass_count = 0
    for result in result_manifest.get("results", []):
        execution_result = run_jest_check(
            result["output"], backend=backend, harness_command=harness_command
        )
        pass_count += 1 if execution_result["passed"] else 0
        evaluated_results.append(
            {
                "example_id": result["example_id"],
                "passed": execution_result["passed"],
                "execution": execution_result,
            }
        )

    result_count = len(evaluated_results)
    return {
        "schema_version": "1.0.0",
        "backend": backend,
        "result_count": result_count,
        "execution_pass_count": pass_count,
        "execution_pass_rate": round(pass_count / result_count, 4) if result_count else 0.0,
        "results": evaluated_results,
    }
