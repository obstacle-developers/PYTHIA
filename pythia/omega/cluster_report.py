"""Week 13 human-review cluster reporting helpers.

The helpers in this module turn mock cluster-engine dictionaries and optional
lightweight consistency checks into a deterministic review report. They do not
write datasets, include raw artifacts, run heavy clustering dependencies, or add
interpretation logic beyond conservative review language.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from pythia.core.export import write_markdown
from pythia.omega.cluster_consistency import derive_cluster_status

JsonRecord = dict[str, Any]

_LIMITATIONS = (
    "mock cluster engine output only; insufficient evidence for physics interpretation",
    "exact feature-signature grouping only; no dense matrix logic or external clustering dependency",
    "cluster consistency checks are review aids, not claims of a signal",
    "does not include raw artifacts or datasets",
)

_NEXT_STEP = "human review required before any later-stage feature work"

_FORBIDDEN_PHRASES = (
    "discov" + "ered",
    "discovery " + "confirmed",
    "new particle",
    "new physics " + "found",
    "proved",
    "certain",
    "guaranteed",
    "confirmed " + "signal",
)


def _safe_text(value: Any) -> str:
    text = str(value)
    lowered = text.lower()
    for phrase in _FORBIDDEN_PHRASES:
        if phrase in lowered:
            raise ValueError(f"unsafe report language is not allowed: {phrase}")
    return text


def _records_by_cluster(records: Sequence[Mapping[str, Any]]) -> dict[str, list[Mapping[str, Any]]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for record in records:
        cluster_id = _safe_text(record.get("cluster_id", "unknown-cluster"))
        grouped.setdefault(cluster_id, []).append(record)
    return grouped


def _normalise_consistency_records(
    consistency_records_by_cluster: Mapping[str, Sequence[Mapping[str, Any]]] | None,
) -> dict[str, list[Mapping[str, Any]]]:
    if consistency_records_by_cluster is None:
        return {}
    return {
        _safe_text(cluster_id): sorted(
            list(records), key=lambda record: (_safe_text(record.get("check_name", "")), repr(sorted(record.items())))
        )
        for cluster_id, records in consistency_records_by_cluster.items()
    }


def _consistency_summary(records_by_cluster: Mapping[str, Sequence[Mapping[str, Any]]]) -> JsonRecord:
    total_checks = 0
    insufficient = 0
    unresolved = 0
    clusters_requiring_review = 0
    by_status: dict[str, int] = {}

    for records in records_by_cluster.values():
        if records:
            clusters_requiring_review += 1
        for record in records:
            total_checks += 1
            status = _safe_text(record.get("status", "insufficient_evidence"))
            by_status[status] = by_status.get(status, 0) + 1
            if status == "insufficient_evidence":
                insufficient += 1
            elif status == "unresolved_anomaly_family":
                unresolved += 1

    return {
        "check_count": total_checks,
        "cluster_count_with_checks": clusters_requiring_review,
        "unresolved_anomaly_family_checks": unresolved,
        "insufficient_evidence_checks": insufficient,
        "by_status": {key: by_status[key] for key in sorted(by_status)},
    }


def build_week13_cluster_report(
    engine_output: Mapping[str, Sequence[Mapping[str, Any]]],
    consistency_records_by_cluster: Mapping[str, Sequence[Mapping[str, Any]]] | None = None,
) -> JsonRecord:
    """Build a deterministic Week 13 cluster report dictionary.

    ``engine_output`` is expected to be the in-memory dictionary returned by
    ``run_mock_cluster_engine``. Optional consistency records should be grouped
    by cluster identifier.
    """
    clusters = sorted(list(engine_output.get("clusters", ())), key=lambda record: _safe_text(record["cluster_id"]))
    members_by_cluster = _records_by_cluster(list(engine_output.get("members", ())))
    consistency = _normalise_consistency_records(consistency_records_by_cluster)

    report_clusters: list[JsonRecord] = []
    for cluster in clusters:
        cluster_id = _safe_text(cluster["cluster_id"])
        checks = consistency.get(cluster_id, [])
        status = derive_cluster_status(checks) if checks else _safe_text(cluster.get("status", "insufficient_evidence"))
        members = sorted(members_by_cluster.get(cluster_id, []), key=lambda record: (_safe_text(record.get("event_id", "")), _safe_text(record.get("trace_id", ""))))
        report_clusters.append(
            {
                "cluster_id": cluster_id,
                "label": _safe_text(cluster.get("label", "unresolved anomaly family")),
                "status": status,
                "feature_space": _safe_text(cluster.get("feature_space", "mock_week13_features_v0")),
                "member_count": len(members),
                "declared_member_count": int(cluster.get("member_count", len(members))),
                "human_review_required": True,
                "summary": _safe_text(cluster.get("summary", "unresolved anomaly family; human review required")),
                "consistency_check_count": len(checks),
                "consistency_status": status if checks else "insufficient_evidence",
            }
        )

    total_members = sum(cluster["member_count"] for cluster in report_clusters)
    summary = _consistency_summary(consistency)
    report_status = "insufficient_evidence" if summary["insufficient_evidence_checks"] else "unresolved_anomaly_family"

    return {
        "report_type": "week13_cluster_report",
        "stage": "Week 13 cluster report integration",
        "status": report_status,
        "cluster_count": len(report_clusters),
        "member_count": total_members,
        "clusters": report_clusters,
        "consistency_summary": summary,
        "human_review_required": True,
        "limitations": list(_LIMITATIONS),
        "next_step": _NEXT_STEP,
    }


def render_week13_cluster_report_markdown(report: Mapping[str, Any]) -> str:
    """Render a Week 13 cluster report as deterministic Markdown."""
    lines = [
        "# Week 13 Cluster Report",
        "",
        f"- Report type: `{_safe_text(report.get('report_type', 'week13_cluster_report'))}`",
        f"- Stage: {_safe_text(report.get('stage', 'Week 13 cluster report integration'))}",
        f"- Status: {_safe_text(report.get('status', 'insufficient_evidence'))}",
        f"- Cluster count: {int(report.get('cluster_count', 0))}",
        f"- Member count: {int(report.get('member_count', 0))}",
        "- Review gate: human review required",
        "",
        "This report treats each cluster as an unresolved anomaly family. It is a candidate pattern review aid with insufficient evidence for interpretation.",
        "",
        "## Clusters",
    ]
    for cluster in report.get("clusters", ()):
        lines.extend(
            [
                "",
                f"### {_safe_text(cluster.get('cluster_id', 'unknown-cluster'))}",
                f"- Label: {_safe_text(cluster.get('label', 'unresolved anomaly family'))}",
                f"- Status: {_safe_text(cluster.get('status', 'insufficient_evidence'))}",
                f"- Feature space: {_safe_text(cluster.get('feature_space', 'mock_week13_features_v0'))}",
                f"- Members: {int(cluster.get('member_count', 0))}",
                f"- Consistency checks: {int(cluster.get('consistency_check_count', 0))}",
                f"- Summary: {_safe_text(cluster.get('summary', 'unresolved anomaly family; human review required'))}",
                "- Review: requires human review",
            ]
        )
    summary = report.get("consistency_summary", {})
    lines.extend([
        "",
        "## Consistency summary",
        f"- Checks: {int(summary.get('check_count', 0))}",
        f"- Checks with insufficient evidence: {int(summary.get('insufficient_evidence_checks', 0))}",
        f"- Checks supporting unresolved anomaly family review: {int(summary.get('unresolved_anomaly_family_checks', 0))}",
        "",
        "## Limitations",
    ])
    for limitation in report.get("limitations", ()):
        lines.append(f"- {_safe_text(limitation)}")
    lines.extend(["", "## Next step", f"- {_safe_text(report.get('next_step', _NEXT_STEP))}", ""])
    return "\n".join(lines)


def write_week13_cluster_report(report: Mapping[str, Any], output_path: str | Path) -> Path:
    """Write the rendered Markdown report to ``output_path`` only."""
    path = Path(output_path)
    return write_markdown(path.parent or Path("."), path.name, render_week13_cluster_report_markdown(report))


def build_and_render_week13_report(
    engine_output: Mapping[str, Sequence[Mapping[str, Any]]],
    consistency_records_by_cluster: Mapping[str, Sequence[Mapping[str, Any]]] | None = None,
) -> tuple[JsonRecord, str]:
    """Build and render the Week 13 report in one deterministic step."""
    report = build_week13_cluster_report(engine_output, consistency_records_by_cluster)
    return report, render_week13_cluster_report_markdown(report)
