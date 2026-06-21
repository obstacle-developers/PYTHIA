# Week 13 Demo Capsule

This directory contains a tiny, synthetic, text-only Week 13 demo capsule for local reviewer runs.

## What it does

The demo:

1. Loads `mock_traces.jsonl`, a tiny set of synthetic mock anomaly traces.
2. Runs the existing Week 13 mock cluster engine using exact feature-signature grouping.
3. Runs lightweight cluster consistency checks.
4. Builds a Week 13 cluster report.
5. Writes deterministic local outputs to `demo/week13/output/` by default.

## Run locally

From the repository root:

```bash
python demo/week13/run_week13_demo.py
```

Outputs are written to:

- `demo/week13/output/clusters.jsonl`
- `demo/week13/output/members.jsonl`
- `demo/week13/output/consistency.jsonl`
- `demo/week13/output/week13_report.md`

The `output/` directory is generated locally and should not be committed.

## Safety scope

This capsule uses only synthetic mock traces. It does not include real LHCO data, large datasets, particle-object construction, later-stage feature extraction, or heavy external clustering/dataframe dependencies.

The report language is intentionally conservative: every result is an unresolved anomaly-family review aid, with insufficient evidence for interpretation, and human review required.
