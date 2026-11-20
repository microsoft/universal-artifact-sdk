# Wire tested digit library into Benford analysis

Status: Successful

Reproduce: implement the specs referenced by experiment `wire-tested-digit-library-into-benford-analysis` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Validation succeeded. The pinned World Bank population CSV was downloaded and verified with SHA-256 `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`, row count 17,195, and schema `Country Name, Country Code, Year, Value`. No rows were excluded. Key metrics: first-digit MAD `0.007314647983807111` (`acceptable conformity`), first-digit chi-square `100.16554215204238` with 8 dof, second-digit MAD `0.004058150935433028`, second-digit chi-square `49.27746805969423` with 9 dof, and deterministic one-order uniform negative-control MAD `0.0602555206731196` (`nonconformity`). Offline smoke validation reran numeric analysis twice from the cached verified CSV and produced stable hashes for `first_digit_table.csv`, `second_digit_table.csv`, and `summary.json`.

## Lessons
Use `python3` in this environment: the initial `python ...` invocation failed because no unversioned `python` executable is on PATH. Once launched with `python3`, the orchestrator uses `sys.executable` for all child steps. The full validation remains small: it completed in about 5.3 seconds here, including network download, figure generation, and two offline numeric reruns. The checksum gate is cheap enough to run before every empirical claim, and the negative-control result confirms the shared scoring path discriminates rather than accepting arbitrary numeric data.
