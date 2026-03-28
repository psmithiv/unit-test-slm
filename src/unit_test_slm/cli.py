"""Command-line entrypoints for the Unit Test SLM pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from unit_test_slm.acquisition.discovery import (
    compare_repository_manifests,
    run_discovery,
)
from unit_test_slm.acquisition.governance import enforce_license_policy
from unit_test_slm.acquisition.quality import apply_quality_filter
from unit_test_slm.acquisition.scraper import scrape_repository
from unit_test_slm.dataset.dedupe import deduplicate_dataset_manifest
from unit_test_slm.dataset.manifest import build_dataset_manifest, validate_dataset_manifest
from unit_test_slm.dataset.normalize import normalize_dataset_manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="unit-test-slm")
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover_parser = subparsers.add_parser(
        "discover", help="Discover candidate repositories from GitHub search"
    )
    discover_parser.add_argument(
        "--criteria",
        type=Path,
        default=Path("config/repository_selection_criteria.json"),
        help="Path to repository selection criteria JSON",
    )
    discover_parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Where to write the discovery manifest JSON",
    )
    discover_parser.add_argument(
        "--per-page",
        type=int,
        default=20,
        help="Number of GitHub results per query",
    )

    compare_parser = subparsers.add_parser(
        "compare-discovery", help="Compare two discovery manifest files"
    )
    compare_parser.add_argument("baseline", type=Path)
    compare_parser.add_argument("candidate", type=Path)

    license_parser = subparsers.add_parser(
        "enforce-license-policy",
        help="Filter a discovery manifest against the configured license policy",
    )
    license_parser.add_argument(
        "--criteria",
        type=Path,
        default=Path("config/repository_selection_criteria.json"),
    )
    license_parser.add_argument("--manifest", type=Path, required=True)
    license_parser.add_argument("--output", type=Path, required=True)

    quality_parser = subparsers.add_parser(
        "score-discovery",
        help="Score and filter repositories from a discovery manifest",
    )
    quality_parser.add_argument(
        "--criteria",
        type=Path,
        default=Path("config/repository_selection_criteria.json"),
    )
    quality_parser.add_argument("--manifest", type=Path, required=True)
    quality_parser.add_argument("--output", type=Path, required=True)

    scrape_parser = subparsers.add_parser(
        "scrape-repo", help="Extract raw source/test pairs from a checked-out repository"
    )
    scrape_parser.add_argument("--repo-root", type=Path, required=True)
    scrape_parser.add_argument("--repository-name", required=True)
    scrape_parser.add_argument("--repository-url", required=True)
    scrape_parser.add_argument("--revision", required=True)
    scrape_parser.add_argument("--license-spdx-id", default=None)
    scrape_parser.add_argument("--output", type=Path, required=True)

    dataset_parser = subparsers.add_parser(
        "build-dataset-manifest",
        help="Convert raw source/test pairs into the curated dataset manifest",
    )
    dataset_parser.add_argument("--raw-manifest", type=Path, required=True)
    dataset_parser.add_argument("--output", type=Path, required=True)

    normalize_parser = subparsers.add_parser(
        "normalize-dataset",
        help="Normalize curated dataset examples deterministically",
    )
    normalize_parser.add_argument("--manifest", type=Path, required=True)
    normalize_parser.add_argument("--output", type=Path, required=True)

    dedupe_parser = subparsers.add_parser(
        "dedupe-dataset",
        help="Filter exact and near-duplicate curated examples",
    )
    dedupe_parser.add_argument("--manifest", type=Path, required=True)
    dedupe_parser.add_argument("--output", type=Path, required=True)
    dedupe_parser.add_argument("--near-duplicate-threshold", type=float, default=0.97)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "discover":
        manifest = run_discovery(args.criteria, args.output, per_page=args.per_page)
        args.output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return 0

    if args.command == "compare-discovery":
        baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
        candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
        print(json.dumps(compare_repository_manifests(baseline, candidate), indent=2))
        return 0

    if args.command == "enforce-license-policy":
        criteria = json.loads(args.criteria.read_text(encoding="utf-8"))
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        filtered = enforce_license_policy(manifest, criteria)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(filtered, indent=2) + "\n", encoding="utf-8")
        return 0

    if args.command == "score-discovery":
        criteria = json.loads(args.criteria.read_text(encoding="utf-8"))
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        filtered = apply_quality_filter(manifest, criteria)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(filtered, indent=2) + "\n", encoding="utf-8")
        return 0

    if args.command == "scrape-repo":
        manifest = scrape_repository(
            args.repo_root,
            repository_name=args.repository_name,
            repository_url=args.repository_url,
            revision=args.revision,
            license_spdx_id=args.license_spdx_id,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return 0

    if args.command == "build-dataset-manifest":
        raw_manifest = json.loads(args.raw_manifest.read_text(encoding="utf-8"))
        manifest = build_dataset_manifest(raw_manifest)
        errors = validate_dataset_manifest(manifest)
        if errors:
            parser.error(f"invalid dataset manifest: {', '.join(errors)}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return 0

    if args.command == "normalize-dataset":
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        normalized = normalize_dataset_manifest(manifest)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(normalized, indent=2) + "\n", encoding="utf-8")
        return 0

    if args.command == "dedupe-dataset":
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        deduped = deduplicate_dataset_manifest(
            manifest, near_duplicate_threshold=args.near_duplicate_threshold
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(deduped, indent=2) + "\n", encoding="utf-8")
        return 0

    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
