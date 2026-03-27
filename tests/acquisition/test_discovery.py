from __future__ import annotations

import json
import unittest
from pathlib import Path

from unit_test_slm.acquisition.discovery import (
    build_discovery_manifest,
    build_repository_queries,
    compare_repository_manifests,
    extract_repository_candidates,
    load_criteria,
)


FIXTURE_DIR = Path(__file__).resolve().parent.parent / "fixtures"


class DiscoveryWorkflowTests(unittest.TestCase):
    def test_build_repository_queries_uses_target_pair_and_thresholds(self) -> None:
        criteria = load_criteria(
            Path("config/repository_selection_criteria.json")
        )
        queries = build_repository_queries(criteria)
        self.assertTrue(queries)
        self.assertTrue(all("language:TypeScript" in query for query in queries))
        self.assertTrue(all("stars:>=5" in query for query in queries))

    def test_extract_repository_candidates_filters_non_typescript_and_archived(self) -> None:
        criteria = load_criteria(
            Path("config/repository_selection_criteria.json")
        )
        search_response = json.loads(
            (FIXTURE_DIR / "github_search_response.json").read_text(encoding="utf-8")
        )
        candidates = extract_repository_candidates(search_response, criteria)
        self.assertEqual([candidate.full_name for candidate in candidates], ["acme/ts-jest-utils"])

    def test_build_manifest_and_compare_are_deterministic(self) -> None:
        criteria = load_criteria(
            Path("config/repository_selection_criteria.json")
        )
        search_response = json.loads(
            (FIXTURE_DIR / "github_search_response.json").read_text(encoding="utf-8")
        )
        baseline = build_discovery_manifest(
            criteria,
            "jest language:TypeScript stars:>=5 archived:false",
            search_response,
            generated_at="2026-03-27T00:00:00+00:00",
        )
        candidate = {
            **baseline,
            "repositories": baseline["repositories"]
            + [
                {
                    "full_name": "acme/another-jest-lib",
                    "html_url": "https://github.com/acme/another-jest-lib",
                    "default_branch": "main",
                    "stargazers_count": 8,
                    "forks_count": 1,
                    "language": "TypeScript",
                    "license_spdx_id": "MIT",
                    "topics": ["jest", "typescript"],
                    "updated_at": "2026-03-10T10:00:00Z",
                    "pushed_at": "2026-03-12T10:00:00Z"
                }
            ],
        }
        comparison = compare_repository_manifests(baseline, candidate)
        self.assertEqual(comparison["added"], ["acme/another-jest-lib"])
        self.assertEqual(comparison["removed"], [])


if __name__ == "__main__":
    unittest.main()
