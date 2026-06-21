"""Lightweight anomaly cluster record interfaces for PYTHIA Ω.

This module defines typed, append-only record helpers for anomaly cluster
interfaces. It intentionally does not run clustering algorithms, construct
candidate particles, or attach raw artifacts.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
import re
from typing import Any

from pythia.core.jsonl import append_jsonl, validate_record_has_keys

JsonValue = Any
JsonRecord = dict[str, JsonValue]

ALLOWED_CLUSTER_STATUSES = (
    "candidate_pattern",
    "unresolved_anomaly_family",
    "requires_review",
    "rejected_pattern",
    "insufficient_evidence",
)

FORBIDDEN_UNSAFE_PHRASES = (
    "new particle " + "discovered",
    "discovery " + "confirmed",
    "new physics " + "found",
    "proved",
    "certain",
    "guaranteed",
    "confirmed " + "signal",
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


def _unsafe_phrases_in_value(value: Any) -> list[str]:
    if isinstance(value, str):
        lowered = value.lower()
        return [
            phrase
            for phrase in FORBIDDEN_UNSAFE_PHRASES
            if re.search(rf"(?<![a-z0-9_]){re.escape(phrase)}(?![a-z0-9_])", lowered)
        ]
    if isinstance(value, Mapping):
        findings: list[str] = []
        for key, nested_value in value.items():
            findings.extend(_unsafe_phrases_in_value(key))
            findings.extend(_unsafe_phrases_in_value(nested_value))
        return findings
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        findings = []
        for nested_value in value:
            findings.extend(_unsafe_phrases_in_value(nested_value))
        return findings
    return []


def _validate_safe_language(record: Mapping[str, Any]) -> None:
    findings = sorted(set(_unsafe_phrases_in_value(record)))
    if findings:
        raise ValueError(f"unsafe discovery language is not allowed: {', '.join(findings)}")


def _validate_cluster_status(status: str) -> None:
    if status not in ALLOWED_CLUSTER_STATUSES:
        allowed = ", ".join(ALLOWED_CLUSTER_STATUSES)
        raise ValueError(f"invalid cluster status {status!r}; expected one of: {allowed}")


def _validate_required_record(record: Mapping[str, Any], required_keys: Sequence[str]) -> None:
    validate_record_has_keys(record, required_keys)
    _validate_safe_language(record)


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
    _validate_cluster_status(status)
    if member_count < 0:
        raise ValueError("member_count must be non-negative")
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
    _validate_required_record(record, CLUSTER_RECORD_KEYS)
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
    record: JsonRecord = {
        "record_type": "anomaly_cluster_member",
        "cluster_id": cluster_id,
        "event_id": event_id,
        "trace_id": trace_id,
        "anomaly_score": float(anomaly_score),
        "features": dict(features),
        "membership_reason": membership_reason,
    }
    _validate_required_record(record, CLUSTER_MEMBER_RECORD_KEYS)
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
    _validate_cluster_status(status)
    record: JsonRecord = {
        "record_type": "anomaly_cluster_consistency",
        "cluster_id": cluster_id,
        "check_name": check_name,
        "status": status,
        "details": details,
        "weakening_conditions": list(weakening_conditions or ()),
        "kill_conditions": list(kill_conditions or ()),
    }
    _validate_required_record(record, CLUSTER_CONSISTENCY_RECORD_KEYS)
    return record


def summarize_cluster(
    cluster_record: Mapping[str, Any],
    member_records: Sequence[Mapping[str, Any]],
    consistency_records: Sequence[Mapping[str, Any]] | None = None,
) -> JsonRecord:
    """Summarize one cluster and its mock member/check records without raw data."""
    _validate_required_record(cluster_record, CLUSTER_RECORD_KEYS)
    for member_record in member_records:
        _validate_required_record(member_record, CLUSTER_MEMBER_RECORD_KEYS)
    for consistency_record in consistency_records or ():
        _validate_required_record(consistency_record, CLUSTER_CONSISTENCY_RECORD_KEYS)

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
    _validate_required_record(record, CLUSTER_RECORD_KEYS)
    return append_jsonl(path, record)


def append_cluster_member(path: str | Path, record: Mapping[str, Any]) -> Path:
    """Append one cluster member record to JSONL without reading existing records."""
    _validate_required_record(record, CLUSTER_MEMBER_RECORD_KEYS)
    return append_jsonl(path, record)


def append_cluster_consistency(path: str | Path, record: Mapping[str, Any]) -> Path:
    """Append one consistency check record to JSONL without reading existing records."""
    _validate_required_record(record, CLUSTER_CONSISTENCY_RECORD_KEYS)
    return append_jsonl(path, record)
