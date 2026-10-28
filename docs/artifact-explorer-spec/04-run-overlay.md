> **Audience**: Builders of research-artifact viewers.
> **Source of truth for**: How the explorer reads a judge/reviewer run, joins it to the artifact,
> and presents it without promoting advisory content.

# 4. Run overlay

The overlay is optional and additive. The core document (§3) is the same with and without it,
except for the cross-reference lists that §4.4 fills on claims and results (`judge_finding_ids`,
`review_finding_ids`) and the reference `check` values (§3.12). Everything in the overlay is
**read** from the run as JR §6 defines it; the explorer evaluates nothing (I2).

## 4.1 `evaluation` skeleton

```json
"evaluation": {
  "run": {
    "sealed": true,
    "run_id": "20261028T213946.517Z-1083",
    "scope": "artifact-informed",
    "judge_only": false,
    "status": "completed",
    "created_at": "…", "completed_at": "…",
    "reviewer_version": "…",
    "input_digest": "<sha256>",
    "configuration": { "…": "manifest configuration, verbatim (JR §6.3)" },
    "options": { "…": "manifest options, verbatim" },
    "llm": { "provider": "…", "model": "…", "prompt_contract": "…" },
    "stages": { "paper_review": "completed", "…": "…" },
    "stage_notes": { },
    "files": { "draft": "<asset reference>", "paper_review": "<asset reference>" }
  },
  "judge": { "…": "§4.2, or null" },
  "review": { "…": "§4.3, or null" },
  "citation_assets": { "review-output:visuals/page-001.png": "<asset reference or null>" }
}
```

`run` copies the manifest fields of JR §6.3 (mode B) or `run.json` fields (mode C, §4.7);
`stages` is the manifest's map (JR §6.5: the authoritative copy), `llm` is `run.json.llm`.
`completed_at` is not a manifest field: it is `run.json.completed_at` in both modes.
Values the run does not provide are `null`. `judge_only` is `true` exactly when `scope` is
`artifact-informed` and `stages.paper_review` is `not-requested` (JR §6.4); it is derived, not
read; in mode C it is derived the same way from the stages available, and is `false` when
`paper_review` is unknown.

## 4.2 `evaluation.judge`

Present when the run has a judge result (`manifest.judge.path`, JR §6.6.1); else `null`.

| Key | Source |
|-----|--------|
| `run_id` | `judge.json.run_id`, verbatim: the **judge's own** run identifier |
| `judge_version`, `format_version`, `rubric`, `method_badge`, `badges`, `origin`, `warnings` | `judge.json`, verbatim |
| `findings` | `judge.json.findings`, each copied verbatim (JR §4.2), plus `joins` (§4.4) |
| `contribution_diagnostics` | `judge.json.contribution_diagnostics`, verbatim; also used for the top-level list (§3.5) |
| `reference_check` | `{available, resolver, counts}` from `judge.json.reference_check`; when that is `null` or absent, from `reference-check.json` if it is a run output (mode B) or present (mode C, §2.7) — JR §6.6.2 stores the same object in both places; else `null`. Per-reference `verdicts` from the same source go to `references[].check` (§3.12) |
| `activity`, `submission_executed` | manifest `judge` block (mode B); `run.json.input_provenance.judge` (mode C, §4.7), which JR §6.7 rule 7 requires to equal the manifest block; `null` when neither exists |

`evaluation.judge.run_id` and `evaluation.run.run_id` are different identifiers and are never
compared or reconciled by the explorer: JR §6.3 records the judge's run identifier in the
manifest's `judge` block separately from the run's own, and JR §6.7 checks the judge result
against that block, not against the run. A judge result produced earlier than, or apart from,
the review run therefore legitimately carries a different `run_id`. The Provenance section shows
both (§5.4.5).

The site MUST show `activity` and, when it is `inspection`, state that no code was executed: the
judge's verdicts on an inspected artifact are checks of consistency and declaration, not fresh
reproduction (JR §5.12 item 15).

## 4.3 `evaluation.review`

Present unless the run is judge-only (§4.1); in a judge-only run it is `null` and the site
says "No review was requested in this run (judge-only)." A judge-only run's `findings.json` is
empty and its drafts only state that no review was requested (JR §6.2, §6.4); the explorer still
copies the drafts (§4.6) but does not present them as a review. In every other run `review` is
present whatever the `paper_review` status, and §4.5 item 1 governs how a non-`completed`
status is shown. A file the table below names that is absent from `outputs` (for example
`contributions.json` in a judge-only run, or `artifact-reconciliation.json` in paper-only scope)
gives `null` or `[]`.

| Key | Source |
|-----|--------|
| `findings` | `findings.json.findings`, each copied verbatim (JR §5.5), plus `joins` (§4.4) |
| `groups` | `run.json.groups`, verbatim (bucket → finding IDs) |
| `synthesis` | `run.json.synthesis`, verbatim, or `null` |
| `human_owned` | `run.json.human_owned`, verbatim |
| `contribution_review` | `contributions.json` (equal to `run.json.contribution_review`, JR §6.5), verbatim |
| `paper_contribution_review` | `run.json.paper_contribution_review`, verbatim, or `null` |
| `reconciliation` | `artifact-reconciliation.json.records`, verbatim, or `[]` (JR §5.10.2) |
| `warnings` | `run.json.warnings` |

If `contributions.json` and `run.json.contribution_review` differ, the explorer uses
`contributions.json` and adds a warning (JR §6.8 SHOULD).

## 4.4 Joins

Joins are **navigational**: they let a reader go from a claim to the analysis that mentions it
and back. They are computed only from identifiers the run itself records, by these rules, and
nothing else (no text matching, no model call):

| From | To | Rule | `via` |
|------|----|------|-------|
| judge finding | claim | an `evidence` entry `<claims index path>#<id>`, where the path is the artifact's claims index path (default `claims.yml`) | `evidence-anchor` |
| judge finding | result | an `evidence` entry `<results index path>#<id>` (default `results.yml`) | `evidence-anchor` |
| review finding | claim | an evidence citation `claim:<id>` (JR §5.3.2) | `citation` |
| review finding | claim | `evidence_details.claim_id` (comparison findings, JR §5.10.2) | `reconciliation` |
| review finding | result | an evidence citation `result:<id>` | `citation` |
| review finding | contribution | an evidence citation `contribution:<id>` | `citation` |
| review finding | claim, result, contribution, or judge finding | `target`, when it is a reference (below) | `target` |
| review finding | judge finding | an evidence citation `judge:<id>` | `citation` |
| review finding | judge finding | an ID in the finding's own `judge_finding_ids` | `judge-ref` |

**The `joins` key.** Every judge and review finding in `data.json` carries `joins`: a list of
`{kind, id, via, resolved}` records, where `kind` is `claim`, `result`, `contribution`, or
`judge_finding`; `id` is the bare identifier (without prefix or anchor); `via` is the rule's
value from the table; and `resolved` is `true` when a record of that kind with that ID exists in
the **resolution set** of its kind:

| Kind | Resolution set |
|------|----------------|
| `claim`, `result` | the artifact's claims, results |
| `contribution` | the artifact's contributions, the run's `contribution_review.declarations`, and `paper_contribution_review.declarations` (by `id`) |
| `judge_finding` | `evaluation.judge.findings` |

Records are listed in this order — `target`, then `evidence` entries in their order, then
`evidence_details.claim_id`, then `judge_finding_ids` in their order — and a `(kind, id, via)`
triple appears once (first occurrence). A finding with no join has `joins: []`. The `joins` key
is the only place the explorer records its joins on a finding; every field the finding itself
carries, including its own `judge_finding_ids` and `target`, stays verbatim and is never
overwritten or merged. An unresolved join (`resolved: false`) is kept, shown as unresolved, and
reported in `warnings` (aggregation per §3.1 allowed): it is an explicit identifier that names
nothing.

**Target grammar.** JR §5.5 makes `target` free text, defaulting to `""`, with
`contribution:<id>` for contribution axes; real targets include prose such as `abstract` or
`Table 3 / Section 5.2.2`. The explorer classifies each `target` as exactly one of:

1. **No target**: absent, `null`, not a string, or empty after trimming. No join.
2. **Prefixed reference**: the trimmed string is `<prefix>:<id>` where `<prefix>` is `claim`,
   `result`, `contribution`, or `judge` (giving kind `claim`, `result`, `contribution`,
   `judge_finding`) and `<id>` is non-empty and contains no whitespace. One `target` join of that
   kind, resolved or not.
3. **Malformed reference**: the trimmed string starts with one of those four prefixes and a colon,
   but the rest is empty or contains whitespace. No join; one warning naming the finding.
4. **Bare reference**: any other trimmed string that equals, exactly and case-sensitively, an ID
   in a resolution set, tried in this order: claims, the run's
   `contribution_review.declarations`, `paper_contribution_review.declarations`, the artifact's
   contributions, judge findings. One resolved `target` join of the first matching kind. (A
   converted judge finding's `target` is the full judge finding ID, JR §5.10.1, and joins this way.)
5. **Free text**: anything else. No join and **no warning**; the site shows it as plain text
   ("About: …", §5.4.6). Prose is not an identifier, so it is never reported as unresolved.

**Direct references only.** A finding is joined to a claim, result, or contribution only when
that finding itself names it by one of the rules above. Joins are never transitive: a review
finding that cites a judge finding (`judge:<id>` or `judge_finding_ids`) is joined to that judge
finding, **not** to the judge finding's claims or results; a review finding that cites a
contribution is not joined to that contribution's claims. The site may show the judge finding's
own claim links when the reader opens it, but never lists the review finding under those claims.

The core claim and result records receive `judge_finding_ids` and `review_finding_ids`, and
artifact contributions receive `review_finding_ids`: the IDs of findings with a resolved join of
that record's kind and ID, in the order the findings appear in their source file, each ID once.
The site lists, for a run's reviewed candidate, the review findings whose `joins` name its ID
(§5.4.2); nothing is stored on the run's records. The explorer MUST NOT derive a per-claim status,
count of "supporting" versus "contradicting" findings, or any other aggregate of finding
assessments (I2). It MAY show the number of linked findings.

In bgpt, the judge finding `claim_validators/claim-4.v1` (verdict `advisory`, mode verdict
`attested`) cites `claims.yml#claim-4` and results `R9`, `R10`, `R11`, `R40`, `R41`, `R44`,
`R45`, `R46`; so claim `claim-4` lists that finding and those eight results list it too.

## 4.5 Presentation obligations

The site inherits every consumer obligation of JR §6.8. In particular it MUST:

1. **Show stage status.** Output of a stage whose status is not `completed` is shown under a
   notice naming the status and the `stage_notes` reason; it is never presented as complete.
2. **Keep human-owned values unset.** Recommendation, scores, and confidence render exactly
   `unset` when `null`; `human_qualification: null` renders "not yet qualified by a human",
   never as a negative (I8).
3. **Keep contribution axes separate.** Claim support, significance, and originality are shown
   as three independent statuses, never combined into a score, rank, colour scale, or vote.
4. **Read `link_basis` with all four values** and label claim support "Claim support (inferred
   links)" when `inferred` and "Claim support (declared and inferred links)" when `mixed`
   (JR §5.13.5). `none` renders "No claims linked"; `declared` renders "Claim support".
5. **Attribute inferred links** with the phrases of §5.6.
6. **Not treat `display` text as evidence**, and not read an empty candidate list as an absence
   of contributions.
7. **Keep diagnostics apart.** Contribution diagnostics are shown in their own block, headed
   "Contribution declaration checks (structural)", never among findings, and never next to a
   verdict as if they affected it.
8. **Label every finding with its source** — "Judge (deterministic)" for judge findings,
   "Reviewer (advisory)" for reviewer findings — and show the finding's own epistemic status,
   confidence, and grounding status verbatim when present.
9. **Separate the artifact from the analysis.** Reviewed contribution candidates come from the
   run. Whether a run's candidates repeat, merge, or replace the artifact's contributions is the
   run's business (JR §5.13); the explorer neither checks it nor depends on it, and shows what it
   reads. The site shows the run's candidates
   as the run's, each with its own `provenance.kind` label (§5.6), links each to the artifact
   contributions named in its `provenance.derived_from` or sharing its ID, and never rewrites the
   artifact's list to match.

## 4.6 Run files copied into the site

Only these run files are copied, under `run/` with their run-relative paths, and each MUST be a
key of the manifest's `outputs` (or `inputs`, for the snapshot paper):

- `review-draft.md` and `paper-review.md` (`files.draft`, `files.paper_review`);
- every file named by a `review-output:<path>` citation at any citation site (below), for
  example the rendered page images under `visuals/`;
- every file that a Markdown link or image in a copied run Markdown file resolves to (§2.5,
  Markdown targets, with the run directory as root), when it is a key of `outputs`; any other
  target is `null` in that file's `embedded` map;
- in paper-only scope, the snapshot paper (`manifest.paper`).

The explorer re-hashes **every** file it reads or copies from the run as it does so — run outputs
against `outputs`, snapshot files (including every artifact asset taken from
`snapshot/artifact/`) against `inputs`. A hash that differs from the manifest means the run
changed after validation, and the build stops with exit `2` without leaving a partial site.
Snapshot artifact files are copied under `assets/` like any artifact file (§3.1), since in mode B
the snapshot **is** the artifact.

**Citation sites** are every list of citation strings in the copied overlay: each finding's
`evidence`; `synthesis.contribution_evidence`, `synthesis.originality_evidence`, and
`synthesis.impact_evidence`; and every `evidence` list inside `contribution_review` and
`paper_contribution_review` (for example in each assessment axis). `evaluation.citation_assets`
maps every `artifact:` and `review-output:` citation string found at any citation site, verbatim
(including any `#<fragment>`), to the asset reference of the copied file (`url` under `assets/`
or `run/`), or to `null` when it is unresolved or not copied. The viewer links these citations
only through this map.

### 4.6.1 Citation rendering

Each citation of JR §5.3.2, at any citation site, renders as:

| Citation | Rendered as |
|----------|-------------|
| `claim:<id>`, `result:<id>`, `reference:<id>`, `contribution:<id>`, `judge:<id>` | a link to that record's route (§5.3); unresolved → the citation text, marked unresolved |
| `paper:p.<n>` | a link to the paper PDF opened at page *n* when a PDF asset exists, else text |
| `paper:document`, `paper:section/<name>`, `paper:chars/<a>-<b>` | the citation text, with the finding's `evidence_quotes` shown beside it; the explorer does not re-extract paper text |
| `artifact:<path>[#<fragment>]` | a link to its `citation_assets` URL; the file is copied like any artifact asset (§3.1) when it resolves under §2.5, else the citation text is shown |
| `review-record:comparison/<i>` | a link to reconciliation record *i* (route `#/evaluation/reconciliation/<i>`, §5.2) |
| other `review-record:` forms | the citation text (the explorer does not copy visual or run-evidence records in v1) |
| `review-output:<path>` | a link to its `citation_assets` URL under `run/` when copied (images inline), else the citation text |
| anything else | the citation text, verbatim |

Judge finding `evidence` entries are artifact paths with optional anchors (JR §4.2), not JR
§5.3.2 citations. An entry that produced a join (§4.4) renders as a link to the joined record's
route, with the entry text visible; every other entry renders as its text, verbatim.

## 4.7 Unsealed preview (mode C)

In mode C the overlay is built from the files of §2.7 by the same rules, with these differences:
run files are copied only from the list in §2.7 and from `review-output:` citations that resolve
inside the outputs directory under §2.5 (with the outputs directory as root); no hash check is
possible; and the banner of §5.5 is mandatory. `evaluation.run` is filled per key:

| Key | Mode C source |
|-----|---------------|
| `sealed` | `false` |
| `run_id`, `reviewer_version`, `created_at`, `completed_at`, `configuration`, `llm` | `run.json`, same-named key |
| `scope` | `run.json.input_provenance.kind` |
| `input_digest` | `run.json.input_provenance.input_digest` (shown as recorded; nothing to verify it against) |
| `stages` | `run.json.input_provenance.stages`, else `{}` |
| `judge_only` | derived as in §4.1 |
| `status`, `options`, `stage_notes` | `null` (manifest-only fields) |
| judge `activity`, `submission_executed` (§4.2) | `run.json.input_provenance.judge` |
| `files` | `draft` / `paper_review`: asset references of `review-draft.md` / `paper-review.md` when present in the outputs directory, else `null` |

Without `run.json`, every key above except `sealed`, `judge_only` (`false`), and `files` is `null`.
