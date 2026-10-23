> **Audience**: Builders of research-artifact evaluation tools, and builders of tools that
> consume their output.
> **Source of truth for**: The `artifact-review-run/v1` sealed run directory: layout, manifest,
> stage statuses, file schemas, sealing, validation, and consumer obligations.

# 6. Run output: `artifact-review-run/v1`

The sealed run directory is the tool's **only interface** to other tools. Viewers, dashboards,
CI gates, comparison tools, and any future human-in-the-loop layer read it. They never call into
the judge or reviewer.

## 6.1 Location and identity

- A run lives at `<base>/runs/<run-id>/`. For a paper-file input, `<base>` is the
  caller-supplied workspace. For an artifact-directory input, `<base>` is caller-supplied or an
  implementation default **outside** the artifact (I1).
- `run-id` MUST match `^[A-Za-z0-9][A-Za-z0-9._-]*$`. Default: a UTC timestamp with milliseconds
  plus a short random suffix, e.g. `20260115T093000.123Z-7f3a`. A conforming command-line tool
  MUST accept an explicit `--run-id <id>`.
- If `<base>/runs/<run-id>/` already exists, the tool MUST refuse to run. Runs are never
  overwritten or appended to.
- The output path MUST NOT pass through a symbolic link.

## 6.2 Layout

```text
<run>/
  manifest.json                    # the seal (§6.3)
  snapshot/
    paper/paper.<ext>              # selected paper
    paper/references.<ext>         # caller-supplied bibliography, if any
    artifact/…                     # artifact-informed only
  run.json                         # run record (§6.5)
  findings.json                    # all reviewer findings (§5.5)
  contributions.json               # contribution review, contribution-review/v1 (§5.13.4)
  specialist-reports.json          # per-specialist status, raw responses, attempts, packets
  review-draft.md                  # complete draft (§5.12)
  paper-review.md                  # reduced paper-facing draft (§5.12)
  evidence-packet.json             # the paper evidence bundle's packet(s) (§5.3)
  visual-coverage.json             # §5.9
  visual-integration.json          # §5.9
  visuals/…                        # rendered page images referenced by review-output: citations
  judge.json                       # artifact-informed: judge result (§6.6)
  artifact-reconciliation.json     # artifact-informed: §5.10.2
  artifact-visual-coverage.json    # artifact-informed: §5.10.3
  run-evidence.json                # artifact-informed: §5.10.4
  reference-check.json             # if reference lookup ran: §6.6.2
  extracted-claims.json/.md        # if the judge's LLM extraction ran: §4.10
  reproduction/<slug>/…            # if a reproduction provider ran: §4.9
```

Every JSON output is UTF-8, and every machine-generated file carries a generated marker: a
`"_generated"` field in JSON naming the tool and stating "do not edit", or an equivalent first
line in Markdown. Every JSON output is therefore an **object**; collections live under a named
key (e.g. `findings.json` is `{"_generated": …, "run_id": …, "findings": [ … ]}`).

**Required files by scope** (each MUST be listed in `outputs`):

| Scope / invocation | Required |
|--------------------|----------|
| All | `manifest.json`, `snapshot/…`, `run.json`, `findings.json`, `review-draft.md`, `paper-review.md` |
| Paper-only review | plus `specialist-reports.json`, `evidence-packet.json`, `visual-coverage.json`, `visual-integration.json`, `contributions.json` |
| Artifact-informed review | plus everything in the paper-only row, `judge.json`, `artifact-reconciliation.json`, `artifact-visual-coverage.json`, `run-evidence.json` |
| Judge-only | plus `judge.json` |

All other files in the layout are present only when their stage ran. A required file for a stage
that did not run still exists and records the stage status and reason (e.g.
`{"_generated": …, "status": "unavailable", "reason": "no LLM provider configured"}`).
In a judge-only run, `findings.json` holds an empty reviewer finding list; judge findings live in
`judge.json`.

## 6.3 Manifest

```json
{
  "_generated": "<tool>: immutable completed review run",
  "format_version": "artifact-review-run/v1",
  "run_id": "20260115T093000Z",
  "scope": "artifact-informed",
  "status": "completed",
  "error": null,
  "reviewer_version": "<tool name and version>",
  "created_at": "2026-01-15T09:30:00Z",
  "options": {
    "model": "<model id or null>",
    "provider": "<provider id or null>",
    "reference_lookup_requested": true,
    "reproduction_requested": false,
    "visual_page_limit": null
  },
  "inputs":  { "snapshot/paper/paper.pdf": "<sha256>", "snapshot/artifact/manifest.yml": "<sha256>" },
  "input_digest": "<sha256>",
  "paper": "snapshot/paper/paper.pdf",
  "artifact_paper": "paper.pdf",
  "configuration": { "venue": "generic-computing/v2", "area": "computer-science/v1",
                     "methodology": "unspecified-methodology/v1", "digest": "<sha256>", "…": "…" },
  "stages": { "paper_review": "completed", "…": "…" },
  "stage_notes": { "visual_inspection": "no image-capable provider configured" },
  "judge": {
    "path": "judge.json",
    "run_id": "20260115T093000Z",
    "judge_version": "<version>",
    "checks": ["structure", "claim_validators", "paper_consistency", "provenance", "assessments"],
    "activity": "inspection",
    "submission_executed": false
  },
  "outputs": { "run.json": "<sha256>", "findings.json": "<sha256>", "…": "…" },
  "files": { "run": "run.json", "findings": "findings.json",
             "draft": "review-draft.md", "paper_review": "paper-review.md" }
}
```

| Field | Rule |
|-------|------|
| `status` | `running` → `completed` or `failed`. A failed run sets `error` to `"<ErrorKind>: <message>"`. |
| `options` | What the caller asked for. `model` and `provider` are `null` when no LLM was used. |
| `inputs` | Map from run-relative snapshot path to SHA-256 of **every** file under `snapshot/`. |
| `input_digest` | SHA-256 of the UTF-8 encoding of `inputs` serialized as JSON with keys sorted and separators `,` and `:` (no spaces). |
| `paper` | The run-relative path of the selected paper, which MUST be a key in `inputs`; or `null` only in `artifact-informed` scope when the artifact has no resolvable paper (§2.6). |
| `artifact_paper` | Artifact-informed only: the artifact-relative path the paper was selected from. `snapshot/artifact/<artifact_paper>` MUST have the same hash as `paper`. `null` otherwise. |
| `configuration` | The resolved configuration (§5.2), including `digest`. |
| `stages` | Map from stage name to status (§6.4). |
| `stage_notes` | Optional. Map from stage name to a one-line reason for any status other than `completed`. |
| `judge` | Artifact-informed: describes `judge.json`. `activity` is `inspection` unless a reproduction provider executed code, in which case it is `reproduction` and `submission_executed` is `true`. Paper-only: MUST be `null`. |
| `outputs` | Map from run-relative path to SHA-256 of every output file **except** `manifest.json` itself and anything under `snapshot/`. MUST be non-empty. |
| `files` | Named entry points. `run`, `findings`, `draft`, and `paper_review` are REQUIRED; each value MUST be a key in `outputs`. |

## 6.4 Stages

| Stage | Meaning |
|-------|---------|
| `snapshot` | Inputs captured and hashed. |
| `paper_review` | Specialists and synthesis (§5.4–5.8). |
| `contribution_digest` | Contribution digest (§5.13.2). |
| `contribution_review` | Contribution review written to `contributions.json` (§5.13.4). |
| `visual_inspection` | Paper visuals interpreted (§5.9). |
| `visual_integration` | Visual records merged into findings (§5.9). |
| `artifact_checks` | Judge ran (§4). |
| `artifact_reconciliation` | §5.10.2 |
| `artifact_visual_inspection` | §5.10.3 |
| `run_evidence` | §5.10.4 |
| `reference_lookup` | Reference existence check (§4.10). |
| `reproduction` | Reproduction provider (§4.9). |
| `seal` | Outputs hashed and manifest completed. |

| Status | Meaning |
|--------|---------|
| `running` | In progress (only visible in a non-completed manifest). |
| `completed` | Ran fully. |
| `incomplete` | Ran but some part did not finish (e.g. one specialist failed). Output exists and is partial. |
| `failed` | Ran and failed; no usable output. |
| `unavailable` | Could not run because a dependency was absent (no LLM, no paper text, resolver down). |
| `not-run` | Applicable but deliberately not run (e.g. requested but out of budget). |
| `not-requested` | Not applicable to this scope, or the caller did not ask for it. |

`snapshot` and `seal` are progress events only; a `completed` manifest implies both, and they
MUST NOT appear as keys in `stages`. Every other
stage name in the table MUST appear in `stages` of a completed run. In `paper-only` scope
all four artifact stages are `not-requested`. `reproduction` is `not-requested` unless requested;
if requested without a provider it is `unavailable`.

In both review scopes, `contribution_digest` and `contribution_review` apply (paper-only reviews
review source-extracted candidates, §5.13.1); without an LLM provider both are `unavailable`.

A judge-only invocation (§1.2) uses scope `artifact-informed` and sets `paper_review`,
`contribution_digest`, `contribution_review`, `visual_inspection`, `visual_integration`, `artifact_reconciliation`,
`artifact_visual_inspection`, and `run_evidence` to `not-requested`; `reference_lookup` is
`not-requested` unless the caller asked for it. Its `review-draft.md` and
`paper-review.md` MUST still exist and say that no review was requested, so the required `files`
keys are always present.

## 6.5 `run.json`

`run.json` is the run record. This is its **complete top-level skeleton**; every key is always
present (absence is `null` or an empty list, never omission):

```json
{
  "_generated": "…",
  "run_id": "…",
  "reviewer_version": "…",
  "created_at": "…",
  "completed_at": "…",
  "input_provenance": {
    "kind": "artifact-informed",
    "input_digest": "<same as manifest>",
    "stages": { "paper_review": "completed", "contribution_digest": "completed", "…": "…" },
    "judge": { "…same as manifest…": "…" },
    "artifact_paper": "<same as manifest>",
    "text_source": "pdf-extraction",
    "extraction_note": "…",
    "uninspected_ranges": [[61234, 80211]]
  },
  "configuration": { "…same as manifest…": "…" },
  "llm": { "provider": "…", "model": "…", "prompt_contract": "<version>" },
  "synthesis": { "contribution_summary": "…", "originality": "…", "likely_impact": "…",
                 "decision_synthesis": "…", "contribution_evidence": [], "originality_evidence": [],
                 "impact_evidence": [] },
  "groups": { "acceptance": ["<finding id>"], "decision_critical": [], "questions": [],
              "writing_quality": [], "improvements": [], "artifact": [], "evidence_review": [] },
  "contribution_review": { "…": "the contributions.json object, §5.13.4" },
  "paper_contribution_review": { "…": "the paper-only contribution review, §5.13.4" },
  "human_owned": { "recommendation": null, "scores": null, "confidence": null },
  "warnings": ["…"]
}
```

**Where stages live.** The authoritative stage map is the manifest's `stages` (§6.3, §6.4).
`run.json` mirrors it **only** at `input_provenance.stages`, which MUST equal the manifest's
(§6.7 rule 7). There is no top-level `stages` key in `run.json`.

`synthesis` is `null` when synthesis did not complete. `human_owned` MUST always be present with
all three values `null` (I4). `contribution_review` MUST equal the content of
`contributions.json`; both always contain `human_qualification: null` for every assessment.

**Fields with no value in a run.** `text_source`, `extraction_note`, and `uninspected_ranges` are
`null` when no paper text was extracted. `llm` is `null` when no provider was used. In a
judge-only run, `configuration` is `{"venue": null, "area": null, "methodology": null,
"digest": null}`, `synthesis`, `contribution_review`, and `paper_contribution_review` are
`null`, and every `groups` list is empty.

## 6.6 Judge outputs

### 6.6.1 `judge.json`

```json
{
  "_generated": "DO NOT EDIT — produced by <tool>. Re-run to regenerate.",
  "format_version": "evaluable-artifact/v3",
  "run_id": "…",
  "generated_at": "…",
  "judge_version": "…",
  "identity": { "id": "<artifact id>", "title": "…" },
  "origin": { "kind": "paper", "evidence_cap": "attested" },
  "rubric": "PARTIAL",
  "method_badge": null,
  "badges": { "available": "unverifiable", "functional": "awarded", "results_reproduced": "unverifiable" },
  "findings": [ { "…": "§4.2" } ],
  "warnings": ["…"],
  "contribution_diagnostics": [
    { "path": "contributions[0].supporting_claims", "message": "claim support not declared", "severity": "warning" }
  ],
  "reference_check": { "…": "§6.6.2, or null" }
}
```

`format_version` echoes the input contract the judge evaluated (`evaluable-artifact/v3` or
`evaluable-artifact/v2`). `badges` has exactly the keys and values of §4.8.
`contribution_diagnostics` is the list of §4.5.7 (empty when no contributions are declared); it
is not part of `findings` and has no effect on `rubric`, `method_badge`, or `badges`. `origin` is copied from the
artifact manifest (or `null`). The result MUST be re-renderable into any report without
re-evaluating the artifact.

### 6.6.2 Reference check

```json
{
  "available": true,
  "resolver": "<resolver id/version>",
  "verdicts": [
    { "id": "cite12", "raw": "Smith et al., 2024, …", "status": "verified",
      "matched_title": "…", "matched_id": "doi:10.1145/…", "reason": null }
  ],
  "counts": { "verified": 31, "unverified": 2, "error": 0, "unchecked": 1 }
}
```

`status` ∈ `verified`, `unverified`, `error`, `unchecked`. When the resolver is unavailable:
`available: false`, every reference `unchecked`, plus a warning. Stored both in
`judge.json.reference_check` and as `reference-check.json`.

## 6.7 Sealing and validation

**Writer obligations:**

1. Write the initial manifest (`status: running`) before any analysis.
2. Every manifest write MUST be atomic: write to a temporary file in the same directory, then
   rename over the target.
3. Before sealing, re-verify the snapshot (§2.5 rule 4).
4. Compute `outputs`, set `files`, set `status: completed`, write atomically, then **run the
   consumer validation below on the result**. If it fails, mark the run `failed`.
5. On any error, set `status: failed` and `error`, and write atomically.
6. After `completed`, nothing in the run directory may change.

**Consumer validation** (fail closed: any failure means "not a valid run"):

1. `format_version` is `artifact-review-run/v1`; `status` is `completed`; `scope` is
   `paper-only` or `artifact-informed`; `run_id` is non-empty.
2. `inputs` and `outputs` are non-empty maps. For every entry, the path is relative, has no `..`
   segment, does not traverse a symlink, stays inside the run directory, names a regular file,
   and that file's SHA-256 equals the recorded value.
3. `input_digest` recomputes from `inputs`.
4. The set of regular files actually under `snapshot/` equals `inputs` exactly (no extra, no
   missing files).
5. If `paper` is non-null it is a key of `inputs`; if `null`, scope is `artifact-informed`. If
   `artifact_paper` is set: scope is `artifact-informed`, the
   path passes rule 2 under `snapshot/artifact/`, and its hash equals the paper's hash.
6. `files` has `run`, `findings`, `draft`, and `paper_review`, all keys of `outputs`.
7. `run.json`: `run_id`, `reviewer_version`, and `configuration` equal the manifest's;
   `input_provenance.kind` equals `scope`; `input_provenance.{input_digest, stages, judge,
   artifact_paper}` equal the manifest's.
8. Artifact-informed: `judge` is an object whose `path` is a key of `outputs`; that file's
   `run_id` and `judge_version` equal the block's; `checks` is a non-empty list of strings;
   `activity`/`submission_executed` are `inspection`/`false`, or `reproduction`/`true` only if
   the `reproduction` stage is `completed` or `incomplete`. Paper-only: `judge` is `null`.

## 6.8 Consumer obligations and exit statuses

Consumers:

- MUST validate (§6.7) before reading anything else.
- MUST be given an explicit run path. They MUST NOT pick "the latest run" implicitly.
- MUST read stage statuses and MUST NOT present output of a non-`completed` stage as if it were
  complete.
- MUST treat the run as read-only. Annotations, human decisions, and edits belong in a separate
  location keyed by `run_id` and `input_digest` (§7.6).
- MUST NOT promote advisory content into verdicts or decisions.
- For contribution reviews (`contributions.json`, `run.json.contribution_review`,
  `run.json.paper_contribution_review`): MUST present the three axes separately and MUST NOT
  combine them into a score, rank, or vote; MUST treat `human_qualification: null` as "not yet
  qualified by a human", never as a negative; MUST label reviewer-inferred claim links
  (`link_basis: inferred`) as the reviewer's, not the authors'; MUST NOT treat `display` text as
  evidence; and MUST NOT read a missing or empty candidate list as absence of contributions.
  `contributions.json` is bound by the seal like every other output (it is in `outputs`, and its
  content is repeated in the hashed `run.json`); a consumer SHOULD check that the two agree.
- MUST NOT treat judge `contribution_diagnostics` as findings or let them affect any verdict,
  badge, or gate.

Exit statuses of a conforming command-line implementation, and when each error is detected:

| Phase | Errors detected | Run directory | Exit |
|-------|-----------------|---------------|------|
| 1. Argument and configuration parsing | unknown option, unknown profile, invalid `run-id`, output inside the artifact | not created | `2` |
| 2. Format gate (§2.2) | missing or unparsable `manifest.yml`, unsupported `format_version`, paper-only with no paper | not created | `2` |
| 3. Run creation | `run-id` already exists, output path through a symlink | not created (existing run untouched) | `2` |
| 4. Snapshot (§2.5) | special file or symlink in the artifact, hash mismatch while copying | created, `status: failed` | `2` |
| 5. Analysis and sealing | unexpected internal error, re-verification failure, self-validation failure | created, `status: failed` | `3` |
| Completed | — | `status: completed` | see below |

| Code | Meaning |
|------|---------|
| `0` | Run completed (judge-only: rubric `REPRODUCED` or `PARTIAL`; review: any rubric). |
| `1` | Judge-only invocation completed with rubric `NOT_REPRODUCED`. Contribution diagnostics, of any severity, never cause `1`. |
| `2` | Input, configuration, or usage error (phases 1–4). |
| `3` | Unexpected failure (phase 5). |

A review run always exits `0` on completion, whatever the judge rubric; the rubric is an
analysis result, not a tool failure.

**Consumer validation is a library obligation.** §6.7's consumer validation MUST be available
to consumers as a callable operation (`validate(run_dir) -> {valid: bool, errors: [text]}`, in
the implementation's idiom); writers also run it on themselves before sealing (§6.7 step 4). A
command-line `validate` subcommand is **not required**. An implementation that offers one MUST
use these exit statuses, never create or modify anything, and print every error:

| Code | Meaning |
|------|---------|
| `0` | The path is a valid sealed run (all §6.7 consumer rules pass). |
| `1` | The path was read but is not a valid run (any rule fails, including a missing or unparsable manifest, or `status` other than `completed`). |
| `2` | Usage error: no path given, unknown option, or the path does not exist or is not a directory. |
