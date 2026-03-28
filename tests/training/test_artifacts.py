from __future__ import annotations

import unittest

from unit_test_slm.training.artifacts import register_training_artifacts


class TrainingArtifactTests(unittest.TestCase):
    def test_register_training_artifacts_includes_required_metadata(self) -> None:
        training_plan = {
            "model_id": "qwen2.5-0.5b-instruct",
            "dataset_version": "dataset-v1",
            "training_config_id": "cfg123",
            "run_id": "run456",
            "output_dir": "artifacts/qwen2.5-0.5b-instruct/dataset-v1/cfg123/run456",
        }
        artifact_manifest = register_training_artifacts(
            training_plan,
            artifact_files=["adapters/adapter_model.safetensors", "metrics.json"],
            generated_at="2026-03-27T00:00:00+00:00",
        )
        self.assertEqual(artifact_manifest["model_id"], "qwen2.5-0.5b-instruct")
        self.assertEqual(artifact_manifest["dataset_version"], "dataset-v1")
        self.assertEqual(artifact_manifest["training_config_id"], "cfg123")
        self.assertEqual(artifact_manifest["run_id"], "run456")
        self.assertEqual(
            artifact_manifest["artifacts"][0]["path"],
            "artifacts/qwen2.5-0.5b-instruct/dataset-v1/cfg123/run456/adapters/adapter_model.safetensors",
        )


if __name__ == "__main__":
    unittest.main()
