from __future__ import annotations

import json
import unittest
from pathlib import Path

from unit_test_slm.acquisition.discovery import build_discovery_manifest, load_criteria
from unit_test_slm.acquisition.quality import apply_quality_filter, score_repository


FIXTURE_DIR = Path(__file__).resolve().parent.parent / "fixtures"


class QualityScoringTests(unittest.TestCase):
    def test_score_repository_exposes_breakdown(self) -> None:
        criteria = load_criteria(Path("config/repository_selection_criteria.json"))
        repository = {
            "full_name": "acme/ts-jest-utils",
            "stargazers_count": 42,
            "forks_count": 5,
            "topics": ["jest", "typescript", "testing"],
            "pushed_at": "2026-03-21T08:00:00Z",
        }
        score = score_repository(
            repository,
            criteria,
            generated_at="2026-03-27T00:00:00+00:00",
        )
        self.assertTrue(score["accepted"])
        self.assertIn("stars", score["signals"])
        self.assertGreater(score["score"], score["threshold"])

    def test_apply_quality_filter_rejects_low_value_repositories(self) -> None:
        criteria = load_criteria(Path("config/repository_selection_criteria.json"))
        search_response = json.loads(
            (FIXTURE_DIR / "github_search_response.json").read_text(encoding="utf-8")
        )
        manifest = build_discovery_manifest(
            criteria,
            "jest language:TypeScript stars:>=5 archived:false",
            {
                "total_count": 2,
                "items": search_response["items"]
                + [
                    {
                        "full_name": "acme/stale-low-signal",
                        "html_url": "https://github.com/acme/stale-low-signal",
                        "default_branch": "main",
                        "stargazers_count": 5,
                        "forks_count": 0,
                        "language": "TypeScript",
                        "license": {"spdx_id": "MIT"},
                        "topics": ["typescript"],
                        "updated_at": "2022-01-10T08:00:00Z",
                        "pushed_at": "2022-01-11T08:00:00Z",
                        "archived": False
                    }
                ],
            },
            generated_at="2026-03-27T00:00:00+00:00",
        )
        filtered = apply_quality_filter(manifest, criteria)
        self.assertEqual([repo["full_name"] for repo in filtered["repositories"]], ["acme/ts-jest-utils"])
        self.assertEqual(
            filtered["rejected_repositories"][-1]["full_name"],
            "acme/stale-low-signal",
        )
        self.assertEqual(
            filtered["rejected_repositories"][-1]["reason"],
            "quality_score_below_threshold",
        )


if __name__ == "__main__":
    unittest.main()
