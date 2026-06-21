"""Lightweight anomaly cluster record interfaces for PYTHIA Ω.

This module defines typed, append-only record helpers for anomaly cluster
interfaces. It intentionally does not run clustering algorithms, construct
candidate particles, or attach raw artifacts.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from numbers import Real
from pathlib import Path
from typing import Any

from pythia.core.jsonl import append_jsonl, validate_record_has_keys
from pythia.core.safety import assert_record_uses_safe_language

JsonValue = Any
JsonRecord = dict[str, JsonValue]

ALLOWED_CLUSTER_STATUSES = (
    "candidate_pattern",
    "unresolved_anomaly_family",
    "requires_review",
    "rejected_pattern",
    "insufficient_evidence",
)

CLUSTER_RECORD_KEYS = (
    "record_type",
    "cluster_id",
    "created_at",
    "status",
    "label",
    "feature_space",
    "member_count",
    "summary",
    "human_review_required",
)

CLUSTER_MEMBER_RECORD_KEYS = (
    "record_type",
    "cluster_id",
    "event_id",
    "trace_id",
    "anomaly_score",
    "features",
    "membership_reason",
)

CLUSTER_CONSISTENCY_RECORD_KEYS = (
    "record_type",
    "cluster_id",
    "check_name",
    "status",
    "details",
    "weakening_conditions",
    "kill_conditions",
)


def _utc_timestamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _validate_safe_language(record: Mapping[str, Any]) -> None:
    assert_record_uses_safe_language(record)


def _validate_cluster_status(status: str) -> None:
    if status not in ALLOWED_CLUSTER_STATUSES:
        allowed = ", ".join(ALLOWED_CLUSTER_STATUSES)
        raise ValueError(f"invalid cluster status {status!r}; expected one of: {allowed}")


def _validate_required_record(record: Mapping[str, Any], required_keys: Sequence[str]) -> None:
    validate_record_has_keys(record, required_keys)
    _validate_safe_language(record)


def _validate_record_type(record: Mapping[str, Any], expected_record_type: str) -> None:
    if record["record_type"] != expected_record_type:
        raise ValueError(
            f"invalid record_type {record['record_type']!r}; expected {expected_record_type!r}"
        )


def _validate_non_empty_string(record: Mapping[str, Any], key: str) -> None:
    value = record[key]
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError(f"{key} must not contain control characters")


def validate_anomaly_cluster_record(record: Mapping[str, Any]) -> None:
    """Validate the schema and safe wording for an anomaly cluster record."""
    _validate_required_record(record, CLUSTER_RECORD_KEYS)
    _validate_record_type(record, "anomaly_cluster")
    _validate_non_empty_string(record, "cluster_id")
    _validate_cluster_status(record["status"])
    _validate_non_empty_string(record, "label")
    _validate_non_empty_string(record, "feature_space")
    if not isinstance(record["member_count"], int) or isinstance(record["member_count"], bool):
        raise ValueError("member_count must be a non-negative integer")
    if record["member_count"] < 0:
        raise ValueError("member_count must be a non-negative integer")
    if not isinstance(record["human_review_required"], bool):
        raise ValueError("human_review_required must be bool")


def validate_cluster_member_record(record: Mapping[str, Any]) -> None:
    """Validate the schema and safe wording for an anomaly cluster member record."""
    _validate_required_record(record, CLUSTER_MEMBER_RECORD_KEYS)
    _validate_record_type(record, "anomaly_cluster_member")
    _validate_non_empty_string(record, "cluster_id")
    _validate_non_empty_string(record, "event_id")
    _validate_non_empty_string(record, "trace_id")
    if not isinstance(record["anomaly_score"], Real) or isinstance(record["anomaly_score"], bool):
        raise ValueError("anomaly_score must be numeric")
    if not isinstance(record["features"], Mapping):
        raise ValueError("features must be a mapping")


def validate_cluster_consistency_record(record: Mapping[str, Any]) -> None:
    """Validate the schema and safe wording for an anomaly consistency record."""
    _validate_required_record(record, CLUSTER_CONSISTENCY_RECORD_KEYS)
    _validate_record_type(record, "anomaly_cluster_consistency")
    _validate_non_empty_string(record, "cluster_id")
    _validate_non_empty_string(record, "check_name")
    _validate_cluster_status(record["status"])
    if not isinstance(record["weakening_conditions"], list):
        raise ValueError("weakening_conditions must be a list")
    if not isinstance(record["kill_conditions"], list):
        raise ValueError("kill_conditions must be a list")


def make_anomaly_cluster_record(
    *,
    cluster_id: str,
    status: str,
    label: str,
    feature_space: str,
    member_count: int,
    summary: str,
    human_review_required: bool = True,
    created_at: str | None = None,
) -> JsonRecord:
    """Build a lightweight anomaly cluster record using safe status labels."""
    record: JsonRecord = {
        "record_type": "anomaly_cluster",
        "cluster_id": cluster_id,
        "created_at": created_at or _utc_timestamp(),
        "status": status,
        "label": label,
        "feature_space": feature_space,
        "member_count": member_count,
        "summary": summary,
        "human_review_required": human_review_required,
    }
    validate_anomaly_cluster_record(record)
    return record


def make_cluster_member_record(
    *,
    cluster_id: str,
    event_id: str,
    trace_id: str,
    anomaly_score: float,
    features: Mapping[str, Any],
    membership_reason: str,
) -> JsonRecord:
    """Build a lightweight anomaly cluster member record."""
    if not isinstance(features, Mapping):
        raise ValueError("features must be a mapping")
    record: JsonRecord = {
        "record_type": "anomaly_cluster_member",
        "cluster_id": cluster_id,
        "event_id": event_id,
        "trace_id": trace_id,
        "anomaly_score": anomaly_score,
        "features": dict(features),
        "membership_reason": membership_reason,
    }
    validate_cluster_member_record(record)
    return record


def make_cluster_consistency_record(
    *,
    cluster_id: str,
    check_name: str,
    status: str,
    details: str,
    weakening_conditions: Sequence[str] | None = None,
    kill_conditions: Sequence[str] | None = None,
) -> JsonRecord:
    """Build a lightweight anomaly cluster consistency check record."""
    record: JsonRecord = {
        "record_type": "anomaly_cluster_consistency",
        "cluster_id": cluster_id,
        "check_name": check_name,
        "status": status,
        "details": details,
        "weakening_conditions": list(weakening_conditions or ()),
        "kill_conditions": list(kill_conditions or ()),
    }
    validate_cluster_consistency_record(record)
    return record


def summarize_cluster(
    cluster_record: Mapping[str, Any],
    member_records: Sequence[Mapping[str, Any]],
    consistency_records: Sequence[Mapping[str, Any]] | None = None,
) -> JsonRecord:
    """Summarize one cluster and its mock member/check records without raw data."""
    validate_anomaly_cluster_record(cluster_record)
    for member_record in member_records:
        validate_cluster_member_record(member_record)
    for consistency_record in consistency_records or ():
        validate_cluster_consistency_record(consistency_record)

    scores = [float(record["anomaly_score"]) for record in member_records]
    summary: JsonRecord = {
        "record_type": "anomaly_cluster_summary",
        "cluster_id": cluster_record["cluster_id"],
        "status": cluster_record["status"],
        "label": cluster_record["label"],
        "feature_space": cluster_record["feature_space"],
        "member_count": len(member_records),
        "declared_member_count": cluster_record["member_count"],
        "human_review_required": cluster_record["human_review_required"],
        "mean_anomaly_score": (sum(scores) / len(scores)) if scores else None,
        "consistency_check_count": len(consistency_records or ()),
    }
    _validate_safe_language(summary)
    return summary


def append_cluster_record(path: str | Path, record: Mapping[str, Any]) -> Path:
    """Append one cluster record to JSONL without reading existing records."""
    validate_anomaly_cluster_record(record)
    return append_jsonl(path, record)


def append_cluster_member(path: str | Path, record: Mapping[str, Any]) -> Path:
    """Append one cluster member record to JSONL without reading existing records."""
    validate_cluster_member_record(record)
    return append_jsonl(path, record)


def append_cluster_consistency(path: str | Path, record: Mapping[str, Any]) -> Path:
    """Append one consistency check record to JSONL without reading existing records."""
    validate_cluster_consistency_record(record)
    return append_jsonl(path, record)
