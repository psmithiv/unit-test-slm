"""Stable dataset manifest helpers for curated training examples."""

from __future__ import annotations

import hashlib
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0.0"


def _stable_example_id(
    repository_name: str, revision: str, source_path: str, test_path: str
) -> str:
    payload = "::".join((repository_name, revision, source_path, test_path))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _required_fields_present(example: dict[str, Any]) -> bool:
    return all(
        (
            example.get("example_id"),
            example.get("split"),
            (example.get("repository") or {}).get("name"),
            (example.get("source") or {}).get("path"),
            (example.get("test") or {}).get("path"),
        )
    )


def build_dataset_manifest(
    raw_manifest: dict[str, Any], *, generated_at: str | None = None
) -> dict[str, Any]:
    repository = deepcopy(raw_manifest["repository"])
    repo_root = Path(repository["root"])
    examples: list[dict[str, Any]] = []

    for pair in raw_manifest.get("pairs", []):
        source_path = pair["source_path"]
        source_code = (repo_root / source_path).read_text(encoding="utf-8")
        ranked_test_paths = pair.get("test_paths", [])
        if not ranked_test_paths:
            continue

        test_path = ranked_test_paths[0]
        test_code = (repo_root / test_path).read_text(encoding="utf-8")
        examples.append(
            {
                "example_id": _stable_example_id(
                    repository["name"], repository["revision"], source_path, test_path
                ),
                "split": "unassigned",
                "repository": {
                    "name": repository["name"],
                    "url": repository["url"],
                    "revision": repository["revision"],
                    "license_spdx_id": repository.get("license_spdx_id"),
                },
                "source": {
                    "path": source_path,
                    "language": "TypeScript",
                    "code": source_code,
                },
                "test": {
                    "path": test_path,
                    "framework": "Jest",
                    "code": test_code,
                },
                "provenance": deepcopy(pair.get("provenance", {})),
            }
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at or datetime.now(UTC).isoformat(),
        "example_count": len(examples),
        "examples": examples,
    }


def validate_dataset_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append("invalid_schema_version")

    examples = manifest.get("examples")
    if not isinstance(examples, list):
        errors.append("examples_must_be_a_list")
        return errors

    for index, example in enumerate(examples):
        if not _required_fields_present(example):
            errors.append(f"example_{index}_missing_required_fields")

    if manifest.get("example_count") != len(examples):
        errors.append("example_count_mismatch")

    return errors
