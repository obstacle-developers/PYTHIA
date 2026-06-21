from pathlib import Path

import pytest

from pythia.core.jsonl import iter_jsonl
from pythia.omega.cluster_consistency import (
    append_consistency_records,
    check_anomaly_score_floor,
    check_min_cluster_size,
    check_signature_repetition,
    derive_cluster_status,
    evaluate_cluster_consistency,
)
from pythia.omega.clusters import make_anomaly_cluster_record, make_cluster_member_record


def _cluster_record(member_count=2):
    return make_anomaly_cluster_record(
        cluster_id="omega-week13-001",
        created_at="2026-06-21T00:00:00Z",
        status="unresolved_anomaly_family",
        label="mock week 13 anomaly family",
        feature_space="mock_week13_features_v0",
        member_count=member_count,
        summary="unresolved anomaly family requiring human review",
    )


def _member(event_id="event-001", channel="muon", region="barrel", score=0.8):
    return make_cluster_member_record(
        cluster_id="omega-week13-001",
        event_id=event_id,
        trace_id=f"trace-{event_id}",
        anomaly_score=score,
        features={"channel": channel, "region": region, "mock_bin": 2},
        membership_reason="candidate pattern from exact mock feature signature; requires human review",
    )


def _passing_members():
    return [_member("event-001"), _member("event-002")]


def test_cluster_passes_minimum_size():
    record = check_min_cluster_size(_cluster_record(), _passing_members(), min_cluster_size=2)

    assert record["check_name"] == "minimum_cluster_size"
    assert record["status"] == "unresolved_anomaly_family"


def test_cluster_fails_minimum_size():
    record = check_min_cluster_size(_cluster_record(member_count=1), [_member()], min_cluster_size=2)

    assert record["status"] == "insufficient_evidence"
    assert record["weakening_conditions"] == ["weakening condition: mock member count below threshold"]


def test_repeated_signature_passes():
    record = check_signature_repetition(_passing_members(), ["channel", "region"])

    assert record["status"] == "unresolved_anomaly_family"


def test_mixed_signature_fails():
    members = [_member("event-001", channel="muon"), _member("event-002", channel="electron")]
    record = check_signature_repetition(members, ["channel", "region"])

    assert record["status"] == "insufficient_evidence"


def test_anomaly_score_floor_passes():
    record = check_anomaly_score_floor(_passing_members(), min_score=0.7)

    assert record["status"] == "unresolved_anomaly_family"


def test_anomaly_score_floor_fails():
    members = [_member("event-001", score=0.8), _member("event-002", score=0.2)]
    record = check_anomaly_score_floor(members, min_score=0.7)

    assert record["status"] == "insufficient_evidence"


def test_evaluate_cluster_consistency_returns_multiple_records():
    records = evaluate_cluster_consistency(
        _cluster_record(), _passing_members(), ["channel", "region"], min_cluster_size=2, min_anomaly_score=0.7
    )

    assert [record["check_name"] for record in records] == [
        "minimum_cluster_size",
        "signature_repetition",
        "anomaly_score_floor",
    ]


def test_derive_cluster_status_returns_insufficient_evidence_if_any_check_fails():
    records = [
        check_min_cluster_size(_cluster_record(), _passing_members()),
        check_anomaly_score_floor([_member(score=0.1)], min_score=0.7),
    ]

    assert derive_cluster_status(records) == "insufficient_evidence"


def test_append_consistency_records_writes_jsonl(tmp_path):
    path = tmp_path / "consistency.jsonl"
    records = evaluate_cluster_consistency(_cluster_record(), _passing_members(), ["channel"], min_anomaly_score=0.7)

    returned_path = append_consistency_records(path, records)

    assert returned_path == path
    assert list(iter_jsonl(path)) == records


def test_append_consistency_records_writes_generator_records(tmp_path):
    path = tmp_path / "consistency.jsonl"
    records = evaluate_cluster_consistency(_cluster_record(), _passing_members(), ["channel"], min_anomaly_score=0.7)

    returned_path = append_consistency_records(path, (record for record in records))

    written_records = list(iter_jsonl(path))
    assert returned_path == path
    assert written_records == records
    assert len(written_records) == len(records)


def test_append_consistency_records_invalid_generator_record_raises(tmp_path):
    path = tmp_path / "consistency.jsonl"
    valid_record = evaluate_cluster_consistency(_cluster_record(), _passing_members(), ["channel"])[0]

    def records():
        yield valid_record
        invalid_record = dict(valid_record)
        invalid_record.pop("status")
        yield invalid_record

    with pytest.raises(ValueError, match="record missing required keys: status"):
        append_consistency_records(path, records())


def test_no_unsafe_discovery_language():
    source = Path("pythia/omega/cluster_consistency.py").read_text(encoding="utf-8").lower()
    rendered = repr(evaluate_cluster_consistency(_cluster_record(), _passing_members(), ["channel"])).lower()

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
    assert all(fragment not in source for fragment in forbidden_fragments)
    assert all(fragment not in rendered for fragment in forbidden_fragments)


def test_no_candidate_particle_logic():
    source = Path("pythia/omega/cluster_consistency.py").read_text(encoding="utf-8").lower()

    assert "candidate particle" not in source
    assert "candidate_particle" not in source
    assert "candidate construction" not in source


def test_no_hdbscan_sklearn_numpy_pandas_imports():
    source = Path("pythia/omega/cluster_consistency.py").read_text(encoding="utf-8").lower()

    assert "hdbscan" not in source
    assert "sklearn" not in source
    assert "numpy" not in source
    assert "pandas" not in source


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
