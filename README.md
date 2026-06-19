# PYTHIA

**An Autonomous Scientific Reasoning System for Particle Physics**

## Current Project Status

PYTHIA v1 has completed its auditable reasoning pipeline through Week 12. The Week 12 Integrated Scientific Report has been verified with status **VERIFIED PASS**.

The project is now moving toward **PYTHIA Ω**, an auditable candidate new-particle discovery workflow. This roadmap is designed to detect, cluster, test, falsify, and document candidate signal patterns for human review.

Important limitation: PYTHIA does **not** claim a new-particle discovery by itself. No particle discovery is claimed, and the current project state does not establish evidence for new physics.

---

## What Is PYTHIA

PYTHIA is not a classifier. It is not a chatbot. It is not a black box.

PYTHIA is a **scientific reasoning infrastructure** that:

- Detects anomalous particle collision events in real LHC data
- Interprets what makes each event physically unusual
- Retrieves candidate theoretical explanations
- Applies physics constraints with cited sources to eliminate theories
- Ranks surviving theories by evidence
- Recommends follow-up analysis
- Stores every decision in an auditable knowledge graph

Every conclusion PYTHIA produces can be traced back to evidence.
Every rejection cites a real physics paper.
Every reasoning step is stored, versioned, and reproducible.

---

## Why It Matters

Current AI in particle physics does this:

```
Data → Model → Score
```

PYTHIA does this:

```
Data
 ↓
Features
 ↓
Anomaly Detection
 ↓
Evidence
 ↓
Phenomenology
 ↓
Theory Retrieval
 ↓
Constraint Evaluation → Rejection (with citation)
 ↓
Surviving Theories
 ↓
Ranking
 ↓
Recommendation
 ↓
Auditable Reasoning Trace
```

The difference is not performance.
The difference is **trustworthiness**.

A system that shows its work is more useful to a physicist
than a system that merely scores higher.

---

## Core Architecture Principles

```
1. No LLM decides physics truth
2. Every rejection requires provenance
3. Store rejected theories — they are scientific results
4. No hidden reasoning
5. Constraints are data
6. Evaluator is code
7. Every reasoning step must be auditable
8. Retrieval scores are relevance, not probability
9. Ranking scores are ordering, not probability
10. Recommendation suggests follow-up, not discovery claims
```

---

## Dataset

**LHCO 2020 R&D Dataset**
- 1.1 million simulated proton-proton collision events
- Background: 1,000,000 QCD dijet events
- Signal: 100,000 W' → XY → 4 quarks events
- Source: [Zenodo 4536377](https://zenodo.org/records/4536377)

---

## Current Results

| Metric | Value |
|---|---|
| AUC-ROC | 0.771 |
| Precision@100 | 0.190 |
| Best Signal Rank | 1 |
| Signal in top 100 | 19 |
| Reasoning traces | 10 complete |
| Week 12 report status | VERIFIED PASS |
| Trace quality scores | 1.0000 |
| Next target | PYTHIA Ω Week 13 — Anomaly Cluster Engine |

---

## First Auditable Reasoning Chain

```
Observed:
Two-prong boosted jets at 2700 GeV

Phenomenology:
Boosted Diboson Candidate

Retrieved:
W', RS Graviton, Heavy Higgs, Dark Photon

Rejected:
Dark Photon
Reason:  Boosted diboson topology inconsistent
         with dark photon explanation
Citation: hep-ex/0312023
Confidence: 0.95

Survivors:
W', RS Graviton, Heavy Higgs

Ranked:
1. W'
2. RS Graviton
3. Heavy Higgs

Recommendation:
Inspect diboson invariant mass, jet mass symmetry,
and two-prong substructure consistency.
```

---

## Progress

| Week | Objective | Status |
|---|---|---|
| 1 | End-to-end anomaly pipeline | ✅ |
| 2 | LHCO dataset integration | ✅ |
| 3 | Jet substructure features | ✅ |
| 4 | Physics Translator | ✅ |
| 5 | Phenomenology Layer | ✅ |
| 6 | Constraint Engine v1 | ✅ |
| 7 | Theory Retrieval v1 | ✅ |
| 8 | Theory Ranking + Recommendation | ✅ |
| 9 | Source Registry v1 | ✅ |
| 10 | Full Reasoning Trace Assembly | ✅ |
| 10.5 | Scaling Patch | ✅ |
| 11 | Reasoning Trace Evaluator | ✅ |
| 12 | Integrated Scientific Report | ✅ |
| 13 | PYTHIA Ω Anomaly Cluster Engine | Planned |

---

## Roadmap

```
Month 1 (Weeks 1-4):   Detection + Interpretation    COMPLETE
Month 2 (Weeks 5-10):  Reasoning Infrastructure      COMPLETE
Month 3 (Weeks 11-12): Evaluation + Reporting       COMPLETE
PYTHIA Ω (Weeks 13-20): Candidate workflow          PLANNED
```

---

## Technology Stack

```
Python          Core language
scikit-learn    Isolation Forest anomaly detection
pandas/numpy    Feature engineering
SQLite          Knowledge graph storage
pyjet           Jet clustering (anti-kT R=1.0)
LHCO dataset    Real LHC collision data
Google Colab    Development environment
```

---

## Knowledge Graph Schema

```
Event → Feature → Anomaly → Evidence → Phenomenology
                                            ↓
                                         Theory
                                            ↓
                                        Constraint
                                        ↙        ↘
                                   Rejection    Survivor
                                                   ↓
                                               Ranking
                                                   ↓
                                           Recommendation
                                                   ↓
                                            Source Bundle
                                                   ↓
                                          Reasoning Trace
```

---

## What PYTHIA Cannot Do (Yet)

```
- Discover new particles
- Prove a new theory
- Verify external citations automatically
- Run on full LHC production data
- Perform cross-experiment analysis
- Generate new hypotheses
- Replace physicists
```

Honesty about limitations is part of the architecture.

---

## License

MIT

---

*Built with Claude, ChatGPT, and Gemini working in parallel
under human direction.*
