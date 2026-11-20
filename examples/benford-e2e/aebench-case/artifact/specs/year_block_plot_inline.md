# Spec: `scripts/year_block_plot_inline.py` — inline (self-contained) year-block re-derivation + plot

> **Audience**: implementers. **Source of truth for**: the self-contained program the original
> `plot-temporal-robustness-diagnostics` run executed inline (heredoc in its run command). It recomputes
> the year blocks from the raw CSV with a **different digit extraction** (DIGITS-STR on `float`) and
> **SEQ-MEAN**, then plots. Standard library + matplotlib.

No CLI flags. **Output root relocated** to `results/year_block_inline/` (the original wrote into an
absolute container directory whose `results/`, `figures/` and `data/` it overwrote; relocation avoids
clobbering the canonical outputs). Creates `<root>/data`, `<root>/results`, `<root>/figures`.

## Algorithm

1. Download `PINNED_URL`; `assert sha256 == EXPECTED_SHA256`; write `<root>/data/population.csv`;
   `rows = list(csv.DictReader(raw.decode("utf-8").splitlines()))`; `assert len(rows) == 17195`.
2. Blocks as in `run_year_block_robustness.md`; `ben = [BENFORD1[d] for d in 1..9]`.
3. Per block: `vals = [r["Value"].strip() for r in rows if a <= int(r["Year"]) <= b]`; `counts = [0]*9`;
   for each `v`: `x = float(v)` (exception → excluded += 1); if not finite or `x <= 0` → excluded;
   else `counts[int(str(int(abs(x)))[0]) − 1] += 1`. `n = Σ counts`; `obs = c/n`;
   `mad = SEQ-SUM |obs_d − ben_d| / 9`; `chisq = SEQ-SUM (c − n·e)²/(n·e)`; NIGRINI1.
   Record `{block, start_year, end_year, rows_total: len(vals), sample_size: n, excluded_rows,
   first_digit_mad, chi_square, dof: 8, nigrini_classification}`.
4. `<root>/results/year_block_robustness.csv` via CSV-DICT (CRLF; floats repr).
5. Plot `<root>/figures/year_block_mad.png`: as `plot_year_block_mad.md` but simplified — default bar
   width, bar colour `#F58518` if label starts with `marginal` else `#4C78A8`, legend label
   `Nonconformity >= 0.015`, plain line with markers.
6. `<root>/figures/year_block_mad_manifest.json` (JSON-STD): `{status: "ok", dataset_sha256, row_count,
   results: [records], figure: path}`; print it.

## Oracle

Per block `rows_total`, `sample_size`, `excluded_rows` (0), `nigrini_classification` exact; MAD/χ²
within rel 1e-12 of `run_year_block_robustness.md` values. No shipped reference copy.
