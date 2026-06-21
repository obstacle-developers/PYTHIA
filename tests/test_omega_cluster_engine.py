from pathlib import Path

from pythia.core.jsonl import iter_jsonl
from pythia.omega.cluster_engine import (
    append_cluster_engine_output,
    build_cluster_records,
    group_by_signature,
    iter_group_sorted_by_signature,
    run_mock_cluster_engine,
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


def test_group_by_signature_is_deterministic():
    first = group_by_signature(_records(), ["channel", "region"])
    second = group_by_signature(list(reversed(_records())), ["channel", "region"])

    assert first == second
    assert [record["event_id"] for record in first[1]["records"]] == ["event-002", "event-003"]


def test_group_by_signature_one_key():
    grouped = group_by_signature(_records(), ["channel"])

    assert [group["signature"] for group in grouped] == [{"channel": "electron"}, {"channel": "muon"}]
    assert [len(group["records"]) for group in grouped] == [1, 2]


def test_group_by_signature_multiple_keys():
    grouped = group_by_signature(_records(), ["channel", "region", "mock_bin"])

    assert grouped[0]["signature"] == {"channel": "electron", "region": "endcap", "mock_bin": 1}
    assert grouped[1]["signature"] == {"channel": "muon", "region": "barrel", "mock_bin": 2}


def test_group_by_signature_rejects_missing_signature_keys():
    records = [{"event_id": "event-001", "trace_id": "trace-001", "features": {"channel": "muon"}}]

    try:
        group_by_signature(records, ["channel", "region"])
    except ValueError as exc:
        assert "missing signature key 'region' in features" in str(exc)
    else:
        raise AssertionError("missing signature key was not rejected")


def test_iter_group_sorted_by_signature_yields_one_group_at_a_time():
    sorted_records = sorted(
        _records(), key=lambda record: (record["features"]["channel"], record["features"]["region"])
    )

    iterator = iter_group_sorted_by_signature(sorted_records, ["channel", "region"])
    first = next(iterator)
    second = next(iterator)

    assert first["signature"] == {"channel": "electron", "region": "endcap"}
    assert [record["event_id"] for record in first["records"]] == ["event-001"]
    assert second["signature"] == {"channel": "muon", "region": "barrel"}
    assert [record["event_id"] for record in second["records"]] == ["event-003", "event-002"]
    try:
        next(iterator)
    except StopIteration:
        pass
    else:
        raise AssertionError("iterator yielded more groups than expected")


def test_iter_group_sorted_by_signature_rejects_missing_keys():
    records = [{"event_id": "event-001", "features": {"channel": "muon"}}]

    try:
        list(iter_group_sorted_by_signature(records, ["region"]))
    except ValueError as exc:
        assert "missing signature key 'region' in features" in str(exc)
    else:
        raise AssertionError("missing signature key was not rejected")


def test_build_cluster_records_creates_clusters_and_members():
    grouped = group_by_signature(_records(), ["channel"])
    output = build_cluster_records(grouped, "mock_week13_features_v0")

    assert [cluster["cluster_id"] for cluster in output["clusters"]] == [
        "mock-anomaly-family-001",
        "mock-anomaly-family-002",
    ]
    assert all(cluster["human_review_required"] is True for cluster in output["clusters"])
    assert len(output["members"]) == 3
    assert output["members"][0]["record_type"] == "anomaly_cluster_member"


def test_run_mock_cluster_engine_creates_summaries_only_in_memory():
    output = run_mock_cluster_engine(_records(), ["channel"], "mock_week13_features_v0")

    assert set(output) == {"grouped_records", "clusters", "members", "summaries"}
    assert [summary["record_type"] for summary in output["summaries"]] == [
        "anomaly_cluster_summary",
        "anomaly_cluster_summary",
    ]
    assert output["summaries"][1]["mean_anomaly_score"] == 0.8


def test_cluster_engine_output_uses_safe_language_only():
    output = run_mock_cluster_engine(_records(), ["channel"], "mock_week13_features_v0")
    rendered = repr(output).lower()

    assert "new particle discovered" not in rendered
    assert "discovery confirmed" not in rendered
    assert "new physics found" not in rendered
    assert "confirmed signal" not in rendered
    assert all(cluster["status"] == "unresolved_anomaly_family" for cluster in output["clusters"])


def test_no_candidate_particle_logic_in_cluster_engine_source():
    source = Path("pythia/omega/cluster_engine.py").read_text(encoding="utf-8").lower()

    assert "candidate particle" not in source
    assert "candidate_particle" not in source
    assert "candidate construction" not in source


def test_no_hdbscan_or_sklearn_imports_in_cluster_engine_source():
    source = Path("pythia/omega/cluster_engine.py").read_text(encoding="utf-8").lower()

    assert "hdbscan" not in source
    assert "sklearn" not in source
    assert "numpy" not in source


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


def test_append_cluster_engine_output_uses_jsonl_helpers(tmp_path):
    output = run_mock_cluster_engine(_records(), ["channel"], "mock_week13_features_v0")
    paths = append_cluster_engine_output(output, tmp_path / "clusters.jsonl", tmp_path / "members.jsonl")

    assert paths == {"cluster_path": tmp_path / "clusters.jsonl", "member_path": tmp_path / "members.jsonl"}
    assert list(iter_jsonl(paths["cluster_path"])) == output["clusters"]
    assert list(iter_jsonl(paths["member_path"])) == output["members"]
