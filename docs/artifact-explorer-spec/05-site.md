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
| `#/review`, `#/review/<bucket>` | Review | §5.4.7, shown in the navigation when `evaluation.review` is non-`null`; the second form opens bucket `<bucket>` (slugs in §5.4.7). With no run: "No analysis run was supplied."; in a judge-only run: the judge-only notice of §5.5 |
| `#/evaluation` | Evaluation | §5.4.6; with no run: "No analysis run was supplied." |
| `#/evaluation/reconciliation/<i>` | Evaluation | reconciliation record *i* (0-based position in `evaluation.review.reconciliation`), the target of `review-record:comparison/<i>` citations |
| `#/evaluation/visual/<i>`, `#/evaluation/artifact-visual/<i>` | Evaluation | visual record *i* of `evaluation.review.visual.paper` / `.artifact` (§4.3): page, check, the record's classification and reason verbatim, observation, paper quote, explanation, and its image with any region (§4.3) |
| `#/contributions`, `#/contributions/<id>` | Contributions | §5.4.2 |
| `#/claims`, `#/claims/<id>` | Claims & Evidence | §5.4.1 |
| `#/paper`, `#/paper/references/<id>` | Paper | the paper PDF and/or source, title, authors, abstract, references with any check status, related work (§5.4.4), and the author reflection; the second form scrolls to and highlights reference `<id>` (the target of `reference:<id>` citations) |
| `#/paper/page/<n>` | Paper | page *n* (a positive integer) of the paper PDF in the site's own viewer (the copied PDF opened at `#page=<n>`), with a link that opens the file in a new tab; without a PDF asset, the text "p. *n*" and the notice "The paper PDF is not part of this site." This is the target of `paper:p.<n>` citations and of known pages in paper locations |
| `#/materials`, `#/materials/<kind>/<id>` | Materials | results, experiments, exhibits, figures, datasets, traces, assessments (`<kind>` is the collection name), and the README as documentation |
| `#/provenance` | Provenance | identity, `producer`, `origin`, environment, research agent, journal, and the run record (§4.1) |
| `#/findings/<id>` | — | one judge or reviewer finding (full ID), with its source label, links, and its `target`: a reference (§4.4 target grammar, cases 2 and 4) as a link, unresolved ones marked; free text as plain text after "About:"; nothing for no target or a malformed reference beyond the verbatim text |

`<id>` is the record's full ID, percent-encoded as a URI component (contribution IDs contain `/`
and are never truncated). An unknown route, ID, bucket, record index, or page number shows a
"not found" notice with a link to the overview; it never shows a blank page.

Navigation order (*reference value (non-normative)*): Overview, Review, Contributions, Claims &
Evidence, Paper, Evaluation, Materials, Provenance. The reference viewer shows it as a left
sidebar with the title, format, and per-section counts.

**Additional content.** A section MAY show content beyond what §5.4 lists, provided it is derived
only from `data.json` and the copied files, every item §5.4 requires is present, and every label
and invariant of this specification (attribution, I2, I3, I8) applies to it. Overview MAY, for
example, show each contribution with its linked claims.

## 5.4 Section contents

### 5.4.1 Claims

The list shows each claim's ID, statement, and stance. Per-claim page, in this order:
statement; stance ("not declared" when `null`); paper location (`paper_location` and the full `paper_ref`, rendered as §5.4.8 describes), linking to the paper page route when the page
is known and a PDF asset exists; a `null` page renders "page unknown" with no page link, never as page 0; validators; results (with evidence links);
experiments; exhibits and figures (each with its link method, §3.11); contributions, declared
then inferred, each inferred link with its attribution phrase (§5.6); and, with a run, the linked
judge findings then review findings (§4.4), each with its source label, verdict or assessment
copied verbatim, and the `via` of the join (from the finding's `joins`) that lists it here.
Values of the claim's `extra` MAY follow as producer metadata (§3.5.1).

*Reference value (non-normative):* the list groups claims by stance (`hypothesis`, then
`finding`, then undeclared, which also holds stances outside SDK §2.4.1) and keeps declaration
order within a group.

### 5.4.2 Contributions

- With no contributions: "No contribution declaration was provided. This is not evidence that
  the work makes no contribution."
- Each artifact contribution shows its label (§5.6), statement, `type`, `paper_ref` (§5.4.8),
  its provenance label (§5.6), declared claims, inferred claims with attribution, `significance`
  and `originality` exactly as recorded (as labeled fields, §5.4.8), its `link_basis` label
  (§4.5 item 4), and, with a run, its `review_finding_ids`. "Declared" claims are those the
  artifact's contribution record lists in `supporting_claims`; the provenance label, not the
  word "declared", says who wrote the record (§3.1). Its own page (`#/contributions/<id>`) shows
  its full ID.
- With a run, a separate block "Reviewed candidates (from analysis run `<run_id>`)" lists the
  run's contribution review per §4.5 items 2–6 and 9. Its source is `evaluation.review.contribution_review`:
  one entry per element of its `declarations`, in order, each paired with the element of
  `assessments` whose `contribution_id` equals the declaration's `id` (a declaration with no
  assessment shows "not assessed"; an assessment with no declaration is listed after the
  declarations under its `contribution_id`). For each candidate: its label (§5.6), statement,
  provenance label (§5.6), "Merged from:" followed by a link to every artifact contribution named
  in its `provenance.derived_from` or sharing its ID (§4.5 item 9), the three axes as separate
  statuses with their points and sources, `human_qualification` as "not yet qualified by a human",
  the review findings whose `joins` name its ID (§4.4), listed by label (§5.6), and the sentence
  "Advisory assessments; the human reviewer decides whether each contribution qualifies." When
  `contribution_review` has no `declarations` list (for example the status object
  `{status: unavailable, reason}` of JR §6.2), the block shows its `status` and `reason`
  instead. When `paper_contribution_review` is non-null it is shown, by the same rules, as a
  separate block headed "Paper-only contribution review (from analysis run `<run_id>`)".
- Contribution diagnostics follow, under §4.5 item 7, grouped and numbered as JR §5.13.5
  describes for the draft.

**Order and folding.** Without a run, or when the run's contribution review has no
`declarations`, the artifact list comes first and is expanded. With declarations, the order
depends on who wrote the artifact's list:

1. When every artifact contribution has `provenance.kind` `author-declaration`, the **authors'
   list stays first and expanded**. Each artifact contribution carries, directly under it, the
   reviewer's assessment of every candidate whose `provenance.derived_from` names it or whose ID
   equals its ID, rendered as the candidate entry above under the heading "Reviewer assessment
   (advisory)". The block "Reviewed candidates (from analysis run `<run_id>`)" follows and lists,
   in order, the candidates attached to no artifact contribution, under the subheading
   "Additional reviewer candidates" (it states "None." when every candidate was attached).
2. Otherwise, the block "Reviewed candidates (from analysis run `<run_id>`)" comes first and is
   expanded, followed by the artifact list in a **collapsed** block (`<details>` or equivalent)
   headed "As extracted from the paper" when every artifact contribution has `provenance.kind`
   `paper-extraction`, else "As recorded in the artifact", with the count.

In both cases the "Paper-only contribution review" block follows, collapsed, then the
diagnostics block. Ordering, attaching, and folding are presentation only: each list is shown in
its own source order with every field as recorded, a candidate is attached only through its own
`derived_from` or ID, an attached candidate is labeled as the run's, and neither list is
rewritten, merged, or filtered. A collapsed block is in the page (searchable and reachable by
its route) and opens when a route targets a record inside it.

### 5.4.3 Materials

Each record shows its copied fields and its cross-references as links. Evidence assets render by
kind (§5.7). Experiments show disposition status; a non-active experiment shows its status and
rationale prominently, since dropped work is part of the record (SDK §2.2.2). Datasets show
`location.kind` and, for `external`, the `uri` as an external link (§6.3).

### 5.4.4 Paper

The paper PDF is shown with the platform's PDF viewing or offered as a link; page citations
and known pages link to the paper page route (§5.3), which opens the copied PDF at `#page=<n>`.
References list `raw` text and identifiers; with a reference check (§4.2, or a separate result,
§4.9), each shows its check `status` verbatim and the summary `counts` (JR §6.6.2), with the
source of the check. Without a check: "References were not checked." A reference MAY be labeled
from its `extra` (for example "First author et al. (year). Title."), with `raw` still shown.

**Related work** (§3.14), when `related_work` is non-empty: a list headed "Related-work
positioning (from the paper)", each statement as the paper's text with its citation markers, its
`relation` and the flags that are `true` (`comparative`, `superiority`, `primacy`) shown as the
producer's labels with the note "Relation labels are heuristic; whether each characterization is
fair is a human judgment." Without it: nothing, or "No related-work export was provided."

### 5.4.5 Provenance

Shows identity, `display_title` with its `display_title_source`, `title` (when they differ), `format_version`, `sdk_version`,
`producer` and `origin` as formatted data, environment (image reference and digest as declared),
the research agent's declared metadata, and the journal (the README is shown under Materials and
the reflection under Paper, §5.3). With a run, also the
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
   `coverage` (a finding without a role goes last). Findings without a role MAY be sub-grouped
   by their `verdict`, in order of first appearance. The grouping is display only and changes
   nothing about the finding (JR §4.1).
4. **Review**: in a judge-only run, "No review was requested in this run (judge-only).";
   otherwise a summary of the review: the decision synthesis (or its first paragraph) and each
   bucket of §5.4.7 with its heading and count, labeled "Reviewer (advisory)", each linking to
   its place on the Review page (§5.3). The full review is on the Review page.
5. **Reconciliation**: the reconciliation records, each linked to its claim and reachable at its
   own route (§5.3).
6. **Contribution review** (when `review` is present): for each reviewed candidate, its label
   (§5.6) and its `human_qualification` ("not yet qualified by a human" when `null`), linking to
   the candidate on the Contributions page; the status and reason of a status-object review; and
   the "Contribution declaration checks (structural)" block with the same content and rules as
   in §5.4.2. So the human-owned qualification of every candidate is visible from the Evaluation
   page.
7. Links to `run/review-draft.md` and `run/paper-review.md`.
8. **Visual inspection** (when `evaluation.review.visual` has a non-`null` member): for each of
   `paper` and `artifact`, its `status`, the outcome counts of `outcome_summary` exactly as the
   run recorded them (labels and counts verbatim), the records the run lists for human
   inspection, `limitations`, and `deferred`, with the note "Counts are observations, not
   validated claims." (JR §5.9). Each record listed links to its route (§5.3).

When `evaluation.approval` is non-`null` (§4.8), the page also shows the approval line of §4.8
next to item 1, without changing it.

### 5.4.7 Review

The Review page presents `evaluation.review` (§4.3) for reading. Every item on it carries
"Reviewer (advisory)". In this order:

1. A header with the run ID, the `paper_review` stage status (with the notice of §4.5 item 1 when
   it is not `completed`), the approval line of §4.8 when present, and the line
   "Human-owned assessment: unset" (or the values, as in §5.4.6 item 1) linking to Evaluation.
2. **Synthesis** (when `synthesis` is non-`null`): "Decision synthesis" first, then
   "Contribution summary", "Originality", and "Likely impact", each followed by its evidence
   citations (`contribution_evidence`, `originality_evidence`, `impact_evidence`) rendered per
   §4.6.1. A `null` or empty value renders "not provided".
3. **Buckets.** The findings of `groups`, one bucket per key, in this order, each headed exactly
   as below with its count, findings in the order the bucket lists them:

   | `groups` key | Heading | Slug (`#/review/<slug>`) |
   |--------------|---------|--------------------------|
   | `acceptance` | Reasons to accept | `acceptance` |
   | `decision_critical` | Decision-critical concerns | `decision-critical` |
   | `questions` | Questions for the authors | `questions` |
   | `writing_quality` | Writing quality | `writing-quality` |
   | `improvements` | Suggested improvements | `improvements` |
   | `artifact` | Artifact observations | `artifact` |
   | `evidence_review` | Evidence review | `evidence-review` |
   | — | Other findings | `other` |

   "Other findings" holds every finding of `findings` that no bucket lists, in file order. A bucket
   ID that names no finding is shown as unresolved. An empty bucket MAY be hidden, except that a
   bucket route always resolves (an empty bucket shows "None."). *Reference value
   (non-normative):* the first three buckets open, the others collapsed.
4. **Each finding** shows: its summary as its label (§5.6); its `assessment` and `dimension` in
   words; `detail`; `reasoning`; each `evidence_quotes` entry as a quotation with its page
   (§4.6.1, "page not recorded" when unknown); `decision_relevance`, `requested_action`, and
   `resolution_evidence` when present; its `target` per §5.3; its other citations per §4.6.1;
   its `epistemic_status`, `confidence`, and `grounding_status` verbatim (§4.5 item 8); and a
   link to its own route `#/findings/<id>`. Visual-record citations (§4.6.1) MAY show the
   record's image inline, with any region labeled as §4.3 requires.

A bucket is a presentation of the run's own grouping (`run.json.groups`, JR §6.5): the explorer
never assigns a finding to a bucket. In a judge-only run the page shows only the notice of §5.5.

### 5.4.8 Paper locations and recorded values

A `paper_ref` or `paper_location` is rendered as reading text, never as serialized data: its
`quote` (when present) as a quotation, then "p. *n*" (linked per §5.4.4 when a PDF asset exists;
"page unknown" when the page is `null`) and "section *s*" when present; `char_start`/`char_end`
as "characters *a*–*b* of the extracted text"; and every other key as a labeled value (its key as
the label). The same applies to a contribution's `significance` and `originality` and to a
reviewed candidate's axis values: mappings render as labeled values, lists as lists, and a
reference ID inside them (for example `originality.comparisons[].reference`) links to
`#/paper/references/<id>` when it resolves. A viewer MAY additionally offer the recorded value as
data behind an explicit control (for example "Show recorded data"), never in place of the
reading form.

## 5.5 Banners and notices

| Condition | Text (MUST appear; wording beyond the quoted part is free) |
|-----------|-------------------------------------------------------------|
| `origin.kind` is `paper` | "Derived from the paper by a paper adapter" and the `evidence_cap` value, on every page |
| Mode C | "Unsealed analysis: these outputs are not protected by a run seal and may have been changed after they were produced.", on every page |
| Paper-only run (§2.4) | "No artifact was supplied; this analysis covers the paper only." |
| Judge-only run (§4.1) | "No review was requested in this run (judge-only)." on Overview, Review, and Evaluation |
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
paper adapter"; `filename-heuristic` → "matched by file name (heuristic)"; `experiment-provenance` → "related via
a declared experiment".

**Findings**: "Judge (deterministic)" or "Reviewer (advisory)" (§4.5 item 8).

**Record labels.** Records are named for readers; their IDs stay available:

| Record | Label |
|--------|-------|
| Artifact contribution | "Contribution *k*: *title*" (*k* = `index`), or "Extracted contribution *k*: *title*" inside the folded block of §5.4.2 case 2 |
| Reviewed candidate | "Contribution *k*: *title*" (*k* = position in `declarations`, 1-based); in the paper-only block "Paper-only contribution *k*: *title*" |
| Review finding | its `summary` (shortened with an ellipsis when long), with its `assessment` |
| Judge finding | its `message`, with its `check` |
| Reconciliation record *i* | "Comparison *i*+1" |
| Visual record *i* | "Visual record *i*" with its page when known |

*title* is the record's `display.title` when present, else the text before the first sentence
end of its `statement` (or the text after a leading "Title:", else a short leading phrase of 3–90
characters before a colon), shortened with an ellipsis when
long. Claims and results keep their IDs as labels when the ID is **readable**. An ID is
**opaque** when it is longer than 40 characters, or is a prefix and `/` followed by at least 16
hexadecimal digits; an opaque ID is never used as a heading or link text, but its record's own
page shows the full ID (for example as an "ID" line), and it remains the route key (§5.3).
Citation chips use the forms of §4.6.1 ("Paper, p. *n*", "Comparison *i*+1", …).

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
