from __future__ import annotations

import sys
import unittest

from unit_test_slm.training.baseline import run_baseline_inference


class BaselineInferenceTests(unittest.TestCase):
    def test_mock_backend_produces_comparable_results(self) -> None:
        manifest = {
            "prompt_manifest_version": "v1",
            "prompts": [
                {"example_id": "one", "mode": "direct", "prompt": "write a unit test"},
                {"example_id": "two", "mode": "test_spec", "prompt": "emit a TEST_SPEC"},
            ],
        }
        results = run_baseline_inference(
            manifest,
            model_id="qwen2.5-0.5b-instruct",
            generated_at="2026-03-27T00:00:00+00:00",
        )
        self.assertEqual(results["result_count"], 2)
        self.assertEqual(results["results"][0]["example_id"], "one")
        self.assertEqual(results["results"][1]["mode"], "test_spec")
        self.assertTrue(results["results"][0]["output"].startswith("mock::"))

    def test_subprocess_backend_can_run_against_prompts(self) -> None:
        manifest = {
            "prompts": [{"example_id": "one", "prompt": "abc"}],
        }
        results = run_baseline_inference(
            manifest,
            model_id="local-candidate",
            backend="subprocess",
            command=[
                sys.executable,
                "-c",
                "import sys; print(sys.stdin.read().strip()[::-1])",
            ],
            generated_at="2026-03-27T00:00:00+00:00",
        )
        self.assertEqual(results["results"][0]["output"], "cba")


if __name__ == "__main__":
    unittest.main()
