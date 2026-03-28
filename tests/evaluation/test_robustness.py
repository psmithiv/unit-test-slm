from __future__ import annotations

import unittest

from unit_test_slm.evaluation.robustness import evaluate_robustness, score_output_robustness


class RobustnessEvaluationTests(unittest.TestCase):
    def test_snapshot_only_tests_score_poorly(self) -> None:
        score = score_output_robustness("it('x', () => { expect(value).toMatchSnapshot() })")
        self.assertEqual(score["score"], 0.0)
        self.assertTrue(score["snapshot_only"])

    def test_evaluate_robustness_reports_average_score(self) -> None:
        report = evaluate_robustness(
            {
                "results": [
                    {"example_id": "one", "output": "it('x', () => { expect(sum(1,2)).toBe(3) })"},
                    {"example_id": "two", "output": "it('x', () => { expect(fn).toThrow() })"},
                ]
            }
        )
        self.assertEqual(report["metric_name"], "equivalent_robustness_signal")
        self.assertEqual(report["result_count"], 2)
        self.assertGreater(report["robustness_score"], 0.0)


if __name__ == "__main__":
    unittest.main()
