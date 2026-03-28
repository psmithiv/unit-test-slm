from __future__ import annotations

import sys
import unittest

from unit_test_slm.evaluation.jest import evaluate_jest_execution


class JestExecutionTests(unittest.TestCase):
    def test_mock_jest_evaluation_reports_execution_rate(self) -> None:
        report = evaluate_jest_execution(
            {
                "results": [
                    {"example_id": "one", "output": "describe('x', () => { it('y', () => { expect(1).toBe(1) }) })"},
                    {"example_id": "two", "output": "describe('x', () => { it('y', () => {}) })"},
                ]
            }
        )
        self.assertEqual(report["execution_pass_count"], 1)
        self.assertEqual(report["execution_pass_rate"], 0.5)

    def test_subprocess_jest_evaluation_can_run_harness(self) -> None:
        report = evaluate_jest_execution(
            {"results": [{"example_id": "one", "output": "run"}]},
            backend="subprocess",
            harness_command=[
                sys.executable,
                "-c",
                "import sys; data=sys.stdin.read(); raise SystemExit(0 if data.strip()=='run' else 1)",
            ],
        )
        self.assertTrue(report["results"][0]["passed"])


if __name__ == "__main__":
    unittest.main()
