"""Tiny deterministic mock anomaly cluster grouping helpers.

This module groups mock anomaly trace dictionaries by exact feature signatures.
It intentionally avoids heavy clustering algorithms, dense matrices, raw artifact
handling, and physics interpretation logic.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import json
from pathlib import Path
from typing import Any

from pythia.omega.clusters import (
    append_cluster_member,
    append_cluster_record,
    make_anomaly_cluster_record,
    make_cluster_member_record,
    summarize_cluster,
)

JsonRecord = dict[str, Any]
GroupedSignature = dict[str, Any]


def _stable_value(value: Any) -> str:
    """Return a deterministic representation for sorting mock values."""
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    except TypeError:
        return repr(value)


def _feature_value(record: Mapping[str, Any], key: str) -> Any:
    features = record.get("features")
    if isinstance(features, Mapping) and key in features:
        return features[key]
    return record.get(key)


def _record_sort_key(record: Mapping[str, Any]) -> tuple[str, str, str]:
    return (
        _stable_value(record.get("event_id", "")),
        _stable_value(record.get("trace_id", "")),
        _stable_value(record),
    )


def group_by_signature(
    records: Sequence[Mapping[str, Any]], signature_keys: Sequence[str]
) -> list[GroupedSignature]:
    """Group mock anomaly records by exact selected feature-key signatures.

    The return value is a list sorted by signature, and records inside each group
    are sorted by stable identifiers. Missing keys are represented as ``None`` so
    repeated calls over the same inputs produce the same grouping.
    """
    if not signature_keys:
        raise ValueError("signature_keys must contain at least one key")

    groups: dict[tuple[tuple[str, str], ...], GroupedSignature] = {}
    for record in records:
        if not isinstance(record, Mapping):
            raise TypeError("records must contain mappings")
        signature = {key: _feature_value(record, key) for key in signature_keys}
        sort_signature = tuple((key, _stable_value(signature[key])) for key in signature_keys)
        groups.setdefault(sort_signature, {"signature": signature, "records": []})["records"].append(
            dict(record)
        )

    grouped = [groups[key] for key in sorted(groups)]
    for group in grouped:
        group["records"] = sorted(group["records"], key=_record_sort_key)
    return grouped


def _features_for_member(record: Mapping[str, Any]) -> dict[str, Any]:
    features = record.get("features")
    if isinstance(features, Mapping):
        return dict(features)
    return {
        key: value
        for key, value in record.items()
        if key not in {"event_id", "trace_id", "anomaly_score"}
    }


def build_cluster_records(
    grouped_records: Sequence[Mapping[str, Any]],
    feature_space: str,
    status: str = "unresolved_anomaly_family",
) -> dict[str, list[JsonRecord]]:
    """Create safe cluster and member records from grouped mock signatures."""
    clusters: list[JsonRecord] = []
    members: list[JsonRecord] = []

    for index, group in enumerate(grouped_records, start=1):
        records = list(group.get("records", ()))
        signature = dict(group.get("signature", {}))
        cluster_id = f"mock-anomaly-family-{index:03d}"
        cluster = make_anomaly_cluster_record(
            cluster_id=cluster_id,
            status=status,
            label=f"mock anomaly signature group {index:03d}",
            feature_space=feature_space,
            member_count=len(records),
            summary="mock anomaly family grouped by exact feature signature; requires human review",
            human_review_required=True,
        )
        clusters.append(cluster)

        for member_index, record in enumerate(records, start=1):
            member = make_cluster_member_record(
                cluster_id=cluster_id,
                event_id=str(record.get("event_id", f"mock-event-{index:03d}-{member_index:03d}")),
                trace_id=str(record.get("trace_id", f"mock-trace-{index:03d}-{member_index:03d}")),
                anomaly_score=float(record.get("anomaly_score", 0.0)),
                features=_features_for_member(record),
                membership_reason="exact mock feature signature match; requires human review",
            )
            members.append(member)

    return {"clusters": clusters, "members": members}


def run_mock_cluster_engine(
    records: Sequence[Mapping[str, Any]], signature_keys: Sequence[str], feature_space: str
) -> dict[str, Any]:
    """Run the tiny in-memory mock cluster pipeline and return dictionaries only."""
    grouped = group_by_signature(records, signature_keys)
    built = build_cluster_records(grouped, feature_space)
    summaries = [
        summarize_cluster(
            cluster,
            [member for member in built["members"] if member["cluster_id"] == cluster["cluster_id"]],
        )
        for cluster in built["clusters"]
    ]
    return {"grouped_records": grouped, **built, "summaries": summaries}


def append_cluster_engine_output(
    output: Mapping[str, Sequence[Mapping[str, Any]]], cluster_path: str | Path, member_path: str | Path
) -> dict[str, Path]:
    """Append cluster-engine cluster/member records to JSONL paths."""
    for cluster in output.get("clusters", ()):
        append_cluster_record(cluster_path, cluster)
    for member in output.get("members", ()):
        append_cluster_member(member_path, member)
    return {"cluster_path": Path(cluster_path), "member_path": Path(member_path)}
