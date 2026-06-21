# Current status

This document records the verified repository state after Codex Sprint 0 through Codex Sprint 6 and before Week 14 implementation.

## Merged sprint list

| Sprint | Repository state |
|---|---|
| Codex Sprint 0 | Merged |
| Codex Sprint 1 | Merged |
| Codex Sprint 2 | Merged |
| Codex Sprint 3 | Merged |
| Codex Sprint 4 | Merged |
| Codex Sprint 5 | Merged |
| Codex Sprint 6 | Merged |

## Verified status

- Week 12 PYTHIA v1 reasoning pipeline: **VERIFIED PASS**.
- Week 13 PYTHIA Ω anomaly-family workflow: **HARDENED VERIFIED PASS**.
- Week 13 demo capsule under `demo/week13/`: **REPRODUCIBLE**.
- Week 14 Signal Fingerprint Extractor: **NEXT — not started**.

## Current capabilities

PYTHIA currently supports audit-oriented anomaly reasoning workflows that can:

- assemble Week 12 reasoning traces and integrated report outputs;
- evaluate reasoning-trace quality and completeness;
- run a Week 13 mock anomaly-family demo capsule;
- produce cluster, member, consistency, and Markdown report outputs from the Week 13 demo;
- describe anomaly groups as candidate patterns or unresolved anomaly families;
- preserve insufficient-evidence and human-review-required language in reports.

## Demo command

Run the reproducible Week 13 demo capsule with:

```bash
python demo/week13/run_week13_demo.py
```

The demo is expected to write:

- `demo/week13/output/clusters.jsonl`
- `demo/week13/output/members.jsonl`
- `demo/week13/output/consistency.jsonl`
- `demo/week13/output/week13_report.md`

Generated demo outputs are intentionally not committed as repository artifacts.

## Test status

The current required regression check is:

```bash
python -m pytest -q
```

This command should pass before merging Sprint 7 documentation updates.

## Current limitations

- Week 13 uses synthetic mock traces for the demo.
- No real LHCO-scale clustering workflow has been implemented yet.
- No candidate-particle construction has been implemented yet.
- No Week 14 signal fingerprint extraction has been implemented yet.
- No autonomous discovery claims are supported.
- Real-data validation and streaming scalability remain future risks.

## Safe-language policy

PYTHIA does not claim particle discovery. PYTHIA reports candidate patterns, unresolved anomaly families, insufficient evidence, and human review required. All outputs are audit-oriented.

Conservative terms such as `candidate pattern`, `unresolved anomaly family`, `insufficient evidence`, and `human review required` are required whenever evidence is incomplete or a conclusion depends on later physics validation.
