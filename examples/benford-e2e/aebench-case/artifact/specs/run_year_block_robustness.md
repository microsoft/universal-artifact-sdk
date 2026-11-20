# Spec: `scripts/run_year_block_robustness.py` — temporal robustness by predeclared year blocks

> **Audience**: implementers. **Source of truth for**: experiment
> `temporal-robustness-by-predeclared-year-blocks`. Depends on `analyze_benford.md`
> (`score_first_digits_from_values`, `verify_data_file`).

CLI: `python scripts/run_year_block_robustness.py [--data data/population.csv] [--results-dir results]`.

## Constants

`YEAR_BLOCKS = (("1960-1979",1960,1979), ("1980-1999",1980,1999), ("2000-2019",2000,2019), ("2020-2024",2020,2024))` (inclusive).

## Algorithm

1. `verify_data_file`; `df = pandas.read_csv`; header check; `df["Year"] = pd.to_numeric(df["Year"],
   errors="raise").astype(int)`. If `min(Year) < 1960` or `max(Year) > 2024` → `SystemExit("Verified CSV contains years outside the predeclared blocks: min=…, max=…")`.
2. For each block (in order): `block = df[(Year >= start) & (Year <= end)]`;
   `score = score_first_digits_from_values(block["Value"].tolist())` (DIGITS-DECIMAL, PAIRWISE-MEAN
   MAD, SEQ-SUM χ², NIGRINI1). Row: `block, start_year, end_year, rows_total = len(block),
   sample_size = analyzed_rows, excluded_rows, first_digit_mad, chi_square, dof (8),
   nigrini_classification` (this column order).
3. Assert `Σ rows_total == len(df)` and every `sample_size > 0` (`AssertionError` otherwise).
4. Write `results/year_block_robustness.csv` (CSV-PANDAS12).
5. `results/year_block_robustness_summary.json` (JSON-STD): `run_timestamp_utc`, `dataset {source_url,
   data_path, sha256, checksum_match, row_count, schema_match, year_min, year_max}`,
   `predeclared_blocks [{block, start_year, end_year}]`, `results` (= table records, full-precision
   floats), `interpretation: "All predeclared year blocks are scored with the same first-digit pipeline as the primary analysis. Classifications are descriptive robustness diagnostics, not strong iid hypothesis tests, because country-year population observations are temporally correlated."`,
   `outputs {year_block_robustness_csv, year_block_robustness_summary_json}`. Print status JSON; exit 0.

## Outputs & oracle

| file | compared fields | tolerance |
|---|---|---|
| `results/year_block_robustness.csv` | all cells | exact text |
| `results/year_block_robustness_summary.json` | `results[*]` (all fields), `dataset.{year_min, year_max}` | ints/labels exact; floats rel 1e-12 |

Expected rows (rows_total = sample_size): 1960-1979 5280, MAD 0.012916039293 (marginally acceptable);
1980-1999 5290, 0.010819211214 (acceptable); 2000-2019 5300, 0.008670439119 (acceptable);
2020-2024 1325, 0.010652512951 (acceptable).
