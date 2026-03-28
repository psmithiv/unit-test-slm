"""Baseline inference harness for candidate small models."""

from __future__ import annotations

import hashlib
import subprocess
from datetime import UTC, datetime
from typing import Any


def _mock_inference(model_id: str, prompt: str) -> str:
    digest = hashlib.sha256(f"{model_id}:{prompt}".encode("utf-8")).hexdigest()[:12]
    return f"mock::{model_id}::{digest}"


def run_prompt_inference(
    *,
    model_id: str,
    prompt: str,
    backend: str = "mock",
    command: list[str] | None = None,
) -> str:
    if backend == "mock":
        return _mock_inference(model_id, prompt)

    if backend == "subprocess":
        if not command:
            raise ValueError("subprocess backend requires a command")
        result = subprocess.run(
            command,
            input=prompt,
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout.strip()

    raise ValueError(f"unsupported backend: {backend}")


def run_baseline_inference(
    prompt_manifest: dict[str, Any],
    *,
    model_id: str,
    backend: str = "mock",
    command: list[str] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    results = []
    for prompt in prompt_manifest.get("prompts", []):
        output = run_prompt_inference(
            model_id=model_id,
            prompt=prompt["prompt"],
            backend=backend,
            command=command,
        )
        results.append(
            {
                "example_id": prompt["example_id"],
                "mode": prompt.get("mode", "direct"),
                "prompt": prompt["prompt"],
                "output": output,
            }
        )

    return {
        "schema_version": "1.0.0",
        "generated_at": generated_at or datetime.now(UTC).isoformat(),
        "model_id": model_id,
        "backend": backend,
        "prompt_manifest_version": prompt_manifest.get("prompt_manifest_version", "v1"),
        "result_count": len(results),
        "results": results,
    }
