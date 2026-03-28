from __future__ import annotations

import unittest
from pathlib import Path

from unit_test_slm.training.finetune import build_adapter_training_plan, training_config_id


class FineTunePlanTests(unittest.TestCase):
    def test_training_config_id_is_stable(self) -> None:
        config = {
            "model_id": "qwen2.5-0.5b-instruct",
            "adapter_strategy": "qlora",
            "train_data_path": "data/train.jsonl",
            "batch_size": 2,
            "learning_rate": 0.0002,
            "iterations": 100,
            "seed": 7,
        }
        self.assertEqual(training_config_id(config), training_config_id(config))

    def test_training_plan_is_reproducible_and_versioned(self) -> None:
        config = {
            "model_id": "qwen2.5-0.5b-instruct",
            "adapter_strategy": "qlora",
            "train_data_path": "data/train.jsonl",
            "batch_size": 2,
            "learning_rate": 0.0002,
            "iterations": 100,
            "seed": 7,
        }
        plan = build_adapter_training_plan(
            config,
            dataset_version="dataset-v1",
            output_root=Path("artifacts"),
            generated_at="2026-03-27T00:00:00+00:00",
        )
        self.assertEqual(plan["adapter_strategy"], "qlora")
        self.assertEqual(plan["dataset_version"], "dataset-v1")
        self.assertIn(plan["training_config_id"], plan["output_dir"])
        self.assertIn(plan["run_id"], plan["output_dir"])
        self.assertEqual(plan["command"][0:3], ["python3", "-m", "mlx_lm.lora"])


if __name__ == "__main__":
    unittest.main()
