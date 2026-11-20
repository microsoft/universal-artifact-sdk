# Spec: `second_digit_pvalue_residuals.py` (workspace root) — second-digit p-value & residuals

> **Audience**: implementers. **Source of truth for**: experiment
> `second-digit-p-value-and-residual-diagnostics`. Standard library only (no SciPy). Writes its three
> outputs **next to the script** (workspace root).

No CLI flags. Run `python second_digit_pvalue_residuals.py`.

## Algorithm

1. Timestamp (UTC ISO, `Z`). Download `PINNED_URL` (timeout 60); sha256 mismatch →
   `SystemExit("SHA-256 mismatch: got …, expected …")`. Decode `utf-8`, `csv.DictReader(text.splitlines())`;
   fieldnames ≠ header → `SystemExit("Schema mismatch: …")`; ≠17195 rows → `SystemExit("Row-count mismatch: …")`.
2. Second digit (DIGITS-RESIDUAL) of each `row["Value"]`: strip; empty → `missing_or_blank`;
   `Decimal` failure → `not_numeric`; not finite → `non_finite`; `<= 0` → `non_positive`;
   `digits = format(abs(dec), "f").replace(".", "").lstrip("0")`; empty → `non_positive`;
   `len(digits) < 2` → **excluded** as `fewer_than_two_significant_digits` (differs from
   `scripts/digits.py`, which maps those to 0); else `int(digits[1])`.
3. `n = Σ counts`; `probs[d] = BENFORD2[d]` for `d = 0..9`. For `d = 0..9` in order:
   `obs = count/n`, `expected_count = p·n`, `residual = (count − expected_count)/sqrt(expected_count)`,
   `abs_dev = |obs − p|`, `chi += (count − expected_count)²/expected_count`, `mad += abs_dev`
   (both SEQ accumulations from 0.0); `mad /= 10.0`; `dof = 9`.
4. `p_value = Q(dof/2, chi/2)` with this regularized upper incomplete gamma (Numerical-Recipes style;
   `eps = 1e-14`, `fpmin = 1e-300`, `max_iter = 10000`, `gln = math.lgamma(a)`):
   * `a <= 0 or x < 0` → `ValueError`; `x == 0` → 1.0.
   * If `x < a + 1`: series — `ap = a; term = 1/a; total = term`; repeat: `ap += 1; term *= x/ap;
     total += term`; when `|term| < |total|·eps`: `p = total·exp(−x + a·log(x) − gln)`; return
     `clamp(1 − p, 0, 1)`. No convergence → `RuntimeError`.
   * Else continued fraction (modified Lentz): `b = x + 1 − a; c = 1/fpmin; d = 1/b` (if `|b| > fpmin`
     else `1/fpmin`); `h = d`; for `i = 1..max_iter`: `an = −i·(i − a); b += 2; d = an·d + b`
     (`|d| < fpmin → d = fpmin`); `c = b + an/c` (`|c| < fpmin → c = fpmin`); `d = 1/d`;
     `delta = d·c; h *= delta`; if `|delta − 1| < eps`: return `clamp(exp(−x + a·log(x) − gln)·h, 0, 1)`.
     No convergence → `RuntimeError`.
5. Result object: `{experiment: "Second-digit p-value and residual diagnostics",
   provenance: {source_url, retrieval_timestamp_utc, sha256, expected_sha256, data_rows, columns},
   analysis: {total_rows, analyzed_positive_finite_values_with_second_digit: n, excluded_rows,
   exclusions_by_reason (sorted), second_digit_mad, chi_square, dof, p_value,
   p_value_method: "regularized upper incomplete gamma Q(dof/2, chi_square/2), pure Python",
   per_digit: [{digit, observed_count, observed_proportion, benford_proportion, expected_count,
   standardized_residual, abs_deviation}]}}`.

## Outputs (workspace root)

* `second_digit_pvalue_residuals_results.json` — JSON-STD.
* `second_digit_pvalue_residuals_by_digit.csv` — CSV-DICT (CRLF, floats repr), columns in the
  per_digit order above.
* `second_digit_pvalue_residuals_summary.md` — LF, trailing newline:

```
# Second-digit p-value and residual diagnostics

Source URL: `<url>`
Retrieval timestamp (UTC): `<ts>`
SHA-256: `<sha>`
Data rows verified: 17195

## Summary

Analyzed rows: <n>
Excluded rows: <k> (<exclusions dict repr, e.g. {}>)
Second-digit MAD: <mad:.12f>
Chi-square(dof=9): <chi:.12f>
p-value: <p:.12g>

## Standardized residuals by second digit

| digit | observed_count | observed_prop | benford_prop | expected_count | residual | abs_deviation |
|---:|---:|---:|---:|---:|---:|---:|
| d | count | obs:.9f | p:.9f | expected:.3f | residual:.6f | abs_dev:.9f |   ← 10 rows
```

Print a JSON status (`rows, analyzed, chi_square, dof, p_value, second_digit_mad, outputs`); exit 0.

## Oracle

| file | compared fields | tolerance |
|---|---|---|
| `second_digit_pvalue_residuals_by_digit.csv` | all cells | exact text |
| `second_digit_pvalue_residuals_results.json` | `analysis.*` except nothing | ints exact; `chi_square` (`49.27746805969423`), `second_digit_mad` (`0.004058150935433028`) rel 1e-12; `p_value` (`1.472389888615024e-07`) rel 1e-9 |
| `second_digit_pvalue_residuals_summary.md` | Summary + residual table lines | exact text |

Largest residual: digit 0, `+5.557610312342366`.
