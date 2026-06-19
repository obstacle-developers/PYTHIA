# PYTHIA Ω Roadmap

PYTHIA Ω is the planned next-stage roadmap for an auditable AI system for discovering, testing, and falsifying candidate new-particle signal patterns in collider data.

The goal is not to let PYTHIA independently declare discoveries. The goal is to build a transparent workflow that can identify candidate signal patterns, test known explanations first, require explicit predictions, apply falsification checks, and produce candidate discovery dossiers for human review.

## Scientific Honesty Requirements

- PYTHIA does not claim new-particle discovery by itself.
- PYTHIA produces candidate discovery dossiers for human review.
- Known explanations must be tested before an unknown candidate is constructed.
- Every candidate must make predictions.
- Every candidate must be falsifiable.
- Candidate status must be updated when background tests, constraint checks, or human review weaken the case.

## Planned Weeks

| Week | Component | Purpose |
|---|---|---|
| 13 | Anomaly Cluster Engine | Group related anomalies into auditable clusters for repeated-pattern analysis. |
| 14 | Signal Fingerprint Extractor | Summarize cluster-level kinematic and phenomenological signatures. |
| 15 | Known Explanation Exhaustion Engine | Test Standard Model, detector, reconstruction, and known beyond-Standard-Model explanations before proposing unknown candidates. |
| 16 | Unknown Candidate Particle Constructor | Construct provisional candidate descriptions only after known explanations are insufficient. |
| 17 | Candidate Prediction Engine | Generate explicit, testable predictions for each surviving candidate. |
| 18 | Candidate Falsification Engine | Define checks that could disconfirm or weaken each candidate. |
| 19 | Background Stress Test Layer | Stress-test candidates against background, systematic, and selection-effect alternatives. |
| 20 | Candidate Discovery Dossier | Assemble auditable candidate dossiers for expert human review. |

## Target Workflow

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
