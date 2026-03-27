"""GitHub repository discovery workflow for TypeScript/Jest candidates."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RepositoryCandidate:
    full_name: str
    html_url: str
    default_branch: str | None
    stargazers_count: int
    forks_count: int
    language: str | None
    license_spdx_id: str | None
    topics: list[str]
    updated_at: str | None
    pushed_at: str | None


def load_criteria(criteria_path: Path) -> dict[str, Any]:
    return json.loads(criteria_path.read_text(encoding="utf-8"))


def build_repository_queries(criteria: dict[str, Any]) -> list[str]:
    minimum_stars = criteria["quality_preferences"]["minimum_stars"]
    framework = criteria["target_pair"]["framework"]
    language = criteria["target_pair"]["language"]
    dependency_markers = criteria["required_signals"]["dependency_markers"]

    queries = []
    for marker in dependency_markers:
        queries.append(
            f"{framework} {marker} language:{language} stars:>={minimum_stars} archived:false"
        )
    return list(dict.fromkeys(queries))


def _normalize_repository_item(
    item: dict[str, Any], captured_fields: list[str]
) -> RepositoryCandidate | None:
    if item.get("archived"):
        return None
    if item.get("language") != "TypeScript":
        return None

    normalized = {
        "full_name": item.get("full_name"),
        "html_url": item.get("html_url"),
        "default_branch": item.get("default_branch"),
        "stargazers_count": item.get("stargazers_count", 0),
        "forks_count": item.get("forks_count", 0),
        "language": item.get("language"),
        "license_spdx_id": (item.get("license") or {}).get("spdx_id"),
        "topics": item.get("topics") or [],
        "updated_at": item.get("updated_at"),
        "pushed_at": item.get("pushed_at"),
    }

    missing = [field for field in captured_fields if field.startswith("license.") and not normalized["license_spdx_id"]]
    if missing:
        return None

    return RepositoryCandidate(**normalized)


def extract_repository_candidates(
    search_response: dict[str, Any], criteria: dict[str, Any]
) -> list[RepositoryCandidate]:
    captured_fields = criteria["captured_metadata_fields"]
    candidates: list[RepositoryCandidate] = []
    for item in search_response.get("items", []):
        candidate = _normalize_repository_item(item, captured_fields)
        if candidate is not None:
            candidates.append(candidate)
    return sorted(candidates, key=lambda candidate: candidate.full_name.lower())


def build_discovery_manifest(
    criteria: dict[str, Any],
    query: str,
    search_response: dict[str, Any],
    *,
    source: str = "github-search-api",
    generated_at: str | None = None,
) -> dict[str, Any]:
    repositories = [candidate.__dict__ for candidate in extract_repository_candidates(search_response, criteria)]
    return {
        "source": source,
        "generated_at": generated_at or datetime.now(UTC).isoformat(),
        "criteria_version": criteria["version"],
        "target_pair": criteria["target_pair"],
        "query": query,
        "total_count": search_response.get("total_count", 0),
        "captured_fields": criteria["captured_metadata_fields"],
        "repositories": repositories,
    }


def compare_repository_manifests(
    baseline: dict[str, Any], candidate: dict[str, Any]
) -> dict[str, Any]:
    baseline_names = {repo["full_name"] for repo in baseline.get("repositories", [])}
    candidate_names = {repo["full_name"] for repo in candidate.get("repositories", [])}
    return {
        "baseline_count": len(baseline_names),
        "candidate_count": len(candidate_names),
        "added": sorted(candidate_names - baseline_names),
        "removed": sorted(baseline_names - candidate_names),
        "unchanged": sorted(baseline_names & candidate_names),
    }


def run_github_search(query: str, *, per_page: int = 20) -> dict[str, Any]:
    command = [
        "gh",
        "api",
        "/search/repositories",
        "-f",
        f"q={query}",
        "-f",
        f"per_page={per_page}",
    ]
    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def run_discovery(
    criteria_path: Path,
    output_path: Path,
    *,
    per_page: int = 20,
) -> dict[str, Any]:
    criteria = load_criteria(criteria_path)
    query = build_repository_queries(criteria)[0]
    search_response = run_github_search(query, per_page=per_page)
    manifest = build_discovery_manifest(criteria, query, search_response)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return manifest
