from __future__ import annotations

import unittest

from unit_test_slm.dataset.splits import assign_split, freeze_benchmark_splits


class DatasetSplitTests(unittest.TestCase):
    def test_assign_split_is_reproducible(self) -> None:
        self.assertEqual(assign_split("example-1", "v1"), assign_split("example-1", "v1"))
        self.assertNotEqual(assign_split("example-1", "v1"), assign_split("example-1", "v2"))

    def test_freeze_benchmark_splits_versions_the_held_out_set(self) -> None:
        manifest = {
            "example_count": 6,
            "examples": [{"example_id": f"example-{index}", "split": "unassigned"} for index in range(6)],
        }
        frozen = freeze_benchmark_splits(manifest, split_version="benchmark-v1")
        self.assertEqual(frozen["split_version"], "benchmark-v1")
        self.assertEqual(frozen["benchmark"]["version"], "benchmark-v1")
        self.assertEqual(frozen["example_count"], 6)
        self.assertEqual(sum(frozen["split_counts"].values()), 6)
        self.assertTrue(
            all(example["split"] in {"train", "validation", "held_out"} for example in frozen["examples"])
        )


if __name__ == "__main__":
    unittest.main()
