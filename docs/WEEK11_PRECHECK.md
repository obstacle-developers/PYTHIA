# Week 11 Precheck — Readiness Gate

## Status

**Pending**

Week 11 should not begin until this readiness gate passes.

## Why This Gate Exists

Weeks 6–10 created the first complete auditable reasoning trace for `interp_rank_001`. Before adding a Reasoning Trace Evaluator, PYTHIA needs to verify that:

1. The constraint evaluator does not use unsafe execution.
2. The completed reasoning chain can scale beyond a single anomaly.
3. Cross-trace behavior is deterministic and consistent.

This prevents building an evaluator on top of a single-trace demonstration only.

## Gate A — eval/exec Safety Audit

The Week 6 audit reported:

```text
No eval/exec used in evaluator: UNKNOWN
```

This must be resolved before Week 11.

Required checks:

```text
- Inspect ConstraintEvaluator source if available.
- Search notebook history for true unsafe calls:
  - eval(
  - exec(
- Do not count words like evaluate, evaluation, execute, executor.
```

Gate A passes only if no unsafe `eval(` or `exec(` calls are found.

## Gate B — Top 10 Reasoning Chain Run

The completed chain must be run or verified for the top 10 anomalies.

Required chain:

```text
Phenomenology
→ Theory Retrieval
→ Constraint Evaluation
→ Survivor Storage
→ Ranking
→ Recommendation
→ Source Bundle
→ Reasoning Trace
```

The system must discover real anomaly IDs from existing records. It must not fabricate anomaly IDs.

Expected checks:

```text
- 10 valid anomaly IDs discovered.
- 10 reasoning traces created or verified.
- Retrieval records exist.
- Survivor records exist.
- Ranking records exist.
- Recommendation records exist.
- Source bundles exist.
- Rejections are stored where constraints legitimately fire.
```

Important: do not force a rejection if no constraint fires. Report the count honestly.

## Gate C — Cross-Trace Consistency

For the top 10 traces, verify deterministic behavior:

```text
- Same phenomenology signature retrieves the same candidate theory set.
- Same phenomenology signature applies the same available constraints.
- Rejected theories do not appear in rankings.
- Ranked theories are survivors.
- Recommendations match the top-ranked survivor or fallback template.
- Source bundles cover rejection, retrieval, and recommendation where applicable.
```

## Final Readiness Decision

Week 11 may start only if:

```text
Gate A: PASS
Gate B: PASS
Gate C: PASS
At least 10 reasoning traces exist
No unsafe eval/exec is found
No fabricated records are created
```

## Planned Week 11 After Gate Passes

Week 11 should implement Reasoning Trace Evaluation v1.

The evaluator should check:

```text
1. Completeness
2. Internal consistency
3. Missing evidence
4. Missing sources
5. Rejected theory linked to constraint
6. Survivor not also rejected
7. Ranking only includes survivors
8. Recommendation matches top-ranked survivor or fallback template
9. Source bundle covers rejection/retrieval/recommendation
10. No probability language
11. No hidden physics decision
12. No contradiction between trace nodes
13. Cross-trace consistency
```

Expected Week 11 output:

```text
Reasoning Trace Evaluation Report
Trace quality score
PASS / PATCH REQUIRED decision
```
