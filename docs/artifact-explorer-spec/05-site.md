> **Audience**: Builders of research-artifact viewers.
> **Source of truth for**: The static site's layout, sections, routes, and the labels and phrases
> it must show.

# 5. The static site

## 5.1 Delivery

- The site is a set of static files. It MUST render fully when the output directory is served by
  any static HTTP server at any path prefix, with no server-side logic.
- The viewer loads `data.json` by a relative URL (an implementation MAY instead embed the same
  document in `index.html`; if it does, `data.json` is still written). Opening `index.html`
  directly from the file system MAY work but is not required.
- The viewer makes no network request outside the site (I6, §6.3). Fonts, scripts, styles, and
  icons are part of the output.
- The viewer is read-only: no control writes, uploads, or submits anything.

## 5.2 Output layout

```text
<out>/
  index.html           # entry point
  data.json            # §3, §4
  assets/<path>        # each artifact file referenced by an asset reference, at its artifact-relative path
  run/<path>           # each run file of §4.6, at its run-relative path (modes B, C)
  <application files>  # scripts, styles, fonts; names are implementation-defined
```

Only referenced files are copied: the site is not a mirror of the artifact. Markdown files that
are copied also bring the images they reference, when those resolve under §2.5. No other file is
written.

## 5.3 Sections and routes

The viewer is a single page with hash routes, so links survive static hosting:

| Route | Section | Shows |
|-------|---------|-------|
| `#/overview` (default) | Overview | `display_title`, origin notice (§5.5), counts, evidence inventory (labeled "as declared in the manifest", §3.2), and, with a run, the run summary of §5.4.6 |
| `#/evaluation` | Evaluation | §5.4.6; with no run: "No analysis run was supplied." |
| `#/evaluation/reconciliation/<i>` | Evaluation | reconciliation record *i* (0-based position in `evaluation.review.reconciliation`), the target of `review-record:comparison/<i>` citations |
| `#/contributions`, `#/contributions/<id>` | Contributions | §5.4.2 |
| `#/claims`, `#/claims/<id>` | Claims | §5.4.1 |
| `#/paper`, `#/paper/references/<id>` | Paper | the paper PDF and/or source, title, authors, abstract, references with any check status; the second form scrolls to and highlights reference `<id>` (the target of `reference:<id>` citations) |
| `#/materials`, `#/materials/<kind>/<id>` | Materials | results, experiments, exhibits, figures, datasets, traces, assessments (`<kind>` is the collection name) |
| `#/provenance` | Provenance | identity, `producer`, `origin`, environment, research agent, journal, README, reflection, and the run record (§4.1) |
| `#/findings/<id>` | — | one judge or reviewer finding (full ID), with its source label, links, and its `target`: a reference (§4.4 target grammar, cases 2 and 4) as a link, unresolved ones marked; free text as plain text after "About:"; nothing for no target or a malformed reference beyond the verbatim text |

`<id>` is the record's full ID, percent-encoded as a URI component (contribution IDs contain `/`
and are never truncated). An unknown route or ID shows a "not found" notice with a link to the
overview; it never shows a blank page.

## 5.4 Section contents

### 5.4.1 Claims

The list shows each claim's ID, statement, and stance. Per-claim page, in this order:
statement; stance ("not declared" when `null`); paper location (`paper_location` and the full `paper_ref`), linking to the PDF page when the page
is known; a `null` page renders "page unknown" with no page link, never as page 0; validators; results (with evidence links);
experiments; exhibits and figures (each with its link method, §3.11); contributions, declared
then inferred, each inferred link with its attribution phrase (§5.6); and, with a run, the linked
judge findings then review findings (§4.4), each with its source label, verdict or assessment
copied verbatim, and the `via` of the join (from the finding's `joins`) that lists it here.

*Reference value (non-normative):* the list groups claims by stance (`hypothesis`, then
`finding`, then undeclared, which also holds stances outside SDK §2.4.1) and keeps declaration
order within a group.

### 5.4.2 Contributions

- With no contributions: "No contribution declaration was provided. This is not evidence that
  the work makes no contribution."
- Each artifact contribution shows its number (`index`), statement, `type`, `paper_ref`, its
  provenance label (§5.6), declared claims, inferred claims with attribution, `significance` and
  `originality` exactly as recorded, its `link_basis` label (§4.5 item 4), and, with a run, its
  `review_finding_ids`. "Declared" claims are those the artifact's contribution record lists in
  `supporting_claims`; the provenance label, not the word "declared", says who wrote the record
  (§3.1).
- With a run, a separate block "Reviewed candidates (from analysis run `<run_id>`)" lists the
  run's contribution review per §4.5 items 2–6 and 9. Its source is `evaluation.review.contribution_review`:
  one entry per element of its `declarations`, in order, each paired with the element of
  `assessments` whose `contribution_id` equals the declaration's `id` (a declaration with no
  assessment shows "not assessed"; an assessment with no declaration is listed after the
  declarations under its `contribution_id`). For each candidate: its statement and provenance
  label (§5.6), the three axes as separate statuses with their points and sources,
  `human_qualification` as "not yet qualified by a human", the review findings whose `joins` name
  its ID (§4.4), and the sentence "Advisory assessments; the human reviewer decides whether each
  contribution qualifies." When `contribution_review` has no `declarations` list (for example
  the status object `{status: unavailable, reason}` of JR §6.2), the block shows its `status` and
  `reason` instead. When `paper_contribution_review` is non-null it is shown, by the same rules,
  as a separate block headed "Paper-only contribution review (from analysis run `<run_id>`)".
- Contribution diagnostics follow, under §4.5 item 7, grouped and numbered as JR §5.13.5
  describes for the draft.

### 5.4.3 Materials

Each record shows its copied fields and its cross-references as links. Evidence assets render by
kind (§5.7). Experiments show disposition status; a non-active experiment shows its status and
rationale prominently, since dropped work is part of the record (SDK §2.2.2). Datasets show
`location.kind` and, for `external`, the `uri` as an external link (§6.3).

### 5.4.4 Paper

The paper PDF is shown with the platform's PDF viewing or offered as a link; `#page=<n>` deep
links are used for page citations. References list `raw` text and identifiers; with a run, each
shows its check `status` verbatim and the summary `counts` (JR §6.6.2). Without a check:
"References were not checked."

### 5.4.5 Provenance

Shows identity, `display_title` with its `display_title_source`, `title` (when they differ), `format_version`, `sdk_version`,
`producer` and `origin` as formatted data, environment (image reference and digest as declared),
the research agent's declared metadata, the journal, README, and reflection. With a run, also the
full run record of §4.1 (run ID, scope, sealed state, `input_digest`, configuration, provider and
model identifiers or "none", every stage status) and, when a judge result is present, the judge's
own run ID (`evaluation.judge.run_id`, §4.2) labeled as such beside the run's.

### 5.4.6 Evaluation

With a run, in this order:

1. **Human-owned assessment.** When the run is not judge-only, exactly:

   ```text
   Overall recommendation: unset
   Criterion scores: unset
   Reviewer confidence: unset
   ```

   (a non-`null` value from the run is shown verbatim instead, with the note that it was supplied
   by a human outside the analysis), followed by "These belong to the human reviewer." In a
   judge-only run (§4.3, where `review` is `null`) the three lines are not shown; the item reads
   "Human-owned assessment: not applicable (no review was requested)."
2. **Stages**: each stage and status, with `stage_notes`.
3. **Judge** (when present): rubric, method badge, and badges verbatim, labeled "Judge
   (deterministic)"; the activity notice of §4.2; findings, each with its `verdict` and `mode_verdict`
   verbatim (JR §4.1), grouped by `presentation_role` in the order `needs_attention`, `holds_up`,
   `coverage` (a finding without a role goes last). The grouping is display only and changes
   nothing about the finding (JR §4.1).
4. **Review**: in a judge-only run, "No review was requested in this run (judge-only).";
   otherwise the synthesis (contribution summary, originality, likely impact,
   decision synthesis), then the finding buckets of `groups` in the order acceptance,
   decision-critical, questions, writing quality, improvements, artifact, evidence review, each
   labeled "Reviewer (advisory)". Findings not in any bucket are listed under "Other findings".
5. **Reconciliation**: the reconciliation records, each linked to its claim and reachable at its
   own route (§5.3).
6. **Contribution review** (when `review` is present): the "Reviewed candidates" block and, after
   it, the "Contribution declaration checks (structural)" block, with the same content and rules
   as in §5.4.2, so that the human-owned `human_qualification` of every candidate is visible from
   the Evaluation page.
7. Links to `run/review-draft.md` and `run/paper-review.md`.

## 5.5 Banners and notices

| Condition | Text (MUST appear; wording beyond the quoted part is free) |
|-----------|-------------------------------------------------------------|
| `origin.kind` is `paper` | "Derived from the paper by a paper adapter" and the `evidence_cap` value, on every page |
| Mode C | "Unsealed analysis: these outputs are not protected by a run seal and may have been changed after they were produced.", on every page |
| Paper-only run (§2.4) | "No artifact was supplied; this analysis covers the paper only." |
| Judge-only run (§4.1) | "No review was requested in this run (judge-only)." on Overview and Evaluation |
| `display_title_source` is `pdf-metadata` | "title from PDF metadata" next to the title in the header |
| Stage not `completed` | "`<stage>`: `<status>`" and the `stage_notes` reason, next to that stage's output |
| Build warnings non-empty | a count of warnings on the Overview, linking to their list on Provenance |

## 5.6 Attribution labels

**Inferred claim links** (§3.5.1), per JR §5.13.5:

| Source kind(s) | Phrase |
|----------------|--------|
| `extractor-inference` | "inferred by the paper adapter's extractor" |
| `reviewer-inference` | "inferred by the reviewer" |
| both | both phrases, joined by " and " |
| any other kind *k* | "inferred by another tool (`k`)" |
| `unrecorded` | "inferred (source not recorded)" |

**Contribution provenance** (`provenance.kind`): `author-declaration` → "declared by the
authors"; `paper-extraction` → "extracted from the paper by the paper adapter";
`reviewer-inference` → "proposed by the reviewer"; any other value *k* → "source: `k`"; absent →
"source not recorded".

**Figure links** (§3.11): `declared` → no qualifier; `adapter-suggested` → "suggested by the
paper adapter"; `filename-heuristic` → "matched by file name (heuristic)".

**Findings**: "Judge (deterministic)" or "Reviewer (advisory)" (§4.5 item 8).

Display text MAY add context (for example the method and model identifiers from the source
record) but MUST contain the phrase.

## 5.7 Rendering assets

| Kind | Rendering |
|------|-----------|
| `image` | inline `<img>` with alternative text (caption, else ID, else file name) |
| `markdown` | rendered as CommonMark with raw HTML disabled (§3.1), then sanitized (§6.2). Each link or image destination is looked up in the asset reference's `embedded` map: a non-`null` value is rewritten to its `url` (keeping the original `#fragment` for links); an external `http:`, `https:`, or `mailto:` link is an external link (§6.3); an external image is never loaded and is shown as its alternative text followed by its URL as text; any other target is shown as text |
| `text` | escaped, preformatted; large files MAY be truncated in view with a link to the full file |
| `pdf` | link, or embedded viewer from the copied file |
| `other` | download link only |

Mathematics in statements MAY be rendered; if it is, the raw text MUST remain available.
