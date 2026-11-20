# Spec: `scripts/metadata_filter_oneliner.py` — inline cross-check of the metadata filter

> **Audience**: implementers. **Source of truth for**: the compact program that the original
> `pinned-world-bank-metadata-filter` run executed inline (it was shipped base64-encoded inside the
> run command). It independently re-derives the metadata filter numbers with a **different digit
> extraction** (DIGITS-STR) and **SEQ-MEAN**. Standard library only.

No required CLI flags; accepts `--on-metadata-drift {fail,embedded}` (default `fail`) and
`--out PATH` (default `results/metadata_filter_oneliner.json`) — both additions; the original only
printed to stdout.

## Algorithm

1. Download population (`PINNED_URL`) and metadata (`METADATA_URL`); `assert` both sha256 equal the
   pinned values (`validate_metadata_filter.md` constants). `rows = list(csv.DictReader(io.StringIO(
   p.decode())))`; `meta = json.loads(m.decode())[1]`; `assert len(rows) == 17195 and len(meta) == 295`.
   Under `--on-metadata-drift embedded`, a metadata hash/length mismatch instead switches to the
   `EMBEDDED_AGGREGATES` list (codes + names) of `validate_metadata_filter.md`.
2. `popcodes = {r["Country Code"]}`; `agg = sorted({r["id"] for r in meta if r.get("region",{}).get("value") == "Aggregates"} & popcodes)`;
   `country = [r for r in rows if r["Country Code"] not in set(agg)]`.
3. `score(rs, kind)`: for each row `s = str(abs(int(r["Value"])))`; kind 1 → `int(s[0])`; kind 2 →
   `int(s[1])` if `len(s) > 1` else `0`. `probs` = BENFORD1 (kind 1) or BENFORD2 (kind 2, SEQ-SUM over k).
   `n = len(vals)`, `c = Counter(vals)`;
   `mad = SEQ-SUM_{d in probs order} |c[d]/n − p_d| / len(probs)`;
   `chi_square = SEQ-SUM (c[d] − n p_d)² / (n p_d)`. Returns `{n, mad, chi_square}`.
4. `aggregate_records` = for metadata aggregate rows present in popcodes, sorted by id:
   `{"code", "metadata_rule": "region.value == Aggregates", "name"}`;
   `aggregate_list_sha256 = sha256((json.dumps(records, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode())`.
5. Output object (printed as one line with `json.dumps(obj, sort_keys=True)`, and written to `--out`
   as JSON-STD): `{status: "ok", population_rows, metadata_rows, aggregate_codes_present: len(agg),
   aggregate_list_sha256, missing_prior_static: sorted(PRIOR_STATIC − set(agg)), country_rows,
   country_first: score(country, 1), country_second: score(country, 2)}`.

## Oracle

`aggregate_codes_present` 47, `aggregate_list_sha256` = `18eb78dd…16c8`, `missing_prior_static`
`["FCS"]`, `country_rows` 14140, `country_first.n` 14140; `country_first.mad` / `chi_square` and
`country_second.*` within rel 1e-12 of `validate_metadata_filter.md`'s country-panel values
(`0.007540426519039584`, `98.71453554721771`; `0.004864316834289349`, `50.29048197306566`).
No shipped reference file (the original printed only to stdout).
