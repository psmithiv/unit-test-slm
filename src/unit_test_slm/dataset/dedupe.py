"""Duplicate and near-duplicate filtering for dataset manifests."""

from __future__ import annotations

import hashlib
from copy import deepcopy
from difflib import SequenceMatcher
from typing import Any


def _example_payload(example: dict[str, Any]) -> str:
    return "\n".join(
        (
            example["source"]["code"].strip(),
            example["test"]["code"].strip(),
        )
    )


def exact_duplicate_signature(example: dict[str, Any]) -> str:
    payload = _example_payload(example)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def similarity_score(left: dict[str, Any], right: dict[str, Any]) -> float:
    return SequenceMatcher(None, _example_payload(left), _example_payload(right)).ratio()


def deduplicate_dataset_manifest(
    manifest: dict[str, Any], *, near_duplicate_threshold: float = 0.97
) -> dict[str, Any]:
    filtered = deepcopy(manifest)
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    signatures: dict[str, str] = {}

    for example in manifest.get("examples", []):
        signature = exact_duplicate_signature(example)
        if signature in signatures:
            rejected.append(
                {
                    "example_id": example["example_id"],
                    "reason": "duplicate_example",
                    "matched_example_id": signatures[signature],
                    "similarity": 1.0,
                }
            )
            continue

        near_match = None
        near_similarity = 0.0
        for accepted_example in accepted:
            score = similarity_score(example, accepted_example)
            if score >= near_duplicate_threshold and score > near_similarity:
                near_match = accepted_example
                near_similarity = score

        if near_match is not None:
            rejected.append(
                {
                    "example_id": example["example_id"],
                    "reason": "near_duplicate_example",
                    "matched_example_id": near_match["example_id"],
                    "similarity": round(near_similarity, 4),
                }
            )
            continue

        signatures[signature] = example["example_id"]
        accepted.append(deepcopy(example))

    filtered["examples"] = accepted
    filtered["example_count"] = len(accepted)
    filtered["rejected_examples"] = rejected
    filtered["dedupe"] = {
        "near_duplicate_threshold": near_duplicate_threshold,
        "rejected_count": len(rejected),
    }
    return filtered
