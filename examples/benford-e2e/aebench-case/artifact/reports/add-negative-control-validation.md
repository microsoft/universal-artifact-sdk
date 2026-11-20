# Add negative-control validation

Status: Successful

Reproduce: implement the specs referenced by experiment `add-negative-control-validation` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Ran `python3 scripts/run_negative_control_validation.py` from `<scratch-file>`; exit status was 0. The provenance gate passed: SHA-256 matched `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`, schema matched, and row count was 17,195. The real population first-digit MAD was `0.007314647983807111` (`acceptable conformity`). The same-size fixed-seed negative control used seed `20260717`, generated 17,195 uniform one-order integers in `[1000, 10000)`, and produced first-digit MAD `0.06025552067311963`, chi-square `6978.557246295499` with 8 dof, and Nigrini classification `nonconformity`. Success criterion met: negative-control MAD is well above the `0.015` nonconformity threshold and sample sizes match.

## Lessons
The smallest validation is sufficient for Success Criterion 4 because it keeps the checksum/schema/row-count gate before all analysis and then reuses exactly one scoring function for real and synthetic values. The control result is deterministic with NumPy seed `20260717`. The observed control MAD (`0.0602555`) is far from the threshold, so the conclusion is not sensitive to numerical rounding. A compact independent Docker reproducer using only `python:3.11` plus `numpy` reproduces the same key numbers from the pinned URL.
