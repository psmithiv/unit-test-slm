"""Reproducible split assignment for dataset manifests."""

from __future__ import annotations

import hashlib
from copy import deepcopy
from typing import Any


def assign_split(example_id: str, split_version: str) -> str:
    digest = hashlib.sha256(f"{split_version}:{example_id}".encode("utf-8")).hexdigest()
    bucket = int(digest[:8], 16) % 100
    if bucket < 80:
        return "train"
    if bucket < 90:
        return "validation"
    return "held_out"


def freeze_benchmark_splits(
    manifest: dict[str, Any], *, split_version: str = "v1"
) -> dict[str, Any]:
    frozen = deepcopy(manifest)
    counts = {"train": 0, "validation": 0, "held_out": 0}
    held_out_ids: list[str] = []

    for example in frozen.get("examples", []):
        split = assign_split(example["example_id"], split_version)
        example["split"] = split
        counts[split] += 1
        if split == "held_out":
            held_out_ids.append(example["example_id"])

    frozen["split_version"] = split_version
    frozen["split_counts"] = counts
    frozen["benchmark"] = {
        "version": split_version,
        "held_out_example_ids": sorted(held_out_ids),
    }
    return frozen
