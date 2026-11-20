# End-to-end reproducibility bundle and offline smoke test

Status: Successful

Reproduce: implement the specs referenced by experiment `end-to-end-reproducibility-bundle-and-offline-smoke-test` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Completed the smallest concrete validation and produced an end-to-end reproducibility entry point under the workspace root.

Command run: `python3 scripts/run_all.py --mode full --clean-smoke`

Validation passed:
- Digit extraction unit tests: ok.
- Provenance gate unit tests: ok.
- Pinned World Bank CSV downloaded and verified before analysis.
- Verified SHA-256: `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`.
- Verified row count: `17195`.
- Regenerated first/second digit result tables, summary JSON, legacy figures, and required table-driven PNG/PDF figures.
- Offline smoke test re-ran analysis twice from cached verified data with no network and confirmed stable numeric output hashes.

Key metrics:
- Analyzed rows: 17,195; excluded rows: 0.
- First-digit MAD: `0.007314647983807111`, Nigrini classification: acceptable conformity; chi-square: `100.16554215204238` with 8 dof.
- Second-digit MAD: `0.004058150935433028`; chi-square: `49.27746805969423` with 9 dof.
- Negative-control first-digit MAD: `0.0602555206731196`, classification: nonconformity.

Offline smoke numeric hashes were identical across the two reruns:
- `first_digit_table.csv`: `eded21643a7f50efc890940d36b264d1ad54e95b9cd23b8b104bdd9f8165cdcb`
- `second_digit_table.csv`: `b49eae88c3d2a6c101b4201258a7fc794fb2cf36825fc8883e313c1e5d58cf00`
- `summary.json`: `0514a46d3180cf46ed748f06fd45eb4f311f9e229263e92cf3eb3e3954eb8e91`

## Lessons
- A single orchestrator is useful even for a small study because it prevents reviewers from having to infer the correct order of tests, provenance validation, analysis, and figure generation.
- The provenance JSON intentionally contains a retrieval timestamp, so the deterministic smoke test should compare stable numeric outputs rather than timestamped provenance.
- Re-running analysis twice into the same offline-smoke output directory gives byte-identical numeric hashes because output paths embedded in `summary.json` remain stable.
- Keeping required figures generated from recorded CSV tables preserves auditability: figures can be refreshed without silently recomputing empirical numbers.
