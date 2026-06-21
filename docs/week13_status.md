# Week 13 status

Week 13 PYTHIA Ω anomaly-family workflow is **HARDENED VERIFIED PASS**. The Week 13 demo capsule under `demo/week13/` is **REPRODUCIBLE** with:

```bash
python demo/week13/run_week13_demo.py
```

The demo uses synthetic mock traces and writes audit-oriented outputs to `demo/week13/output/`:

- `clusters.jsonl`
- `members.jsonl`
- `consistency.jsonl`
- `week13_report.md`

Generated demo outputs are not committed as repository artifacts.

## Safe report language

The report language is intentionally conservative:

- clusters are described as unresolved anomaly families or candidate patterns;
- every report keeps human review required as the review gate;
- insufficient evidence is stated where checks are absent or weakening conditions appear;
- weakening-condition and kill-condition wording is reserved for consistency-check context;
- no output claims particle discovery or evidence for new physics by itself.

## Limitations

- Week 13 uses mock records only.
- It does not add datasets or raw artifacts.
- It does not add heavy clustering dependencies.
- It does not construct candidate particles.
- It does not make discovery claims.
- Week 14 signal fingerprint extraction is not part of Week 13.

## Next step

Week 14 Signal Fingerprint Extractor is next, after Sprint 7 documentation updates are complete. Candidate construction remains out of scope until known explanations have been tested.
