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
from unit_test_slm.dataset.renderer import render_jest_test_spec
from unit_test_slm.dataset.splits import freeze_benchmark_splits
from unit_test_slm.dataset.test_spec import validate_test_spec
from unit_test_slm.evaluation.compile import evaluate_compile
from unit_test_slm.evaluation.jest import evaluate_jest_execution
from unit_test_slm.evaluation.reporting import build_run_report, compare_run_reports
from unit_test_slm.evaluation.robustness import evaluate_robustness
from unit_test_slm.evaluation.syntax import evaluate_syntax
from unit_test_slm.training.artifacts import register_training_artifacts
from unit_test_slm.training.baseline import run_baseline_inference
from unit_test_slm.training.compare import compare_training_paths
from unit_test_slm.training.finetune import build_adapter_training_plan


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

    spec_parser = subparsers.add_parser(
        "validate-test-spec",
        help="Validate a TEST_SPEC document against the current schema",
    )
    spec_parser.add_argument("--spec", type=Path, required=True)

    render_parser = subparsers.add_parser(
        "render-test-spec",
        help="Render a TEST_SPEC document into normalized Jest code",
    )
    render_parser.add_argument("--spec", type=Path, required=True)
    render_parser.add_argument("--output", type=Path, required=True)

    split_parser = subparsers.add_parser(
        "freeze-splits",
        help="Assign reproducible train/validation/held-out splits",
    )
    split_parser.add_argument("--manifest", type=Path, required=True)
    split_parser.add_argument("--output", type=Path, required=True)
    split_parser.add_argument("--split-version", default="v1")

    baseline_parser = subparsers.add_parser(
        "run-baseline",
        help="Run baseline inference for candidate base models",
    )
    baseline_parser.add_argument("--model-id", required=True)
    baseline_parser.add_argument("--prompts", type=Path, required=True)
    baseline_parser.add_argument("--output", type=Path, required=True)
    baseline_parser.add_argument("--backend", choices=("mock", "subprocess"), default="mock")
    baseline_parser.add_argument("--runner-command", nargs="+")

    finetune_parser = subparsers.add_parser(
        "prepare-finetune-run",
        help="Build a reproducible adapter-based training plan",
    )
    finetune_parser.add_argument("--config", type=Path, required=True)
    finetune_parser.add_argument("--dataset-version", required=True)
    finetune_parser.add_argument("--output-root", type=Path, required=True)
    finetune_parser.add_argument("--output", type=Path, required=True)

    artifact_parser = subparsers.add_parser(
        "register-artifacts",
        help="Register versioned training artifacts for a run",
    )
    artifact_parser.add_argument("--training-plan", type=Path, required=True)
    artifact_parser.add_argument("--artifact-file", action="append", dest="artifact_files", required=True)
    artifact_parser.add_argument("--output", type=Path, required=True)

    compare_parser = subparsers.add_parser(
        "compare-training-paths",
        help="Compare direct generation and TEST_SPEC training results",
    )
    compare_parser.add_argument("--direct", type=Path, required=True)
    compare_parser.add_argument("--test-spec", type=Path, required=True)
    compare_parser.add_argument("--output", type=Path, required=True)

    syntax_parser = subparsers.add_parser(
        "evaluate-syntax",
        help="Run fast syntax and parse validation on generated outputs",
    )
    syntax_parser.add_argument("--results", type=Path, required=True)
    syntax_parser.add_argument("--output", type=Path, required=True)

    compile_parser = subparsers.add_parser(
        "evaluate-compile",
        help="Run compile validation on generated outputs",
    )
    compile_parser.add_argument("--results", type=Path, required=True)
    compile_parser.add_argument("--output", type=Path, required=True)
    compile_parser.add_argument("--backend", choices=("mock", "subprocess"), default="mock")
    compile_parser.add_argument("--checker-command", nargs="+")

    jest_parser = subparsers.add_parser(
        "evaluate-jest",
        help="Run Jest execution evaluation on generated outputs",
    )
    jest_parser.add_argument("--results", type=Path, required=True)
    jest_parser.add_argument("--output", type=Path, required=True)
    jest_parser.add_argument("--backend", choices=("mock", "subprocess"), default="mock")
    jest_parser.add_argument("--harness-command", nargs="+")

    robustness_parser = subparsers.add_parser(
        "evaluate-robustness",
        help="Score generated outputs with the robustness signal",
    )
    robustness_parser.add_argument("--results", type=Path, required=True)
    robustness_parser.add_argument("--output", type=Path, required=True)

    report_parser = subparsers.add_parser(
        "build-report",
        help="Build a standard benchmark report from evaluation manifests",
    )
    report_parser.add_argument("--run-label", required=True)
    report_parser.add_argument("--syntax", type=Path)
    report_parser.add_argument("--compile", type=Path, dest="compile_report")
    report_parser.add_argument("--jest", type=Path)
    report_parser.add_argument("--robustness", type=Path)
    report_parser.add_argument("--output", type=Path, required=True)

    compare_reports_parser = subparsers.add_parser(
        "compare-reports",
        help="Compare baseline and candidate benchmark reports",
    )
    compare_reports_parser.add_argument("--baseline", type=Path, required=True)
    compare_reports_parser.add_argument("--candidate", type=Path, required=True)
    compare_reports_parser.add_argument("--output", type=Path, required=True)

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

    if args.command == "validate-test-spec":
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        errors = validate_test_spec(spec)
        if errors:
            parser.error(f"invalid TEST_SPEC: {', '.join(errors)}")
        print(json.dumps({"valid": True}, indent=2))
        return 0

    if args.command == "render-test-spec":
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        rendered = render_jest_test_spec(spec)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        return 0

    if args.command == "freeze-splits":
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        frozen = freeze_benchmark_splits(manifest, split_version=args.split_version)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(frozen, indent=2) + "\n", encoding="utf-8")
        return 0

    if args.command == "run-baseline":
        prompt_manifest = json.loads(args.prompts.read_text(encoding="utf-8"))
        baseline_results = run_baseline_inference(
            prompt_manifest,
            model_id=args.model_id,
            backend=args.backend,
            command=args.runner_command,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(baseline_results, indent=2) + "\n", encoding="utf-8"
        )
        return 0

    if args.command == "prepare-finetune-run":
        config = json.loads(args.config.read_text(encoding="utf-8"))
        plan = build_adapter_training_plan(
            config,
            dataset_version=args.dataset_version,
            output_root=args.output_root,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
        return 0

    if args.command == "register-artifacts":
        training_plan = json.loads(args.training_plan.read_text(encoding="utf-8"))
        artifact_manifest = register_training_artifacts(
            training_plan,
            artifact_files=args.artifact_files,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(artifact_manifest, indent=2) + "\n", encoding="utf-8"
        )
        return 0

    if args.command == "compare-training-paths":
        direct_manifest = json.loads(args.direct.read_text(encoding="utf-8"))
        test_spec_manifest = json.loads(args.test_spec.read_text(encoding="utf-8"))
        comparison = compare_training_paths(direct_manifest, test_spec_manifest)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(comparison, indent=2) + "\n", encoding="utf-8")
        return 0

    if args.command == "evaluate-syntax":
        result_manifest = json.loads(args.results.read_text(encoding="utf-8"))
        syntax_report = evaluate_syntax(result_manifest)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(syntax_report, indent=2) + "\n", encoding="utf-8")
        return 0

    if args.command == "evaluate-compile":
        result_manifest = json.loads(args.results.read_text(encoding="utf-8"))
        compile_report = evaluate_compile(
            result_manifest,
            backend=args.backend,
            checker_command=args.checker_command,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(compile_report, indent=2) + "\n", encoding="utf-8")
        return 0

    if args.command == "evaluate-jest":
        result_manifest = json.loads(args.results.read_text(encoding="utf-8"))
        execution_report = evaluate_jest_execution(
            result_manifest,
            backend=args.backend,
            harness_command=args.harness_command,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(execution_report, indent=2) + "\n", encoding="utf-8")
        return 0

    if args.command == "evaluate-robustness":
        result_manifest = json.loads(args.results.read_text(encoding="utf-8"))
        robustness_report = evaluate_robustness(result_manifest)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(robustness_report, indent=2) + "\n", encoding="utf-8")
        return 0

    if args.command == "build-report":
        metric_manifests = {}
        for name, path in (
            ("syntax", args.syntax),
            ("compile", args.compile_report),
            ("jest", args.jest),
            ("robustness", args.robustness),
        ):
            if path:
                metric_manifests[name] = json.loads(path.read_text(encoding="utf-8"))
        report = build_run_report(args.run_label, metric_manifests)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        return 0

    if args.command == "compare-reports":
        baseline_report = json.loads(args.baseline.read_text(encoding="utf-8"))
        candidate_report = json.loads(args.candidate.read_text(encoding="utf-8"))
        comparison = compare_run_reports(baseline_report, candidate_report)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(comparison, indent=2) + "\n", encoding="utf-8")
        return 0

    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
