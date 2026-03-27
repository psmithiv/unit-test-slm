from __future__ import annotations

import json
import unittest
from pathlib import Path

from unit_test_slm.acquisition.governance import enforce_license_policy, license_allowed
from unit_test_slm.acquisition.discovery import build_discovery_manifest, load_criteria


FIXTURE_DIR = Path(__file__).resolve().parent.parent / "fixtures"


class GovernanceTests(unittest.TestCase):
    def test_license_allowed_follows_allowlist(self) -> None:
        criteria = load_criteria(Path("config/repository_selection_criteria.json"))
        self.assertTrue(license_allowed(criteria, "MIT"))
        self.assertFalse(license_allowed(criteria, None))
        self.assertFalse(license_allowed(criteria, "GPL-3.0"))

    def test_enforce_license_policy_rejects_blocked_repositories(self) -> None:
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
                        "full_name": "acme/gpl-jest-lib",
                        "html_url": "https://github.com/acme/gpl-jest-lib",
                        "default_branch": "main",
                        "stargazers_count": 7,
                        "forks_count": 1,
                        "language": "TypeScript",
                        "license": {"spdx_id": "GPL-3.0"},
                        "topics": ["jest", "typescript"],
                        "updated_at": "2026-03-20T08:00:00Z",
                        "pushed_at": "2026-03-21T08:00:00Z",
                        "archived": False
                    }
                ],
            },
            generated_at="2026-03-27T00:00:00+00:00",
        )
        filtered = enforce_license_policy(manifest, criteria)
        self.assertEqual(len(filtered["repositories"]), 1)
        self.assertEqual(filtered["rejected_repositories"][0]["full_name"], "acme/gpl-jest-lib")


if __name__ == "__main__":
    unittest.main()
