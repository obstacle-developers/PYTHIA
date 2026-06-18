# PYTHIA Architecture

This root file is intentionally kept as a short pointer to avoid duplicate architecture documents.

The canonical architecture document is:

```text
docs/ARCHITECTURE.md
```

## Current Frozen Architecture v1.0

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

## Current Status

PYTHIA has completed Weeks 1 through 10.

The current system is an early auditable scientific reasoning infrastructure prototype. It can detect anomalous LHCO events, translate them into physics-aware phenomenology, retrieve candidate theories, reject candidates through source-linked constraints, rank surviving explanations, recommend follow-up analysis, register sources, and export a full reasoning trace.

For the full architecture, governing rules, completed layers, and current reasoning chain, see:

```text
docs/ARCHITECTURE.md
```

## Important Protocol

Do not treat this root file as the detailed source of truth. Keep detailed architecture updates in `docs/ARCHITECTURE.md` and keep this file as a stable pointer.
