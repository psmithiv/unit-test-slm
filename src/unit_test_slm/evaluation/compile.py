"""Compile evaluation for generated benchmark outputs."""

from __future__ import annotations

import subprocess
from typing import Any


def run_compile_check(
    output: str, *, backend: str = "mock", checker_command: list[str] | None = None
) -> dict[str, Any]:
    if backend == "mock":
        passed = "TYPE_ERROR" not in output and "SYNTAX_ERROR" not in output
        return {"passed": passed, "backend": backend}

    if backend == "subprocess":
        if not checker_command:
            raise ValueError("subprocess compile evaluation requires a checker command")
        result = subprocess.run(
            checker_command,
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


def evaluate_compile(
    result_manifest: dict[str, Any], *, backend: str = "mock", checker_command: list[str] | None = None
) -> dict[str, Any]:
    evaluated_results = []
    pass_count = 0
    for result in result_manifest.get("results", []):
        compile_result = run_compile_check(
            result["output"], backend=backend, checker_command=checker_command
        )
        pass_count += 1 if compile_result["passed"] else 0
        evaluated_results.append(
            {
                "example_id": result["example_id"],
                "passed": compile_result["passed"],
                "compile": compile_result,
            }
        )

    result_count = len(evaluated_results)
    return {
        "schema_version": "1.0.0",
        "backend": backend,
        "result_count": result_count,
        "compile_pass_count": pass_count,
        "compile_pass_rate": round(pass_count / result_count, 4) if result_count else 0.0,
        "results": evaluated_results,
    }
