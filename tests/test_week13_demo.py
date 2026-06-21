from __future__ import annotations

import ast
import json
from pathlib import Path
import subprocess
import sys

from pythia.core.safety import find_forbidden_discovery_language

REPO_ROOT = Path(__file__).resolve().parents[1]
DEMO_SCRIPT = REPO_ROOT / "demo" / "week13" / "run_week13_demo.py"
MOCK_TRACES = REPO_ROOT / "demo" / "week13" / "mock_traces.jsonl"
README = REPO_ROOT / "demo" / "week13" / "README.md"


def _read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                rows.append(json.loads(stripped))
    return rows


def _run_demo(tmp_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(DEMO_SCRIPT), "--output-dir", str(tmp_path)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_demo_script_runs_successfully_and_creates_outputs_in_temp_dir(tmp_path):
    result = _run_demo(tmp_path)

    assert result.returncode == 0, result.stderr
    assert (tmp_path / "clusters.jsonl").is_file()
    assert (tmp_path / "members.jsonl").is_file()
    assert (tmp_path / "consistency.jsonl").is_file()
    assert (tmp_path / "week13_report.md").is_file()


def test_demo_jsonl_outputs_are_valid(tmp_path):
    result = _run_demo(tmp_path)
    assert result.returncode == 0, result.stderr

    clusters = _read_jsonl(tmp_path / "clusters.jsonl")
    members = _read_jsonl(tmp_path / "members.jsonl")
    consistency = _read_jsonl(tmp_path / "consistency.jsonl")

    assert len(clusters) == 2
    assert len(members) == 4
    assert len(consistency) == 6
    assert all(record["record_type"] == "anomaly_cluster" for record in clusters)
    assert all(record["record_type"] == "anomaly_cluster_member" for record in members)
    assert all(record["record_type"] == "anomaly_cluster_consistency" for record in consistency)


def test_report_requires_human_review_and_uses_safe_language(tmp_path):
    result = _run_demo(tmp_path)
    assert result.returncode == 0, result.stderr

    report = (tmp_path / "week13_report.md").read_text(encoding="utf-8").lower()

    assert "human review required" in report
    assert find_forbidden_discovery_language(report) == []


def test_demo_contains_no_candidate_particle_or_week14_fingerprint_logic():
    combined = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in (DEMO_SCRIPT, MOCK_TRACES, README)
    )

    assert "candidate-particle" not in combined
    assert "candidate_particle" not in combined
    assert "candidate particle" not in combined
    assert "week 14" not in combined
    assert "fingerprint" not in combined


def test_demo_uses_no_disallowed_dependency_imports():
    tree = ast.parse(DEMO_SCRIPT.read_text(encoding="utf-8"))
    imported_roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".")[0])

    assert imported_roots.isdisjoint({"hdbscan", "sklearn", "numpy", "pandas"})


def test_mock_traces_are_tiny_synthetic_text_only_and_no_large_data_files():
    records = _read_jsonl(MOCK_TRACES)
    assert 0 < len(records) <= 10
    assert MOCK_TRACES.stat().st_size < 10_000
    assert all(str(record["event_id"]).startswith("mock-week13-event-") for record in records)
    assert all("synthetic" in record["features"]["channel"] for record in records)

    disallowed_suffixes = {".csv", ".parquet", ".h5", ".hdf5", ".root", ".npy", ".npz", ".pkl"}
    ignored_parts = {".git", "__pycache__", ".pytest_cache"}
    oversized_paths = []
    data_paths = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file() or any(part in ignored_parts for part in path.parts):
            continue
        if path.suffix.lower() in disallowed_suffixes:
            data_paths.append(path.relative_to(REPO_ROOT))
        if path.stat().st_size > 1_000_000:
            oversized_paths.append(path.relative_to(REPO_ROOT))

    assert data_paths == []
    assert oversized_paths == []
