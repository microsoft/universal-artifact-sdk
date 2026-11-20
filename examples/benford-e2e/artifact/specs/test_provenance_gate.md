# Spec: `tests/test_provenance_gate.py` — unit tests for `scripts/validate_provenance.py`

> **Audience**: implementers. **Source of truth for**: the provenance-gate unit tests (`check` command).

Loads `scripts/validate_provenance.py` by file path (as in `test_digits.md`). Runnable as
`python tests/test_provenance_gate.py` (runs all tests, prints `ok`, exit 0) and under pytest.
`H = ["Country Name", "Country Code", "Year", "Value"]`.

1. **accepts exact bytes**: `raw = b"Country Name,Country Code,Year,Value\nA,AAA,2000,123\nB,BBB,2001,456\n"`;
   `validate(raw, sha256_bytes(raw), 2, H)` → `checksum_match is True`, `schema_match is True`,
   `row_count_match is True`, `failures == []`.
2. **rejects wrong hash**: `raw = b"Country Name,Country Code,Year,Value\nA,AAA,2000,123\n"`;
   `validate(raw + b"#corrupt", "0"*64, 1, H)` → `checksum_match is False` and some failure contains
   `"checksum mismatch"`.
3. **rejects schema/row count**: `raw = b"country,code,year,value\nA,AAA,2000,123\n"`;
   `validate(raw, sha256_bytes(raw), 2, H)` → `schema_match is False`, `row_count_match is False`,
   failures contain `"schema mismatch"` and `"row-count mismatch"`.
