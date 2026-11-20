# Benford conformity analysis tables and figures

Status: Successful

Reproduce: implement the specs referenced by experiment `benford-conformity-analysis-tables-and-figures` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Ran the smallest concrete end-to-end validation with `python3 scripts/run_all.py --mode full --clean-smoke`.

Validation succeeded:
- Digit-extraction unit tests: passed.
- Provenance gate unit tests: passed.
- Downloaded pinned World Bank population CSV and verified SHA-256, schema, and row count before analysis.
- Generated primary Benford first/second digit tables, summary statistics, negative control, and required figures.
- Ran offline smoke test twice from the cached verified CSV and confirmed byte-identical numeric output hashes.

Key results:
- Dataset rows: 17,195 total; 17,195 analyzed; 0 excluded.
- Dataset SHA-256: `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`.
- First digit: MAD `0.007314647983807111`, Nigrini classification `acceptable conformity`, chi-square `100.16554215204238` with dof `8`.
- Largest first-digit deviations: digit 1 underrepresented by `0.017575503078927412`; digit 5 overrepresented by `0.013578277069560413`; digit 4 overrepresented by `0.009923368788977607`.
- Second digit: MAD `0.004058150935433028`, chi-square `49.27746805969423` with dof `9`.
- Negative control: first-digit MAD `0.0602555206731196`, Nigrini classification `nonconformity`, chi-square `6978.557246295499` with dof `8`, seed `20260717`.
- Offline deterministic numeric hashes matched across both reruns for `first_digit_table.csv`, `second_digit_table.csv`, and `summary.json`.

## Lessons
- The provenance gate remains cheap and effective: checksum, schema, and row-count validation completed before empirical claims were produced.
- The primary population data supports the Benford conformity claim by MAD/Nigrini criteria, while the large-N chi-square is sensitive to modest deviations and should be interpreted cautiously.
- The fixed-seed one-order uniform negative control strongly failed the same scoring path, supporting discriminating power.
- Generating publication figures from recorded result tables, followed by an offline smoke test, gives an auditable path from verified data to figures and summary outputs.
