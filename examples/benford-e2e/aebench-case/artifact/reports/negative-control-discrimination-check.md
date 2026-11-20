# Negative-control discrimination check

Status: Successful

Reproduce: implement the specs referenced by experiment `negative-control-discrimination-check` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Created and ran `negative_control_validation.py`.

Results:
- Dataset checksum gate passed: `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`.
- Dataset row-count gate passed: `17,195` rows.
- Real-data retained rows used for same-size control: `17,195`.
- Exclusions from real retained-row count: `{}`.
- Control seed: `20260717`.
- Control distribution: `uniform[1000.0, 9999.0]`.
- Control first-digit MAD: `0.060888779695445226`.
- Control Nigrini classification: `nonconformity`.
- Control chi-square: `6897.74230178361` with `8` degrees of freedom.

The validation passes: the negative control is well above the nonconformity threshold (`MAD >= 0.015`), demonstrating that the scoring path discriminates rather than accepting arbitrary numeric input.

## Lessons
- The checksum/schema/row-count gate is fast enough to include even in this smallest validation and protects the external-input claim.
- Using the exact retained-row count from the verified dataset avoids a hidden sample-size mismatch between real data and control.
- A single-order uniform control is strongly non-Benford under the shared first-digit scoring function, supporting the experiment's negative-control hypothesis.
