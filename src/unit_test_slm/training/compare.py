"""Comparison helpers for direct generation and TEST_SPEC training paths."""

from __future__ import annotations

from typing import Any


PRIMARY_METRICS = (
    "overall_score",
    "syntax_pass_rate",
    "compile_pass_rate",
    "jest_pass_rate",
    "robustness_score",
)


def _score(manifest: dict[str, Any]) -> float:
    metrics = manifest.get("metrics", {})
    for metric in PRIMARY_METRICS:
        if metric in metrics:
            return float(metrics[metric])
    return 0.0


def compare_training_paths(
    direct_manifest: dict[str, Any], test_spec_manifest: dict[str, Any]
) -> dict[str, Any]:
    direct_score = _score(direct_manifest)
    test_spec_score = _score(test_spec_manifest)

    if test_spec_score > direct_score:
        preferred_path = "test_spec"
        rationale = "test_spec_outperformed_direct_generation"
    elif direct_score > test_spec_score:
        preferred_path = "direct"
        rationale = "direct_generation_outperformed_test_spec"
    else:
        preferred_path = "test_spec"
        rationale = "scores_tied_defaulting_to_v1_structured_path"

    return {
        "paths": {
            "direct": direct_manifest,
            "test_spec": test_spec_manifest,
        },
        "preferred_v1_path": preferred_path,
        "rationale": rationale,
        "side_by_side_metrics": {
            metric: {
                "direct": direct_manifest.get("metrics", {}).get(metric),
                "test_spec": test_spec_manifest.get("metrics", {}).get(metric),
            }
            for metric in PRIMARY_METRICS
        },
    }
