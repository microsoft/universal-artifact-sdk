# DATA — download recipe

> **Audience**: anyone reproducing this artifact. **Source of truth for**: how to obtain and verify
> the input data. Dataset metadata is declared in `datasets.yml`. No data files are shipped.

## 1. `wb-population` — World Bank total population (pinned CSV)

| Field | Value |
|---|---|
| URL (immutable, pinned by commit) | `https://raw.githubusercontent.com/datasets/population/425fc447a53a26c767a15a7de60c4cc2478a0595/data/population.csv` |
| SHA-256 | `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a` |
| Bytes | `552112` |
| Rows | 17,195 data rows + 1 header row (17,196 lines) |
| Columns | `Country Name`, `Country Code`, `Year`, `Value` (header exactly in this order) |
| Years | 1960–2024 |
| Encoding | UTF-8; some `Country Name` values are quoted because they contain commas |
| License | Data package: ODC-PDDL-1.0 (datasets/population). Upstream data: World Bank, indicator `SP.POP.TOTL`, CC BY 4.0 — attribute "The World Bank: World Development Indicators". |
| Workspace path | `data/population.csv` |

Fetch and verify:

```bash
mkdir -p data
curl -fsSL -o data/population.csv \
  https://raw.githubusercontent.com/datasets/population/425fc447a53a26c767a15a7de60c4cc2478a0595/data/population.csv
echo "7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a  data/population.csv" | sha256sum -c -
test "$(wc -c < data/population.csv)" -eq 552112
test "$(wc -l < data/population.csv)" -eq 17196
head -1 data/population.csv   # Country Name,Country Code,Year,Value
```

Most experiments download and verify this file themselves (`scripts/validate_provenance.py`, see
`specs/validate_provenance.md`), so pre-fetching is optional; a few standalone scripts download it into
memory or into their own output directory (see `specs/README.md` §5).

## 2. `wb-country-metadata` — World Bank API v2 country metadata (NOT immutable)

| Field | Value |
|---|---|
| URL | `https://api.worldbank.org/v2/country?format=json&per_page=400` |
| Recorded SHA-256 (July 2026 response) | `d29d57f8adf954c5e2a1520a02fb2c7b45575d8db3bd327a9dff47d66914231c` |
| Recorded shape | JSON array `[page_info, rows]`, `page_info.total == 295`, 295 rows |
| License | World Bank data, CC BY 4.0 |
| Workspace path | `data/world_bank_country_metadata.json` (written by `scripts/validate_metadata_filter.py`) |

This endpoint is a live API, not a pinned file. **The recorded hash does not reproduce today** (a
November 2026 fetch returned 296 rows and a different hash). Only one experiment
(`pinned-world-bank-metadata-filter`) uses it, to derive the list of 47 World Bank aggregate codes.
What to do:

1. Run the experiment with `--on-metadata-drift embedded` (its `run.command` does). The script then
   records the drift and uses the 47 aggregate codes embedded in `specs/validate_metadata_filter.md`
   (taken from the July 2026 snapshot).
2. Verify the derived list: `results/metadata_aggregate_codes.json` must have SHA-256
   `18eb78dd7f7093e3dd9e26ae569875ef138f5cb3b2c2d7b1a402016aea1616c8` (canonical serialization defined in
   the spec). All downstream numbers depend only on this list and on the pinned population CSV.
3. If you obtain a byte-identical copy of the July 2026 response (hash above), place it at
   `data/world_bank_country_metadata.json` and pass `--metadata-path data/world_bank_country_metadata.json
   --on-metadata-drift fail` to reproduce the original fail-closed behaviour.
