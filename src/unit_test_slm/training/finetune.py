"""Adapter-based fine-tuning plan generation for MLX workflows."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def training_config_id(config: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(config).encode("utf-8")).hexdigest()[:12]


def _safe_segment(value: str) -> str:
    return value.replace("/", "__")


def build_adapter_training_plan(
    config: dict[str, Any],
    *,
    dataset_version: str,
    output_root: Path,
    generated_at: str | None = None,
) -> dict[str, Any]:
    config_id = training_config_id(config)
    run_seed = str(config["seed"])
    run_id = hashlib.sha256(
        f"{config['model_id']}:{dataset_version}:{config_id}:{run_seed}".encode("utf-8")
    ).hexdigest()[:12]
    output_dir = (
        output_root
        / _safe_segment(config["model_id"])
        / dataset_version
        / config_id
        / run_id
    )

    command = [
        "python3",
        "-m",
        "mlx_lm.lora",
        "--model",
        config["model_id"],
        "--train",
        "--data",
        config["train_data_path"],
        "--batch-size",
        str(config["batch_size"]),
        "--learning-rate",
        str(config["learning_rate"]),
        "--iters",
        str(config["iterations"]),
        "--adapter-path",
        str(output_dir / "adapters"),
    ]

    return {
        "schema_version": "1.0.0",
        "generated_at": generated_at or datetime.now(UTC).isoformat(),
        "model_id": config["model_id"],
        "dataset_version": dataset_version,
        "adapter_strategy": config["adapter_strategy"],
        "training_config_id": config_id,
        "run_id": run_id,
        "seed": config["seed"],
        "output_dir": str(output_dir),
        "command": command,
        "config": config,
    }
