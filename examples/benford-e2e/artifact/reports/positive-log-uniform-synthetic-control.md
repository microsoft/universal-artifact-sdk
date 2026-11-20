# Positive log-uniform synthetic control

Status: Successful

Reproduce: implement the specs referenced by experiment `positive-log-uniform-synthetic-control` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Ran the smallest concrete validation for the positive log-uniform synthetic control under the workspace root.

Key results:
- Dataset checksum/schema/row-count gate passed before deriving the sample size.
- Pinned SHA-256: `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`.
- Dataset rows / positive-control sample size: `17,195`.
- Digit extraction smoke tests passed (`54922 -> 5`, `0.0071 -> 7`, zero/blank/NaN exclusions checked).
- Positive control: `X = 10**U`, `U ~ Uniform(0, 6)`, seed `424242`.
- First-digit MAD: `0.001620904667174733`.
- Chi-square: `6.177076780388321` with `8` dof.
- Nigrini class: `close conformity`.
- Existing unit tests also passed: `9 passed`.

This satisfies the success criterion: the same scoring procedure accepts Benford-like data by construction, supporting that the pipeline is not spuriously rejecting conforming inputs.

## Lessons
- A six-order log-uniform control with the same retained-row count as the real dataset produces very low first-digit MAD under the existing scoring path.
- Keeping the dataset provenance gate at the start is cheap and preserves consistency with the primary analysis, even for a synthetic-control validation.
- The positive control complements the existing one-order uniform negative control: one fails clearly, while this Benford-like generator is classified as close conformity.
- A focused standalone reproducer can validate this result from a clean Python container with only `numpy` installed.
