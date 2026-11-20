# Spec: `tests/test_digits.py` — unit tests for `scripts/digits.py`

> **Audience**: implementers. **Source of truth for**: the digit-library unit tests (`check` command).

Loads `scripts/digits.py` by file path (`importlib.util.spec_from_file_location`, path =
`<tests dir>/../scripts/digits.py`, registered in `sys.modules["digits"]` before exec). Runnable both
as `python tests/test_digits.py` (calls every test in order, prints `ok`, exit 0) and under pytest.
Any failed `assert` → non-zero exit.

Helpers: `assert_digits(v, f, s)` asserts `is_valid`, `.first == f`, `.second == s`, and the two
convenience functions agree. `assert_excluded(v, reason)` asserts not valid, `.reason == reason`, both
digits `None` and both convenience functions return `None`.

| test | assertions |
|---|---|
| integer/power-of-ten | `54922→(5,4)`, `1000→(1,0)`, `10→(1,0)`, `19→(1,9)` |
| one-significant-digit | `"7"` valid, first 7, second 0, `significant_digit_count == 1` |
| decimals/negatives | `Decimal("0.0071")`, `"0.0071"`, `"-0.0071"` → `(7,1)`; `-54922 → (5,4)` |
| strings/scientific | `"00123.45"→(1,2)`, `"5.4922e4"→(5,4)`, `"7.1E-3"→(7,1)`, `Decimal("1E+6")→(1,0)`, `Decimal("9.9E-6")→(9,9)` |
| exclusions | `0, 0.0, "0", "0.000"` → `zero`; `None, "", "   ", "not-a-number", True, False` → `missing_or_blank`; `float("nan"), float("inf"), float("-inf"), "NaN", "Infinity", "-Infinity"` → `non_finite` |
| ranges | for `"1","2.5","99","0.00042","8e8",Decimal("3.14159")`: valid, `1≤first≤9`, `0≤second≤9` |
