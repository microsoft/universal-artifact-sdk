# Spec: `scripts/validate_provenance.py` — pinned-dataset checksum gate

> **Audience**: implementers. **Source of truth for**: fetching + fail-closed verification of the
> population CSV. Tests: `specs/test_provenance_gate.md`. Constants: `specs/common.md` §2.

## Module-level API (imported by other scripts and tests)

* Constants `PINNED_URL`, `EXPECTED_SHA256`, `EXPECTED_ROW_COUNT`, `EXPECTED_HEADER` (common.md §2) and
  `ATTRIBUTION` (dict, exact strings — they are rendered into the provenance appendix):
  `dataset: "World Bank total population by country/year"`,
  `upstream_package: "datasets/population community data package"`,
  `source: "World Bank Open Data via datasets/population"`,
  `license_note: "World Bank Open Data / datasets-population attribution recorded; see upstream package metadata for full license terms."`.
* `sha256_bytes(data: bytes) -> str` — lowercase hex SHA-256.
* `fetch_bytes(url, timeout=60) -> bytes` — HTTP GET (urllib) with a generic User-Agent
  (e.g. `benford-provenance-validator/1.0`).
* `parse_csv(raw) -> (header: list[str], row_count: int)` — decode `utf-8-sig`, `csv.reader` over
  `text.splitlines()`; header = first row (`ValueError("CSV is empty")` if none); `row_count` = number
  of remaining rows.
* `validate(raw, expected_sha256, expected_row_count, expected_header) -> dict` returning keys
  `sha256, expected_sha256, checksum_match, byte_count, row_count, expected_row_count,
  row_count_match, header, expected_header (list), schema_match, failures`. `failures` is a list, in
  this order, of the applicable messages:
  * `f"checksum mismatch: expected {expected_sha256}, got {digest}"`
  * `f"schema mismatch: expected {expected_header}, got {header}"` (Python list reprs)
  * `f"row-count mismatch: expected {expected_row_count}, got {row_count}"`
* `main(argv=None) -> int`.

## CLI

`python scripts/validate_provenance.py [--url URL] [--expected-sha256 H] [--expected-row-count N]
[--data-out PATH] [--provenance-out PATH] [--source-file PATH]`

Defaults: `--url PINNED_URL`, `--data-out data/population.csv`, `--provenance-out results/provenance.json`.
`--source-file` reads bytes from a local file instead of the network.

Behaviour: record `retrieval_timestamp_utc` (`datetime.now(utc).isoformat()` with `+00:00`→`Z`), read
bytes, `validate`. On any failure: print `FAIL: dataset provenance validation failed` then each
failure as ` - <msg>` to **stderr**, write nothing, return **1**. Otherwise create parent dirs, write
the raw bytes unchanged to `--data-out`, write `--provenance-out` (JSON-STD) with keys:
`source_url, retrieval_timestamp_utc, <all validate() keys>, attribution (ATTRIBUTION),
software_versions ({python: sys.version, platform: platform.platform(), numpy, pandas, matplotlib,
requests: __version__ or "not_installed"}), validated_data_path (str of --data-out)`; print a JSON-STD
status object `{status:"ok", data_out, provenance_out, sha256, row_count, byte_count}` to stdout; return 0.

## Outputs & oracle

| file | compared fields | tolerance |
|---|---|---|
| `data/population.csv` | sha256 = `EXPECTED_SHA256` | exact |
| `results/provenance.json` | `sha256`, `checksum_match` (true), `byte_count` (552112), `row_count` (17195), `row_count_match`, `schema_match`, `header`, `failures` ([]) | exact |

Reference copy: `reference-outputs/results/provenance.json`.
