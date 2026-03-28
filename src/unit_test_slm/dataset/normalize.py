"""Deterministic normalization for TypeScript and Jest examples."""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any


NORMALIZATION_RULES = [
    "normalize_line_endings",
    "replace_tabs_with_two_spaces",
    "strip_trailing_whitespace",
    "collapse_excess_blank_lines",
    "ensure_terminal_newline",
    "rename_test_blocks_to_it",
    "normalize_describe_and_it_quotes",
]


def _normalize_common(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized = normalized.replace("\t", "  ")
    normalized = "\n".join(line.rstrip() for line in normalized.split("\n"))
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.rstrip("\n") + "\n"


def _normalize_quote_blocks(text: str) -> str:
    pattern = re.compile(r"\b(describe|it)\(\"([^\"]+)\"")
    return pattern.sub(lambda match: f"{match.group(1)}('{match.group(2)}'", text)


def normalize_typescript_source(text: str) -> str:
    return _normalize_common(text)


def normalize_jest_test(text: str) -> str:
    normalized = _normalize_common(text)
    normalized = re.sub(r"\btest\(", "it(", normalized)
    normalized = _normalize_quote_blocks(normalized)
    return normalized


def normalize_example(example: dict[str, Any]) -> dict[str, Any]:
    normalized = deepcopy(example)
    normalized["source"]["code"] = normalize_typescript_source(
        normalized["source"]["code"]
    )
    normalized["test"]["code"] = normalize_jest_test(normalized["test"]["code"])
    normalized["normalization"] = {
        "version": "1.0.0",
        "deterministic": True,
        "rules": NORMALIZATION_RULES,
    }
    return normalized


def normalize_dataset_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    normalized = deepcopy(manifest)
    normalized["examples"] = [
        normalize_example(example) for example in manifest.get("examples", [])
    ]
    normalized["example_count"] = len(normalized["examples"])
    normalized["normalization_version"] = "1.0.0"
    return normalized
