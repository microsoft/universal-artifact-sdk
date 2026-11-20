# Spec: `scripts/run_positive_control_validation.py` — positive log-uniform synthetic control

> **Audience**: implementers. **Source of truth for**: experiment
> `positive-log-uniform-synthetic-control` (canonical outputs). Depends on `digits.md`,
> `validate_provenance.md`. Companion: `reproduce_positive_control_standalone.md`.

## CLI

`python scripts/run_positive_control_validation.py [--data data/population.csv] [--results-dir results]
[--seed 424242] [--log10-min 0.0] [--log10-max 6.0] [--download]`

If not `log10_max > log10_min` → `SystemExit("--log10-max must be greater than --log10-min")`.

## Algorithm

1. Create results dir. **Smoke tests** (raise `AssertionError` on mismatch) with DIGITS-DECIMAL:
   `54922→(5,4)`, `"0.0071"→(7,1)`, `"1e5"→(1,0)`, `-92.5→(9,2)` (and valid); reasons
   `0→zero`, `""→missing_or_blank`, `None→missing_or_blank`, `float("nan")→non_finite`.
2. Data: if `--download` or the data file is missing, `fetch_bytes(PINNED_URL)` and write it to
   `--data`; else read it. `validate(...)`; failures → `SystemExit("Dataset validation failed before positive control:\n - …")`.
3. `df = pandas.read_csv(data)`; `sample_size` = number of `Value`s valid under DIGITS-DECIMAL (17195).
4. `rng = numpy.random.default_rng(seed)`; `u = rng.uniform(log10_min, log10_max, size=sample_size)`;
   `values = numpy.power(10.0, u)` (float64 array).
5. Score (DIGITS-DECIMAL on each float — i.e. `Decimal(str(x))`): first digits, `n`, counts; DataFrame
   rows for `d = 1..9` with columns `digit, observed_count, observed_proportion, benford_proportion,
   abs_deviation`; `mad = table["abs_deviation"].mean()` (**PAIRWISE-MEAN**); χ² SEQ-SUM; NIGRINI1.
6. Write `results/positive_control_first_digit_table.csv` (CSV-PANDAS12).
7. Write `results/positive_control_summary.json` (JSON-STD):

```
experiment: "Positive log-uniform synthetic control", status: "ok",
digit_extraction_smoke_tests_passed: true,
dataset_gate: {source_url, data_path, sha256, expected_sha256, checksum_match, row_count,
               expected_row_count, schema_match},
positive_control: {description: "X = 10**U with U uniform on the recorded log10 range, scored by the shared first-digit pipeline.",
   positive_control_seed, generation_log10_min, generation_log10_max,
   generation_orders_of_magnitude: max − min (float),
   sample_size, excluded_rows, exclusions_by_reason, positive_control_first_digit_mad,
   positive_control_first_digit_chi_square, dof: 8, nigrini_classification,
   observed_counts {"1".."9"}},
success: label in {"close conformity", "acceptable conformity"},
outputs: {positive_control_first_digit_table_csv, positive_control_summary_json}
```

8. Print the summary (JSON-STD); exit 0 if `success` else 2.

## Outputs & oracle

| file | compared fields | tolerance |
|---|---|---|
| `results/positive_control_summary.json` | `positive_control.{sample_size, observed_counts, nigrini_classification}`, `success` | exact |
| same | `positive_control.positive_control_first_digit_mad`, `…_chi_square` | rel 1e-12 |
| `results/positive_control_first_digit_table.csv` | all cells | exact text |

Expected: counts `5106,3045,2141,1649,1331,1205,1017,882,819`, MAD `0.001620904667174733`,
χ² `6.177076780388321`, `close conformity`, success true.
