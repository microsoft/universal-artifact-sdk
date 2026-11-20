# Spec: `scripts/validate_metadata_filter.py` — checksum-pinned World Bank metadata aggregate filter

> **Audience**: implementers. **Source of truth for**: experiment `pinned-world-bank-metadata-filter`
> (main script; the inline variant is `metadata_filter_oneliner.md`). Standard library only
> (no numpy/pandas). Does **not** import `scripts/digits.py` (own copy of the algorithm).

## Constants

* `POPULATION_URL/SHA256/EXPECTED_ROWS/EXPECTED_HEADER` = common.md §2.
* `METADATA_URL = "https://api.worldbank.org/v2/country?format=json&per_page=400"`
* `METADATA_SHA256 = "d29d57f8adf954c5e2a1520a02fb2c7b45575d8db3bd327a9dff47d66914231c"` (raw response bytes as retrieved July 2026)
* `METADATA_EXPECTED_TOTAL = 295`
* `PRIOR_STATIC_AGGREGATE_CODES` = the 48-code set of `run_country_only_sensitivity.md`.
* `EMBEDDED_AGGREGATES` — the 47 `[code, name]` pairs derived from the pinned snapshot (names are
  exact, including the trailing space in `"Latin America & Caribbean "` and `"Sub-Saharan Africa "`):

```json
[["AFE", "Africa Eastern and Southern"], ["AFW", "Africa Western and Central"], ["ARB", "Arab World"], ["CEB", "Central Europe and the Baltics"], ["CSS", "Caribbean small states"], ["EAP", "East Asia & Pacific (excluding high income)"], ["EAR", "Early-demographic dividend"], ["EAS", "East Asia & Pacific"], ["ECA", "Europe & Central Asia (excluding high income)"], ["ECS", "Europe & Central Asia"], ["EMU", "Euro area"], ["EUU", "European Union"], ["HIC", "High income"], ["HPC", "Heavily indebted poor countries (HIPC)"], ["IBD", "IBRD only"], ["IBT", "IDA & IBRD total"], ["IDA", "IDA total"], ["IDB", "IDA blend"], ["IDX", "IDA only"], ["LAC", "Latin America & Caribbean (excluding high income)"], ["LCN", "Latin America & Caribbean "], ["LDC", "Least developed countries: UN classification"], ["LIC", "Low income"], ["LMC", "Lower middle income"], ["LMY", "Low & middle income"], ["LTE", "Late-demographic dividend"], ["MEA", "Middle East, North Africa, Afghanistan & Pakistan"], ["MIC", "Middle income"], ["MNA", "Middle East, North Africa, Afghanistan & Pakistan (excluding high income)"], ["NAC", "North America"], ["OED", "OECD members"], ["OSS", "Other small states"], ["PRE", "Pre-demographic dividend"], ["PSS", "Pacific island small states"], ["PST", "Post-demographic dividend"], ["SAS", "South Asia"], ["SSA", "Sub-Saharan Africa (excluding high income)"], ["SSF", "Sub-Saharan Africa "], ["SST", "Small states"], ["TEA", "East Asia & Pacific (IDA & IBRD countries)"], ["TEC", "Europe & Central Asia (IDA & IBRD countries)"], ["TLA", "Latin America & the Caribbean (IDA & IBRD countries)"], ["TMN", "Middle East, North Africa, Afghanistan & Pakistan (IDA & IBRD)"], ["TSA", "South Asia (IDA & IBRD)"], ["TSS", "Sub-Saharan Africa (IDA & IBRD countries)"], ["UMC", "Upper middle income"], ["WLD", "World"]]
```

* `CANONICAL_LIST_SHA256 = "18eb78dd7f7093e3dd9e26ae569875ef138f5cb3b2c2d7b1a402016aea1616c8"`.

**Metadata drift.** The World Bank API is not immutable; today it returns a different body
(296 rows, different hash). The original script fails closed on a hash mismatch. To keep the
experiment reproducible this spec adds `--on-metadata-drift {fail,embedded}` (default `fail`,
the original behaviour). With `embedded`, a metadata hash/shape/row-count mismatch is *recorded*
instead of fatal and the aggregate records are taken from `EMBEDDED_AGGREGATES`; the run command
uses `embedded`. Either way the generated list must hash to `CANONICAL_LIST_SHA256`.

## CLI

`python scripts/validate_metadata_filter.py [--data-dir data] [--results-dir results]
[--population-path P] [--metadata-path M] [--on-metadata-drift fail|embedded]`

`fetch_or_read(url, path)`: if `path` given **and exists** → `(bytes, "local:<path>")`; else HTTP GET
(timeout 60) → `(bytes, url)`.

## Algorithm

1. Create dirs; `retrieved_at` = UTC ISO timestamp with `Z`. Read population then metadata.
2. **Population** (fatal on mismatch, `SystemExit(msg)`): sha256 must equal; decode **`utf-8`**;
   `rows = list(csv.DictReader(text.splitlines()))`; non-empty; keys of first row == header; 17195 rows.
   Messages: `Population checksum mismatch: got {d}, expected {e}`, `Population CSV has no data rows`,
   `Population header mismatch: got {keys!r}`, `Population row-count mismatch: got {n}, expected 17195`.
3. **Metadata**: sha256 must equal `METADATA_SHA256` (`Metadata checksum mismatch: got {d}, expected {e}`);
   JSON must be a 2-element list `[page: dict, rows: list]` (`Unexpected World Bank metadata JSON shape`);
   `int(page["total"]) == len(rows) == 295` (`Metadata row-count mismatch: page total {t}, rows {n}, expected 295`).
   In `embedded` mode these failures are recorded (`metadata_drift: true`, `drift_reasons: [msgs]`) and
   step 5 uses the embedded list.
4. Write the exact downloaded bytes to `data/population_metadata_filter.csv` and
   `data/world_bank_country_metadata.json`.
5. Aggregates: `population_codes = {row["Country Code"]}`. Normal mode: aggregate rows = metadata rows with
   `(row.get("region") or {}).get("value") == "Aggregates"`; `all_codes = {row["id"]}`. Embedded mode:
   `all_codes` = the 47 embedded codes (total-in-metadata then reported as 47, absent list `[]`).
   `derived_present = sorted(all_codes ∩ population_codes)`, `absent = sorted(all_codes − population_codes)`,
   `static_missing = sorted(PRIOR_STATIC − set(derived_present))`, `extra = sorted(set(derived_present) − PRIOR_STATIC)`,
   `static_match = not static_missing and not extra`.
   `intentional_update_note` = `None` if match else
   `"The checksum-pinned World Bank metadata snapshot is authoritative for this validation. It does not mark the prior static code(s) {static_missing} as current aggregate metadata rows, so those code(s) are kept in the metadata-driven country/territory panel rather than carried forward from the static list."`
   (`{static_missing}` = Python list repr, e.g. `['FCS']`).
6. Records: for aggregate rows sorted by id and present in the population:
   `{"code": id, "name": name or "", "metadata_rule": "region.value == Aggregates"}` (dict key order
   code, name, metadata_rule). Canonical bytes = `(json.dumps(records, indent=2, sort_keys=True,
   ensure_ascii=False) + "\n").encode("utf-8")` → write to `results/metadata_aggregate_codes.json`;
   its sha256 is `aggregate_list_sha`. CSV `results/metadata_aggregate_codes.csv` via CSV-DICT
   (header `code,name,metadata_rule`).
7. Digit extraction for each `row.get("Value")`: identical to DIGITS-DECIMAL (returns first, second, reason).
   Panel scoring: `tabulate(values, probs)` builds rows `{digit, observed_count, observed_proportion,
   benford_proportion, abs_deviation}` in probs order, **`mad = statistics.fmean(abs_deviations)`
   (FSUM-MEAN)**, χ² SEQ-SUM, NIGRINI1 for first digit. `score_panel` returns the same structure as
   `run_country_only_sensitivity.md` (`first_digit` with nigrini; `second_digit` without).
8. Score full rows and `country_rows` (Country Code ∉ derived_present). Write (CSV-DICT, CRLF, floats
   as repr): `results/metadata_country_only_first_digit_table.csv`, `…_second_digit_table.csv`
   (country panel), `results/metadata_country_only_comparison.csv` (same columns as the country-only
   comparison; panels `full_verified_panel`, `metadata_country_only_panel`; `unique_codes` = distinct codes).
9. `results/metadata_provenance.json` (JSON-STD): `retrieved_at_utc`, `metadata {source_url,
   fetch_source, snapshot_path, sha256, expected_sha256, checksum_match, row_count, expected_row_count: 295,
   page, aggregate_rule: "World Bank country metadata row has region.value == 'Aggregates'",
   aggregate_codes_total_in_metadata, aggregate_codes_present_in_population,
   aggregate_codes_absent_from_population}` (+ `metadata_drift`, `drift_reasons` in embedded mode),
   `population {source_url, fetch_source, snapshot_path, sha256, expected_sha256, checksum_match: true,
   row_count, expected_row_count, schema}`, `generated_aggregate_code_list {json_path, csv_path,
   sha256_canonical_json, code_count, matches_prior_static_list, prior_static_missing_from_metadata,
   metadata_extra_present_vs_prior_static}`.
10. `results/metadata_country_only_summary.json` (JSON-STD): `run_timestamp_utc`,
    `validation_status` (`"passed"` if static_match else `"passed_with_intentional_update"`),
    `claim_validated: "Aggregate-row exclusion is derived from a separately checksum-pinned World Bank metadata source instead of an unprovenanced static list."`,
    `metadata_provenance_json`, `generated_aggregate_code_list_json`, `…_csv`, `…_sha256`,
    `filter {metadata_rule: "region.value == Aggregates", removed_unique_codes, removed_rows,
    country_only_rows, country_only_unique_codes, matches_prior_static_list,
    prior_static_missing_from_metadata, metadata_extra_present_vs_prior_static, intentional_update_note}`,
    `full_panel {analyzed_rows, excluded_rows, first_digit, second_digit}`,
    `metadata_country_only_panel {analyzed_rows, excluded_rows, exclusions_by_reason, first_digit,
    second_digit}`, `outputs {…7 paths}`. Print status JSON; exit 0.

## Outputs & oracle

| file | compared fields | tolerance |
|---|---|---|
| `results/metadata_aggregate_codes.json` | sha256 = `CANONICAL_LIST_SHA256` | exact |
| `results/metadata_country_only_comparison.csv` | all cells | exact text (floats repr) |
| `results/metadata_country_only_summary.json` | `validation_status`, `filter.*`, `metadata_country_only_panel.*`, `generated_aggregate_code_list_sha256` | ints/labels exact; floats rel 1e-12 |

Expected: 47 codes removed (static list's `FCS` is not a metadata aggregate → kept), 3,055 rows
removed, 14,140 rows / 218 codes remain; country first-digit MAD `0.007540426519039584`
(acceptable), χ² `98.71453554721771`; second-digit MAD `0.004864316834289349`.
