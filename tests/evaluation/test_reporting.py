from __future__ import annotations

import unittest

from unit_test_slm.evaluation.reporting import build_run_report, compare_run_reports


class EvaluationReportingTests(unittest.TestCase):
    def test_build_run_report_creates_standard_metric_shape(self) -> None:
        report = build_run_report(
            "baseline",
            {
                "syntax": {"parse_pass_rate": 0.8},
                "compile": {"compile_pass_rate": 0.7},
                "jest": {"execution_pass_rate": 0.6},
                "robustness": {"robustness_score": 0.5},
            },
        )
        self.assertEqual(report["run_label"], "baseline")
        self.assertEqual(report["overall_score"], 0.65)

    def test_compare_run_reports_captures_baseline_vs_candidate(self) -> None:
        baseline = {"run_label": "baseline", "metrics": {"parse_pass_rate": 0.8}, "overall_score": 0.8}
        candidate = {"run_label": "tuned", "metrics": {"parse_pass_rate": 0.9}, "overall_score": 0.9}
        comparison = compare_run_reports(baseline, candidate)
        self.assertEqual(comparison["overall_delta"], 0.1)
        self.assertEqual(comparison["improvements"], ["parse_pass_rate"])


if __name__ == "__main__":
    unittest.main()
