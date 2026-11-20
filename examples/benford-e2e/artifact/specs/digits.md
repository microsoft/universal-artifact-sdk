# Spec: `scripts/digits.py` — significant-digit extraction library (DIGITS-DECIMAL)

> **Audience**: implementers. **Source of truth for**: the digit-extraction API used by every
> `scripts/` analysis. Tests: `specs/test_digits.md`.

## API

```python
@dataclass(frozen=True)
class DigitResult:
    first: int | None
    second: int | None
    reason: str | None = None
    significant_digit_count: int = 0
    @property
    def is_valid(self) -> bool: return self.reason is None

def extract_significant_digits(value) -> DigitResult
def first_significant_digit(value) -> int | None   # extract_significant_digits(value).first
def second_significant_digit(value) -> int | None  # extract_significant_digits(value).second
```

## Algorithm `extract_significant_digits(value)`

1. Parse to `decimal.Decimal`:
   * `None` or any `bool` → unparseable.
   * `str`: strip whitespace; empty → unparseable; else `Decimal(text)`.
   * anything else (int, float, numpy scalar, Decimal): `Decimal(str(value))`.
   * `InvalidOperation`/`ValueError` → unparseable.
2. unparseable → `DigitResult(None, None, "missing_or_blank")`.
3. `not dec.is_finite()` (NaN, ±Infinity, also strings `"NaN"`, `"Infinity"`, `"-Infinity"`) →
   `DigitResult(None, None, "non_finite")`.
4. `dec = abs(dec)`; if `dec.is_zero()` → `DigitResult(None, None, "zero")`.
5. `fixed = format(dec, "f")` (fixed-point, expands exponents, keeps trailing zeros of the input such
   as `1000`, `10`, `1.0`); `significant = fixed.replace(".", "").lstrip("0")`.
6. `first = int(significant[0])`; `second = int(significant[1])` if `len(significant) > 1` else `0`;
   return `DigitResult(first, second, None, len(significant))`.

Reason labels are exactly `missing_or_blank`, `non_finite`, `zero`.

Examples: `54922 → (5,4)`, `1000 → (1,0)`, `"7" → (7,0, count 1)`, `"0.0071" → (7,1)`,
`"-0.0071" → (7,1)`, `"00123.45" → (1,2)`, `"5.4922e4" → (5,4)`, `Decimal("9.9E-6") → (9,9)`.

No CLI. No output files.
