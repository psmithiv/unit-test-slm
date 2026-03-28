from __future__ import annotations

import unittest

from unit_test_slm.dataset.normalize import normalize_dataset_manifest, normalize_jest_test


class DatasetNormalizationTests(unittest.TestCase):
    def test_normalize_jest_test_is_deterministic(self) -> None:
        raw = 'describe("math", () => {\r\n\ttest("adds", () => {  \r\n\t\texpect(sum(1, 2)).toBe(3)\r\n\t})\r\n\r\n\r\n})'
        normalized = normalize_jest_test(raw)
        self.assertEqual(
            normalized,
            "describe('math', () => {\n"
            "  it('adds', () => {\n"
            "    expect(sum(1, 2)).toBe(3)\n"
            "  })\n"
            "\n"
            "})\n",
        )

    def test_normalize_dataset_manifest_adds_metadata(self) -> None:
        manifest = {
            "schema_version": "1.0.0",
            "example_count": 1,
            "examples": [
                {
                    "example_id": "abc",
                    "split": "unassigned",
                    "repository": {"name": "acme/repo"},
                    "source": {"path": "src/a.ts", "code": "export const a = 1;\r\n"},
                    "test": {"path": "tests/a.test.ts", "code": 'test("a", () => {\r\n\t})\r\n'},
                }
            ],
        }
        normalized = normalize_dataset_manifest(manifest)
        self.assertEqual(normalized["normalization_version"], "1.0.0")
        self.assertTrue(normalized["examples"][0]["normalization"]["deterministic"])
        self.assertIn("rename_test_blocks_to_it", normalized["examples"][0]["normalization"]["rules"])
        self.assertEqual(normalized["examples"][0]["test"]["code"], "it('a', () => {\n  })\n")


if __name__ == "__main__":
    unittest.main()
