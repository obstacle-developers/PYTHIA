#!/usr/bin/env python3
"""Run the tiny reproducible Week 13 demo capsule.

The demo uses only synthetic JSONL records committed under demo/week13. It runs
Week 13 mock anomaly-family grouping, consistency checks, and report rendering.
It does not load real datasets, perform later-stage feature work, or make any
interpretation claim.
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
from pathlib import Path
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pythia.core.jsonl import append_jsonl, iter_jsonl
from pythia.core.safety import assert_no_forbidden_discovery_language
from pythia.omega.cluster_consistency import evaluate_cluster_consistency
from pythia.omega.cluster_engine import run_mock_cluster_engine
from pythia.omega.cluster_report import build_week13_cluster_report, write_week13_cluster_report

DEMO_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT_PATH = DEMO_DIR / "mock_traces.jsonl"
DEFAULT_OUTPUT_DIR = DEMO_DIR / "output"
FEATURE_SPACE = "mock_week13_demo_features_v0"
SIGNATURE_KEYS = ("channel", "region", "mock_bin")
DETERMINISTIC_CREATED_AT = "2026-06-21T00:00:00Z"
OUTPUT_FILENAMES = ("clusters.jsonl", "members.jsonl", "consistency.jsonl", "week13_report.md")


def _read_records(path: Path) -> list[dict[str, Any]]:
    return [dict(record) for record in iter_jsonl(path)]


def _members_for_cluster(cluster_id: str, members: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return [member for member in members if member.get("cluster_id") == cluster_id]


def _normalise_engine_output(engine_output: dict[str, Any]) -> dict[str, Any]:
    """Make demo output reproducible by replacing runtime timestamps."""
    for cluster in engine_output["clusters"]:
        cluster["created_at"] = DETERMINISTIC_CREATED_AT
    return engine_output


def _remove_previous_outputs(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename in OUTPUT_FILENAMES:
        path = output_dir / filename
        if path.exists():
            path.unlink()


def run_demo(input_path: Path = DEFAULT_INPUT_PATH, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Path]:
    """Run the Week 13 demo and write deterministic local outputs."""
    records = _read_records(input_path)
    engine_output = _normalise_engine_output(
        run_mock_cluster_engine(records, SIGNATURE_KEYS, FEATURE_SPACE)
    )

    consistency_by_cluster: dict[str, list[dict[str, Any]]] = {}
    consistency_records: list[dict[str, Any]] = []
    for cluster in engine_output["clusters"]:
        cluster_id = str(cluster["cluster_id"])
        members = _members_for_cluster(cluster_id, engine_output["members"])
        checks = evaluate_cluster_consistency(
            cluster,
            members,
            SIGNATURE_KEYS,
            min_cluster_size=2,
            min_anomaly_score=0.70,
        )
        consistency_by_cluster[cluster_id] = checks
        consistency_records.extend(checks)

    report = build_week13_cluster_report(engine_output, consistency_by_cluster)
    report_markdown = write_week13_cluster_report(report, output_dir / "week13_report.md")
    assert_no_forbidden_discovery_language(report_markdown.read_text(encoding="utf-8"))

    _remove_previous_outputs(output_dir)
    cluster_path = output_dir / "clusters.jsonl"
    member_path = output_dir / "members.jsonl"
    consistency_path = output_dir / "consistency.jsonl"
    report_markdown = write_week13_cluster_report(report, output_dir / "week13_report.md")

    for cluster in engine_output["clusters"]:
        append_jsonl(cluster_path, cluster)
    for member in engine_output["members"]:
        append_jsonl(member_path, member)
    for record in consistency_records:
        append_jsonl(consistency_path, record)

    return {
        "clusters": cluster_path,
        "members": member_path,
        "consistency": consistency_path,
        "report": report_markdown,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the synthetic Week 13 demo capsule.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_PATH, help="Synthetic mock trace JSONL path.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for demo outputs.")
    args = parser.parse_args(argv)

    paths = run_demo(args.input, args.output_dir)
    for label in ("clusters", "members", "consistency", "report"):
        print(f"{label}: {paths[label]}")
    print("human review required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
