# Deterministic uniform one-order negative control

Status: Successful

Reproduce: implement the specs referenced by experiment `deterministic-uniform-one-order-negative-control` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Implemented and ran the smallest concrete validation under the workspace root.

Key results:
- Dataset checksum verified: `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`
- Dataset row count verified: 17,195 rows
- Real retained first-digit sample size: 17,195; excluded rows: 0
- Real first-digit MAD: 0.007314647983807111, classified as `acceptable conformity`
- Negative-control seed: 20260717
- Negative-control distribution: uniform one-order integers `[1000, 10000)`
- Control sample size: 17,195, matching the real retained sample size
- Control first-digit MAD: 0.06025552067311963
- Control chi-square: 6978.557246295499, dof=8
- Control Nigrini classification: `nonconformity`

Validation command rerun successfully with assertions that checksum/schema/row-count passed, sample sizes matched, and the negative control was classified as nonconforming.

## Lessons
- A one-order uniform control is strongly rejected by the same first-digit scoring path used for the real population data, supporting the discriminating-power claim.
- The pinned provenance gate is cheap enough to keep at the start of every run and fail closed before producing empirical claims.
- The real World Bank population data remains in the acceptable MAD conformity range, while the deterministic control is far into nonconformity, making the contrast clear and reproducible.
- Keeping the scoring path in a single shared function (`score_first_digits`) reduces risk that the control and real-data analyses are inadvertently incomparable.
