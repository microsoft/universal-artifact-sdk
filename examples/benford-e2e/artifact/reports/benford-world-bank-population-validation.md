# Benford World Bank population validation

Status: Successful

Reproduce: implement the specs referenced by experiment `benford-world-bank-population-validation` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Implemented and ran a minimal reproducible validation.

Key results from `benford_validation_run/summary.md`:
- Dataset provenance gate passed for the pinned URL.
- SHA-256: `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`.
- Data rows: `17195`; rows analyzed: `17195`; rows excluded: `0`.
- First digit: MAD `0.007314648`, Nigrini classification `acceptable conformity`, chi-square `100.165542`, dof `8`.
- Second digit: MAD `0.004058151`, Nigrini classification `close conformity`, chi-square `49.277468`, dof `9`.
- Negative control: same-size fixed-seed uniform values on `[1, 10)`, MAD `0.060501070`, classification `nonconformity`, chi-square `7312.294283`, dof `8`.

Interpretation: the empirical claim is supported when stated in MAD/Nigrini terms: the real population panel is acceptable/close conformity, and the negative control clearly fails the same scoring path. The chi-square values show statistically detectable deviations at this sample size, so the paper should avoid language implying a perfect Benford fit.

## Lessons
- Keep the checksum/schema/row-count gate before every empirical claim; it is cheap and protects the external-data provenance claim.
- A minimal stdlib-first script is sufficient for analysis and testing; only `matplotlib` is needed for required PNG figures.
- Returning reason-coded digit extraction exclusions makes data-quality reporting explicit; this dataset excluded zero rows.
- MAD/Nigrini classification is the clearest conformity summary here; chi-square should be reported but interpreted cautiously because large N makes modest deviations detectable.
- The same-size one-order uniform negative control strongly discriminates, supporting that the test is not trivially accepting arbitrary numeric inputs.
