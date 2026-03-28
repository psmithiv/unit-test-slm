"""Structured TEST_SPEC schema for bounded Jest generation."""

from __future__ import annotations

from typing import Any


TEST_SPEC_VERSION = "1.0.0"
CASE_TYPES = {
    "returns",
    "throws",
    "resolves",
    "rejects",
    "side_effect",
}


def validate_test_spec(spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if spec.get("schema_version") != TEST_SPEC_VERSION:
        errors.append("invalid_schema_version")

    for field in ("suite", "target", "setup", "mocks", "cases"):
        if field not in spec:
            errors.append(f"missing_{field}")

    if "target" in spec:
        target = spec["target"]
        for field in ("module_path", "export_name"):
            if field not in target:
                errors.append(f"missing_target_{field}")

    if "cases" in spec:
        cases = spec["cases"]
        if not isinstance(cases, list) or not cases:
            errors.append("cases_must_be_non_empty_list")
        else:
            for index, case in enumerate(cases):
                if case.get("type") not in CASE_TYPES:
                    errors.append(f"case_{index}_invalid_type")
                if "name" not in case:
                    errors.append(f"case_{index}_missing_name")
                if "assertion" not in case:
                    errors.append(f"case_{index}_missing_assertion")

    return errors


def example_test_spec() -> dict[str, Any]:
    return {
        "schema_version": TEST_SPEC_VERSION,
        "suite": {
            "describe": "sum",
        },
        "target": {
            "module_path": "./sum",
            "export_name": "sum",
        },
        "setup": {
            "imports": ["sum"],
            "before_each": [],
        },
        "mocks": [],
        "cases": [
            {
                "name": "adds two positive integers",
                "type": "returns",
                "input": ["1", "2"],
                "assertion": "toBe(3)",
            }
        ],
    }
