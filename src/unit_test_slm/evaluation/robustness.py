"""Equivalent robustness signal for generated tests."""

from __future__ import annotations

import re
from typing import Any


MATCHER_PATTERN = re.compile(r"\.(to[A-Z][A-Za-z0-9_]+)")


def score_output_robustness(output: str) -> dict[str, Any]:
    assertion_count = output.count("expect(")
    matchers = set(MATCHER_PATTERN.findall(output))
    negative_signal = any(token in output for token in ("not.", "toThrow", "rejects"))
    snapshot_only = matchers == {"toMatchSnapshot"} and assertion_count > 0

    if snapshot_only:
        score = 0.0
    else:
        score = min(assertion_count / 3, 1.0) * 0.5
        score += min(len(matchers) / 3, 1.0) * 0.3
        score += 0.2 if negative_signal else 0.0

    return {
        "score": round(score, 4),
        "assertion_count": assertion_count,
        "matcher_diversity": len(matchers),
        "negative_signal": negative_signal,
        "snapshot_only": snapshot_only,
        "signal_type": "equivalent_robustness_signal",
    }


def evaluate_robustness(result_manifest: dict[str, Any]) -> dict[str, Any]:
    evaluated_results = []
    total = 0.0
    for result in result_manifest.get("results", []):
        robustness = score_output_robustness(result["output"])
        total += robustness["score"]
        evaluated_results.append(
            {
                "example_id": result["example_id"],
                "robustness": robustness,
            }
        )

    result_count = len(evaluated_results)
    return {
        "schema_version": "1.0.0",
        "metric_name": "equivalent_robustness_signal",
        "result_count": result_count,
        "robustness_score": round(total / result_count, 4) if result_count else 0.0,
        "results": evaluated_results,
    }
