# PYTHIA Architecture

PYTHIA is a physics-aware anomaly detection and scientific reasoning infrastructure for high-energy particle collision data.

The project began as an anomaly detection pipeline and has evolved into an auditable reasoning system. The current architecture is designed to preserve every major step from event observation to source-linked recommendation.

## Frozen Architecture v1.0

```text
Event
→ Feature
→ Anomaly
→ Evidence
→ Phenomenology
→ Theory Retrieval
→ Constraint Evaluation
→ Rejection / Survivor
→ Ranking
→ Recommendation
→ Source Bundle
→ Reasoning Trace
```

## Governing Rules

1. No LLM decides physics truth.
2. Every rejection requires provenance.
3. Store rejected theories, not only survivors.
4. No hidden reasoning.
5. Constraints are data.
6. The evaluator is code.
7. Retrieval scores are relevance scores, not probabilities.
8. Ranking scores are ordering scores, not probabilities.
9. Recommendations suggest follow-up analysis, not discovery claims.
10. Every reasoning step must be auditable.

## Current Completed Layers

### 1. Data and Feature Layer

- Real LHCO anomaly benchmark integration.
- Physics-aware feature extraction.
- Jet mass, tau21, mass asymmetry, and pT asymmetry features.
- Percentile estimation for anomaly interpretation.

### 2. Anomaly Detection Layer

- Isolation Forest baseline.
- Real benchmark performance:
  - AUC-ROC: 0.771
  - Precision@100: 0.190
  - Best Signal Rank: 1
  - Signal events in top 100: 19

### 3. Physics Translation Layer

- Rule-based translation from unusual feature values into physicist-readable descriptions.
- 100 anomaly reports generated.
- 0 empty summaries.
- 100 interpretations stored in the knowledge graph.

### 4. Evidence Layer

Evidence grounds reasoning in observed values and percentiles. It links detector-level quantities to later interpretation steps.

Example:

```text
jet1_mass = 1123 GeV
percentile ≈ extreme
→ evidence for unusually massive jet
```

### 5. Phenomenology Layer

Maps evidence into controlled physics signatures.

Examples:

```text
boosted_diboson
heavy_resonance
high_mass_dijet
two_prong_jet
boosted_object
qcd_outlier
```

### 6. Theory Retrieval Layer

Retrieves candidate theories from data-driven theory-signature links.

Current top-anomaly retrieval for `interp_rank_001`:

```text
1. w_prime       relevance_score 0.9900
2. rs_graviton  relevance_score 0.9400
3. heavy_higgs  relevance_score 0.6900
4. dark_photon  relevance_score 0.3900
```

Retrieval only suggests candidates. It does not decide truth.

### 7. Constraint Engine

Applies structured constraints stored as SQLite data. The evaluator is code and must not use unsafe `eval()` or `exec()`.

First cited rejection:

```text
Rejected theory: dark_photon
Constraint: dp_diboson_topology
Reason: dark_photon rejected by dp_diboson_topology
Source: hep-ex/0312023
Version: constraint_db_v1.0
```

Survivors:

```text
w_prime
rs_graviton
heavy_higgs
```

### 8. Ranking Layer

Ranks only surviving theories. Rejected theories are excluded.

Current ranked survivors:

```text
1. w_prime       ranking_score 0.9900
2. rs_graviton  ranking_score 0.9400
3. heavy_higgs  ranking_score 0.6900
```

### 9. Recommendation Layer

Generates deterministic follow-up recommendations from templates.

Current recommendation:

```text
Prioritize a W Prime-style boosted diboson follow-up: inspect dijet/diboson invariant mass, jet mass symmetry, and two-prong substructure consistency.
```

### 10. Source Registry Layer

Converts citation strings and internal mappings into structured source records and links.

Current registered source labels:

```text
hep-ex/0312023
CMS-HIG-19-009
CMS-EXO-19-016
curated_mapping_v0.7
recommendation_rules_v1.0
```

External sources are marked `needs_review` unless metadata is verified. Internal mappings are marked `placeholder`.

### 11. Reasoning Trace Layer

Assembles the full chain into one exportable scientific reasoning object.

Current trace:

```text
Trace ID: trace_interp_rank_001_v1
Anomaly ID: interp_rank_001
Phenomenology: boosted_diboson
Completeness Score: 1.0
Status: PASS
```

Trace includes:

```text
anomaly node
phenomenology node
retrieval nodes
rejection node
survivor / ranking nodes
recommendation node
source nodes
reasoning edges
```

## Current End-to-End Reasoning Chain

```text
Anomaly: interp_rank_001
→ Phenomenology: boosted_diboson
→ Retrieved: w_prime, rs_graviton, heavy_higgs, dark_photon
→ Rejected: dark_photon
→ Constraint: dp_diboson_topology
→ Source: hep-ex/0312023
→ Survivors: w_prime, rs_graviton, heavy_higgs
→ Ranked top survivor: w_prime
→ Recommendation: W Prime-style boosted diboson follow-up
→ Source-linked reasoning trace exported
```

## Current Status

PYTHIA has completed Weeks 1 through 10 and is now an early auditable scientific reasoning infrastructure prototype.

Next step: Week 11 — Reasoning Trace Evaluation v1.

Week 11 should evaluate whether traces are complete, internally consistent, source-linked, non-contradictory, and scientifically useful before adding new capabilities.
