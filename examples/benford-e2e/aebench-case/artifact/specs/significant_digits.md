# Spec: `significant_digits.py` (workspace root) — standalone digit library (DIGITS-NORMALIZE)

> **Audience**: implementers. **Source of truth for**: experiment
> `significant-digit-extraction-unit-tests` (the original created this file inline in its run command;
> the same code also shipped as a root-level file). Tests: `test_significant_digits.md`.

```python
@dataclass(frozen=True)
class DigitResult:
    first: Optional[int]
    second: Optional[int]
    excluded_reason: Optional[str] = None
```

`_to_decimal(value) -> (Decimal | None, reason | None)`: `None` → `missing_or_blank`; a `str` is
stripped and empty → `missing_or_blank`; `Decimal(str(value))` failure (`InvalidOperation`,
`ValueError`) → `missing_or_blank`; not finite → `non_finite`; `== 0` → `zero`; else `(abs(dec), None)`.
(Unlike DIGITS-DECIMAL, `bool` is not special-cased: `True` parses as `Decimal("True")` → invalid →
`missing_or_blank`.)

`significant_digits(value) -> DigitResult`: on a reason → `DigitResult(None, None, reason)`.
`text = format(dec.normalize(), "f")`; `digits = [ch for ch in text if ch.isdigit()]`; if no non-zero
digit → `DigitResult(None, None, "zero")`; `i` = index of the first non-zero digit;
`first = int(digits[i])`; `second = int(digits[i+1])` if `i + 1 < len(digits)` else **`None`**.

`first_significant_digit(v)` / `second_significant_digit(v)` return the respective fields.

Differences vs `scripts/digits.py`: a value with a single significant digit gets `second = None`
(not 0). `normalize()` does not lose integer zeros in fixed format: `Decimal("1000").normalize()` is
`1E+3` and `format(..., "f")` gives `"1000"`, so `second("1000") == 0`; `"1.0"` normalizes to `1` →
second `None`. Examples: `"7"` → `(7, None)`; `"6.02e23"` → `(6, 0)`; `-123.45` → `(1, 2)`;
`"-0.000904"` → `(9, 0)`.
