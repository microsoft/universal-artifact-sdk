# Spec: `scripts/run_negative_control_validation.py` — deterministic one-order uniform negative control

> **Audience**: implementers. **Source of truth for**: experiment
> `deterministic-uniform-one-order-negative-control`. Depends on `digits.md`, `validate_provenance.md`.

No CLI arguments. Run: `python scripts/run_negative_control_validation.py`. Needs network (downloads
`PINNED_URL`; it does **not** read an existing `data/population.csv`).

## Algorithm

1. Create `data/`, `results/`. Timestamp as in `validate_provenance.md`. `raw = fetch_bytes(PINNED_URL)`;
   `validate(...)`; on failures print `FAIL: pinned population CSV failed validation` + ` - <msg>` lines
   to stderr, return 1.
2. Write `data/population.csv` (raw bytes) and `results/provenance.json` (same schema as
   `validate_provenance.md`, `validated_data_path = "data/population.csv"`).
3. Values: decode `utf-8-sig`, `csv.DictReader(text.splitlines())`; if `fieldnames != EXPECTED_HEADER`
   → `SystemExit`. Values are the **strings** of column `Value`.
4. `score_first_digits(values)` (shared for real data and control):
   DIGITS-DECIMAL on each value; first digits of valid results; `n`; for `digit in 1..9`: row
   `{digit, observed_count, observed_proportion = count/n (0.0 if n=0), benford_proportion = BENFORD1,
   abs_deviation = |obs − p|}`; `mad = SEQ-SUM(abs_deviation of the 9 rows) / 9` (**SEQ-MEAN**, not
   pandas); `chi_square` (SEQ-SUM, common.md §5); `dof = 8`; NIGRINI1;
   `observed_counts {"1".."9"}`; `excluded_rows`, `exclusions_by_reason` (sorted).
5. Control: `rng = numpy.random.default_rng(20260717)`;
   `rng.integers(1000, 10000, size=real_n, endpoint=False)`; score with the same function.
   (These draws produce the same first-digit counts as `analyze_benford.md`'s `[10000,100000)` control.)
6. Write tables (CSV-DICT, **CRLF**) with header `digit,observed_count,observed_proportion,benford_proportion,abs_deviation`,
   the three float columns formatted as `f"{x:.12f}"`:
   * `results/first_digit_table.csv` (real data) — **quirk**: overwrites `analyze_benford.py`'s
     LF/pandas version of the same file; the canonical reference copy is the later `analyze_benford`
     (run_all) output.
   * `results/negative_control_first_digit_table.csv` (control).
7. `results/negative_control_validation_summary.json` (JSON-STD):

```
dataset: {source_url, retrieval_timestamp_utc, sha256, expected_sha256, checksum_match, row_count,
          expected_row_count, row_count_match, schema_match, data_path}
real_population_first_digit: {sample_size, excluded_rows, exclusions_by_reason, first_digit_mad,
          first_digit_chi_square, dof, nigrini_classification, table_csv}
negative_control: {control_seed: 20260717,
          distribution: "numpy.random.Generator.integers uniform one-order integers [1000, 10000)",
          control_low_inclusive: 1000, control_high_exclusive: 10000, control_sample_size,
          control_excluded_rows, control_exclusions_by_reason, control_first_digit_mad,
          control_chi_square, dof, control_nigrini_classification, table_csv}
success_checks: {sample_sizes_match: real_n == control_n,
          negative_control_nonconformity: label == "nonconformity" and mad >= 0.015,
          shared_scoring_function: "score_first_digits used for real Value rows and negative control values"}
outputs: {provenance_json, real_first_digit_table_csv, negative_control_first_digit_table_csv,
          summary_json, experiment_run_json}
```

8. `results/experiment_run.json` (JSON-STD): `{name: "Deterministic uniform one-order negative control",
   status: "success" if all success_checks values truthy else "failed_success_check",
   command: "python3 scripts/run_negative_control_validation.py", artifact_paths: outputs,
   key_results: {real_sample_size, real_first_digit_mad, real_nigrini_classification,
   control_sample_size, control_first_digit_mad, control_chi_square, control_nigrini_classification}}`.
   Print it (JSON-STD) to stdout. Exit 0 on success, 2 otherwise.

## Outputs & oracle

| file | compared fields | tolerance |
|---|---|---|
| `results/negative_control_validation_summary.json` | `real_population_first_digit.{sample_size, first_digit_mad, first_digit_chi_square, nigrini_classification}`, `negative_control.{control_sample_size, control_first_digit_mad, control_chi_square, control_nigrini_classification}`, `success_checks` | floats rel 1e-12; rest exact |
| `results/negative_control_first_digit_table.csv` | all cells | exact text |
| `results/experiment_run.json` | `status`, `key_results` | as above |

Key values: real MAD `0.007314647983807111` (SEQ-MEAN; happens to equal the pandas value here),
control MAD `0.06025552067311963` (SEQ-MEAN; the PAIRWISE-MEAN of the same rows is `0.0602555206731196`), control χ² `6978.557246295499`, both sample sizes 17195.
Reference copies: `reference-outputs/results/negative_control_validation_summary.json`,
`…/negative_control_first_digit_table.csv`, `…/experiment_run.json`.
