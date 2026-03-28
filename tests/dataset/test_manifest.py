from __future__ import annotations

import unittest
from pathlib import Path

from unit_test_slm.acquisition.scraper import scrape_repository
from unit_test_slm.dataset.manifest import (
    SCHEMA_VERSION,
    build_dataset_manifest,
    validate_dataset_manifest,
)


FIXTURE_REPO = Path(__file__).resolve().parent.parent / "fixtures" / "sample_repo"


class DatasetManifestTests(unittest.TestCase):
    def test_build_dataset_manifest_creates_examples_with_split_assignment(self) -> None:
        raw_manifest = scrape_repository(
            FIXTURE_REPO,
            repository_name="acme/sample-repo",
            repository_url="https://github.com/acme/sample-repo",
            revision="abc123",
            license_spdx_id="MIT",
        )
        dataset_manifest = build_dataset_manifest(
            raw_manifest, generated_at="2026-03-27T00:00:00+00:00"
        )

        self.assertEqual(dataset_manifest["schema_version"], SCHEMA_VERSION)
        self.assertEqual(dataset_manifest["example_count"], 2)
        self.assertEqual(dataset_manifest["examples"][0]["split"], "unassigned")
        self.assertEqual(
            dataset_manifest["examples"][0]["repository"]["license_spdx_id"], "MIT"
        )
        self.assertTrue(dataset_manifest["examples"][0]["source"]["code"].startswith("export"))

    def test_validate_dataset_manifest_requires_required_fields(self) -> None:
        errors = validate_dataset_manifest(
            {
                "schema_version": SCHEMA_VERSION,
                "example_count": 1,
                "examples": [{"split": "train"}],
            }
        )
        self.assertIn("example_0_missing_required_fields", errors)


if __name__ == "__main__":
    unittest.main()
