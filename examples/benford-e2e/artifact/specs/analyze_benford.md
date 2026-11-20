# Spec: `scripts/analyze_benford.py` — primary first/second-digit Benford analysis

> **Audience**: implementers. **Source of truth for**: the core analysis (experiments
> `primary-first-digit-benford-conformity-analysis`, `second-digit-generalized-benford-analysis`,
> used by `run_all.py`). Depends on `digits.md`, `validate_provenance.md`, `common.md`.

## Imports / module API (also used by other scripts and by `tests/test_p_values.py`)

* SciPy is optional: `try: from scipy.stats import chi2 as scipy_chi2 except Exception: scipy_chi2 = None`
  (catch `Exception`, not only `ImportError`).
* `CONTROL_SEED = 20260717`.
* `PVALUE_METHOD = "scipy.stats.chi2.sf"` if SciPy available else `None`.
* `PVALUE_NOTE = None` if SciPy available else
  `"SciPy is not available; chi-square p_value fields are null. Install scipy to compute exact survival-function p-values."`
* `benford_first_probs() -> {1..9: BENFORD1}`, `benford_second_probs() -> {0..9: BENFORD2}` (common.md §3).
* `classify_nigrini_first_digit_mad(mad)` — NIGRINI1.
* `chi_square(counts, probs, n)` — SEQ-SUM over `probs` in key order of `(counts.get(d,0) − n·p)²/(n·p)`, as `float`.
* `chi_square_p_value(stat, dof)` — `float(scipy_chi2.sf(stat, dof))` or `None` without SciPy.
* `tabulate_digits(results, digit_kind, probs)` — `digit_kind ∈ {"first","second"}` else
  `ValueError("digit_kind must be 'first' or 'second'")`. Collect `.first`/`.second` of each result where
  not `None`; `n` = count; `counts = Counter`. Build a pandas DataFrame with one row per digit in
  `probs` order and columns, in order: `digit` (int), `observed_count` (int),
  `observed_proportion = count/n` (0.0 if n = 0), `benford_proportion = p`,
  `abs_deviation = abs(observed − p)`. `mad = float(table["abs_deviation"].mean())` (**PAIRWISE-MEAN**),
  `chi = chi_square(counts, probs, n)`. Returns `(table, dict(counts), n, mad, chi)`.
* `score_first_digits_from_values(values)` — extract digits (DIGITS-DECIMAL) for each value; exclusions
  = Counter of non-None reasons; tabulate valid results with "first" / BENFORD1; return dict
  `{table, counts, analyzed_rows: n, excluded_rows, exclusions_by_reason (sorted dict), mad,
  chi_square, dof: 8, p_value: chi_square_p_value(chi, 8), nigrini_classification}`.

## CLI

`python scripts/analyze_benford.py [--data data/population.csv] [--results-dir results]
[--figures-dir figures] [--control-seed 20260717]`

## Algorithm

1. Create output dirs. Verify `--data` bytes with `validate(raw, EXPECTED_SHA256, EXPECTED_ROW_COUNT,
   EXPECTED_HEADER)`; if failures → exit via `SystemExit("Input CSV failed checksum/schema/row-count
   validation:\n - <f1>\n - <f2>...")` (non-zero exit).
2. `df = pandas.read_csv(data)`; if columns ≠ EXPECTED_HEADER → `SystemExit`.
3. `extracted = [extract_significant_digits(v) for v in df["Value"].tolist()]`; exclusions, `valid`,
   `analyzed_rows = len(valid)`, `excluded_rows`, `lacking_second_digit` = number of valid results with
   `significant_digit_count == 1`.
4. First digits: `tabulate_digits(valid, "first", BENFORD1)`; second: `tabulate_digits(valid, "second",
   BENFORD2)`; p-values with dof 8 and 9.
5. **Negative control**: `rng = numpy.random.default_rng(seed)`;
   `control_values = rng.integers(10000, 100000, size=analyzed_rows, endpoint=False)` (numpy int64);
   `control = score_first_digits_from_values(control_values)`.
6. Write `results/first_digit_table.csv`, `results/second_digit_table.csv` (CSV-PANDAS12, columns as
   above), figures `figures/figure1_first_digit.png`
   (title `World Bank population first digits vs. Benford`) and `figures/figure2_second_digit.png`
   (title `World Bank population second digits vs. generalized Benford`).
7. `largest_deviations` = first table sorted by `abs_deviation` descending (pandas `sort_values`),
   columns `digit, observed_proportion, benford_proportion, abs_deviation`, first 3 rows as records.
8. Write `results/summary.json` (JSON-STD):

```
dataset: {source_url: PINNED_URL, data_path, sha256, expected_sha256, checksum_match, row_count,
          expected_row_count, schema_match, byte_count}
p_value_calculation: {method: PVALUE_METHOD, note: PVALUE_NOTE}
analysis: {value_column: "Value", total_rows, analyzed_rows, excluded_rows, exclusions_by_reason}
first_digit: {mad, chi_square, dof: 8, p_value, nigrini_classification,
              observed_counts: {"1".."9": int}, largest_deviations_by_digit: [3 records],
              benford_probability_sum: SEQ-SUM of BENFORD1 values}
second_digit: {mad, chi_square, dof: 9, p_value, analyzable_rows, values_lacking_second_digit,
               one_significant_digit_convention: "For valid values with only one significant digit, the second significant digit is recorded as 0 and counted here; no population rows used this convention in the verified dataset.",
               observed_counts: {"0".."9"}, benford_probability_sum: SEQ-SUM of BENFORD2 values}
negative_control: {description: "Uniform random integers over one order of magnitude [10000, 100000), scored with the same first-digit pipeline.",
                   seed, sample_size: analyzed_rows, first_digit_mad, first_digit_chi_square, dof,
                   p_value, nigrini_classification, observed_counts: {"1".."9"}}
outputs: {first_digit_table_csv, second_digit_table_csv, summary_json, figure1_png, figure2_png}
```

9. Print a JSON-STD status object (`status: "ok"`, the outputs, `first_digit_mad`,
   `negative_control_mad`) to stdout; exit 0.

## Figure spec (`plot_distribution(table, title, path)`)

7.0×4.4 in, dpi 150; bars of `observed_proportion` per digit (width 0.72, colour `#4C78A8`, label
`Observed`); line+circle markers of `benford_proportion` (colour `#F58518`, linewidth 2, label
`Benford`); x label `Significant digit`, y label `Proportion`, x ticks = digits, y limit
`[0, 1.18 × max(max observed, max expected)]`, y-grid alpha 0.25, legend without frame,
`tight_layout`, Agg backend. PNGs are not compared byte-for-byte.

## Outputs & oracle (with SciPy installed)

| file | compared fields | tolerance |
|---|---|---|
| `results/summary.json` | `first_digit.{observed_counts, mad, chi_square, nigrini_classification, largest_deviations_by_digit}`; `second_digit.{observed_counts, mad, chi_square, values_lacking_second_digit}`; `negative_control.{observed_counts, first_digit_mad, first_digit_chi_square, nigrini_classification}`; `analysis.*` | counts/labels exact; floats rel 1e-12 (byte-identical expected) |
| `results/summary.json` | `first_digit.p_value`, `second_digit.p_value` | rel 1e-9 (SciPy version not recorded) |
| `results/first_digit_table.csv`, `results/second_digit_table.csv` | all cells | exact text |

Key values: first-digit MAD `0.007314647983807111` (acceptable conformity), χ² `100.16554215204238`;
second-digit MAD `0.004058150935433028`, χ² `49.27746805969423`; control MAD `0.0602555206731196`
(nonconformity), counts `1908,1960,1822,1965,1872,1922,1863,1943,1940`.
Reference copies: `reference-outputs/results/summary.json`, `…/first_digit_table.csv`,
`…/second_digit_table.csv`.
