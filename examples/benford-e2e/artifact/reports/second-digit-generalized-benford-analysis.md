# Second-digit generalized Benford analysis

Status: Completed

Reproduce: implement the specs referenced by experiment `second-digit-generalized-benford-analysis` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Ran the smallest concrete end-to-end validation under the workspace root.

Command executed successfully:

```bash
python3 tests/test_digits.py && python3 tests/test_provenance_gate.py && python3 scripts/validate_provenance.py && python3 scripts/analyze_benford.py
```

Key results:
- Dataset checksum verified: `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`.
- Dataset rows: 17,195; analyzed rows: 17,195; excluded rows: 0.
- Second-digit analyzable rows: 17,195; values lacking a second significant digit: 0.
- Generalized-Benford second-digit probability sum: 0.9999999999999997.
- Second-digit MAD: 0.004058150935433028.
- Second-digit Pearson chi-square: 49.27746805969423 with dof=9.
- Negative-control first-digit MAD: 0.0602555206731196, classified as nonconformity.

The second-digit table was generated with exactly 10 rows and observed counts summing to 17,195. The largest second-digit deviation was digit 0, with observed proportion 0.134341378308 vs. expected 0.119679268597, absolute deviation 0.014662109711.

## Lessons
- The pinned dataset gate is fast and should remain the first step; it verified checksum, schema, and row count before analysis.
- The second-digit result is stronger than the first-digit result by MAD: second-digit MAD is about 0.00406, while the first-digit MAD is about 0.00731.
- Explicitly recording the one-significant-digit convention avoids ambiguity in second-digit analyses. In this dataset, no rows required that convention.
- The same scoring path continues to discriminate: the fixed-seed single-order-of-magnitude control is clearly non-Benford by MAD.
