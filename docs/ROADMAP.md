# PYTHIA Roadmap

PYTHIA is being developed as a physics-aware anomaly detection and auditable scientific reasoning infrastructure for high-energy particle collision data.

## Current Status

Weeks 1 through 10 are complete.

Current classification:

```text
Working research prototype
Physics-aware anomaly analysis platform
Early scientific reasoning infrastructure
```

PYTHIA is not yet an autonomous scientist and does not claim particle discovery. It currently demonstrates a complete auditable reasoning trace for one top LHCO anomaly.

## Completed Phase 1 — Month 1: Detection and Interpretation

### Week 1 — Foundation Pipeline ✅

Built:

- Synthetic/event processing pipeline
- Frozen feature schema v0.1
- Feature extraction
- Isolation Forest baseline
- PercentileEstimator
- Evaluation framework
- SQLite knowledge graph
- Logging and provenance
- Report generation

### Week 2 — Real LHCO Benchmark ✅

Built:

- LHCO anomaly benchmark integration
- Real benchmark evaluation
- Background/signal split handling

Result:

```text
AUC-ROC: 0.74
Precision@100: 0.13
Best Signal Rank: 5
```

### Week 3 — Jet Substructure Features ✅

Built:

- jet1_mass
- jet2_mass
- jet1_tau21
- jet2_tau21
- mass_asymmetry
- pt_asymmetry

Result:

```text
AUC-ROC: 0.771
Precision@100: 0.190
Best Signal Rank: 1
```

### Week 4 — Physics Translator ✅

Built:

- Rule-based physics translator
- Anomaly severity labels
- Human-readable anomaly reports
- Knowledge graph interpretations

Result:

```text
100 anomaly reports generated
0 empty summaries
19 signal events in top 100
100 interpretations stored
```

## Completed Phase 2 — Scientific Reasoning Chain

### Week 5 — Phenomenology Layer ✅

Built:

- Controlled phenomenology vocabulary
- Evidence-to-phenomenology mapping
- Phenomenology records in KG

Example signature:

```text
boosted_diboson
```

### Week 6 — Constraint Engine v1 ✅

Built:

- `theories` table
- `constraints` table
- `rejections` table
- `survivors` table
- Structured condition schema
- Data-driven constraints
- Citation-backed rejection records

First cited rejection:

```text
Theory: dark_photon
Constraint: dp_diboson_topology
Source: hep-ex/0312023
```

Final Week 6 audit:

```text
theories: 6
constraints: 3
rejections: 1
survivors: 3
```

### Week 7 — Theory Retrieval v1 ✅

Built:

- `theory_signature_links` table
- `theory_retrievals` table
- Data-driven retrieval mappings
- Relevance scoring

Top anomaly retrieval:

```text
1. w_prime       relevance_score 0.9900
2. rs_graviton  relevance_score 0.9400
3. heavy_higgs  relevance_score 0.6900
4. dark_photon  relevance_score 0.3900
```

### Week 8 — Theory Ranking + Recommendation ✅

Built:

- `theory_rankings` table
- `recommendation_templates` table
- `recommendations` table
- Survivor-only ranking
- Deterministic follow-up recommendation

Ranked survivors:

```text
1. w_prime
2. rs_graviton
3. heavy_higgs
```

Recommendation:

```text
Prioritize a W Prime-style boosted diboson follow-up: inspect dijet/diboson invariant mass, jet mass symmetry, and two-prong substructure consistency.
```

### Week 9 — Source Registry v1 ✅

Built:

- `sources` table
- `source_links` table
- `source_retrievals` table
- Source registry for constraints, retrieval mappings, and recommendations

Registered source labels:

```text
hep-ex/0312023
CMS-HIG-19-009
CMS-EXO-19-016
curated_mapping_v0.7
recommendation_rules_v1.0
```

Final Week 9 audit:

```text
sources: 5
source_links: 9
source_retrievals: 3
```

### Week 10 — Full Reasoning Trace Assembly ✅

Built:

- `reasoning_traces` table
- `reasoning_trace_nodes` table
- `reasoning_trace_edges` table
- `reasoning_trace_exports` table
- JSON reasoning trace export
- Markdown reasoning trace report
- Google Drive trace backup

Trace:

```text
Trace ID: trace_interp_rank_001_v1
Anomaly ID: interp_rank_001
Phenomenology: boosted_diboson
Completeness Score: 1.0
Status: PASS
```

Current full chain:

```text
interp_rank_001
→ boosted_diboson
→ retrieve w_prime, rs_graviton, heavy_higgs, dark_photon
→ reject dark_photon with source hep-ex/0312023
→ rank w_prime, rs_graviton, heavy_higgs
→ recommend W Prime-style boosted diboson follow-up
→ export source-linked reasoning trace
```

## Current Next Step — Pre-Week 11 Readiness Gate

Before Week 11 begins, two checks must be completed:

1. Resolve the previous `eval/exec` UNKNOWN audit status.
2. Run the completed reasoning chain on the top 10 anomalies, not only `interp_rank_001`.

The project should not proceed to new capability development until this readiness gate passes.

## Planned Week 11 — Reasoning Trace Evaluation v1

Goal:

Evaluate reasoning traces for quality, consistency, and auditability.

Planned checks:

- Trace completeness
- Internal consistency
- Missing evidence
- Missing sources
- Rejected theory linked to constraint
- Survivor not also rejected
- Ranking only includes survivors
- Recommendation matches top-ranked survivor or fallback template
- Source bundle covers rejection, retrieval, and recommendation
- No probability language
- No hidden physics decision
- No contradiction between trace nodes
- Cross-trace consistency

Expected output:

```text
Reasoning Trace Evaluation Report
Trace quality score
PASS / PATCH REQUIRED decision
```

## Future Roadmap

### Week 12 — Integrated Scientific Report v1

Generate polished scientific reports from validated reasoning traces.

### Month 4 — Literature Verification Layer

Replace placeholder/needs-review metadata with verified source metadata where possible.

### Month 5 — Expanded Constraint Database

Add more theory classes, experimental bounds, topology constraints, and detector consistency checks.

### Month 6 — Cross-Anomaly Scientific Memory

Compare multiple anomalies and detect repeated phenomenology/theory patterns.

### Later Research Directions

- Literature-aware retrieval
- Constraint contradiction detection
- Cross-experiment consistency checks
- Multi-dataset validation
- Hypothesis generation after strong constraint validation
- Experiment design recommendations

## Long-Term Vision

A mature PYTHIA should help answer:

```text
What was observed?
Why is it unusual?
What explanations are possible?
Which explanations fail?
Why do they fail?
Which explanations survive?
What should be checked next?
Which sources support each step?
```

PYTHIA is not intended to replace physicists. It is intended to structure and accelerate the reasoning workflow they already use.
