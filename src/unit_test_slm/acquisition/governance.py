"""License policy and provenance helpers for acquisition manifests."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


def license_allowed(criteria: dict[str, Any], spdx_id: str | None) -> bool:
    policy = criteria["license_policy"]
    if not spdx_id:
        return not policy.get("deny_missing_license", False)
    return spdx_id in policy["allowlist"]


def enforce_license_policy(
    manifest: dict[str, Any], criteria: dict[str, Any]
) -> dict[str, Any]:
    filtered = deepcopy(manifest)
    accepted = []
    rejected = []
    for repository in manifest.get("repositories", []):
        spdx_id = repository.get("license_spdx_id")
        if license_allowed(criteria, spdx_id):
            accepted.append(repository)
        else:
            rejected.append(
                {
                    "full_name": repository.get("full_name"),
                    "license_spdx_id": spdx_id,
                    "reason": "blocked_or_missing_license",
                }
            )

    filtered["repositories"] = accepted
    filtered["rejected_repositories"] = rejected
    filtered["repository_count"] = len(accepted)
    return filtered
