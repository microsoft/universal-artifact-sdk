> **Audience**: Builders of research-artifact viewers.
> **Source of truth for**: The `artifact-explorer/data/v1` document — the contract between the
> explorer's builder and its viewer.

# 3. Data model: `artifact-explorer/data/v1`

## 3.1 General rules

- **"Declared" means recorded in the artifact, not "written by the authors".** Throughout this
  specification a *declared* value (a declared path, a declared link, `link_basis: declared`,
  the figure link method `declared`) is one the artifact's own files contain, whoever produced
  them: the authors, a paper adapter, or another producer. Who produced a contribution is
  recorded only by its `provenance.kind` (`author-declaration`, `paper-extraction`, …, SDK
  §2.4.2) and the artifact's `origin`, and the site shows that separately (§5.5, §5.6). The
  explorer never describes a declared value as author-written unless `provenance.kind` is
  `author-declaration`.

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
  resolved. When the declared value is a list of path strings, `<key>_asset` is a list of the same
  length whose *i*-th element is the asset reference (or `null`) of the *i*-th path; a list element
  that is not a string gives `null`.
- An **asset reference** is either `null` (not declared, or unresolved — §2.5) or
  `{"path": <artifact-relative path>, "url": "assets/<encoded path>", "kind": <asset kind>}`. Each
  referenced file is copied to `assets/<path>` (§5.2). `path` is the plain relative path (for run
  files, the run-relative path, with `url` under `run/`). In `url`, each `/`-separated segment of
  the path is percent-encoded: every byte of its UTF-8 encoding other than the RFC 3986 unreserved
  characters `A–Z a–z 0–9 - . _ ~` is written as `%XX` with upper-case hex digits (so a space is
  `%20`, `#` is `%23`, `?` is `%3F`); the `/` separators are kept. Asset kinds are assigned by lower-cased extension
  (*reference value (non-normative)*):

  | Kind | Extensions |
  |------|------------|
  | `image` | `.png .jpg .jpeg .gif .svg .webp .bmp` |
  | `pdf` | `.pdf` |
  | `markdown` | `.md .markdown` |
  | `text` | `.txt .log .csv .tsv .json .jsonl .yml .yaml .tex .py .r .jl .sh .toml .ini .cfg` |
  | `other` | anything else (offered as a download, never rendered inline) |

  A `markdown` asset reference also carries `embedded`: an object whose keys are the link
  destinations of the file and whose values are the asset reference of the file each resolves to
  (§2.5, Markdown targets), or `null` when it is external, does not resolve, or is rejected.
  Markdown is parsed as **CommonMark** (version 0.31.2) with raw HTML disabled: raw HTML is
  rendered as literal text and contributes no targets. The link destinations are those of every
  inline link, inline image, and link reference definition in the CommonMark parse, as the
  parser yields them (after backslash-escape and entity processing, before percent-decoding);
  autolinks and text inside code spans or code blocks contribute none. The builder and the viewer
  MUST use the same parse, so every destination the viewer meets is a key of `embedded`. The
  viewer serves embedded images and links only through this map (§5.7, §6.2).
- **YAML to JSON.** Values read from YAML are projected into JSON as: dates → `YYYY-MM-DD`;
  timestamps → the **timestamp form** below; `.nan`, `.inf`, `-.inf` → the strings `"nan"`,
  `"inf"`, `"-inf"`. Non-string mapping keys become strings: `true`/`false`, `null`, integers in
  plain decimal, floats in the shortest decimal form that reads back as the same value with `.0`
  appended when it has no fractional part (`1.0` → `"1.0"`, `2.5e-07` → `"2.5e-07"`), and dates
  and timestamps as above. Every other YAML scalar maps to the JSON scalar of the same type.
- **Timestamp form.** Every timestamp the explorer writes or converts (`generated_at`, YAML
  timestamps) is RFC 3339 in UTC with a `Z` suffix: `YYYY-MM-DDTHH:MM:SSZ`, with a fractional
  part only when it is non-zero, written with its trailing zeros removed
  (`2026-10-27T21:40:00.5Z`). A YAML timestamp without a time zone is taken as UTC (as YAML
  specifies). Timestamps copied from run JSON files are strings and are kept verbatim.

- Cross-references between records are **by ID** (`claim_ids`, `result_ids`, …), never by
  embedding. A cross-reference to an ID that does not exist is kept and flagged in `warnings`;
  the viewer renders it as an unresolved reference.
- **Warnings** are human-readable and their wording is not normative. A builder MAY aggregate
  warnings that share a cause into one (for example "38 results declare evidence `paper.pdf`,
  which is not in the artifact: R1, R2, …"), provided it names every affected file or ID.

## 3.2 Top-level skeleton

```json
{
  "schema": "artifact-explorer/data/v1",
  "_generated": "<explorer name and version>: generated site data, do not edit",
  "generated_at": "2026-10-27T21:40:00Z",
  "identity": { "…": "§3.3" },
  "counts": { "claims": 18, "contributions": 6, "results": 80, "experiments": 0, "exhibits": 0,
              "datasets": 0, "traces": 0, "assessments": 0, "references": 0,
              "journal": 0, "figures": 0, "related_work": 0 },
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
  "related_work": [ "§3.14" ],
  "reference_check": "§4.9, or null",
  "readme": "asset reference or null (§3.13)",
  "reflection": "asset reference or null (§3.13)",
  "evaluation": { "…": "§4, or null in mode A" },
  "warnings": [ "build warnings, human-readable, in the order encountered" ]
}
```

`counts` holds the length of each listed collection as built. `evidence_inventory` is the
manifest's own declaration and may disagree with `counts` (for example when the producer counted
records the explorer could not read); the site labels the inventory "as declared in the
manifest" and never reconciles the two. `generated_at` is the only value allowed to
differ between two builds of the same inputs (I5). An explorer SHOULD let the caller fix it (for
example from a `SOURCE_DATE_EPOCH`-style environment value) so that builds can be byte-identical.

**Keys added within v1.** `related_work`, `counts.related_work`, `reference_check` (§4.9),
`evaluation.paper_pages` (§4.6.2), `evaluation.approval` (§4.8), and `evaluation.review.visual`
(§4.3) were added as optional keys within v1 (§1.5). A builder that implements them writes them
as every other key (always present, `null` or `[]` when empty); a viewer MUST treat a missing one
as `null` or `[]`, so documents from earlier v1 builders still render.

## 3.3 `identity`

| Key | Source |
|-----|--------|
| `id`, `title`, `format_version`, `sdk_version` | manifest root (SDK §2.1); `title` trimmed, empty → `null` |
| `display_title` | the first available of: the title derived from the paper source (§3.10), the PDF's document-metadata title, `title`, `id`; else `null` |
| `display_title_source` | which of those supplied `display_title`: `paper-source`, `pdf-metadata`, `manifest-title`, `manifest-id`, or `null` |
| `origin` | manifest `origin`, verbatim, or `null` (JR §2.3.1) |
| `producer` | manifest `producer`, verbatim, or `null` |
| `extra` | every other manifest root key not read elsewhere in this chapter and other than `_generated` (which describes the manifest file itself), verbatim, keys sorted; for example a producer's `warnings` or `identity` object |

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
| `validators` | each validator from `validators`, or the singular `validator` (SDK §3), as `{id, kind, name, gated_by, validation_mode, extra}`: the five named keys copied under the SDK's own names (`null` when absent), every other key of the validator (for example `checks`, `inputs`, `criteria`) in `extra` |
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
| `index` | 1-based position among the **kept** records (list elements that are not mappings are skipped, §2.3), used for the site's numbering. Diagnostic `path` values use the raw 0-based position in the file's list (JR §2.3.1), so they can differ from `index − 1` when an earlier element was skipped |
| `declared_claim_ids` | `supporting_claims` |
| `inferred_claims` | `[{claim_id, sources}]` per §3.5.1, excluding claims already declared |
| `link_basis` | `declared` (only declared links), `inferred` (only inferred), `mixed` (both), `none` (neither) — the vocabulary of JR §6.8 |
| `review_finding_ids` | filled by the run overlay: review findings with a resolved `contribution` join to this ID (§4.4), in source order; `[]` without a run |

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
read as one record of kind `reviewer-inference` (whatever `kind` the object itself carries) covering
**every** claim in `inferred_supporting_claims`, exactly as JR §5.13.2 tells readers to. These per-contribution records are the **only** source of link attribution. When no record lists
*c*, the source list is `["unrecorded"]`. Source kinds are kept as strings; unknown kinds are
preserved and labeled per §5.6.

Claim-side link fields that some producers add (for example a per-claim `contributions` list,
a `contribution_rank`, or a links-provenance object in the claims index) are not part of the SDK
or JR contracts. Claim fields are carried in the claim's `extra`; claims-index keys other than `claims` are
ignored. Neither may create, remove, or re-attribute a link: the contribution record is the
single source of truth for which claims it is linked to and who linked them.

A viewer MAY show the values of a claim's `extra` (for example a producer's `role`,
`contribution_rank`, or per-claim `contributions` list) as **producer metadata**: each value
labeled with its key, under a heading that names it as recorded by the producer, never as a link
or as the authors' statement. Such values MUST NOT reorder claims away from declaration order,
and never create, remove, or re-attribute a link; a contribution named in a claim's `extra`
is shown as text, not as a contribution link.

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
  `in_artifact`, else `null`; `sample_asset` is the asset reference of `sample.path`. An external `uri` is
  rendered as an external link (§6.3) and never fetched.
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
2. otherwise, when an exhibits index is **in use** — declared by `paths.exhibits`, or present at
   its default name `exhibits.yml` (§2.3) — one entry per exhibit of type `figure`. A declared
   exhibits index that is missing gives `[]` and the warning of §2.3, with no probing. An index
   that is in use but lists no exhibit of type `figure` falls through to item 3: exhibits
   indexes that record only tables and reports are common, and the artifact's plots would
   otherwise never be shown.
3. OPTIONALLY, only when `paths.figures` is not declared and item 2 produced no figure, the image
   files that §2.6 probes, at any depth, skipping hidden directories and `node_modules`,
   `__pycache__`, `assets`, and `_app`, and a top-level `evaluation/` (an evaluator's output
   written into the artifact), sorted by path (byte order of the UTF-8 path).
   Byte-identical copies (a report re-embedding an experiment's plot) appear once: under the copy
   inside a probe directory, else the shallowest path, else the first by path; the links of
   every copy are kept. An explorer that does not scan simply has no figures in this case. A
   probed figure's `id` is its artifact-relative path; `number`, `caption`, and `page` are
   `null`.

Each entry: `{id, number, caption, page, path, path_asset, claim_links: [{claim_id, method}]}`;
`path` is the declared or probed path string and `path_asset` its asset reference; `page`
follows the page-unknown rule of §3.4. `method`
records how the link was made and is shown with it: `declared` (exhibit `validates` or a result's
evidence), `adapter-suggested` (a figures-index `claims` entry, which JR §3.6.1 calls advisory),
`experiment-provenance` (a probed image, or one of its byte-identical copies, inside the declared
`directory` of an experiment in the claim's `tested_by`), or `filename-heuristic` (a probed image
whose name matches a claim or experiment; *the matching rule is a reference value
(non-normative)*). Heuristic and suggested links MUST be
labeled as such in the site; they are never shown as the authors' links. `claim_links` lists
`declared` links first (exhibit `validates` in order, then results in results order), then
`adapter-suggested`, then `experiment-provenance` (claims order), then `filename-heuristic`; a
`(claim_id, method)` pair appears once.

## 3.12 `references`

- **references**: the references export (JR §2.3.1), every record kept in file order (no
  de-duplication): `id`, `raw`, `doi`, `arxiv`, `isbn`, `url`, `cited_for` copied, every other key
  (for example `authors`, `title`, `year`) in `extra`, plus `check`: with a judge overlay (§4.2), the matching JR §6.6.2 verdict (by `id`)
  `{status, matched_title, matched_id, reason}`; else, with an accepted separate result (§4.9),
  the verdict at the same position, in the same shape; else `null`. No reference lookup happens at build time (§6.3).

## 3.13 `readme`, `reflection`, `research_agent`

`readme` and `reflection` are asset references (§2.6). `research_agent` is the manifest's
`research_agent` object copied, with `path_asset` added for its `path`; the explorer never runs or
contacts the agent.

## 3.14 `related_work`

Read only when the manifest declares `paths.paper_related_work` (the paper adapter's related-work
export, JR §3.6.3, top-level key `related_work`). The file is read like every other index (§2.3,
§2.5); a declared file that is missing or unreadable gives `[]` and a warning. Each element of
the list that is a mapping is copied verbatim, in file order (for example `id`, `statement`,
`refs`, `relation`, `distinction`, `comparative`, `superiority`, `primacy`); other elements are
skipped with a warning. Nothing is resolved or classified at build time: the citation markers in
`refs` stay strings, and `relation` and the three flags are the producer's labels.

The export's statements are the paper's own sentences; its `relation` labels and flags are
heuristic. The site shows them as such (§5.4.4) and never as an assessment of the related work.
No other related-work file name or manifest key is read.
