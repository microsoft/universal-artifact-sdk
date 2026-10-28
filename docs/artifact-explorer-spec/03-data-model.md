> **Audience**: Builders of research-artifact viewers.
> **Source of truth for**: The `artifact-explorer/data/v1` document — the contract between the
> explorer's builder and its viewer.

# 3. Data model: `artifact-explorer/data/v1`

## 3.1 General rules

- `data.json` is one UTF-8 JSON object at the site root. Every top-level key in §3.2 is always
  present; absence is `null` or `[]`, never omission.
- Collections keep **declaration order** (the order of the list in the source file). Viewers MAY
  reorder for display (§5.4) but the document does not.
- Values copied from the artifact keep their type. A field the source does not provide is `null`.
  Unknown fields of artifact records are carried in an `extra` object on the record (keys sorted),
  so nothing the authors wrote is silently dropped.
- **Declared strings and asset references** (one convention everywhere): a path or location the
  artifact declares is copied as the string it is, under the SDK key that declared it; the
  explorer's resolved copy of that file is a separate key named `<key>_asset` (for example a
  result's `evidence` and `evidence_asset`). So the declared value is never lost when it cannot be
  resolved.
- An **asset reference** is either `null` (not declared, or unresolved — §2.5) or
  `{"path": <artifact-relative path>, "url": "assets/<path>", "kind": <asset kind>}`. Each referenced
  file is copied to that `url` (§5.2). Asset kinds are assigned by lower-cased extension
  (*reference value (non-normative)*):

  | Kind | Extensions |
  |------|------------|
  | `image` | `.png .jpg .jpeg .gif .svg .webp .bmp` |
  | `pdf` | `.pdf` |
  | `markdown` | `.md .markdown` |
  | `text` | `.txt .log .csv .tsv .json .jsonl .yml .yaml .tex .py .r .jl .sh .toml .ini .cfg` |
  | `other` | anything else (offered as a download, never rendered inline) |

  A `markdown` asset reference also carries `embedded`: an object mapping each image or link
  target written in that Markdown file, verbatim, to the asset reference of the file it resolves to
  relative to the Markdown file's directory (§2.5), or `null` when it does not resolve or is not a
  relative path. The viewer serves embedded images only through this map (§5.7, §6.2); a target
  that maps to `null` is shown as text.
- **YAML to JSON.** Values read from YAML are projected into JSON as: dates and timestamps → ISO 8601
  strings (`2026-10-27`, `2026-10-27T21:40:00Z`); `.nan`, `.inf`, `-.inf` → the strings `"nan"`,
  `"inf"`, `"-inf"`; non-string mapping keys → their string form. Every other YAML scalar maps to
  the JSON scalar of the same type.

- Cross-references between records are **by ID** (`claim_ids`, `result_ids`, …), never by
  embedding. A cross-reference to an ID that does not exist is kept and flagged in `warnings`;
  the viewer renders it as an unresolved reference.

## 3.2 Top-level skeleton

```json
{
  "schema": "artifact-explorer/data/v1",
  "_generated": "<explorer name and version>: generated site data, do not edit",
  "generated_at": "2026-10-27T21:40:00Z",
  "identity": { "…": "§3.3" },
  "counts": { "claims": 18, "contributions": 6, "results": 80, "experiments": 0, "exhibits": 0,
              "datasets": 0, "traces": 0, "assessments": 0, "references": 0,
              "journal": 0, "figures": 0 },
  "evidence_inventory": { "…": "copied verbatim from the manifest (SDK §5.1), or null" },
  "environment": { "…": "copied verbatim (SDK §2.5), or null" },
  "research_agent": { "…": "§3.13, or null" },
  "claims": [ "§3.4" ],
  "contributions": [ "§3.5" ],
  "contribution_diagnostics": [ "§3.5" ],
  "results": [ "§3.6" ],
  "experiments": [ "§3.7" ],
  "exhibits": [ "§3.8" ],
  "datasets": [ "§3.9" ],
  "traces": [ "§3.9" ],
  "assessments": [ "§3.9" ],
  "references": [ "§3.12" ],
  "journal": [ "§3.9" ],
  "paper": { "…": "§3.10, or null" },
  "figures": [ "§3.11" ],
  "readme": "asset reference or null (§3.13)",
  "reflection": "asset reference or null (§3.13)",
  "evaluation": { "…": "§4, or null in mode A" },
  "warnings": [ "build warnings, human-readable, in the order encountered" ]
}
```

`counts` holds the length of each listed collection. `generated_at` is the only value allowed to
differ between two builds of the same inputs (I5). An explorer SHOULD let the caller fix it (for
example from a `SOURCE_DATE_EPOCH`-style environment value) so that builds can be byte-identical.

## 3.3 `identity`

| Key | Source |
|-----|--------|
| `id`, `title`, `format_version`, `sdk_version` | manifest root (SDK §2.1); `title` trimmed, empty → `null` |
| `display_title` | the first available of: the title derived from the paper source (§3.10), the PDF's document-metadata title, `title`, `id`; else `null` |
| `display_title_source` | which of those supplied `display_title`: `paper-source`, `pdf-metadata`, `manifest-title`, `manifest-id`, or `null` |
| `origin` | manifest `origin`, verbatim, or `null` (JR §2.3.1) |
| `producer` | manifest `producer`, verbatim, or `null` |
| `extra` | every other manifest root key not read elsewhere in this chapter, verbatim (keys sorted) |

`display_title` exists because paper-origin artifacts may carry a placeholder `title` (lfmu's
manifest title is `paper`); the site header uses `display_title`, and the Provenance section
shows both. A PDF metadata title is often wrong (a template name, a file name); it is used only
when the paper source yields no title, and the site labels it (§5.4.5). A metadata title that is
empty after trimming is not used.

## 3.4 `claims`

One entry per claim in the claims index (SDK §2.4), in declaration order:

| Key | Derivation |
|-----|------------|
| `id`, `statement`, `paper_ref`, `tested_by` | copied; `tested_by` `[]` when absent |
| `stance` | SDK §2.4.1 value, or `null` when undeclared (the site shows "not declared", not a default). A value outside SDK §2.4.1 is copied verbatim, flagged in `warnings`, and grouped with undeclared stances for display |
| `validators` | each validator from `validators`, or the singular `validator` (SDK §3), as `{id, kind, name, mode, gated_by, extra}`: the five named keys copied (`null` when absent), every other key of the validator (for example `checks`, `inputs`, `expected`) in `extra` |
| `result_ids` | IDs of results whose `validates` lists this claim (SDK §2.3), in results order |
| `experiment_refs` | `tested_by`, then each listed result's `produced_by` not already present |
| `exhibit_ids` | IDs of exhibits whose `validates` lists this claim (SDK §2.3.1) |
| `figure_ids` | IDs of figures linked to this claim (§3.11) |
| `paper_location` | `{page, section, quote}` from `paper_ref` (an open record, SDK §2.4; JR §3 writes `page`, `section`, `quote`), else `null`. `page` is kept only when it is an integer ≥ 1; a missing, zero, negative, or non-integer page becomes `null`, meaning **page unknown** (the original value stays in `paper_ref`) |
| `contribution_ids` | IDs of contributions whose `supporting_claims` lists this claim — **declared** links |
| `inferred_contribution_links` | `[{contribution_id, sources: [<source kind>…]}]` — **inferred** links, §3.5.1 |
| `judge_finding_ids`, `review_finding_ids` | filled by the run overlay (§4.4); `[]` without a run |

The explorer MUST NOT add a verdict, status, or score to a claim record; per-claim analysis is
reached only through the finding IDs (I2).

## 3.5 `contributions` and `contribution_diagnostics`

Contributions are read per JR §2.3.1 (v3 only, through `paths.contributions` only). Each entry
copies the record (SDK §2.4.2) — `id`, `statement`, `type`, `paper_ref`, `supporting_claims`,
`inferred_supporting_claims` (`[]` when absent), `significance`, `originality`, and `provenance`
— with every other key in `extra`, and adds:

| Key | Derivation |
|-----|------------|
| `index` | 1-based position in the declaration list (used by diagnostics and the site) |
| `declared_claim_ids` | `supporting_claims` |
| `inferred_claims` | `[{claim_id, sources}]` per §3.5.1, excluding claims already declared |
| `link_basis` | `declared` (only declared links), `inferred` (only inferred), `mixed` (both), `none` (neither) — the vocabulary of JR §6.8 |

`contribution_diagnostics` is, when the overlay has a judge result (§4.2), that result's
`contribution_diagnostics` verbatim (JR §4.5.7); otherwise the explorer's own load-time
diagnostics of the JR §2.3.1 contributions table, in the same `{path, message, severity}` shape.
The explorer does not compute the judge's other contribution diagnostics itself (I2). They are structural notes about the
declaration file, never findings about the work (JR §6.8).

### 3.5.1 Sources of inferred links

An inferred link between claim *c* and contribution *k* exists when *c* is in *k*'s
`inferred_supporting_claims` and not in its `supporting_claims` (JR §3.7). Its **sources** are
the `kind` of every record in *k*'s `provenance.claim_link_sources` whose `claims` list contains
*c*, in record order, with repeated kinds kept once (first occurrence wins). A legacy `provenance.claim_links` object on the same contribution (no `claim_link_sources`) is
read as one record, with that object's `kind`, covering **every** claim in
`inferred_supporting_claims`, as JR §5.13.2 requires of readers. These per-contribution records are the **only** source of link attribution. When no record lists
*c*, the source list is `["unrecorded"]`. Source kinds are kept as strings; unknown kinds are
preserved and labeled per §5.6.

Claim-side link fields that some producers add (for example a per-claim `contributions` list,
a `contribution_rank`, or a links-provenance object in the claims index) are not part of the SDK
or JR contracts. Claim fields are carried in the claim's `extra`; claims-index keys other than `claims` are
ignored. Neither may create, remove, or re-attribute a link: the contribution record is the
single source of truth for which claims it is linked to and who linked them.

## 3.6 `results`

One entry per result (SDK §2.3): `id`, `produced_by`, `validates`, `kind`, `validation_mode`,
`locators`, `support`, `extra` copied; `evidence` is the declared string and `evidence_asset`
its asset reference (§3.1). For paper-origin results, the paper-adapter fields
(`quote`, `page`, `value`, …) are carried in `extra`. `judge_finding_ids` and
`review_finding_ids` are filled by the run overlay (§4.4), `[]` without a run.

## 3.7 `experiments`

One entry per manifest experiment (SDK §2.2): `slug`, `directory`, `run` (copied), `command`
(`run.command` or `null`), `depends_on`, `runs_in`, `expected_runtime`, and `disposition`
(`{status, rationale, superseded_by, failure}`; `status` is `active` when the experiment has no
disposition, SDK §2.2.2). Derived: `result_ids` (results whose `produced_by` is the slug),
`claim_ids` (claims listing the slug in `tested_by` or validated by one of those results), and
`trace_ids` (traces whose `covers` lists the slug).

## 3.8 `exhibits`

One entry per exhibit (SDK §2.3.1): `id`, `type`, `caption`, `validates`, `from_result`,
`alt_text`, `path` copied; `path_asset` is the asset reference of `path`. An exhibit of an image type without
`alt_text` is rendered with its caption, else its ID, as alternative text.

## 3.9 `datasets`, `traces`, `assessments`, `journal`

- **datasets** (SDK §2.7): `id`, `name`, `description`, `license`, `study` copied;
  `location` and `sample` copied (`location` as `{kind, path, uri, sha256, access}`);
  `location_asset` is the asset reference of `location.path` when `location.kind` is
  `in_artifact`, else `null`; `sample_asset` is the asset reference of `sample.path`. External `uri` values are shown as text, never fetched or hyperlinked to load
  automatically (§6.3).
- **traces** (SDK §2.2.1): `id`, `kind`, `covers`, `terminal_state`, `counters`, `path` copied;
  `path_asset` for `path`.
- **assessments** (SDK §2.1.1): copied records; each declared evidence path keeps its key and gains
  a `<key>_asset` sibling.
- **journal** (SDK §2.8): copied entries in file order.

## 3.10 `paper`

```json
{ "pdf": "<asset reference or null>", "source": "<asset reference or null>",
  "declared": { "pdf": "paper.pdf", "source": null },
  "title": null, "metadata_title": null, "authors": [], "abstract": null }
```

`pdf` and `source` follow SDK §2.6 and the probes of §2.6 (declared, else probed). A declared
`source` that is a directory (a multi-file paper source) is resolved by applying the paper-source
probe list of §2.6 inside that directory, first match wins; with no match `source` is `null` and a
warning is recorded. `declared` records what
the manifest declared, so a declared-but-unresolved paper stays visible (§2.6). `title`,
`authors`, and `abstract` MAY be derived from the paper source (for example LaTeX `\title`,
`\author`, `abstract` environment) by a deterministic extractor; *the extraction method is a
reference value (non-normative)*, and a field the explorer cannot derive is `null`/`[]`.
`metadata_title` is the PDF document-information dictionary's `/Title`, trimmed; when that is absent or empty an
explorer MAY use the XMP `dc:title` instead; otherwise `null`. It is kept
separate from `title` so that its origin is never lost (§3.3). In mode B paper-only scope the
paper is the run's snapshot paper (§4.6): `declared` records the run-relative path the run
manifest gives for it, in the `pdf` slot when its extension is `.pdf` and in the `source` slot
otherwise; the matching asset key refers to the copied snapshot and the other slot is `null`.

## 3.11 `figures`

Figures come from exactly one source, chosen by what the manifest **declares**:

1. `paths.figures` declared (JR §3.6.1): the figures index is authoritative, one entry per
   record. If the declared file is missing or unreadable, `figures` is `[]` and a warning is
   recorded; the explorer does not fall back to exhibits or probing.
2. otherwise, an exhibits index declared: one entry per exhibit of type `figure` (an empty list
   when there are none).
3. OPTIONALLY, only when neither index is declared, image files under the probe directories of
   §2.6, sorted by path. An explorer that does not scan simply has no figures in this case.

Each entry: `{id, number, caption, page, path, path_asset, claim_links: [{claim_id, method}]}`;
`path` is the declared or probed path string and `path_asset` its asset reference; `page`
follows the page-unknown rule of §3.4. `method`
records how the link was made and is shown with it: `declared` (exhibit `validates` or a result's
evidence), `adapter-suggested` (a figures-index `claims` entry, which JR §3.6.1 calls advisory),
or `filename-heuristic` (a probe-directory image whose name matches a claim or experiment;
*the matching rule is a reference value (non-normative)*). Heuristic and suggested links MUST be
labeled as such in the site; they are never shown as the authors' links.

## 3.12 `references`

- **references**: the references export (JR §2.3.1), every record kept in file order (no
  de-duplication): `id`, `raw`, `doi`, `arxiv`, `isbn`, `url`, `cited_for` copied, plus `check`: with a judge overlay (§4.2), the matching JR §6.6.2 verdict (by `id`)
  `{status, matched_title, matched_id, reason}`, else `null`. No reference lookup happens at build time (§6.3).

## 3.13 `readme`, `reflection`, `research_agent`

`readme` and `reflection` are asset references (§2.6). `research_agent` is the manifest's
`research_agent` object copied, with `path_asset` added for its `path`; the explorer never runs or
contacts the agent.
