# Spec: `scripts/generate_required_figures_from_tables.py` — table-driven publication figures

> **Audience**: implementers. **Source of truth for**: experiment `required-figure-generation`
> (figures 1–2 of the paper). Reads only `results/first_digit_table.csv` and
> `results/second_digit_table.csv` (LF/pandas versions from `analyze_benford.md`). pandas + matplotlib (Agg).

CLI: `python scripts/generate_required_figures_from_tables.py [--results-dir results] [--figures-dir figures]`.

## Table validation (`load_and_validate_table(path, expected_digits, prob_fn)`) — failure → `SystemExit`

1. Required columns `{digit, observed_count, observed_proportion, benford_proportion, abs_deviation}`
   (`"{path} is missing required columns: {sorted(missing)}"`).
2. `digit` column as int list must equal `[1..9]` (first) / `[0..9]` (second)
   (`"{path} has digits {digits!r}, expected {expected!r}"`).
3. `max |benford_proportion − closed form| ≤ 5e-12` (closed forms BENFORD1 / BENFORD2) else
   `"{path} theoretical probabilities differ from closed-form Benford values by up to {err:.3g}"`.
4. `max | |observed − benford| − abs_deviation | ≤ 5e-12` else
   `"{path} abs_deviation column is inconsistent by up to {err:.3g}"`.

Note: the tables carry 12 decimals, so the check tolerates the ≤5e-13 rounding error.

## Figures (`plot_table(table, title, xlabel, stem)`)

rcParams: figsize 7.0×4.4, dpi/savefig.dpi 150, top/right spines off, font size 10. Bars of
`observed_proportion` (width 0.72, `#4C78A8`, label `Observed proportion`); line of
`benford_proportion` (`#F58518`, marker `o`, lw 2.0, markersize 5, label `Benford expectation`);
y label `Proportion`, x ticks = digits, y limit `[0, 1.18·max(max obs, max expected)]`, y-grid α0.25
lw 0.8, legend no frame, tight layout. Saved as `<stem>.png` and `<stem>.pdf` (PDF metadata fixed:
`Title`=title, `Author`="Benford reproduction", `Subject`="Benford figure generated from recorded CSV tables",
`Keywords`="Benford, reproducibility, World Bank population", `Creator`="generate_required_figures_from_tables.py",
`Producer`="matplotlib", `CreationDate`=None, `ModDate`=None).

| stem | title | x label |
|---|---|---|
| `figures/first_digit_benford` | `World Bank population first digits vs. Benford` | `First significant digit` |
| `figures/second_digit_benford` | `World Bank population second digits vs. generalized Benford` | `Second significant digit` |

## Manifest `figures/figure_generation_manifest.json` (JSON-STD)

`{status: "ok", source_tables: {first_digit_table_csv, first_digit_table_sha256,
second_digit_table_csv, second_digit_table_sha256}, generated_figures: [{path, sha256, bytes}] ×4 in
order first.png, first.pdf, second.png, second.pdf}`. Print manifest + `manifest` path. Exit 0.

## Oracle

| file | compared fields | tolerance |
|---|---|---|
| `figures/figure_generation_manifest.json` | `status`; `source_tables.first_digit_table_sha256` = `eded21643a7f50efc890940d36b264d1ad54e95b9cd23b8b104bdd9f8165cdcb`, `second_digit_table_sha256` = `b49eae88c3d2a6c101b4201258a7fc794fb2cf36825fc8883e313c1e5d58cf00` (i.e. byte-identical tables); 4 figure entries with matching on-disk sha/bytes | exact |
| `figures/first_digit_benford.png`, `figures/second_digit_benford.png` | exist, non-empty; visually: bars = table proportions | not byte-compared |
