from __future__ import annotations

import unittest

from unit_test_slm.training.compare import compare_training_paths


class TrainingComparisonTests(unittest.TestCase):
    def test_compare_training_paths_prefers_higher_scoring_path(self) -> None:
        direct = {"metrics": {"overall_score": 0.61, "syntax_pass_rate": 0.8}}
        test_spec = {"metrics": {"overall_score": 0.72, "syntax_pass_rate": 0.9}}
        comparison = compare_training_paths(direct, test_spec)
        self.assertEqual(comparison["preferred_v1_path"], "test_spec")
        self.assertEqual(
            comparison["side_by_side_metrics"]["overall_score"],
            {"direct": 0.61, "test_spec": 0.72},
        )

    def test_compare_training_paths_defaults_to_test_spec_on_tie(self) -> None:
        direct = {"metrics": {"overall_score": 0.7}}
        test_spec = {"metrics": {"overall_score": 0.7}}
        comparison = compare_training_paths(direct, test_spec)
        self.assertEqual(comparison["preferred_v1_path"], "test_spec")
        self.assertEqual(
            comparison["rationale"],
            "scores_tied_defaulting_to_v1_structured_path",
        )


if __name__ == "__main__":
    unittest.main()
