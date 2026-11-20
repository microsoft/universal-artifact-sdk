# Spec: `negative_control_validation.py` (workspace root) — uniform-float negative-control discrimination check

> **Audience**: implementers. **Source of truth for**: experiment `negative-control-discrimination-check`.
> Self-contained (numpy + stdlib; does not import `scripts/`). Note the different control
> (**uniform floats**) and different label set from `run_negative_control_validation.md`.

No CLI flags. Run `python negative_control_validation.py`. Output dirs `data/`, `results/` next to the script.

## Digit extraction (local)

`first_significant_digit(v)`: `None` → `missing_or_blank`; `text = str(v).strip()`; empty →
`missing_or_blank`; `Decimal(text)` failure → `missing_or_blank`; not finite → `non_finite`; `== 0` →
`zero`; `normalized = format(abs(dec), "f").replace(".", "").lstrip("0")`; empty → `zero`; else
`int(normalized[0])`. (Iterating a numpy float64 array yields `numpy.float64`; `str()` of it is the
shortest round-trip repr, e.g. `'5034.776339651108'`.)

## Labels (`classify_mad`) — QUIRK

`< 0.006` close conformity; `< 0.012` acceptable conformity; `< 0.015` **`marginal conformity`**
(not "marginally acceptable conformity"); else nonconformity.

## Scoring (`score_first_digits(values)`)

`counts = {1..9: 0}`, exclusions dict, `total`. If `total == 0` → `ValueError("no scoreable positive finite values")`.
For `d = 1..9` (in order): `obs = count/total`, `p = BENFORD1[d]` (`math.log10(1 + 1/d)`),
`abs_dev = |obs − p|`, `expected_count = total·p`, `chi += (count − expected_count)²/expected_count`
(SEQ accumulation starting at 0.0), row `{digit, observed_count, observed_proportion,
benford_proportion, abs_deviation}` (raw floats). `mad = SEQ-SUM(abs_devs) / 9`.
Summary: `{n_analyzed, excluded, mad, nigrini_classification, chi_square, degrees_of_freedom: 8}`.

## Algorithm

1. Download `PINNED_URL` (timeout 60); sha256 must match else `SystemExit("checksum mismatch: got …,
   expected …")`; write `data/population.csv`; decode `utf-8`; `csv.DictReader(text.splitlines())`;
   fieldnames must equal header (`schema mismatch: got …, expected …`); 17195 rows
   (`row-count mismatch: got …, expected 17195`).
2. `results/dataset_provenance.json` (JSON-STD): `{source_url, retrieved_at_utc (isoformat, "+00:00"
   kept), sha256, expected_sha256, row_count, expected_row_count, columns,
   license_attribution: "World Bank Open Data via datasets/population community package", local_path}`.
3. Score real `Value` strings → `n` (17195).
4. Control: `rng = numpy.random.default_rng(20260717)`; `rng.uniform(1000.0, 9999.0, size=n)`; score.
5. Control table → **`results/negative_control_uniform_float_table.csv`** (CSV-DICT: CRLF, floats repr).
   *Relocated*: the original wrote `results/negative_control_first_digit_table.csv`, which collides
   with `run_negative_control_validation.md`'s canonical table (and was overwritten there).
6. `results/negative_control_summary.json` (JSON-STD): `{experiment: "Negative-control discrimination check",
   dataset_source_url, dataset_sha256_verified, dataset_row_count_verified: 17195,
   real_data_retained_rows: n, real_data_excluded: {}, control_seed: 20260717,
   control_distribution: "uniform[1000.0, 9999.0]", control_first_digit_mad, control_nigrini_classification,
   control_chi_square, control_degrees_of_freedom: 8,
   success_criterion: "control MAD >= 0.015 and classified as nonconformity",
   success: mad >= 0.015 and label == "nonconformity", artifacts: {provenance, control_table}}`.
   Print it; exit 0 if success else 2.

## Oracle

| file | compared fields | tolerance |
|---|---|---|
| `results/negative_control_summary.json` | `real_data_retained_rows`, `control_nigrini_classification`, `success` | exact |
| same | `control_first_digit_mad` = `0.060888779695445226`, `control_chi_square` = `6897.74230178361` | rel 1e-12 |
| `results/dataset_provenance.json` | `sha256`, `row_count`, `columns` | exact |
