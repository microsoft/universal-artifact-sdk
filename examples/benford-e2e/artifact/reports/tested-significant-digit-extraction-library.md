# Tested significant-digit extraction library

Status: Successful

Reproduce: implement the specs referenced by experiment `tested-significant-digit-extraction-library` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Implemented the smallest concrete validation for the significant-digit primitive under the workspace root. The new `scripts/digits.py` exposes deterministic first/second significant-digit helpers and a `DigitResult` carrying explicit exclusion reasons. The tests in `tests/test_digits.py` cover the required examples (`54922`, `0.0071`, `1000`, `10`, `19`), negative values, numeric strings, scientific notation, valid digit ranges, and exclusions for zero, blank, `None`, non-numeric strings, booleans, `NaN`, and infinities. Validation was run in `python:3.11` Docker along with the existing provenance-gate tests; both passed with output `ok` / `ok`.

## Lessons
Use `Decimal(str(value))` plus fixed-point formatting to keep one normalization path for integers, decimals below one, powers of ten, and scientific notation. Preserve reason-coded exclusions (`zero`, `missing_or_blank`, `non_finite`) so later Benford analysis can report skipped rows transparently. When importing a dataclass module via `importlib.util.module_from_spec`, register it in `sys.modules` before `exec_module`; otherwise postponed annotations can break dataclass processing.
