"""Lightweight consistency checks for mock anomaly clusters.

The checks in this module are deterministic, in-memory helpers for Week 13
cluster review. They avoid dense matrices, external clustering libraries, raw
artifact handling, and interpretation claims.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from numbers import Real
from pathlib import Path
from typing import Any

from pythia.omega.clusters import append_cluster_consistency, make_cluster_consistency_record

JsonRecord = dict[str, Any]


def _cluster_id_from(record: Mapping[str, Any] | None) -> str:
    if record is None:
        return "unknown-cluster"
    cluster_id = record.get("cluster_id", "unknown-cluster")
    return str(cluster_id) if str(cluster_id).strip() else "unknown-cluster"


def _feature_value(record: Mapping[str, Any], key: str) -> Any:
    features = record.get("features")
    if isinstance(features, Mapping) and key in features:
        return features[key]
    return record.get(key)


def _signature_for(record: Mapping[str, Any], signature_keys: Sequence[str]) -> tuple[tuple[str, Any], ...]:
    return tuple((key, _feature_value(record, key)) for key in signature_keys)


def check_min_cluster_size(
    cluster_record: Mapping[str, Any],
    member_records: Sequence[Mapping[str, Any]],
    min_cluster_size: int = 2,
) -> JsonRecord:
    """Check whether a mock cluster has enough members for review."""
    if not isinstance(min_cluster_size, int) or isinstance(min_cluster_size, bool):
        raise ValueError("min_cluster_size must be an integer")
    if min_cluster_size < 0:
        raise ValueError("min_cluster_size must be non-negative")

    member_count = len(member_records)
    passes = member_count >= min_cluster_size
    return make_cluster_consistency_record(
        cluster_id=_cluster_id_from(cluster_record),
        check_name="minimum_cluster_size",
        status="unresolved_anomaly_family" if passes else "insufficient_evidence",
        details=(
            "unresolved anomaly family has enough mock members; requires human review"
            if passes
            else "insufficient evidence from mock member count; requires human review"
        ),
        weakening_conditions=[] if passes else ["weakening condition: mock member count below threshold"],
        kill_conditions=["kill condition: no repeatable mock members remain"],
    )


def check_signature_repetition(
    member_records: Sequence[Mapping[str, Any]], signature_keys: Sequence[str]
) -> JsonRecord:
    """Check whether all members repeat one exact selected feature signature."""
    if not signature_keys:
        raise ValueError("signature_keys must contain at least one key")

    cluster_id = _cluster_id_from(member_records[0] if member_records else None)
    signatures = {_signature_for(record, signature_keys) for record in member_records}
    passes = bool(member_records) and len(signatures) == 1
    return make_cluster_consistency_record(
        cluster_id=cluster_id,
        check_name="signature_repetition",
        status="unresolved_anomaly_family" if passes else "insufficient_evidence",
        details=(
            "candidate pattern repeats the selected exact mock feature signature; requires human review"
            if passes
            else "insufficient evidence because selected exact mock feature signatures are not repeated; requires human review"
        ),
        weakening_conditions=[] if passes else ["weakening condition: mixed mock feature signature values"],
        kill_conditions=["kill condition: selected mock signature does not repeat"],
    )


def check_anomaly_score_floor(
    member_records: Sequence[Mapping[str, Any]], min_score: float
) -> JsonRecord:
    """Check whether every mock member meets a minimum anomaly-score floor."""
    failing_count = 0
    for record in member_records:
        score = record.get("anomaly_score")
        if not isinstance(score, Real) or isinstance(score, bool) or float(score) < min_score:
            failing_count += 1

    cluster_id = _cluster_id_from(member_records[0] if member_records else None)
    passes = bool(member_records) and failing_count == 0
    return make_cluster_consistency_record(
        cluster_id=cluster_id,
        check_name="anomaly_score_floor",
        status="unresolved_anomaly_family" if passes else "insufficient_evidence",
        details=(
            "unresolved anomaly family members meet the mock anomaly score floor; requires human review"
            if passes
            else "insufficient evidence because one or more mock members miss the anomaly score floor; requires human review"
        ),
        weakening_conditions=[] if passes else ["weakening condition: mock anomaly score below floor"],
        kill_conditions=["kill condition: mock anomaly score floor is not met"],
    )


def evaluate_cluster_consistency(
    cluster_record: Mapping[str, Any],
    member_records: Sequence[Mapping[str, Any]],
    signature_keys: Sequence[str],
    min_cluster_size: int = 2,
    min_anomaly_score: float = 0.0,
) -> list[JsonRecord]:
    """Run all lightweight consistency checks without writing files."""
    return [
        check_min_cluster_size(cluster_record, member_records, min_cluster_size),
        check_signature_repetition(member_records, signature_keys),
        check_anomaly_score_floor(member_records, min_anomaly_score),
    ]


def derive_cluster_status(consistency_records: Sequence[Mapping[str, Any]]) -> str:
    """Derive the conservative cluster status from consistency records."""
    if any(record.get("status") == "insufficient_evidence" for record in consistency_records):
        return "insufficient_evidence"
    return "unresolved_anomaly_family"


def append_consistency_records(path: str | Path, records: Sequence[Mapping[str, Any]]) -> Path:
    """Append consistency records to JSONL using cluster JSONL validation."""
    output_path = Path(path)
    for record in records:
        append_cluster_consistency(output_path, record)
    return output_path
