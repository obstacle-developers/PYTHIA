from pathlib import Path

from pythia.omega.cluster_consistency import evaluate_cluster_consistency
from pythia.omega.cluster_engine import run_mock_cluster_engine
from pythia.omega.cluster_report import (
    build_and_render_week13_report,
    build_week13_cluster_report,
    render_week13_cluster_report_markdown,
    write_week13_cluster_report,
)


def _records():
    return [
        {
            "event_id": "event-003",
            "trace_id": "trace-003",
            "anomaly_score": 0.9,
            "features": {"channel": "muon", "region": "barrel", "mock_bin": 2},
        },
        {
            "event_id": "event-001",
            "trace_id": "trace-001",
            "anomaly_score": 0.5,
            "features": {"channel": "electron", "region": "endcap", "mock_bin": 1},
        },
        {
            "event_id": "event-002",
            "trace_id": "trace-002",
            "anomaly_score": 0.7,
            "features": {"channel": "muon", "region": "barrel", "mock_bin": 2},
        },
    ]


def _engine_output():
    return run_mock_cluster_engine(_records(), ["channel"], "mock_week13_features_v0")


def _consistency_by_cluster(output):
    grouped = {}
    for cluster in output["clusters"]:
        members = [member for member in output["members"] if member["cluster_id"] == cluster["cluster_id"]]
        grouped[cluster["cluster_id"]] = evaluate_cluster_consistency(
            cluster, members, ["channel"], min_cluster_size=2, min_anomaly_score=0.6
        )
    return grouped


def _passing_consistency_by_cluster(output):
    grouped = {}
    for cluster in output["clusters"]:
        members = [member for member in output["members"] if member["cluster_id"] == cluster["cluster_id"]]
        grouped[cluster["cluster_id"]] = evaluate_cluster_consistency(
            cluster, members, ["channel"], min_cluster_size=1, min_anomaly_score=0.5
        )
    return grouped


def test_report_dictionary_creation():
    report = build_week13_cluster_report(_engine_output())

    assert report["report_type"] == "week13_cluster_report"
    assert report["stage"] == "Week 13 cluster report integration"
    assert set(report) == {
        "report_type",
        "stage",
        "status",
        "cluster_count",
        "member_count",
        "clusters",
        "consistency_summary",
        "human_review_required",
        "limitations",
        "next_step",
    }


def test_cluster_count_and_member_count_correctness():
    report = build_week13_cluster_report(_engine_output())

    assert report["cluster_count"] == 2
    assert report["member_count"] == 3
    assert [cluster["member_count"] for cluster in report["clusters"]] == [1, 2]


def test_consistency_summary_behavior():
    output = _engine_output()
    report = build_week13_cluster_report(output, _consistency_by_cluster(output))

    assert report["consistency_summary"]["check_count"] == 6
    assert report["consistency_summary"]["insufficient_evidence_checks"] == 2


def test_report_without_consistency_records_is_insufficient_evidence():
    report = build_week13_cluster_report(_engine_output())

    assert report["consistency_summary"]["check_count"] == 0
    assert report["status"] == "insufficient_evidence"


def test_report_with_all_passing_consistency_records_is_unresolved_anomaly_family():
    output = _engine_output()
    report = build_week13_cluster_report(output, _passing_consistency_by_cluster(output))

    assert report["consistency_summary"]["check_count"] == 6
    assert report["consistency_summary"]["insufficient_evidence_checks"] == 0
    assert report["status"] == "unresolved_anomaly_family"


def test_report_with_any_failing_consistency_record_is_insufficient_evidence():
    output = _engine_output()
    report = build_week13_cluster_report(output, _consistency_by_cluster(output))

    assert report["consistency_summary"]["insufficient_evidence_checks"] > 0
    assert report["status"] == "insufficient_evidence"


def test_markdown_rendering_contains_required_safe_language():
    markdown = render_week13_cluster_report_markdown(build_week13_cluster_report(_engine_output()))

    assert markdown.startswith("# Week 13 Cluster Report")
    assert "unresolved anomaly family" in markdown
    assert "human review required" in markdown
    assert "insufficient evidence" in markdown


def test_safe_language_only_and_forbidden_language_absent():
    report, markdown = build_and_render_week13_report(_engine_output())
    rendered = repr(report).lower() + markdown.lower()
    forbidden_fragments = [
        "discov" + "ered",
        "discovery " + "confirmed",
        "new particle",
        "new physics " + "found",
        "proved",
        "certain",
        "guaranteed",
        "confirmed " + "signal",
    ]

    assert "candidate pattern" in rendered
    assert "requires human review" in rendered
    assert all(fragment not in rendered for fragment in forbidden_fragments)


def test_forbidden_report_language_blocked():
    report = build_week13_cluster_report(_engine_output())
    report["clusters"][0]["summary"] = "new physics " + "found"

    try:
        render_week13_cluster_report_markdown(report)
    except ValueError as exc:
        assert "unsafe report language" in str(exc)
    else:
        raise AssertionError("unsafe language was not blocked")


def test_human_review_required_is_true_and_limitations_are_included():
    report = build_week13_cluster_report(_engine_output())

    assert report["human_review_required"] is True
    assert all(cluster["human_review_required"] is True for cluster in report["clusters"])
    assert len(report["limitations"]) >= 3


def test_no_later_stage_feature_logic_or_candidate_particle_logic():
    source = Path("pythia/omega/cluster_report.py").read_text(encoding="utf-8").lower()

    assert "fingerprint" not in source
    assert "candidate particle" not in source
    assert "candidate_particle" not in source
    assert "candidate construction" not in source


def test_no_hdbscan_sklearn_numpy_pandas_imports():
    source = Path("pythia/omega/cluster_report.py").read_text(encoding="utf-8").lower()

    assert "hdbscan" not in source
    assert "sklearn" not in source
    assert "numpy" not in source
    assert "pandas" not in source


def test_write_report_writes_only_markdown(tmp_path):
    report = build_week13_cluster_report(_engine_output())
    path = write_week13_cluster_report(report, tmp_path / "week13_cluster_report.md")

    assert path == tmp_path / "week13_cluster_report.md"
    assert path.read_text(encoding="utf-8").startswith("# Week 13 Cluster Report")
    assert sorted(item.name for item in tmp_path.iterdir()) == ["week13_cluster_report.md"]


def test_no_raw_data_or_artifact_files_are_added():
    repo_root = Path(__file__).resolve().parents[1]
    disallowed_suffixes = {".csv", ".parquet", ".h5", ".hdf5", ".root", ".npy", ".npz", ".pkl"}
    ignored_parts = {".git", "__pycache__", ".pytest_cache"}

    disallowed_paths = [
        path.relative_to(repo_root)
        for path in repo_root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in disallowed_suffixes
        and not any(part in ignored_parts for part in path.parts)
    ]

    assert disallowed_paths == []


def test_forbidden_report_nested_cluster_text_blocked():
    report = build_week13_cluster_report(_engine_output())
    report["clusters"][0]["label"] = "discovery confirmed"

    try:
        render_week13_cluster_report_markdown(report)
    except ValueError as exc:
        assert "unsafe report language" in str(exc)
    else:
        raise AssertionError("unsafe report label was not blocked")
