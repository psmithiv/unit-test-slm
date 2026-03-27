from __future__ import annotations

import unittest
from pathlib import Path

from unit_test_slm.acquisition.scraper import pair_sources_with_tests, scrape_repository


FIXTURE_REPO = Path(__file__).resolve().parent.parent / "fixtures" / "sample_repo"


class SourceTestPairScraperTests(unittest.TestCase):
    def test_pair_sources_with_tests_finds_expected_matches(self) -> None:
        pairs = pair_sources_with_tests(FIXTURE_REPO)
        pair_map = {pair.source_path: pair.test_paths for pair in pairs}
        self.assertIn("src/math.ts", pair_map)
        self.assertIn("src/format.ts", pair_map)
        self.assertEqual(pair_map["src/math.ts"][0], "src/__tests__/math.test.ts")
        self.assertEqual(pair_map["src/format.ts"][0], "tests/format.spec.ts")

    def test_scrape_repository_preserves_provenance(self) -> None:
        manifest = scrape_repository(
            FIXTURE_REPO,
            repository_name="acme/sample-repo",
            repository_url="https://github.com/acme/sample-repo",
            revision="abc123",
            license_spdx_id="MIT",
        )
        self.assertEqual(manifest["repository"]["name"], "acme/sample-repo")
        self.assertEqual(manifest["pair_count"], 2)
        self.assertEqual(manifest["pairs"][0]["provenance"]["revision"], "abc123")
        self.assertEqual(manifest["pairs"][0]["provenance"]["license_spdx_id"], "MIT")


if __name__ == "__main__":
    unittest.main()
