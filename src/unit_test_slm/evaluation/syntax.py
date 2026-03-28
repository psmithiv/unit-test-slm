"""Fast syntax and parse validation for generated outputs."""

from __future__ import annotations

import json
from typing import Any

from unit_test_slm.dataset.test_spec import validate_test_spec


PAIRS = {"(": ")", "[": "]", "{": "}"}


def _balanced_delimiters(text: str) -> bool:
    stack: list[str] = []
    for char in text:
        if char in PAIRS:
            stack.append(PAIRS[char])
        elif char in PAIRS.values():
            if not stack or stack.pop() != char:
                return False
    return not stack


def validate_output_syntax(output: str, *, mode: str = "direct") -> dict[str, Any]:
    if mode == "test_spec":
        try:
            spec = json.loads(output)
        except json.JSONDecodeError:
            return {"passed": False, "parse_mode": "json", "reason": "invalid_json"}
        errors = validate_test_spec(spec)
        return {
            "passed": not errors,
            "parse_mode": "test_spec",
            "error_count": len(errors),
            "errors": errors,
        }

    balanced = _balanced_delimiters(output)
    has_test_structure = "describe(" in output and ("it(" in output or "test(" in output)
    passed = balanced and has_test_structure
    return {
        "passed": passed,
        "parse_mode": "jest_text",
        "balanced_delimiters": balanced,
        "has_test_structure": has_test_structure,
    }


def evaluate_syntax(result_manifest: dict[str, Any]) -> dict[str, Any]:
    evaluated_results = []
    pass_count = 0
    for result in result_manifest.get("results", []):
        validation = validate_output_syntax(
            result["output"], mode=result.get("mode", "direct")
        )
        pass_count += 1 if validation["passed"] else 0
        evaluated_results.append(
            {
                "example_id": result["example_id"],
                "passed": validation["passed"],
                "validation": validation,
            }
        )

    result_count = len(evaluated_results)
    return {
        "schema_version": "1.0.0",
        "result_count": result_count,
        "parse_pass_count": pass_count,
        "parse_pass_rate": round(pass_count / result_count, 4) if result_count else 0.0,
        "results": evaluated_results,
    }
