# Primary first-digit Benford conformity analysis

Status: Completed

Reproduce: implement the specs referenced by experiment `primary-first-digit-benford-conformity-analysis` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Created and ran a minimal concrete validation under the workspace root.

Validation command passed end-to-end: unit tests, provenance gate, checksum verification, and Benford analysis.

Key results:
- Dataset SHA-256 verified: `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`
- Dataset rows: 17,195; analyzed rows: 17,195; excluded rows: 0
- First-digit MAD: `0.007314647983807111`
- First-digit chi-square: `100.16554215204238`, dof `8`
- Nigrini classification: `acceptable conformity`
- Largest first-digit deviations: digit 1 underrepresented by `0.017575503078927412`, digit 5 overrepresented by `0.013578277069560413`, digit 4 overrepresented by `0.009923368788977607`
- Second-digit MAD: `0.004058150935433028`; chi-square: `49.27746805969423`, dof `9`
- Negative-control first-digit MAD: `0.0602555206731196`, classified as `nonconformity`

The primary hypothesis is supported at the planned Nigrini threshold level: the real World Bank population first digits show acceptable Benford conformity, while the deterministic negative control clearly fails the same test.

## Lessons
- Provenance gating is essential and cheap: the script fails closed on checksum, schema, or row-count mismatch before any empirical claim is generated.
- The real population dataset conforms acceptably by first-digit MAD but not perfectly; digit 1 is lower than Benford expectation and digit 5 is higher.
- The large-N chi-square is sensitive even for visually/moderately small deviations, so MAD/Nigrini classification is the clearer conformity summary for this artifact.
- The fixed-seed uniform one-order-of-magnitude control produced strong nonconformity, confirming that the scoring path discriminates rather than trivially accepting all numeric inputs.
- Keeping figures generated from recorded CSV result tables makes the artifact auditable.
