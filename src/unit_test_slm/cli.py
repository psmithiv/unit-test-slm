"""Command-line entrypoints for the Unit Test SLM pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from unit_test_slm.acquisition.discovery import (
    compare_repository_manifests,
    run_discovery,
)
from unit_test_slm.acquisition.scraper import scrape_repository


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

    scrape_parser = subparsers.add_parser(
        "scrape-repo", help="Extract raw source/test pairs from a checked-out repository"
    )
    scrape_parser.add_argument("--repo-root", type=Path, required=True)
    scrape_parser.add_argument("--repository-name", required=True)
    scrape_parser.add_argument("--repository-url", required=True)
    scrape_parser.add_argument("--revision", required=True)
    scrape_parser.add_argument("--output", type=Path, required=True)

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

    if args.command == "scrape-repo":
        manifest = scrape_repository(
            args.repo_root,
            repository_name=args.repository_name,
            repository_url=args.repository_url,
            revision=args.revision,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return 0

    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
