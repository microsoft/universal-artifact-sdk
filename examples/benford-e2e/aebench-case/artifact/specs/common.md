# Common definitions (shared by all specs)

> **Audience**: implementers re-creating the code from specs. **Source of truth for**: constants,
> numeric conventions, file-format conventions and summation semantics referenced by every other spec.

Every other spec refers to the definitions below by name (e.g. "SEQ-SUM", "JSON-STD").

## 1. Workspace

All paths are relative to the **workspace root** (the current working directory when a `run.command`
is executed). The implementation creates:

```
scripts/        library + experiment scripts (see specs/README.md for the full list)
tests/          unit tests for scripts/
*.py            five root-level standalone scripts (negative_control_validation.py,
                run_benford_validation.py, second_digit_pvalue_residuals.py,
                significant_digits.py, test_significant_digits.py)
data/           input data (fetched by recipe, see DATA.md) and derived copies
results/        machine-readable outputs (JSON / CSV / MD / TEX)
figures/        PNG figures + figure manifests
```

Scripts that import siblings (`digits`, `validate_provenance`, `analyze_benford`) must insert their own
directory (`scripts/`) at the front of `sys.path` so they run as `python scripts/<name>.py` from the
workspace root.

## 2. Constants

| Name | Value |
|---|---|
| `PINNED_URL` | `https://raw.githubusercontent.com/datasets/population/425fc447a53a26c767a15a7de60c4cc2478a0595/data/population.csv` |
| `EXPECTED_SHA256` | `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a` |
| `EXPECTED_ROW_COUNT` | `17195` (data rows, header excluded) |
| `EXPECTED_BYTES` | `552112` |
| `EXPECTED_HEADER` | `["Country Name", "Country Code", "Year", "Value"]` |
| `CONTROL_SEED` | `20260717` (negative controls) |
| `POSITIVE_SEED` | `424242` (positive control) |
| `METADATA_URL` | `https://api.worldbank.org/v2/country?format=json&per_page=400` |
| `METADATA_SHA256` (canonical) | `18eb78dd7f7093e3dd9e26ae569875ef138f5cb3b2c2d7b1a402016aea1616c8` (see `validate_metadata_filter.md`) |

## 3. Benford probabilities

* `BENFORD1[d] = log10(1 + 1/d)` for `d = 1..9` (use `math.log10`).
* `BENFORD2[d2] = Σ_{k=1..9} log10(1 + 1/(10k + d2))` for `d2 = 0..9`, accumulated with SEQ-SUM in
  increasing `k`.

## 4. Nigrini first-digit MAD classification ("NIGRINI1")

Strict `<` comparisons, evaluated in order:

| condition | label |
|---|---|
| `mad < 0.006` | `close conformity` |
| `mad < 0.012` | `acceptable conformity` |
| `mad < 0.015` | `marginally acceptable conformity` |
| otherwise | `nonconformity` |

(One script uses a different third label — see `negative_control_validation.md`.)

## 5. Summation semantics (IMPORTANT for byte-identical floats)

Floating-point sums in the original code were performed under Python ≤ 3.11 / numpy 2.2 / pandas 2.3.
Three different summation orders were used; each spec says which one applies:

* **SEQ-SUM** — plain left-to-right IEEE-754 double accumulation: `acc = 0.0; for x in xs: acc += x`.
  This equals the built-in `sum()` of Python ≤ 3.11. **Python ≥ 3.12's built-in `sum()` of floats is
  compensated (Neumaier) and gives different last bits — do not use it; write the loop explicitly.**
  `SEQ-MEAN(xs) = SEQ-SUM(xs) / len(xs)`.
* **PAIRWISE-MEAN** — what `pandas.Series.mean()` (numpy pairwise reduction) produces for a float64
  column of length `n < 128` (all uses here have n = 9 or 10). With `a` the values in row order:
  `r = ((a0+a1)+(a2+a3)) + ((a4+a5)+(a6+a7))`, then `r += a8`, then (if n = 10) `r += a9`; result `r / n`.
  Using `pandas.Series.mean()` / `numpy.mean()` on a contiguous float64 array satisfies this.
* **FSUM-MEAN** — `statistics.fmean(xs)` (exactly rounded `math.fsum(xs) / n`).

Chi-square statistics are always SEQ-SUM over digits in increasing order of
`(count_d − n·p_d)² / (n·p_d)` unless the spec states otherwise.

Example (verifies your summation): the uniform negative control in `analyze_benford.md` has
first-digit MAD `0.0602555206731196` with PAIRWISE-MEAN and `0.06025552067311963` with SEQ-MEAN.

## 6. File-format conventions

* **JSON-STD**: `json.dumps(obj, indent=2, sort_keys=True) + "\n"`, UTF-8, LF newlines. Floats are
  serialised with Python `repr` (shortest round-trip). Integers stay integers. `None` → `null`.
* **JSON-NOSORT**: as JSON-STD but `sort_keys=False` (insertion order as listed in the spec).
* **CSV-PANDAS12**: written by `pandas.DataFrame.to_csv(path, index=False, float_format="%.12f")`;
  header row, comma separator, LF line endings, integer columns printed as integers, float columns
  printed with exactly 12 decimals (`%.12f`).
* **CSV-DICT**: written with `csv.DictWriter` (or `csv.writer`) using the default dialect: CRLF
  (`\r\n`) line endings, minimal quoting, floats as Python `str()`/`repr` (e.g. `0.30102999566398120`
  prints as `0.3010299956639812`), ints as ints. Files are opened with `newline=""`.
* Paths written into JSON/MD outputs are informational; the oracle ignores path- and
  timestamp-valued fields and the `software_versions`/`platform` blocks.

## 7. Significant-digit extraction variants

Several scripts extract digits differently (this is faithful to the original artifact):

* **DIGITS-DECIMAL** — `scripts/digits.py` (`digits.md`): Decimal-based, sign-insensitive, handles
  decimals/scientific notation, one-significant-digit values get `second = 0`.
* **DIGITS-NORMALIZE** — `significant_digits.py` (`significant_digits.md`): Decimal `normalize()`-based;
  one-significant-digit values get `second = None`.
* **DIGITS-STR** — `str(value).strip()` / `str(int(value))` first character (inline one-liners; only
  used on positive integers ≥ 1).
* **DIGITS-RESIDUAL** — `second_digit_pvalue_residuals.md`: values with fewer than two significant
  digits are *excluded* from the second-digit test.

## 8. Reading the population CSV

Unless a spec says otherwise: read the bytes from `data/population.csv`, decode `utf-8-sig`, parse with
`csv` / `pandas.read_csv`. All 17,195 `Value` cells are non-empty positive integers written without
quotes or decimals (some `Country Name` values are quoted and contain commas). Years span 1960–2024.
pandas reads `Value` as `int64`; `str()` of each value is its decimal integer text.

## 9. Environment

See `specs/README.md` §Environment.
