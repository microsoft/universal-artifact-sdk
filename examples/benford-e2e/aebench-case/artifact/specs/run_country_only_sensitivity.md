# Spec: `scripts/run_country_only_sensitivity.py` — country-only sensitivity (static aggregate list)

> **Audience**: implementers. **Source of truth for**: experiment
> `country-only-sensitivity-analysis-excluding-aggregate-world-bank-series`. Depends on
> `analyze_benford.md` (imports `benford_first_probs, benford_second_probs,
> classify_nigrini_first_digit_mad, tabulate_digits, verify_data_file`), `digits.md`.

CLI: `python scripts/run_country_only_sensitivity.py [--data data/population.csv] [--results-dir results]`.
Requires the verified `data/population.csv` (run `validate_provenance.py` first).

## Constant `AGGREGATE_CODES` (48 World Bank aggregate codes)

```
AFE AFW ARB CEB CSS EAP EAR EAS ECA ECS EMU EUU FCS HIC HPC IBD IBT IDA IDB IDX LAC LCN LDC LIC
LMC LMY LTE MEA MIC MNA NAC OED OSS PRE PST PSS SAS SSA SSF SST TEA TEC TLA TMN TSA TSS UMC WLD
```

(48 codes. The metadata-derived list of `validate_metadata_filter.md` has 47: it lacks `FCS`.)

## Algorithm

1. `verify_data_file(data)`; `df = pandas.read_csv(data)`; header check as in `analyze_benford.md`.
2. `codes_in_data = set(df["Country Code"].astype(str).unique())`; `present = sorted(AGG ∩ codes)`,
   `absent = sorted(AGG − codes)`; `aggregate_df = df[df["Country Code"].isin(AGG)]`,
   `country_df` = the complement (row order preserved).
3. `score_panel(frame)`: DIGITS-DECIMAL over `frame["Value"].tolist()`; tabulate valid results for
   first (BENFORD1) and second (BENFORD2) digits via `tabulate_digits` (PAIRWISE-MEAN MAD, SEQ-SUM χ²);
   if the two `n` differ → `AssertionError`. Returns tables, `analyzed_rows`, `excluded_rows`,
   `exclusions_by_reason`, `first_digit {mad, chi_square, dof: 8, nigrini_classification,
   observed_counts "1".."9"}`, `second_digit {mad, chi_square, dof: 9, observed_counts "0".."9"}`.
4. Score full `df` and `country_df`. Write (CSV-PANDAS12) `results/country_only_first_digit_table.csv`,
   `results/country_only_second_digit_table.csv` (country panel tables, columns as in `tabulate_digits`).
5. `results/country_only_comparison.csv` (CSV-PANDAS12): two rows, columns in order
   `panel, rows_total, analyzed_rows, excluded_rows, aggregate_rows_removed, unique_codes,
   first_digit_mad, first_digit_chi_square, first_digit_dof, first_digit_classification,
   second_digit_mad, second_digit_chi_square, second_digit_dof`; panels `full_verified_panel`
   (aggregate_rows_removed 0, unique_codes = `df["Country Code"].nunique()`) and `country_only_panel`
   (aggregate_rows_removed = len(aggregate_df)).
6. `removed_codes` = `aggregate_df[["Country Code","Country Name"]].drop_duplicates()
   .sort_values("Country Code")` renamed to `{code, name}` records.
7. `robustness_limitations_paragraph` (exact template; `{x:.6f}`):
   `"After excluding World Bank aggregate region/income/world series, the country/territory-only panel has first-digit MAD {c1:.6f} ({c_label}) versus {f1:.6f} for the full panel, and second-digit MAD {c2:.6f} versus {f2:.6f}. The first-digit conformity conclusion remains acceptable, and the second-digit generalized Benford fit remains small by MAD; therefore the primary conclusion is not driven solely by aggregate World Bank series. The limitation is that the filter relies on a documented static aggregate-code list for this pinned CSV rather than a separately checksummed World Bank metadata file."`
8. `results/country_only_summary.json` (JSON-STD): `run_timestamp_utc`,
   `dataset {source_url, data_path, sha256, checksum_match, row_count, schema_match}`,
   `filter {rule: "Exclude rows whose Country Code is in the documented static World Bank aggregate-code set embedded in run_country_only_sensitivity.py.", aggregate_codes_present, aggregate_codes_absent_from_pinned_csv, removed_unique_codes: len(present), removed_rows, removed_codes, country_only_unique_codes, country_only_rows}`,
   `full_panel {analyzed_rows, excluded_rows, first_digit, second_digit}`,
   `country_only_panel {analyzed_rows, excluded_rows, exclusions_by_reason, first_digit, second_digit}`,
   `robustness_limitations_paragraph`, `outputs {country_only_first_digit_table_csv,
   country_only_second_digit_table_csv, country_only_comparison_csv, country_only_summary_json}`.
   Print a status JSON. Exit 0.

## Outputs & oracle

| file | compared fields | tolerance |
|---|---|---|
| `results/country_only_comparison.csv` | all cells | exact text |
| `results/country_only_first_digit_table.csv`, `…_second_digit_table.csv` | all cells | exact text |
| `results/country_only_summary.json` | `filter.{removed_unique_codes, removed_rows, country_only_unique_codes, country_only_rows, aggregate_codes_absent_from_pinned_csv}`, `country_only_panel.*` | ints/labels exact, floats rel 1e-12 |

Expected: 48 codes present, 0 absent, 3,120 rows removed, 14,075 rows / 217 codes remain;
country first-digit MAD `0.007368305780` (acceptable), second-digit MAD `0.004879224846`.
