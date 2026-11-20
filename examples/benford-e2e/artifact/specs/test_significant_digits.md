# Spec: `test_significant_digits.py` (workspace root) — unittest suite for `significant_digits.py`

> **Audience**: implementers. **Source of truth for**: the check of experiment
> `significant-digit-extraction-unit-tests`. Run: `python -m unittest discover -s . -p "test_significant_digits.py" -v`
> (the original ran `-p "test_*.py"` in a directory containing only these two files).

`from significant_digits import DigitResult, first_significant_digit, second_significant_digit, significant_digits`;
class `SignificantDigitExtractionTests(unittest.TestCase)` with exactly five tests:

1. `test_first_digit_examples_from_experiment`: `first(54922) == 5`, `first("0.0071") == 7`.
2. `test_second_digit_examples`: `second(54922) == 4`, `second("0.0071") == 1`, `second("1000") == 0`,
   `second("7") is None`.
3. `test_negative_and_scientific_notation`: `significant_digits(-123.45) == DigitResult(1, 2, None)`,
   `("-0.000904") == DigitResult(9, 0, None)`, `("6.02e23") == DigitResult(6, 0, None)`.
4. `test_excluded_values_have_reasons` (subTest per case): `0, "0.000"` → `zero`;
   `"", "   ", None, "not-a-number"` → `missing_or_blank`; `inf, -inf, nan` → `non_finite`; first and
   second are `None`.
5. `test_reason_counts_are_explicitly_countable`: over `[54922, "0.0071", 0, "", float("nan"), "1.0"]`
   → 3 retained and reason counts `{"zero": 1, "missing_or_blank": 1, "non_finite": 1}`.

`if __name__ == "__main__": unittest.main(verbosity=2)`. Expected: `Ran 5 tests … OK`
(the original transcript is kept among the reference outputs as `test_output.txt`).
