# Spec: `scripts/plot_year_block_mad.py` — CSV-backed year-block MAD diagnostic figure

> **Audience**: implementers. **Source of truth for**: experiment `plot-temporal-robustness-diagnostics`
> (canonical outputs). Reads only `results/year_block_robustness.csv` (from
> `run_year_block_robustness.md`); no raw data, no re-scoring. Packages: pandas, matplotlib (Agg).

CLI: `python scripts/plot_year_block_mad.py [--results-dir results] [--figures-dir figures]`.

## Validation of the input CSV (`load_and_validate`) — each failure → `SystemExit(msg)` (exit 1)

1. Required columns `{block, start_year, end_year, rows_total, sample_size, excluded_rows,
   first_digit_mad, chi_square, dof, nigrini_classification}`; missing →
   `"{path} is missing required columns: {sorted(missing)}"`. Empty → `"{path} has no year-block rows"`.
2. Coerce `start_year`, `end_year`, `sample_size` to int and `first_digit_mad` to float
   (`pd.to_numeric(errors="raise")`). Any `sample_size <= 0` → `"Every year block must have a positive sample size"`.
3. `start_year` and `end_year` must both be monotonic increasing → else
   `"Year blocks must be sorted in chronological order"`.
4. Re-classify each `first_digit_mad` with NIGRINI1; any disagreement with the recorded
   `nigrini_classification` → `"Nigrini classification mismatches: [(block, mad, recorded, expected), …]"`.

## Figure `figures/year_block_mad.png`

rcParams: figsize 7.2×4.2, dpi/savefig.dpi 150, top/right spines off, font size 10. Background
`axhspan` bands: [0,0.006] `#54A24B` α0.10 label `Close < 0.006`; [0.006,0.012] `#4C78A8` α0.08
`Acceptable < 0.012`; [0.012,0.015] `#F58518` α0.10 `Marginal < 0.015`; [0.015, ymax] `#E45756` α0.07
`Nonconformity ≥ 0.015`, with `ymax = max(0.017, 1.18·max MAD)`. Line (`#333333`, lw 1.4, marker `o`,
size 4, zorder 3) and bars (width 0.62, α0.85, zorder 2) of MAD per block; bar colour by class
(close `#54A24B`, acceptable `#4C78A8`, marginal `#F58518`, nonconformity `#E45756`). Dashed threshold
lines at 0.006/0.012/0.015 (`#555555`, lw 0.9, α0.75) with right-aligned labels
`"0.006 close"`, `"0.012 acceptable"`, `"0.015 marginal"` at x = n_blocks − 0.52, y = t + 0.00018 (fontsize 8).
Above each bar (y = MAD + 0.00035) the class label without the word ` conformity`. Title
`First-digit Benford MAD by predeclared year block`, x label `Year block`, y label
`Mean absolute deviation from Benford`, y limit [0, ymax], y-grid α0.22 lw 0.8, legend upper right,
no frame, fontsize 8. PNG not compared byte-for-byte.

## Manifest `figures/year_block_mad_manifest.json` (JSON-STD)

`{status: "ok", source_csv, source_csv_sha256 (sha256 of the CSV file bytes),
generated_figure: {path, sha256, bytes}, thresholds: {close_conformity_lt: 0.006,
acceptable_conformity_lt: 0.012, marginally_acceptable_conformity_lt: 0.015, nonconformity_gte: 0.015},
blocks: [{block, first_digit_mad, nigrini_classification, sample_size}]}` — `first_digit_mad` values are
the floats **as parsed from the 12-decimal CSV** (e.g. `0.012916039293`). Print the manifest plus
`manifest` path; exit 0.

## Oracle

| file | compared fields | tolerance |
|---|---|---|
| `figures/year_block_mad_manifest.json` | `blocks` (all), `thresholds`, `source_csv_sha256` (= `f6520a0e80f8ce8497681f52fb17437c464d87973d45bbc92a6e3d4d0c6d241b` when the CSV is byte-identical) | exact |
| `figures/year_block_mad.png` | exists, non-empty PNG | — |
