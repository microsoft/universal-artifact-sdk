> **Audience**: Builders of research-artifact evaluation tools.
> **Source of truth for**: Accepted inputs, the format gate, path safety, snapshotting, the
> artifact facts the judge and reviewer read, and how quotes are located in extracted text.

# 2. Inputs

## 2.1 Accepted input forms

| Form | Description | Allowed scopes |
|------|-------------|----------------|
| **Artifact directory** | A directory conforming to `evaluable-artifact/v3` (or the older `evaluable-artifact/v2`) as defined by the Universal Artifact SDK specification ([`SPEC.md`](../../SPEC.md): object model §2, serialization §5, versioning §6). | `paper-only`, `artifact-informed` |
| **Paper file** | A compiled paper (PDF) or authored source (e.g. Markdown, LaTeX single file). | `paper-only` |
| **Paper-origin artifact** | An artifact produced from a paper by the paper adapter (§3). It is an ordinary `evaluable-artifact/v3` directory whose results are capped at `attested`. | `paper-only`, `artifact-informed` |

Optional companion inputs:

- a **bibliography** file (e.g. BibTeX) supplied explicitly by the caller; and
- a **paper override**: a relative path selecting a different paper file inside the artifact
  than the one the manifest declares.

A paper-file input requires the caller to name a **workspace** directory where the run will be
written (§6.1). An artifact-directory input MAY default to writing runs outside the artifact;
it MUST NOT write inside the artifact (I1). An output location inside the artifact, or an
artifact inside the output location, is an input error (exit status 2).

## 2.2 Format gate

1. The tool MUST read `manifest.yml` at the artifact root and MUST reject the input unless
   `format_version` is a version it supports. A conforming tool MUST support
   `evaluable-artifact/v3` (the current contract) and MUST also read `evaluable-artifact/v2`.
   It MAY additionally read older versions under its own legacy policy. Rejection is an input
   error (exit status 2, §6.8), not a finding.
   - **v3** may declare contributions (SDK §2.4.2, §5.2); they are read as described in §2.3.1.
   - **v2** has no contributions. A v2 artifact is processed exactly as before: no contribution
     diagnostics are produced unless the manifest wrongly declares `paths.contributions`
     (§2.3.1), and the reviewer falls back to source-extracted candidates (§5.13).
2. The tool SHOULD record `sdk_version` for provenance but MUST NOT branch on it.
3. The root `producer` block and any other producer extension MUST be treated as opaque:
   displayable, never interpreted (I8).

## 2.3 Facts read from an artifact

The judge and reviewer read only the SDK contract. Index files (`claims.yml`, `results.yml`,
`exhibits.yml`, `datasets.yml`, `traces.yml`, `assessments.yml`, `journal.yml`) are optional;
**absence means "not declared"** and triggers `unassessable` coverage notes, never failures.

| SDK object (SDK §) | Fields used | Used by |
|--------------------|-------------|---------|
| Artifact root (SDK §2.1) | `format_version`, `sdk_version`, `id`, `title` | identity in all outputs |
| Evidence inventory (SDK §5.1) | every `has_*` flag (including `has_contributions`), counts, `evidence_kinds`, `validation_modes` | evidence-conditioned activation of every check (SDK §5.1) |
| Experiment (SDK §2.2, SDK §2.2.2) | `slug`, `directory`, `run.command` (and the rest of `run`), `depends_on`, `runs_in`, `disposition.{status,rationale,superseded_by,failure}` | structure, reproduction provider, process-transparency signals, reviewer run-evidence |
| Trace (SDK §2.2.1) | `id`, `kind`, `path`, `covers`, `terminal_state`, `counters`; body only via cite-addressable reads | execution authenticity, trace-report faithfulness, reviewer run-evidence. `human_interaction` traces MUST be excluded from run-oriented dimensions. |
| Result (SDK §2.3) | `id`, `produced_by`, `validates`, `evidence`, `kind`, `validation_mode`, `locators`, `support` | claim validators, reconciliation |
| Exhibit (SDK §2.3.1) | `id`, `type`, `caption`, `validates`, `path`, `from_result`, `alt_text` | reviewer artifact-visual inspection (figures/tables); evidence display |
| Claim (SDK §2.4, SDK §2.4.1) | `id`, `statement`, `paper_ref`, `validators` (or singular `validator`), `stance`, `tested_by` | claim validators, stance handling, reconciliation |
| Contribution (SDK §2.4.2; v3 only) | `id`, `statement`, `supporting_claims`, `type`, `paper_ref`, `significance.*`, `originality.comparisons[].{reference,distinction,locator,evidence}`, `originality.coverage.{sources,uninspected,cutoff,limitations}`, `provenance.{kind,source,method,locator}`; unknown fields preserved, never interpreted | contribution diagnostics (§4.5.7), reviewer contribution review (§5.13) |
| Environment (SDK §2.5) | `name`, `image.reference`, `image.digest` (shape and "pinned" rule: §2.3.1) | structure (declared, pinned), reproduction provider |
| Paper (SDK §2.6) | `pdf`, `source`, `claims_export`, `references_export` | paper selection, paper consistency, citation integrity, reviewer |
| Dataset (SDK §2.7) | `id`, `location.kind`, `location.{path,uri,sha256,access}`, `sample`, `study` | structure coverage, reproduction provider, advisory ethics notes |
| Journal (SDK §2.8) | presence, entry count, entries with non-empty `rationale` | provenance journal signal |
| Research agent (SDK §2.9) | `model`, `grounding_sources`, `scope` | agent faithfulness |
| Assessments (SDK §2.1.1) | producer-declared `dimension`, `id` | honored as annotations on the evaluator-instantiated dimensions |
| `reflection.md` | presence and content | limitation transparency |
| `SHA256SUMS` | lines of `<hex>  <path>` | integrity audit |
| License file at root (`LICENSE`, `LICENSE.*`, `COPYING`) | presence | `Available` badge (badge profile only, §4.8) |

### 2.3.1 On-disk shape

The SDK leaves some field names provisional (SDK §11 Q1). A conforming v1 tool reads this shape
and MUST also accept a shape produced by the SDK's reference writer that differs from it only in
optional fields.

- **`manifest.yml`** is a flat YAML mapping at the artifact root (no wrapper key) with:
  `format_version`, `sdk_version`, `id`, `title`, `producer` (opaque), `experiments` (list),
  `environment` (one object, SDK §2.5; absent if none; see *Environment* below), `paths` (map of index name → relative
  file), `paper` (object, SDK §2.6), `research_agent` (object `{path, model, grounding_sources,
  scope?}`, SDK §2.9), `evidence_inventory` (map, SDK §5.1), and optionally `origin` (object;
  for paper-origin artifacts `{kind, evidence_cap, extractor}`, §3.3; otherwise opaque and
  copied verbatim into `judge.json`, §6.6.1).
- **Index files.** Each index is located through `paths.<name>` if present, otherwise at its
  default name at the root. Each is a YAML mapping with **one top-level key equal to the index
  name**, holding a list:

  | Index (`paths` key) | Default file | Top-level key |
  |---------------------|--------------|---------------|
  | `claims` | `claims.yml` | `claims` |
  | `results` | `results.yml` | `results` |
  | `exhibits` | `exhibits.yml` | `exhibits` |
  | `datasets` | `datasets.yml` | `datasets` |
  | `traces` | `traces.yml` | `traces` |
  | `assessments` | `assessments.yml` | `assessments` |
  | `journal` | `journal.yml` | `journal` |

  A `_generated` key MAY also be present and is ignored. A file that does not parse, or whose
  top-level key is missing or not a list, is **declared-but-unresolved** for every check that
  needs it.
- **Contributions index (v3).** Located **only** through `paths.contributions`; there is no
  default file name and no fallback discovery (SDK §5.2). A `contributions.yml` that the manifest
  does not point at is ignored. The document is a mapping whose `contributions` key holds a
  list of records (SDK §2.4.2 defines the record shape; this specification relies only on the
  fields in §2.3). Reading rules, each producing a **contribution diagnostic** (§4.5.7) rather
  than a crash or an input error:

  | Situation | Diagnostic (`path`, `severity`) | Contributions read |
  |-----------|--------------------------------|--------------------|
  | `paths.contributions` absent (any version) | none | none ("not declared") |
  | `paths.contributions` declared but `format_version` is not v3 | `paths.contributions`, `error`: contributions require `evaluable-artifact/v3` | none |
  | Declared path fails §2.4, is missing, does not parse, or has no `contributions` list | `paths.contributions`, `error`: cannot load contribution declarations | none |
  | A list element is not a mapping | `contributions[<i>]`, `error`: expected a contribution object | the other elements |

  Contributions are **candidate** advances, not assessments. Their absence means "no
  declaration was provided", never "no contribution".
- **Environment.** `environment` is one mapping `{name, image: {reference, digest?}, …}`
  (SDK §2.5). The image is **declared** when `image.reference` is a non-empty string. It is
  **pinned** when `image.digest` matches `^sha256:[0-9a-f]{64}$` **or** `image.reference`
  embeds such a digest after `@` (`repo[:tag]@sha256:<64 hex>`). A bare tag
  (`repo:1.2`) is declared but not pinned. A missing or non-mapping `environment` is "not
  declared".
- **References export.** Located by `paper.references_export` (conventionally
  `paper_references.yml`). Top-level key `references` (**not** the file stem; this file is the one exception to the
  index-key rule above), a list of entries
  `{id, raw, doi?, arxiv?, isbn?, url?, cited_for?}` (SDK §2.6). This is the file meant
  wherever this specification says "references export".
- **Research agent.** The file at `research_agent.path` (conventionally `research-agent.md`).
  Its metadata is the manifest's `research_agent` object; the file's YAML front matter MAY repeat
  `model` and `grounding_sources`, in which case the manifest wins.
- **Other root files:** `reflection.md`, `SHA256SUMS`, and the license file are read at fixed
  names at the root.

### 2.3.2 Paper roles

A paper may be declared with `pdf`, `source`, or both. Distinguish two roles:

- **Paper of record**: the file snapshotted as the paper and shown to humans. This is the first of
  `pdf`, `source` that is declared **and** resolves (§2.6).
- **Text source**: the file text is extracted from. This is `source` if it is declared and
  resolves, otherwise the paper of record. Page numbers in locators come from the PDF when one
  resolves; otherwise locators use sections only.

## 2.4 Path safety

Every path read from an artifact (manifest pointers, `evidence`, `path`, `grounding_sources`,
paper override, `SHA256SUMS` entries, …) is untrusted. Before reading, the tool MUST reject a
path that:

- is absolute, uses a drive letter or backslash form, or contains `.` or `..` segments;
- resolves (after following the path) outside the artifact root; or
- is, or traverses, a symbolic link.

A rejected path is treated as **declared-but-unresolved** (→ `unverifiable` plus an integrity
note in the relevant check), never as a crash and never as a silent pass. (Symbolic links are
already excluded at snapshot time, §2.5.)

## 2.5 Snapshot

Before any analysis, the tool copies its inputs into the run directory:

```text
<run>/snapshot/
  paper/paper.<ext>        # the selected paper, renamed; extension preserved
  paper/references.<ext>   # the caller-supplied bibliography, if any
  artifact/...             # artifact-informed only: the complete artifact tree (regular files)
```

Rules:

1. Only regular files and directories are captured. A symbolic link, device, socket, or other
   special file anywhere in the artifact tree is an **input error** (the run fails before analysis).
   Exactly these directory names are excluded, at any depth, and are not walked (so special
   files inside them do not matter): `.git`, `.hg`, `.svn`, `__pycache__`. Nothing else is
   excluded.
2. Each source file is hashed **before** copying and each copy is hashed **after**; a mismatch
   aborts the run (`status: "failed"`).
3. The snapshot inventory is the map `relative path under the run → sha256` for every copied
   file. It becomes the manifest's `inputs` (§6.3).
4. Before sealing, the tool MUST re-verify that (a) every snapshot file still has its recorded
   hash and (b) the original sources are unchanged. If either check fails, the run fails. This
   catches concurrent modification of the input during analysis.
5. All analysis reads the snapshot, never the original location.

## 2.6 Paper selection

| Input | Selected paper |
|-------|----------------|
| Paper file | That file. A paper override is an input error. |
| Artifact directory | The paper of record (§2.3.2). If `source` is a directory, the implementation selects its main document and records which. A caller-supplied override replaces this. The override MUST be relative, MUST pass §2.4, and MUST resolve to a regular file. |
| Artifact whose paper is absent or does not resolve | `paper-only` scope is an input error. In `artifact-informed` scope the judge still runs, the manifest's `paper` is `null` (§6.3), and reviewer paper analysis is `unavailable` with a reason. |

## 2.7 Paper text extraction

The reviewer and the judge's paper-consistency check both need paper text.

- **PDF:** extract text per page. Record `text_source: "pdf-extraction"` and a standing warning
  that math symbols, formulas, sub/superscripts, and special glyphs may be dropped or garbled,
  so the extracted text is not reliable evidence of how something renders. The extracted text
  is built by the **page and paragraph rule** below.
- **Source:** read as UTF-8 text. Record `text_source: "authored-source"`. Blank lines are the
  ones written in the file.
- Section boundaries SHOULD be detected (headings) so evidence can be cited by section. When
  they are, the rule below is used; every stage that labels text by section (§3.4, §3.5,
  §3.6.4, §4.5.3) uses this one rule.
- Extraction failure is not fatal: the dependent stages report `unavailable` with the reason.

**Page and paragraph rule (PDF).** Several rules depend on line structure and blank lines
(reference entries and page furniture in §3.4, contribution lists and sentences in §3.6.4,
headings below), so the extracted text of a PDF is assembled deterministically from the text
lines the reader reports with their positions:

1. **Lines.** On each page, take the reader's text lines in its reading order. Each line's text
   has trailing whitespace removed. Lines are separated by one line feed (`\n`).
2. **Paragraph breaks.** Between two consecutive lines of the same page, insert exactly one
   empty line (so the separator is `\n\n`) when either (a) the vertical distance from the first
   line's baseline to the second line's baseline exceeds **1.5 ×** the first line's height
   (its font size; reference value), or (b) the second line begins above the first line's top
   (reading order moved to a new column or text block). No other empty lines are produced; any
   empty or whitespace-only lines the reader itself reports are dropped first.
3. **Pages.** Page texts are joined in page order with a single form feed (U+000C) and nothing
   else. A form feed is a line break but **not** a blank line: a list item, reference entry, or
   sentence continues across it. The page of a character offset is 1 + the number of form feeds
   before it.

The resulting string is the extracted text that every offset (§2.8) and every rule in this
specification refers to. A **blank line** is a line that is empty or contains only spaces and
tabs; for a PDF it arises only from step 2. Conformance fixtures (§8.2) that call for "a blank
line" in a PDF render it as a vertical gap of at least twice the line height; a source fixture
writes an empty line.

**Section headings.** A line of the text source, with surrounding whitespace removed, is a
**heading line** when it matches one of these forms (reference values in parentheses):

1. **Markup heading:** a Markdown heading (`^#{1,6}\s+\S`) or a LaTeX sectioning command
   (`\section`, `\subsection`, `\subsubsection`, starred or not). Its *title* is the text after
   the `#` run or inside the braces.
2. **Numbered heading:** `^(\d{1,2}(\.\d{1,2}){0,3})\.?\s+(.+)$`, where the remainder is the
   *title* and the title is a *title phrase*: at most 80 characters (whole line) and 12 words;
   its first character is an uppercase letter; it does not end with `.`, `,`, `;` or `:`; it
   contains no `%`, `=`, `±`, and no number with a radix point; and it is either **all caps**
   (every letter uppercase, e.g. `5 DISCUSSION`) or **title case** (every word of four or more
   letters begins with an uppercase letter, e.g. `2.4 Cross-Domain Robustness Analysis`,
   `3. Method`). So `2.4 Cross-Domain Robustness Analysis`, `5 DISCUSSION`, and `3. Method`
   are headings, while `2 datasets were used.` and `3 Results improved by 4.1%` are not.
3. **Named heading:** the line, optionally ending in `:` or `.`, equals (case-insensitively) a
   name in the label table below. A line that begins with `Abstract` followed by `.`, `:`, a dash,
   or whitespace and an uppercase letter is an abstract heading glued to its first sentence; only
   the word `Abstract` and its punctuation are the heading.

A heading line is not part of any section's text: its numbers are never harvested and it never
starts a sentence. The section it opens runs to the next heading line. Text before the first
heading is the section `front`.

**Section labels.** The *label* of a section is derived from its heading's title: strip a
leading section number, surrounding punctuation, and LaTeX commands, *collapse* whitespace, and
lowercase. If the result (or its first component before ` and `, `&`, or `,`) is in the table,
the label is the table's canonical label; otherwise the label is the lowercased title itself (so
`5 DISCUSSION` is labelled `discussion`, and `1 INTRODUCTION & RELATED WORK` is labelled
`introduction`).

| Title (case-insensitive; reference list) | Label |
|------------------------------------------|-------|
| abstract | `abstract` |
| introduction | `introduction` |
| contribution(s), our contributions, main contributions | `contributions` |
| conclusion(s), concluding remarks, summary, summary and conclusion(s), conclusion(s) and future work, discussion and conclusion(s) | `conclusion` |
| results, result, evaluation(s), experiment(s), experimental results, experiments and results, results and discussion, empirical results, empirical evaluation, main results, experimental evaluation, evaluation and results | `results` |
| related work(s) | `related work` |
| references, bibliography | `references` |

## 2.8 Quotes and locating them in extracted text

Text extracted from a PDF is not a faithful copy of the rendered page: line-break hyphenation
(`effi-\ncient`), soft hyphens (U+00AD), ligatures (`ﬁ`), collapsed or doubled whitespace, and
words glued across columns are all common. A **quote** in this specification is therefore an
**excerpt of the extracted text**, located by one of the procedures below. It is evidence that
the text exists in the paper, not a byte-exact copy of the PDF.

**Normalizations** (each is a pure function of a string):

| Name | Definition |
|------|-----------|
| *collapse* | Replace every run of whitespace with one space and trim both ends. |
| *squash* | Delete every `-` immediately followed by a line break, delete U+00AD, lowercase, then delete all whitespace. |
| *fold* | Apply Unicode NFKC to each character (so `ﬁ` → `fi`), lowercase, and keep only alphanumeric characters. |
| *rejoin* | Delete U+00AD, then *collapse*; then delete every `-` that is preceded by a lowercase letter and followed by exactly one space and a lowercase letter, together with that space (`evalua- tion` → `evaluation`, `We in- troduce` → `We introduce`), **except** when the following word is `and`, `or`, `nor`, or `to` (a suspended hyphen, as in `pre- and post-training`); finally insert one space after a `:` that is directly followed by an uppercase letter. |

*rejoin* is for **display text only** (contribution and claim statements, §3.5, §3.6.4). It is
never applied to a `quote`: locators keep the exact extracted span and its offsets, so a quote
such as `We in- troduce a parser` still slices out of the extracted text unchanged while the
statement beside it reads `We introduce a parser`.

**Locating procedures.** A conforming tool uses the procedure named by each producing step:

1. **Exact** (reviewer findings, §5.5): the quote MUST be a substring of the cited excerpt. If
   it is not, but exactly one span of the excerpt equals the quote with every whitespace run
   allowed to match any whitespace run, that span is used instead. Quotes outside
   12–4000 characters (reference values, non-normative) are rejected.
2. **Squashed** (LLM-proposed quotes in the adapter, §3.7, and the judge, §4.10): accept when
   *squash*(quote) is at least 12 characters (reference value) and is a substring of
   *squash*(text).
3. **Folded span** (contribution quotes, §3.6.4, §5.13): first try a whitespace-insensitive match
   as in (1); otherwise match *fold*(quote) (at least 10 characters, reference value) inside
   *fold*(text), and map the match back to the smallest covering span of the original text.
   The stored quote is the **exact original span** `text[char_start:char_end]`, so it can be
   re-checked by slicing.

**Character locators.** When a locator carries `char_start`/`char_end`, they are zero-based,
half-open offsets (`end ≥ start`) into the **text source** the locating tool extracted
(§2.3.2), not into PDF bytes. A different extractor may produce different offsets; consumers
that re-check a locator MUST use the quote, and MAY use the offsets only against the same
extracted text.

**Normalized excerpts.** Some quotes are *produced* rather than located: a harvested result's
context (§3.4) is a *collapse*-normalized sentence of extracted text, and its `quote` is the
raw numeric token. Such fields are labeled as normalized excerpts where they are defined; a
consumer locates them with the *squash* procedure.
