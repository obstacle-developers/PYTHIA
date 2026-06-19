# PYTHIA Architecture

PYTHIA is a physics-aware anomaly detection and scientific reasoning infrastructure for high-energy particle collision data.

The project began as an anomaly detection pipeline and has evolved into an auditable reasoning system. The current v1 architecture preserves the path from event observation to evaluated scientific report. The future PYTHIA Ω architecture extends this into a candidate workflow that requires known-explanation testing, explicit predictions, falsification checks, and human review.

## Current v1 Architecture

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
→ Trace Evaluation
→ Scientific Report
```

## Future PYTHIA Ω Architecture

```text
Collision Data
→ Anomaly Detection
→ Anomaly Clustering
→ Signal Fingerprint Extraction
→ Known Explanation Testing
→ Unknown Candidate Particle Constructor
→ Prediction Engine
→ Falsification Engine
→ Background Stress Test
→ Candidate Survivor Update
→ Discovery Dossier
→ Human Review
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
11. PYTHIA does not claim a new-particle discovery by itself.
12. Candidate dossiers require human review.
13. Known explanations must be tested before unknown candidates are constructed.
14. Every candidate must make predictions and be falsifiable.

## Current Completed Layers

### 1. Data and Feature Layer

- LHCO anomaly benchmark integration.
- Physics-aware feature extraction.
- Jet mass, tau21, mass asymmetry, and pT asymmetry features.
- Percentile estimation for anomaly interpretation.

### 2. Anomaly Detection Layer

- Isolation Forest baseline.
- Benchmark performance:
  - AUC-ROC: 0.771
  - Precision@100: 0.190
  - Best Signal Rank: 1
  - Signal events in top 100: 19

### 3. Physics Translation Layer

- Rule-based translation from unusual feature values into physicist-readable descriptions.
- 100 anomaly reports generated.
- 0 empty summaries.
- 100 interpretations stored in the knowledge graph.

### 4. Evidence and Phenomenology Layer

Evidence grounds reasoning in observed values and percentiles, then maps those observations into controlled physics signatures such as:

```text
boosted_diboson
heavy_resonance
high_mass_dijet
two_prong_jet
boosted_object
qcd_outlier
```

### 5. Theory Retrieval Layer

Retrieves candidate theories from data-driven theory-signature links. Retrieval suggests candidates for evaluation; it does not decide truth.

### 6. Constraint Evaluation Layer

Applies structured constraints stored as data. Rejections require source linkage and survivors are preserved separately from rejected candidates.

### 7. Ranking and Recommendation Layer

Ranks only surviving candidates and generates deterministic follow-up recommendations from templates. Ranking and recommendation are workflow outputs, not discovery claims.

### 8. Source Bundle Layer

Links constraints, retrieval mappings, recommendations, and trace outputs to source records. External sources remain subject to review unless metadata has been verified.

### 9. Reasoning Trace Layer

Assembles each anomaly workflow into a source-linked reasoning trace containing anomaly, phenomenology, retrieval, rejection, survivor, ranking, recommendation, and source nodes.

Week 10.5 scaled this layer to 10 traces with status **PASS**.

### 10. Trace Evaluation Layer

Week 11 evaluated the scaled trace set:

```text
traces evaluated: 10
trace evaluation checks: 140
cross-trace evaluations: 3
trace quality scores: 1.0000
status: PASS
```

### 11. Scientific Report Layer

Week 12 generated the integrated scientific report and verified it with status **VERIFIED PASS**.

Verified source DB counts:

```text
reasoning_traces: 10
trace_evaluations: 10
trace_evaluation_checks: 140
cross_trace_evaluations: 3
recommendations: 10
source_retrievals: 33
```

## PYTHIA Ω Planned Layers

### Week 13 — Anomaly Cluster Engine

Group related anomalies into auditable clusters for repeated-pattern analysis.

### Week 14 — Signal Fingerprint Extractor

Extract cluster-level kinematic and phenomenological signatures.

### Week 15 — Known Explanation Exhaustion Engine

Test known Standard Model, detector, reconstruction, and known beyond-Standard-Model alternatives before unknown candidate construction.

### Week 16 — Unknown Candidate Particle Constructor

Construct provisional unknown-candidate descriptions only after known explanations are insufficient.

### Week 17 — Candidate Prediction Engine

Require every candidate to produce explicit, testable predictions.

### Week 18 — Candidate Falsification Engine

Define checks that could disconfirm or weaken each candidate.

### Week 19 — Background Stress Test Layer

Stress-test candidates against background, systematic, and selection-effect explanations.

### Week 20 — Candidate Discovery Dossier

Assemble auditable candidate dossiers for expert human review.

## Current Status

PYTHIA v1 is complete through Week 12. The next target is PYTHIA Ω Week 13 — Anomaly Cluster Engine.
