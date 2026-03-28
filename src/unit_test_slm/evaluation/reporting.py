"""Standard benchmark reporting and regression comparison."""

from __future__ import annotations

from typing import Any


SUMMARY_FIELDS = (
    "parse_pass_rate",
    "compile_pass_rate",
    "execution_pass_rate",
    "robustness_score",
)


def build_run_report(run_label: str, metric_manifests: dict[str, dict[str, Any]]) -> dict[str, Any]:
    metrics = {}
    for field in SUMMARY_FIELDS:
        for manifest in metric_manifests.values():
            if field in manifest:
                metrics[field] = manifest[field]
                break

    overall_score = round(sum(metrics.values()) / len(metrics), 4) if metrics else 0.0
    return {
        "schema_version": "1.0.0",
        "run_label": run_label,
        "metrics": metrics,
        "overall_score": overall_score,
    }


def compare_run_reports(
    baseline_report: dict[str, Any], candidate_report: dict[str, Any]
) -> dict[str, Any]:
    metrics = sorted(set(baseline_report.get("metrics", {})) | set(candidate_report.get("metrics", {})))
    deltas = {}
    regressions = []
    improvements = []
    for metric in metrics:
        baseline_value = baseline_report.get("metrics", {}).get(metric, 0.0)
        candidate_value = candidate_report.get("metrics", {}).get(metric, 0.0)
        delta = round(candidate_value - baseline_value, 4)
        deltas[metric] = delta
        if delta < 0:
            regressions.append(metric)
        elif delta > 0:
            improvements.append(metric)

    overall_delta = round(
        candidate_report.get("overall_score", 0.0) - baseline_report.get("overall_score", 0.0),
        4,
    )
    return {
        "schema_version": "1.0.0",
        "baseline": baseline_report,
        "candidate": candidate_report,
        "deltas": deltas,
        "overall_delta": overall_delta,
        "regressions": regressions,
        "improvements": improvements,
    }
