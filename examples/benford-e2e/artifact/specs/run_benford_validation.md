# Spec: `run_benford_validation.py` (workspace root) — standalone end-to-end validation

> **Audience**: implementers. **Source of truth for**: experiment `benford-world-bank-population-validation`
> (run as `python run_benford_validation.py --outdir benford_validation_run`). Standard library +
> matplotlib only. Self-contained: it does **not** import `scripts/`.

## CLI

`--outdir PATH` (default: the directory containing the script). The directory is resolved to an
absolute path and created (`parents=True, exist_ok=True`). All outputs, including the downloaded CSV,
go into it.

## Constants

`URL = PINNED_URL`, `EXPECTED_SHA256`, `EXPECTED_ROWS = 17195`, `EXPECTED_SCHEMA = EXPECTED_HEADER`,
`CONTROL_SEED = 20260717`, MAD ranges = NIGRINI1 (common.md §4) — **applied to both first- and
second-digit MADs** (quirk: the second digit is classified with first-digit cutoffs).

## Digit extraction (`extract_significant_digits(value) -> DigitResult(first, second, excluded_reason)`)

Same semantics as DIGITS-DECIMAL (`digits.md`), restated:

1. `None` → `(None, None, "missing_or_blank")`. `text = str(value).strip()`; `""` → `missing_or_blank`.
2. `Decimal(text)`; on `InvalidOperation`/`ValueError` → `missing_or_blank` (quirk: no separate
   non-numeric code). Not finite (`NaN`, `Infinity`) → `"non_finite"`.
3. `dec = abs(dec)`; `dec == 0` → `"zero"`.
4. `fixed = format(dec, "f")`; keep digit characters; drop leading zeros; first = 1st remaining digit,
   second = 2nd remaining digit or **0** if only one; no digits → `"zero"`.

## Unit tests (run first, in-process)

Before any download, print `Running digit extraction unit tests...` and run (unittest, verbosity 2,
to stdout) these five tests; any failure → `SystemExit("digit extraction unit tests failed")`:

| test | assertion |
|---|---|
| `test_first_digit_integer` | `"54922"` → first 5 |
| `test_first_digit_small_decimal` | `"0.0071"` → first 7, second 1 |
| `test_scientific_and_negative` | `"-1.23e5"` → `DigitResult(1, 2, None)` |
| `test_zero_and_blank_exclusions` | `"0"` → `zero`; `"  "` → `missing_or_blank` |
| `test_non_finite_exclusion` | `"NaN"`, `"Infinity"` → `non_finite` |

## Download & gate

1. Print `Downloading pinned dataset to <outdir>/population.csv...`. Record
   `retrieved_at = datetime.now(timezone.utc).isoformat()` (e.g. `2026-07-17T01:44:52.767970+00:00`),
   download `URL` (timeout 60), write the raw bytes to `<outdir>/population.csv`.
2. sha256 of the bytes ≠ `EXPECTED_SHA256` → `SystemExit("checksum mismatch: got <sha>, expected <exp>")`.
3. Open with `newline=""`, `encoding="utf-8"`, `csv.DictReader`; `fieldnames != EXPECTED_SCHEMA` →
   `SystemExit("schema mismatch: got [...], expected [...]")` (both lists `repr`); data rows ≠ 17195 →
   `SystemExit("row-count mismatch: got N, expected 17195")`.
4. Write `<outdir>/provenance.json` (JSON-STD):
   `{source_url, retrieved_at_utc, sha256, expected_sha256, byte_count (552112), data_rows,
   expected_data_rows, schema (list), license_attribution: "World Bank Open Data via datasets/population community package"}`.
   Print `Checksum/schema/row-count gate passed.`

## Analysis

1. For each row in file order, extract digits of `row["Value"]`; exclusions counted per reason, else
   append first to `first_digits`, second to `second_digits`.
2. `score_distribution(observed, support, probs)` with `n = len(observed)`, counts via `Counter`; for
   each `d` in `support` (increasing): `obs = count/n` (0.0 if n = 0), `exp = probs[d]`,
   `abs_dev = |obs − exp|`, `expected_count = n·exp`; if `expected_count > 0`:
   `chi += (count − expected_count)²/expected_count` (SEQ). Row dict (key order):
   `digit, observed_count, observed_proportion, benford_proportion, abs_deviation`.
   `mad = SEQ-SUM(abs_devs) / len(abs_devs)` (SEQ-MEAN); `dof = len(support) − 1`.
3. First digit: support `1..9`, `BENFORD1`. Second digit: support `0..9`, `BENFORD2` (SEQ-SUM over k).
4. **Negative control**: `rng = random.Random(20260717)`; `control_values = [rng.uniform(1.0, 10.0)
   for _ in range(len(first_digits))]` (17195 draws, in order); first digit of each via the extractor
   applied to `f"{v:.12f}"`; any `None` → `AssertionError`. Score with support `1..9`, `BENFORD1`.
   (Different seed path/distribution from the other negative controls — see README Known quirks.)

## Outputs (`<outdir>/`)

* `first_digit_results.csv`, `second_digit_results.csv`, `negative_control_first_digit_results.csv` —
  CSV-DICT (CRLF, floats repr), header `digit,observed_count,observed_proportion,benford_proportion,abs_deviation`.
* `figure1_first_digit_benford.png` (title `First-digit distribution vs Benford`) and
  `figure2_second_digit_benford.png` (title `Second-digit distribution vs generalized Benford`):
  matplotlib Agg, `figsize=(7, 4.5)`, `dpi=150`; bar of observed proportions (color `#4C78A8`,
  alpha 0.8, label `Observed`); line of Benford proportions (color `#F58518`, marker `o`, linewidth 2,
  label `Benford expected`); xticks = digits; xlabel `Digit`; ylabel `Proportion`; legend; y-grid
  alpha 0.25; `tight_layout`. Not byte-compared.
* `summary.json` — JSON-STD:

```
{
  "claim_interpretation": "supports primary Benford conformity claim by MAD; chi-square is sensitive at this sample size; negative control is nonconforming",
  "dataset": <provenance object above>,
  "analysis": {
    "total_rows", "rows_analyzed", "rows_excluded_total",
    "rows_excluded_by_reason": {sorted reason: count},
    "first_digit":  {"mad", "classification", "chi_square", "dof"},
    "second_digit": {"mad", "classification", "chi_square", "dof"},
    "negative_control": {
      "description": "same-size fixed-seed uniform random values on [1, 10), scored through same first-digit path",
      "seed": 20260717, "n", "first_digit_mad", "classification", "chi_square", "dof"}
  },
  "artifacts": {"provenance_json": "provenance.json", "summary_json": "summary.json",
    "summary_markdown": "summary.md", "first_digit_csv": "first_digit_results.csv",
    "second_digit_csv": "second_digit_results.csv",
    "negative_control_csv": "negative_control_first_digit_results.csv",
    "figure1": "figure1_first_digit_benford.png", "figure2": "figure2_second_digit_benford.png",
    "downloaded_csv": "population.csv"}
}
```

* `summary.md` — LF, trailing newline, lines joined by `\n`:

```
# Benford World Bank Population Validation

Interpretation: **<claim_interpretation>**.

## Dataset provenance

- Source URL: `<source_url>`
- Retrieval timestamp (UTC): `<retrieved_at_utc>`
- SHA-256: `<sha256>`
- Data rows: `<data_rows>`
- Schema: `Country Name, Country Code, Year, Value`

## Results

- Rows analyzed: <rows_analyzed> / <total_rows>
- Rows excluded: <rows_excluded_total> (<repr of rows_excluded_by_reason dict, e.g. {}>)
- First digit MAD: <mad:.9f> (<classification>); chi-square=<chi:.6f>, dof=<dof>
- Second digit MAD: <mad:.9f> (<classification>); chi-square=<chi:.6f>, dof=<dof>
- Negative control first digit MAD: <mad:.9f> (<classification>); chi-square=<chi:.6f>, dof=<dof>

## Artifact files

- <label>: `<file>`        ← one line per "artifacts" entry, in the insertion order listed above
```

Finally print `json.dumps(analysis, indent=2, sort_keys=True)` and `Wrote artifacts to <outdir>`; exit 0.

## Oracle (paths relative to workspace root)

| file | compared fields | tolerance |
|---|---|---|
| `benford_validation_run/first_digit_results.csv`, `second_digit_results.csv`, `negative_control_first_digit_results.csv` | all cells | exact text |
| `benford_validation_run/summary.json` | `analysis.*`, `dataset.sha256`, `dataset.byte_count`, `dataset.data_rows` | ints/strings exact; floats rel 1e-12 |
| `benford_validation_run/summary.md` | `## Results` lines | exact text |
| `benford_validation_run/provenance.json` | all but `retrieved_at_utc` | exact |

Reference values: first-digit MAD `0.007314647983807111` (acceptable conformity), chi-square
`100.16554215204238`; second-digit MAD `0.004058150935433028` (close conformity), chi-square
`49.27746805969423`; negative control MAD `0.06050107008993974` (nonconformity), chi-square
`7312.294283374889`; control counts for digits 1 and 2: `1875`, `1890`; 0 exclusions.
