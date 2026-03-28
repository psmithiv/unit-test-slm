from __future__ import annotations

import unittest

from unit_test_slm.dataset.dedupe import deduplicate_dataset_manifest


def _example(example_id: str, source_code: str, test_code: str) -> dict[str, object]:
    return {
        "example_id": example_id,
        "source": {"code": source_code},
        "test": {"code": test_code},
    }


class DatasetDedupeTests(unittest.TestCase):
    def test_exact_duplicates_are_removed_and_traced(self) -> None:
        manifest = {
            "example_count": 2,
            "examples": [
                _example("one", "export const sum = () => 1;", "it('works', () => expect(sum()).toBe(1));"),
                _example("two", "export const sum = () => 1;", "it('works', () => expect(sum()).toBe(1));"),
            ],
        }
        deduped = deduplicate_dataset_manifest(manifest)
        self.assertEqual(deduped["example_count"], 1)
        self.assertEqual(deduped["rejected_examples"][0]["reason"], "duplicate_example")
        self.assertEqual(deduped["rejected_examples"][0]["matched_example_id"], "one")

    def test_near_duplicates_are_removed_and_traced(self) -> None:
        manifest = {
            "example_count": 2,
            "examples": [
                _example(
                    "one",
                    "export const sum = (a: number, b: number) => a + b;",
                    "it('adds numbers', () => expect(sum(1, 2)).toBe(3));",
                ),
                _example(
                    "two",
                    "export const sum = (left: number, right: number) => left + right;",
                    "it('adds numbers', () => expect(sum(1, 2)).toBe(3));",
                ),
            ],
        }
        deduped = deduplicate_dataset_manifest(manifest, near_duplicate_threshold=0.8)
        self.assertEqual(deduped["example_count"], 1)
        self.assertEqual(
            deduped["rejected_examples"][0]["reason"], "near_duplicate_example"
        )
        self.assertGreaterEqual(deduped["rejected_examples"][0]["similarity"], 0.8)


if __name__ == "__main__":
    unittest.main()
