# Significant-digit extraction unit tests

Status: Completed

Reproduce: implement the specs referenced by experiment `significant-digit-extraction-unit-tests` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Created the smallest concrete validation under the workspace root: a pure-stdlib `significant_digits.py` module and `test_significant_digits.py` unit tests. Ran `python3 -m unittest discover -s . -p 'test_*.py' -v`; all 5 tests passed. Covered required examples `54922 -> 5` and `0.0071 -> 7`, second-digit extraction, negatives, scientific notation, zeros, blanks, invalid strings, NaN, and infinities. Exclusions are reason-coded as `zero`, `missing_or_blank`, or `non_finite`, enabling later transparent row-exclusion reporting.

## Lessons
A minimal pure-stdlib validation is enough to support the digit-extraction success criterion before running any empirical Benford scoring. Using `Decimal(str(value))` with fixed-point formatting provides one normalization path for integers, decimals below one, negatives, and scientific notation. Returning a structured result with `excluded_reason` makes exclusion counting explicit and testable.
