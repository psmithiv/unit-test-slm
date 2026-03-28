from __future__ import annotations

import json
import unittest

from unit_test_slm.dataset.test_spec import example_test_spec
from unit_test_slm.evaluation.syntax import evaluate_syntax, validate_output_syntax


class SyntaxEvaluationTests(unittest.TestCase):
    def test_validate_output_syntax_detects_invalid_jest_output(self) -> None:
        validation = validate_output_syntax("describe('x', () => {")
        self.assertFalse(validation["passed"])
        self.assertFalse(validation["balanced_delimiters"])

    def test_validate_output_syntax_supports_test_spec_mode(self) -> None:
        output = json.dumps(example_test_spec())
        validation = validate_output_syntax(output, mode="test_spec")
        self.assertTrue(validation["passed"])
        self.assertEqual(validation["parse_mode"], "test_spec")

    def test_evaluate_syntax_reports_parse_metrics(self) -> None:
        report = evaluate_syntax(
            {
                "results": [
                    {"example_id": "one", "mode": "direct", "output": "describe('x', () => { it('y', () => {}) })"},
                    {"example_id": "two", "mode": "direct", "output": "describe('x', () => {"},
                ]
            }
        )
        self.assertEqual(report["result_count"], 2)
        self.assertEqual(report["parse_pass_count"], 1)
        self.assertEqual(report["parse_pass_rate"], 0.5)


if __name__ == "__main__":
    unittest.main()
