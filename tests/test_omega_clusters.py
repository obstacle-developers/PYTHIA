import json
from pathlib import Path

import pytest

from pythia.core.jsonl import iter_jsonl
from pythia.omega.clusters import (
    append_cluster_consistency,
    append_cluster_member,
    append_cluster_record,
    make_anomaly_cluster_record,
    make_cluster_consistency_record,
    make_cluster_member_record,
    summarize_cluster,
)


def _cluster_record():
    return make_anomaly_cluster_record(
        cluster_id="omega-cluster-001",
        created_at="2026-06-21T00:00:00Z",
        status="candidate_pattern",
        label="tiny mock timing residual group",
        feature_space="mock_residual_features_v0",
        member_count=2,
        summary="candidate pattern requiring human review with insufficient evidence",
    )


def _member_record(event_id="event-001", score=0.7):
    return make_cluster_member_record(
        cluster_id="omega-cluster-001",
        event_id=event_id,
        trace_id=f"trace-{event_id}",
        anomaly_score=score,
        features={"mock_residual": score, "mock_channel_count": 1},
        membership_reason="similar tiny mock residual shape; requires human review",
    )


def _consistency_record():
    return make_cluster_consistency_record(
        cluster_id="omega-cluster-001",
        check_name="mock_feature_overlap",
        status="requires_review",
        details="requires human review; insufficient evidence for interpretation",
        weakening_conditions=["weakening condition: low member count"],
        kill_conditions=["kill condition: inconsistent mock trace metadata"],
    )


def test_creating_valid_anomaly_cluster_record():
    record = _cluster_record()

    assert record["record_type"] == "anomaly_cluster"
    assert record["cluster_id"] == "omega-cluster-001"
    assert record["created_at"] == "2026-06-21T00:00:00Z"
    assert record["status"] == "candidate_pattern"
    assert record["human_review_required"] is True


def test_creating_valid_cluster_member_record():
    record = _member_record()

    assert record["record_type"] == "anomaly_cluster_member"
    assert record["cluster_id"] == "omega-cluster-001"
    assert record["event_id"] == "event-001"
    assert record["trace_id"] == "trace-event-001"
    assert record["anomaly_score"] == 0.7
    assert record["features"] == {"mock_residual": 0.7, "mock_channel_count": 1}


def test_creating_valid_consistency_record():
    record = _consistency_record()

    assert record["record_type"] == "anomaly_cluster_consistency"
    assert record["cluster_id"] == "omega-cluster-001"
    assert record["check_name"] == "mock_feature_overlap"
    assert record["status"] == "requires_review"
    assert record["weakening_conditions"] == ["weakening condition: low member count"]
    assert record["kill_conditions"] == ["kill condition: inconsistent mock trace metadata"]


def test_summary_generation_from_one_cluster_and_multiple_members():
    summary = summarize_cluster(
        _cluster_record(),
        [_member_record("event-001", 0.7), _member_record("event-002", 0.9)],
        [_consistency_record()],
    )

    assert summary == {
        "record_type": "anomaly_cluster_summary",
        "cluster_id": "omega-cluster-001",
        "status": "candidate_pattern",
        "label": "tiny mock timing residual group",
        "feature_space": "mock_residual_features_v0",
        "member_count": 2,
        "declared_member_count": 2,
        "human_review_required": True,
        "mean_anomaly_score": 0.8,
        "consistency_check_count": 1,
    }


def test_appending_cluster_records_to_jsonl(tmp_path):
    path = tmp_path / "clusters.jsonl"
    returned_path = append_cluster_record(path, _cluster_record())

    assert returned_path == path
    assert list(iter_jsonl(path)) == [_cluster_record()]


def test_appending_member_records_to_jsonl(tmp_path):
    path = tmp_path / "members.jsonl"
    record = _member_record()
    append_cluster_member(path, record)

    assert list(iter_jsonl(path)) == [record]


def test_appending_consistency_records_to_jsonl(tmp_path):
    path = tmp_path / "consistency.jsonl"
    record = _consistency_record()
    append_cluster_consistency(path, record)

    assert list(iter_jsonl(path)) == [record]


def test_jsonl_append_uses_deterministic_key_order(tmp_path):
    path = tmp_path / "clusters.jsonl"
    append_cluster_record(path, _cluster_record())

    first_line = path.read_text(encoding="utf-8").splitlines()[0]
    assert first_line.startswith('{"cluster_id":')
    assert json.loads(first_line) == _cluster_record()


def test_rejecting_forbidden_unsafe_discovery_language():
    with pytest.raises(ValueError, match="unsafe discovery language"):
        make_anomaly_cluster_record(
            cluster_id="omega-cluster-unsafe",
            status="candidate_pattern",
            label="unsafe mock label",
            feature_space="mock_residual_features_v0",
            member_count=1,
            summary="new physics " + "found",
        )


def test_rejecting_invalid_status_labels():
    with pytest.raises(ValueError, match="invalid cluster status"):
        make_anomaly_cluster_record(
            cluster_id="omega-cluster-invalid",
            status="verified",
            label="tiny mock timing residual group",
            feature_space="mock_residual_features_v0",
            member_count=1,
            summary="candidate pattern requiring human review",
        )


def test_ensuring_no_raw_datasets_or_artifacts_are_added():
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
