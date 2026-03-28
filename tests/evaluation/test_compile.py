from __future__ import annotations

import sys
import unittest

from unit_test_slm.evaluation.compile import evaluate_compile


class CompileEvaluationTests(unittest.TestCase):
    def test_mock_compile_evaluation_reports_pass_rate(self) -> None:
        report = evaluate_compile(
            {
                "results": [
                    {"example_id": "one", "output": "describe('x', () => {})"},
                    {"example_id": "two", "output": "TYPE_ERROR"},
                ]
            }
        )
        self.assertEqual(report["compile_pass_count"], 1)
        self.assertEqual(report["compile_pass_rate"], 0.5)

    def test_subprocess_compile_evaluation_can_check_outputs(self) -> None:
        report = evaluate_compile(
            {"results": [{"example_id": "one", "output": "ok"}]},
            backend="subprocess",
            checker_command=[
                sys.executable,
                "-c",
                "import sys; data=sys.stdin.read(); raise SystemExit(0 if data.strip()=='ok' else 1)",
            ],
        )
        self.assertTrue(report["results"][0]["passed"])


if __name__ == "__main__":
    unittest.main()
