"""Repository scraper for raw TypeScript source and Jest test pairs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


TEST_SUFFIXES = (".test.ts", ".spec.ts", ".test.tsx", ".spec.tsx")
SOURCE_SUFFIXES = (".ts", ".tsx")
EXCLUDED_DIRECTORIES = {"node_modules", "dist", "build", ".git"}


@dataclass(frozen=True)
class SourceTestPair:
    source_path: str
    test_paths: list[str]


def is_test_file(path: Path) -> bool:
    return path.name.endswith(TEST_SUFFIXES)


def is_source_file(path: Path) -> bool:
    return path.suffix in SOURCE_SUFFIXES and not is_test_file(path) and not path.name.endswith(".d.ts")


def iter_repository_files(repo_root: Path) -> list[Path]:
    paths: list[Path] = []
    for path in repo_root.rglob("*"):
        if any(part in EXCLUDED_DIRECTORIES for part in path.parts):
            continue
        if path.is_file():
            paths.append(path)
    return paths


def discover_source_files(repo_root: Path) -> list[Path]:
    return sorted(
        [path for path in iter_repository_files(repo_root) if is_source_file(path)],
        key=lambda path: str(path.relative_to(repo_root)).lower(),
    )


def discover_test_files(repo_root: Path) -> list[Path]:
    return sorted(
        [path for path in iter_repository_files(repo_root) if is_test_file(path)],
        key=lambda path: str(path.relative_to(repo_root)).lower(),
    )


def _source_stem(path: Path) -> str:
    return path.name.rsplit(".", maxsplit=1)[0]


def _test_stem(path: Path) -> str:
    stem = path.name
    for suffix in TEST_SUFFIXES:
        if stem.endswith(suffix):
            return stem[: -len(suffix)]
    return path.stem


def rank_candidate_tests(source: Path, tests: list[Path], repo_root: Path) -> list[Path]:
    source_stem = _source_stem(source)
    source_parent = source.parent.name
    scored: list[tuple[int, str, Path]] = []

    for test in tests:
        score = 0
        if _test_stem(test) == source_stem:
            score += 100
        if source_parent and source_parent in test.parts:
            score += 10
        if source_stem in test.stem:
            score += 5
        scored.append((score, str(test.relative_to(repo_root)).lower(), test))

    return [path for score, _, path in sorted(scored, key=lambda item: (-item[0], item[1])) if score > 0]


def pair_sources_with_tests(repo_root: Path) -> list[SourceTestPair]:
    sources = discover_source_files(repo_root)
    tests = discover_test_files(repo_root)
    pairs: list[SourceTestPair] = []

    for source in sources:
        ranked_tests = rank_candidate_tests(source, tests, repo_root)
        if not ranked_tests:
            continue
        pairs.append(
            SourceTestPair(
                source_path=str(source.relative_to(repo_root)),
                test_paths=[str(test.relative_to(repo_root)) for test in ranked_tests[:3]],
            )
        )

    return pairs


def scrape_repository(
    repo_root: Path,
    *,
    repository_name: str,
    repository_url: str,
    revision: str,
    license_spdx_id: str | None = None,
) -> dict[str, object]:
    repo_root = repo_root.resolve()
    pairs = pair_sources_with_tests(repo_root)
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "repository": {
            "name": repository_name,
            "url": repository_url,
            "revision": revision,
            "license_spdx_id": license_spdx_id,
            "root": str(repo_root),
        },
        "pair_count": len(pairs),
        "pairs": [
            {
                "source_path": pair.source_path,
                "test_paths": pair.test_paths,
                "provenance": {
                    "repository_name": repository_name,
                    "repository_url": repository_url,
                    "revision": revision,
                    "license_spdx_id": license_spdx_id,
                    "source_path": pair.source_path,
                    "test_paths": pair.test_paths,
                },
            }
            for pair in pairs
        ],
    }
