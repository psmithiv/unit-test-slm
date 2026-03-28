"""Artifact versioning helpers for training outputs."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def register_training_artifacts(
    training_plan: dict[str, Any],
    *,
    artifact_files: list[str],
    metrics: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    output_dir = Path(training_plan["output_dir"])
    artifacts = []
    for artifact_file in artifact_files:
        artifact_path = output_dir / artifact_file
        artifacts.append(
            {
                "artifact_type": "adapter" if artifact_path.suffix in {".safetensors", ".bin"} else "metadata",
                "path": str(artifact_path),
                "relative_path": artifact_file,
            }
        )

    return {
        "schema_version": "1.0.0",
        "generated_at": generated_at or datetime.now(UTC).isoformat(),
        "model_id": training_plan["model_id"],
        "dataset_version": training_plan["dataset_version"],
        "training_config_id": training_plan["training_config_id"],
        "run_id": training_plan["run_id"],
        "output_dir": training_plan["output_dir"],
        "artifacts": artifacts,
        "metrics": metrics or {},
    }
