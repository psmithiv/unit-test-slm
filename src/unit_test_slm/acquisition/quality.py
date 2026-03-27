"""Quality scoring and filtering for discovery manifests."""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from typing import Any


TOPIC_ALIASES = {
    "framework": {"jest"},
    "language": {"typescript", "ts"},
}


def _parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized).astimezone(UTC)


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _score_stars(repository: dict[str, Any], criteria: dict[str, Any]) -> dict[str, Any]:
    minimum = criteria["quality_preferences"]["minimum_stars"]
    observed = repository.get("stargazers_count", 0)
    target = max(minimum * 4, 1)
    normalized = _clamp(observed / target)
    return {
        "observed": observed,
        "target": target,
        "normalized": normalized,
    }


def _score_forks(repository: dict[str, Any], criteria: dict[str, Any]) -> dict[str, Any]:
    minimum = criteria["quality_preferences"].get("minimum_forks", 0)
    observed = repository.get("forks_count", 0)
    target = max(minimum * 5, 1)
    normalized = _clamp(observed / target)
    return {
        "observed": observed,
        "target": target,
        "normalized": normalized,
    }


def _score_recency(repository: dict[str, Any], criteria: dict[str, Any], generated_at: str) -> dict[str, Any]:
    threshold_days = criteria["quality_preferences"]["prefer_recent_push_within_days"]
    generated = _parse_timestamp(generated_at)
    pushed_at = _parse_timestamp(repository.get("pushed_at"))
    if generated is None or pushed_at is None:
        return {
            "observed_days_since_push": None,
            "threshold_days": threshold_days,
            "normalized": 0.0,
        }

    age_days = max((generated - pushed_at).days, 0)
    if age_days <= threshold_days:
        normalized = 1.0
    else:
        overflow = age_days - threshold_days
        normalized = _clamp(1.0 - (overflow / max(threshold_days, 1)))

    return {
        "observed_days_since_push": age_days,
        "threshold_days": threshold_days,
        "normalized": normalized,
    }


def _score_topic_alignment(repository: dict[str, Any]) -> dict[str, Any]:
    topics = {topic.lower() for topic in repository.get("topics", [])}
    required = TOPIC_ALIASES["framework"] | TOPIC_ALIASES["language"]
    matched = sorted(required & topics)
    normalized = _clamp(len(matched) / max(len(required), 1))
    return {
        "observed_topics": sorted(topics),
        "matched_topics": matched,
        "required_topics": sorted(required),
        "normalized": normalized,
    }


def score_repository(
    repository: dict[str, Any], criteria: dict[str, Any], *, generated_at: str
) -> dict[str, Any]:
    weights = criteria["quality_preferences"]["scoring"]["weights"]
    signals = {
        "stars": _score_stars(repository, criteria),
        "forks": _score_forks(repository, criteria),
        "recency": _score_recency(repository, criteria, generated_at),
        "topic_alignment": _score_topic_alignment(repository),
    }
    score = sum(weights[name] * signals[name]["normalized"] for name in weights)
    threshold = criteria["quality_preferences"]["scoring"]["minimum_score"]
    accepted = score >= threshold
    reasons = [] if accepted else ["quality_score_below_threshold"]
    return {
        "score": round(score, 4),
        "threshold": threshold,
        "accepted": accepted,
        "weights": weights,
        "signals": signals,
        "reasons": reasons,
    }


def apply_quality_filter(
    manifest: dict[str, Any], criteria: dict[str, Any]
) -> dict[str, Any]:
    filtered = deepcopy(manifest)
    generated_at = manifest.get("generated_at") or datetime.now(UTC).isoformat()
    accepted = []
    rejected = list(filtered.get("rejected_repositories", []))

    for repository in manifest.get("repositories", []):
        scored_repository = deepcopy(repository)
        scored_repository["quality"] = score_repository(
            repository, criteria, generated_at=generated_at
        )
        if scored_repository["quality"]["accepted"]:
            accepted.append(scored_repository)
            continue
        rejected.append(
            {
                "full_name": scored_repository.get("full_name"),
                "reason": "quality_score_below_threshold",
                "quality": scored_repository["quality"],
            }
        )

    filtered["repositories"] = accepted
    filtered["rejected_repositories"] = rejected
    filtered["repository_count"] = len(accepted)
    filtered["quality_threshold"] = criteria["quality_preferences"]["scoring"][
        "minimum_score"
    ]
    return filtered
