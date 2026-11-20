# Spec: `scripts/render_provenance_appendix.py` — paper-ready provenance appendix table

> **Audience**: implementers. **Source of truth for**: experiment
> `add-paper-ready-provenance-appendix-table`. Standard library only. Reads
> `results/provenance.json` (`validate_provenance.md`) and `results/summary.json` (`analyze_benford.md`).

CLI: `python scripts/render_provenance_appendix.py [--provenance results/provenance.json]
[--summary results/summary.json] [--out-dir results]`.

`nested(d, *keys, default="")` walks dicts, returning `default` when a key is missing.
`fmt_bool`: `True→"yes"`, `False→"no"`, else `str`. `fmt_exclusions(summary)`:
`excluded = analysis.excluded_rows (default 0)`, reasons = `analysis.exclusions_by_reason`; empty →
`f"{excluded} (none)"`, else `f"{excluded} (r1: c1, r2: c2)"` sorted by reason.
`software_line(prov)`: for keys `python, numpy, pandas, matplotlib, requests, platform` in that order,
include `"key: value"` if truthy, joined by `"; "`; none → `"not recorded"`.

## Rows (field, value) — 15 rows in this order

| Field | Value |
|---|---|
| `Dataset` | `prov.attribution.dataset` (default `World Bank total population by country/year`) |
| `Source URL` | `prov.source_url` (default `summary.dataset.source_url`) |
| `Attribution/license note` | `prov.attribution.license_note` (default `not recorded`) |
| `Retrieval timestamp (UTC)` | `prov.retrieval_timestamp_utc` (default `not recorded`) |
| `SHA-256` | `prov.sha256` (default summary.dataset.sha256) |
| `Expected SHA-256` | `prov.expected_sha256` (default summary) |
| `Checksum verified` | fmt_bool(`prov.checksum_match`) |
| `Schema verified` | fmt_bool(`prov.schema_match`) |
| `Data rows` | `f"{row_count} observed / {expected_row_count} expected"` |
| `Analyzed rows` | `str(summary.analysis.analyzed_rows)` |
| `Excluded rows` | fmt_exclusions(summary) |
| `First-digit MAD/classification` | `f"{first_digit.mad:.12f} ({first_digit.nigrini_classification})"` |
| `Second-digit MAD` | `f"{second_digit.mad:.12f}"` |
| `Negative-control MAD/classification` | `f"{negative_control.first_digit_mad:.12f} ({negative_control.nigrini_classification})"` |
| `Software versions` | software_line(prov) |

## Outputs

`results/provenance_appendix.md` (LF, ends with a single `\n`):

```
# Provenance appendix

This table is generated deterministically from `results/provenance.json` and `results/summary.json`.

| Field | Value |
| --- | --- |
| <field> | <value> |      ← one line per row, newlines in values replaced by spaces
```

`results/provenance_appendix.tex` (LF, ends with `\n`): lines
`\begin{table*}[t]`, `\centering`,
`\caption{Dataset provenance and reproducibility metadata. Generated from recorded JSON artifacts.}`,
`\label{tab:provenance-appendix}`, `\begin{tabular}{p{0.25\linewidth}p{0.70\linewidth}}`, `\toprule`,
`Field & Value \\`, `\midrule`, then per row `"{tex(field)} & {tex(value)} \\"`, then `\bottomrule`,
`\end{tabular}`, `\end{table*}`. `tex()` replaces newlines by spaces and escapes per character:
`\`→`\textbackslash{}`, `&`→`\&`, `%`→`\%`, `$`→`\$`, `#`→`\#`, `_`→`\_`, `{`→`\{`, `}`→`\}`,
`~`→`\textasciitilde{}`, `^`→`\textasciicircum{}`.

Print `{"latex": path, "markdown": path, "rows": 15}` (indent 2, sorted). Exit 0.

## Oracle

| file | compared | tolerance |
|---|---|---|
| `results/provenance_appendix.md` | rows `Dataset` … `Negative-control MAD/classification` except `Retrieval timestamp (UTC)`; row count 15 | exact text |
| `results/provenance_appendix.tex` | same rows (escaped) | exact text |

Expected: `0.007314647984 (acceptable conformity)`, `0.004058150935`, `0.060255520673 (nonconformity)`,
`17195 observed / 17195 expected`, `0 (none)`.
