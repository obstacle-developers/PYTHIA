# Changelog

## v0.3-week10

Status: Weeks 1 through 10 complete.

Added:
- Week 9 Source Registry v1.
- Week 10 Full Reasoning Trace Assembly v1.
- `sources`, `source_links`, and `source_retrievals` tables.
- `reasoning_traces`, `reasoning_trace_nodes`, `reasoning_trace_edges`, and `reasoning_trace_exports` tables.
- Source-linked JSON and Markdown reasoning trace export.
- Documentation for Week 10 reasoning trace.
- Documentation for Pre-Week 11 readiness gate.

Current top reasoning trace:
- Trace ID: `trace_interp_rank_001_v1`
- Anomaly ID: `interp_rank_001`
- Phenomenology: `boosted_diboson`
- Completeness score: `1.0`
- Status: PASS

Current reasoning chain:
```text
interp_rank_001
→ boosted_diboson
→ retrieve w_prime, rs_graviton, heavy_higgs, dark_photon
→ reject dark_photon with source hep-ex/0312023
→ rank w_prime, rs_graviton, heavy_higgs
→ recommend W Prime-style boosted diboson follow-up
→ export source-linked reasoning trace
```

Registered source labels:
- `hep-ex/0312023`
- `CMS-HIG-19-009`
- `CMS-EXO-19-016`
- `curated_mapping_v0.7`
- `recommendation_rules_v1.0`

Pre-Week 11 requirement:
- Resolve the prior `eval/exec` UNKNOWN audit status.
- Expand the completed reasoning chain to the top 10 anomalies.
- Run cross-trace consistency checks before building the Week 11 evaluator.

## v0.2-month2

Status: Completed scientific reasoning chain through ranking and recommendation.

Added:
- Week 5 Phenomenology Layer.
- Week 6 Constraint Engine v1.
- Week 7 Theory Retrieval v1.
- Week 8 Theory Ranking + Recommendation.
- Controlled phenomenology signatures.
- Data-driven theory-signature links.
- Structured SQLite constraints.
- Citation-backed rejection records.
- Survivor storage.
- Survivor-only ranking.
- Deterministic recommendation templates.

First cited rejection:
- Rejected theory: `dark_photon`
- Constraint: `dp_diboson_topology`
- Source: `hep-ex/0312023`

Retrieved candidates for top anomaly:
```text
1. w_prime       relevance_score 0.9900
2. rs_graviton  relevance_score 0.9400
3. heavy_higgs  relevance_score 0.6900
4. dark_photon  relevance_score 0.3900
```

Ranked survivors:
```text
1. w_prime       ranking_score 0.9900
2. rs_graviton  ranking_score 0.9400
3. heavy_higgs  ranking_score 0.6900
```

Recommendation:
```text
Prioritize a W Prime-style boosted diboson follow-up: inspect dijet/diboson invariant mass, jet mass symmetry, and two-prong substructure consistency.
```

## v0.1-month1

Status: Completed anomaly detection and interpretation foundation.

Added:
- Week 1 foundation pipeline.
- Week 2 real LHCO benchmark integration.
- Week 3 jet substructure features.
- Week 4 physics translator.
- Isolation Forest baseline.
- Percentile-based anomaly interpretation.
- SQLite knowledge graph.
- Human-readable anomaly reports.

Metrics:
- AUC-ROC: 0.771
- Precision@100: 0.190
- Best Signal Rank: 1
- Signal events in top 100: 19

Week 4 output:
- 100 anomaly reports generated.
- 0 empty summaries.
- 100 KG interpretations stored.
