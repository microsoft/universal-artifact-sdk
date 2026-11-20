# Spec: `scripts/reproduce_positive_control_standalone.py` — self-contained positive-control rerun

> **Audience**: implementers. **Source of truth for**: the clean-environment re-derivation used by
> experiment `positive-log-uniform-synthetic-control` (the original also ran this exact program
> inline). Needs only numpy + network. No imports from `scripts/`.

No CLI flags. Output directory: `results/positive_control_standalone/` (create it).
**Path note**: the original wrote into an absolute directory of a throw-away container; the
directory is relocated here so the run does not overwrite the canonical outputs of
`run_positive_control_validation.md`.

## Algorithm

1. `raw` = HTTP GET `PINNED_URL` (timeout 60). `sha = sha256(raw)`;
   `rows = list(csv.reader(io.StringIO(raw.decode("utf-8-sig"))))`; `assert sha == EXPECTED_SHA256`,
   `assert rows[0] == EXPECTED_HEADER`, `assert len(rows) − 1 == 17195` (AssertionError → non-zero exit).
2. `n = 17195`; `rng = numpy.random.default_rng(424242)`;
   `values = numpy.power(10.0, rng.uniform(0.0, 6.0, size=n))` (same draws as the main script).
3. First digit of each `x`: `format(Decimal(str(x)), "f").replace(".", "").lstrip("0")[0]` as int.
4. Table text (LF line endings, trailing newline):
   header `digit,observed_count,observed_proportion,benford_proportion,abs_deviation`, then for
   `d = 1..9`: `f"{d},{count},{obs:.12f},{p:.12f},{abs_dev:.12f}"` with `obs = count/n`,
   `p = BENFORD1[d]`, `abs_dev = |obs − p|` → `positive_control_first_digit_table.csv`.
5. `mad = SEQ-SUM(abs_devs) / 9.0` (**SEQ-MEAN**); `chi = SEQ-SUM_{d=1..9} (count_d − n p_d)²/(n p_d)`;
   NIGRINI1 label.
6. `positive_control_summary.json` (JSON-STD):
   `{experiment: "Positive log-uniform synthetic control",
   dataset_gate: {source_url, sha256, checksum_match: true, row_count: n, schema_match: true},
   positive_control: {positive_control_seed: 424242, sample_size: n, generation_log10_min: 0.0,
   generation_log10_max: 6.0, generation_orders_of_magnitude: 6.0, positive_control_first_digit_mad,
   positive_control_first_digit_chi_square, dof: 8, nigrini_classification, observed_counts {"1".."9"}},
   outputs: {dir: "<output dir>"}, success: label in {close, acceptable conformity}}`. Print it.
   Exit 0 (no success-based exit code).

## Oracle

Counts and label must equal `run_positive_control_validation.md`'s; MAD/χ² rel 1e-12 of
`0.001620904667174733` / `6.177076780388321` (the SEQ-MEAN and PAIRWISE-MEAN may differ in the last
ulp; tolerance covers it). Table text must equal the main script's table byte-for-byte.
