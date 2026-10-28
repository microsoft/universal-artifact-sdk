> **Audience**: Builders who want to claim their explorer implements this specification, and
> reviewers who want to check that claim.
> **Source of truth for**: Conformance levels and the acceptance scenarios each level must pass.

# 7. Conformance

## 7.1 Levels

| Level | Requires | Optional |
|-------|----------|----------|
| **L1 Data model** | §2 (except §2.4, §2.7), §3, mode A; a valid `data.json` for every accepted artifact | — |
| **L2 Run overlay** | L1 plus §2.4, §4 (except §4.7), mode B | **+C**: mode C (§2.7, §4.7) |
| **L3 Static site** | L1 plus §5 and §6 for every `data.json` L1 produces; if L2 is also claimed, for every overlay | — |

A tool claims conformance as, for example, "artifact-explorer/v1 L1+L2+L3" or
"artifact-explorer/v1 L1+L2(+C)+L3". Every level also requires the invariants of §1.4. A viewer
alone (no builder) MAY claim L3 against data documents produced by any L1 builder.

## 7.2 How scenarios are written

Each scenario gives a **fixture**, the **action**, and the **expected** observable result.
Expectations about `data.json` name keys and values; expectations about the site name a route
and text that MUST appear on it (other wording is free). L3 expectations are checked in a
browser against the site served by a static HTTP server.

Unless stated otherwise, the fixture is a valid `evaluable-artifact/v3` directory with a
`manifest.yml` declaring `format_version`, `id: demo`, `title: Demo`, and `paper: {pdf: paper.pdf}`,
a `paper.pdf`, a claims index holding `C1` ("Accuracy is 0.91.", `stance: finding`,
`validators: []`), and a results index holding `R1` (`validates: [C1]`,
`evidence: evidence/metrics.csv`) with that file present.

**Example fixtures.** "bgpt" and "lfmu" are the published review examples
([`docs/examples/reviews/`](../examples/reviews/README.md)). Their `artifact/` directories are
artifacts. Their other files are the outputs of an artifact-informed run, published **without**
the seal; they are used as-is for mode C scenarios and as the artifact for mode A scenarios.
Sealed-run scenarios use the hand-built fixtures of §7.3, so no judge/reviewer tool is needed to
run them.

## 7.3 Hand-sealed run fixtures

The explorer validates a run's **seal and structure** (JR §6.7); it never checks that a judge or
reviewer actually produced the content. A conforming sealed run can therefore be written by hand.
Each fixture below lists only the values to write; the meaning of every field, and the rules the
result must satisfy, are those of JR §6.2–§6.7, which this section does not restate.

**Recipe** (all three fixtures):

1. Create `runs/<run_id>/snapshot/` with the files listed, byte-for-byte.
2. `inputs`: SHA-256 of every file under `snapshot/`, keyed by run-relative path.
3. `input_digest`: computed from `inputs` exactly as JR §6.3 specifies.
4. Write the output files listed, then `outputs`: SHA-256 of each, keyed by run-relative path.
5. Write `manifest.json` with the values listed and the maps from steps 2–4.

Common values: `format_version` `artifact-review-run/v1`, `status` `completed`, `error` `null`,
`reviewer_version` `fixture/0`, `created_at` `2026-01-01T00:00:00Z`, `options` with `model` and
`provider` `null` and the three other JR §6.3 options `false`, `false`, `null`; `files`
`{run: run.json, findings: findings.json, draft: review-draft.md, paper_review: paper-review.md}`;
`judge.json` (when present) has `format_version`, `judge_version` `fixture/0`, the fixture's judge
`run_id`, `rubric` `PARTIAL`, `findings` as listed, and every other JR §6.6.1 key `null` or empty.
`run.json` copies `run_id`, `reviewer_version`, `configuration`, and the
`input_provenance` values JR §6.7 rule 7 requires from the manifest, sets `completed_at`
`2026-01-01T00:05:00Z` and `human_owned` all `null`, and gives every other JR §6.5 key its empty
value. A file "with status `unavailable`" is `{"_generated": "fixture", "status": "unavailable",
"reason": "no LLM provider configured"}`.

| Fixture | `run_id`; scope | Snapshot | Stages (JR §6.4) | Outputs and other values |
|---------|-----------------|----------|------------------|--------------------------|
| **S-AI** artifact-informed, no LLM | `S-AI`; `artifact-informed` | `snapshot/artifact/` = the default fixture; `snapshot/paper/paper.pdf` = its `paper.pdf` | `artifact_checks` `completed`; `reproduction` and `reference_lookup` `not-requested`; every other stage `unavailable` | `paper` `snapshot/paper/paper.pdf`, `artifact_paper` `paper.pdf`; `configuration` `{digest: "fixture"}`; `judge` block `{path: judge.json, run_id: J-AI, judge_version: fixture/0, checks: [claim_validators], activity: inspection, submission_executed: false}`; `judge.json` with one finding `claim_validators/C1.v1` (`check` `claim_validators`, `verdict` `advisory`, `evidence` `[claims.yml#C1, results.yml#R1]`); `findings.json` with `findings: []`; `review-draft.md` and `paper-review.md` one line each; every other file of the artifact-informed row of JR §6.2 with status `unavailable` |
| **S-JO** judge-only | `S-JO`; `artifact-informed` | as S-AI | `artifact_checks` `completed`; every other stage `not-requested` (JR §6.4, judge-only) | as S-AI, except `configuration` is the judge-only value of JR §6.5; `review-draft.md` and `paper-review.md` say "No review was requested."; only the "All" and "Judge-only" rows of JR §6.2 are written |
| **S-PO** paper-only | `S-PO`; `paper-only` | `snapshot/paper/paper.pdf` only | the four artifact stages, `reproduction`, and `reference_lookup` `not-requested`; every other stage `unavailable` | `paper` `snapshot/paper/paper.pdf`, `artifact_paper` `null`, `judge` `null`; `configuration` `{digest: "fixture"}`; `findings.json` with `findings: []`; files of the paper-only row of JR §6.2 with status `unavailable` |

Scenarios that change a fixture (for example by adding a finding) re-run steps 4–5 afterwards,
unless the scenario is about a broken seal.

## 7.4 L1 — data model

| ID | Fixture / action | Expected |
|----|------------------|----------|
| X1 | Default fixture; build. | Exit `0`. `data.json` has every key of §3.2; `schema` is `artifact-explorer/data/v1`; `identity.id` `demo`; `counts.claims` `1`; `claims[0].result_ids` `[R1]`; `results[0].evidence` `evidence/metrics.csv`; `results[0].evidence_asset.url` `assets/evidence/metrics.csv`, and that file exists in the output with identical bytes; `evaluation` `null`. |
| X2 | Default fixture declared as `evaluable-artifact/v2`. | Same as X1 except `identity.format_version`; `contributions` `[]`. |
| X3 | `format_version: evaluable-artifact/v9`. | Exit `2`; output directory not created. |
| X4 | No `manifest.yml`; and separately, a `manifest.yml` that is not YAML. | Exit `2` both times; nothing written. |
| X5 | Default fixture built twice into two output directories, with the build time fixed. | The two `data.json` files are byte-identical; the copied file sets are identical. With the build time not fixed, the files differ at most in `generated_at`. |
| X6 | Results index file is `results: 42`. | Exit `0`; `results` `[]`; `claims[0].result_ids` `[]`; `warnings` names the results index. |
| X7 | `R1.evidence` is `../secret.txt`; separately `/etc/hostname`; separately a symbolic link inside the artifact pointing outside it. | Exit `0` each time; `results[0].evidence_asset` `null`, `results[0].evidence` the declared string; `warnings` non-empty; no file outside the artifact copied. |
| X8 | `R1.evidence` names a missing file. | `results[0].evidence_asset` `null`; `results[0].evidence` `evidence/metrics.csv` kept; a warning; exit `0`. |
| X9 | No claims index, no results index, and no `paper.pdf` file (the manifest still declares it). | Exit `0`; `claims`, `results` `[]`; `paper.pdf` `null`; `paper.declared.pdf` `paper.pdf` (still declared in the manifest), with a warning. |
| X10 | `paper.pdf` not declared; files `paper.pdf` and `main.pdf` both present. | `paper.pdf.path` `paper.pdf` (first probe wins). |
| X11 | `paper: {pdf: docs/p.pdf}` declared but missing; `paper.pdf` present at root. | `paper.pdf` `null` (declaration wins over probe, §2.6); a warning. |
| X12 | v3; `contributions.yml` present but `paths.contributions` not declared. | `contributions` `[]`; `contribution_diagnostics` `[]`. |
| X13 | v2 manifest declaring `paths.contributions`. | `contributions` `[]`; one diagnostic, path `paths.contributions`, severity `error`. |
| X14 | v3; contributions index `contributions: [{id: K1, statement: "A parser.", supporting_claims: [C1]}, 7]`. | `contributions` has `K1` only, with `index` `1`, `link_basis` `declared`; diagnostic `contributions[1]`, `error`; `claims[0].contribution_ids` `[K1]`. |
| X15 | K1 with `supporting_claims: []`, `inferred_supporting_claims: [C1]`, `provenance.claim_link_sources: [{kind: extractor-inference, method: m/v1, model: x, claims: [C1]}]`. | `K1.link_basis` `inferred`; `K1.inferred_claims` `[{claim_id: C1, sources: [extractor-inference]}]`; `claims[0].inferred_contribution_links` `[{contribution_id: K1, sources: [extractor-inference]}]`; `claims[0].contribution_ids` `[]`. |
| X16 | X15 with a second record `{kind: reviewer-inference, …, claims: [C1]}`. | `sources` `[extractor-inference, reviewer-inference]`. |
| X17 | X15 with `claim_link_sources` removed. | `sources` `[unrecorded]`. |
| X18 | X15 with `claim_link_sources` replaced by legacy `claim_links: {kind: reviewer-inference, method: contribution-digest/v1}`. | `sources` `[reviewer-inference]`. |
| X19 | X15 plus `supporting_claims: [C1]`. | `link_basis` `declared`; `inferred_claims` `[]` (declared wins). |
| X20 | Claim `C1` carries `contributions: [K1]` and the claims index carries a `contribution_links` object; K1 has no `inferred_supporting_claims`. | No inferred link (`claims[0].inferred_contribution_links` `[]`); the claim's `extra.contributions` is `[K1]` (§3.5.1). |
| X21 | X15 plus a claims-index key `contribution_links: {provenance: reviewer-inference, method: m/v1}`. | `sources` still `[extractor-inference]`; no key of `data.json` carries `contribution_links` (§3.5.1). |
| X22 | `C1.paper_ref` is `{page: 0, section: "4"}`; separately `{section: "4"}`; separately `{page: "6"}`. | `claims[0].paper_location.page` `null` each time (page unknown); `section` `"4"` in the first two; `claims[0].paper_ref` keeps the original value (`page: 0` in the first case). |
| X23 | Default fixture plus `paper: {pdf: paper.pdf, source: paper.tex}`, `paper.tex` containing `\title{Streaming Parsers}`, and `paper.pdf` with document-metadata title `Untitled`. | `paper.title` `Streaming Parsers`; `paper.metadata_title` `Untitled`; `identity.display_title` `Streaming Parsers`; `display_title_source` `paper-source`. |
| X24 | X23 without `paper.tex` (and without `source`); separately with a metadata title of only spaces. | First: `display_title` `Untitled`, `display_title_source` `pdf-metadata`. Second: `display_title` `Demo`, `display_title_source` `manifest-title`, `paper.metadata_title` `null`. |
| X25 | Default fixture plus a root `related_work.yml` (top-level `related_work`, one entry) declared as `paths.related_work`. | `data.json` has no `related_work` key and `counts` has no `related_work` entry; the file is not copied; no warning is required. |
| X26 | bgpt `artifact/`; build. | `counts`: `claims` 18, `contributions` 6, `results` 36, `references` 58, `experiments` 0. Claims in file order (`claim-1`, …, `claim-5`, `claim-15`, …). `claim-4.paper_location.page` `null` (the example records `0`); `claim-5.paper_location.page` `6`. `contributions[3].link_basis` `none`. `claim-1` has 4 inferred links, each with `sources` `[extractor-inference]`. `paths.figures` declared but no file: `figures` `[]` and a warning (no probe). `paper.pdf` `null` (declared, absent). `identity.origin.kind` `paper`. |
| X27 | lfmu `artifact/`; build. | `identity.title` `paper`; `identity.display_title` `paper` with `display_title_source` `manifest-title` (the example ships no paper file); `counts.contributions` 3; `counts.results` 74. |
| X28 | Default fixture plus `manifest.producer: {tool: x, anything: [1, 2]}` and an unknown claim field `foo: bar`. | `identity.producer` copied verbatim; `claims[0].extra` `{foo: bar}`. |
| X29 | Output directory equal to the artifact directory; separately inside it. | Exit `2`; nothing written. |
| X30 | Output directory exists and holds `keep.txt`; build without, then with, the explicit replace option. | Without: exit `2`, `keep.txt` untouched. With: exit `0`, `keep.txt` gone. An existing empty output directory is used without the option. |
| X31 | `C1` has `added: 2026-10-27`, `score: .nan`, and `notes: {1: a}`. | `claims[0].extra` `{added: "2026-10-27", notes: {"1": "a"}, score: "nan"}`. |
| X32 | `C1` has `stance: maybe` and `validators: [{id: v1, kind: numeric_close, result: R1, expected: 0.91}]`; the manifest has a root key `source_format: latex`. | `claims[0].stance` `maybe` with a warning; `claims[0].validators` `[{id: v1, kind: numeric_close, name: null, mode: null, gated_by: null, extra: {expected: 0.91, result: R1}}]`; `identity.extra` `{source_format: latex}`. |
| X33 | `README.md` contains `![p](img/p.png)` and `![q](img/missing.png)`; `img/p.png` exists. | `readme.embedded` `{"img/p.png": {path: img/p.png, url: assets/img/p.png, kind: image}, "img/missing.png": null}`; `assets/img/p.png` is written. |
| X34 | `paper: {source: tex}` where `tex/` holds `main.tex` with `\title{Streaming Parsers}`; separately an empty `tex/`. | First: `paper.source.path` `tex/main.tex`; `paper.declared.source` `tex`; `paper.title` `Streaming Parsers`. Second: `paper.source` `null` and a warning. |
| X35 | No `paths.figures`; exhibits index with `E1` (`type: figure`, `path: fig/a.png`, file present) and `E2` (`type: table`). | `figures` has one entry, `id` `E1`, `path` `fig/a.png`, `path_asset.url` `assets/fig/a.png`; `exhibits[0].path` `fig/a.png` and `exhibits[0].path_asset` set. |

## 7.5 L2 — run overlay

| ID | Fixture / action | Expected |
|----|------------------|----------|
| X36 | S-AI; build with the run only. | Exit `0`. `evaluation.run.sealed` `true`; `run_id` `S-AI`, `scope`, `input_digest` equal the manifest's; `completed_at` `2026-01-01T00:05:00Z` (from `run.json`); `evaluation.judge.rubric` `PARTIAL`; `evaluation.judge.run_id` `J-AI`; `evaluation.review.human_owned` all `null`; `identity.id` `demo` (read from `snapshot/artifact/`). |
| X37 | X36 with one byte of `findings.json` changed. | Exit `2` (JR §6.7 rule 2); nothing written; the message names `findings.json`. |
| X38 | X36 with `status: failed` in the manifest; separately with `manifest.json` removed. | Exit `2` both times. |
| X39 | X36 plus the artifact directory as a second input. | Exit `2` (§1.2). |
| X40 | X36 with an extra file `notes.txt` in the run directory, not in `outputs`. | Exit `0`; `notes.txt` is not read and not copied. |
| X41 | X36. | Judge finding `claim_validators/C1.v1` has `joins` `[{kind: claim, id: C1, via: evidence-anchor, resolved: true}, {kind: result, id: R1, via: evidence-anchor, resolved: true}]`; `claims[0].judge_finding_ids` and `results[0].judge_finding_ids` are `[claim_validators/C1.v1]`. No key on `claims[0]` holds a verdict. |
| X42 | S-PO. | Exit `0`; `identity.id` `null`; `claims` `[]`; `paper.declared` `{pdf: snapshot/paper/paper.pdf, source: null}`; `paper.pdf.url` `run/snapshot/paper/paper.pdf`; `paper.source` `null`; `evaluation.judge` `null`. |
| X43 | X36 where `contributions.json` and `run.json.contribution_review` differ. | `evaluation.review.contribution_review` equals `contributions.json`; `warnings` notes the difference. |
| X44 | S-AI with `findings.json` holding, written by hand: `F1` with `target` `C1`, `evidence` `[judge:claim_validators/C1.v1]`, and its own `judge_finding_ids` `[claim_validators/C1.v1]`; `F2` with only `evidence` `[judge:claim_validators/C1.v1]`; re-sealed. | `F1.joins` `[{kind: claim, id: C1, via: target, resolved: true}, {kind: judge_finding, id: claim_validators/C1.v1, via: citation, resolved: true}, {kind: judge_finding, id: claim_validators/C1.v1, via: judge-ref, resolved: true}]`; `F1.judge_finding_ids` is still exactly the copied `[claim_validators/C1.v1]`. `F2.joins` has only the `judge_finding` entry (`via` `citation`); `claims[0].review_finding_ids` `[F1]`. |
| X45 | X36 where a copied run file is changed after validation and before copy (simulated). | Exit `2`; no partial site. |
| X46 | S-JO. | Exit `0` (the run passes JR §6.7 like any other). `evaluation.run.judge_only` `true`; `evaluation.judge` present with `rubric` equal to `judge.json.rubric`; `evaluation.review` `null`; `run/review-draft.md` copied. |
| X47 | X36 (not judge-only). | `evaluation.run.judge_only` `false`; `evaluation.review` present even though no LLM provider was used (`paper_review` `unavailable`). |
| X48 | S-AI with `findings.json` holding `F3` (`target` `C1x`, no evidence) and `F4` (`target` `K1`), and the artifact declaring contribution `K1`; re-sealed. | `F3.joins` `[{kind: unknown, id: C1x, via: target, resolved: false}]`, listed in `warnings`. `F4.joins` `[{kind: contribution, id: K1, via: target, resolved: true}]`. |
| X49 | S-AI with `findings.json` holding `F5` with `evidence` `[artifact:evidence/metrics.csv, artifact:missing.txt]`; re-sealed. | `evaluation.citation_assets["artifact:evidence/metrics.csv"].url` `assets/evidence/metrics.csv`; `evaluation.citation_assets["artifact:missing.txt"]` `null`. |

**L2 +C (mode C).**

| ID | Fixture / action | Expected |
|----|------------------|----------|
| X50 | bgpt: artifact `bgpt/artifact`, outputs `bgpt/` without the opt-in flag. | Exit `2`. |
| X51 | Same with the opt-in flag. | Exit `0`. `evaluation.run.sealed` `false`; `run_id` `20261027T212706.923Z-179e`; `input_digest` equals `run.json.input_provenance.input_digest`; `status`, `options`, `stage_notes` `null`; `stages.visual_inspection` `incomplete`. `evaluation.judge.rubric` `PARTIAL`; `badges` all `unverifiable`. `contribution_diagnostics` is the judge's single entry, path `contributions[3].supporting_claims`, severity `warning`. `evaluation.review.findings` has 123 entries. |
| X52 | X51. | Judge finding `claim_validators/claim-4.v1` has a `joins` entry `{kind: claim, id: claim-4, via: evidence-anchor, resolved: true}` and `result` entries for `R9`, `R10`, `R11`, `R40`, `R41`, `R44`, `R45`, `R46`, in that order; `claim-4.judge_finding_ids` contains it and `R9.judge_finding_ids` contains it. The comparison finding whose `evidence_details.claim_id` is `claim-1` has a `joins` entry `{kind: claim, id: claim-1, via: reconciliation, resolved: true}` and appears in `claim-1.review_finding_ids`. |
| X53 | X51. | `evaluation.judge.run_id` `20261027T214351.399Z-75bf` while `evaluation.run.run_id` is `20261027T212706.923Z-179e`; no warning about the difference (§4.2). |
| X54 | lfmu with the opt-in flag. | `run_id` `20261027T212642.530Z-3a86`; review findings 86; the run's contribution review has 2 candidates while `contributions` has 3 (both kept, §4.5 item 9). |
| X55 | A hand-written outputs directory (opt-in flag) over the default fixture with `run.json` (minimal, JR §6.5 skeleton) and `findings.json` holding one finding with `target` `contribution:K9` and evidence `[claim:C9]`; neither ID exists. | Exit `0`; the finding's `joins` `[{kind: contribution, id: K9, via: target, resolved: false}, {kind: claim, id: C9, via: citation, resolved: false}]`; `warnings` names both as unresolved; `judge` `null`. |
| X56 | Hand-written outputs directory (opt-in flag) over the default fixture: `judge.json` with one finding `claim_validators/C1.v1` whose `evidence` is `[claims.yml#C1, results.yml#R1]`; `findings.json` with finding `F1` (evidence `[judge:claim_validators/C1.v1]`, no `target`, no `evidence_details`) and finding `F2` (evidence `[claim:C1]`). | `F1.joins` `[{kind: judge_finding, id: claim_validators/C1.v1, via: citation, resolved: true}]` (no claim or result entry: joins are direct only). `F2.joins` `[{kind: claim, id: C1, via: citation, resolved: true}]`. `claims[0].review_finding_ids` `[F2]`; `claims[0].judge_finding_ids` `[claim_validators/C1.v1]`. |

## 7.6 L3 — static site

| ID | Fixture / action | Expected |
|----|------------------|----------|
| X57 | X1's site served from a sub-path. | `#/overview` shows "Demo"; `#/claims/C1` shows "Accuracy is 0.91." and links to `R1`; following that link shows `R1` with a working link to the CSV. No request leaves the site's origin (verified with the browser's network log). |
| X58 | X26's site. | Every page shows "Derived from the paper by a paper adapter" and `attested`. `#/contributions` shows contribution 4 with "No claims linked". `#/claims/claim-1` shows four contribution links, each with "inferred by the paper adapter's extractor". |
| X59 | X16's site. | `#/claims/C1` shows "inferred by the paper adapter's extractor and inferred by the reviewer"; X17's site shows "inferred (source not recorded)". |
| X60 | X12's site. | `#/contributions` shows "No contribution declaration was provided" and "not evidence that the work makes no contribution". |
| X61 | Default fixture with `README.md` containing `<script>alert(1)</script>`, `<img src=x onerror=alert(1)>`, `[a](javascript:alert(1))`, and `![r](https://example.org/i.png)`. | `#/provenance` renders the README; no script runs; no `onerror` attribute and no `javascript:` link remain in the DOM; no request is made to `example.org`. A claim statement `<b>x</b>` renders as the literal text. |
| X62 | X51's site. | Every page shows "Unsealed analysis". `#/evaluation` shows exactly the three lines "Overall recommendation: unset", "Criterion scores: unset", "Reviewer confidence: unset"; shows `visual_inspection`: `incomplete`; labels judge findings "Judge (deterministic)" and reviewer findings "Reviewer (advisory)"; shows no combined score for any contribution; shows "not yet qualified by a human" for each reviewed candidate; shows the diagnostics block "Contribution declaration checks (structural)" with "Warning, contribution 4: claim support not declared or inferred." |
| X63 | X36's site. | `#/evaluation` shows the run ID in full and `input_digest`; states that no code was executed (`activity` `inspection`); `run/review-draft.md` is reachable from the page. |
| X64 | Any site; route `#/claims/does-not-exist`. | A "not found" notice with a link to the overview. |
| X65 | A contribution with ID `contribution/` + 64 hex digits. | Its route uses the full, percent-encoded ID and resolves; the page shows the full ID. |
| X66 | X26's site, `#/claims/claim-4`; and `#/claims/claim-5`. | `claim-4` shows "page unknown" with no page link and no "page 0"; `claim-5` shows page 6 with a link to the PDF page only if a PDF asset exists (bgpt has none, so plain text). |
| X67 | X24's first site. | The header shows "Untitled" with "title from PDF metadata". X23's site shows "Streaming Parsers" without that label. |
| X68 | X46's site. | Overview and `#/evaluation` show "No review was requested in this run (judge-only)." and "Human-owned assessment: not applicable (no review was requested)."; the three "unset" lines are absent; judge findings are shown; no reviewer finding bucket is shown. |
| X69 | X56's site. | `#/claims/C1` lists `F2` and `claim_validators/C1.v1` but not `F1`; `#/findings/F1` links to `claim_validators/C1.v1`. |
| X70 | X51's site. | `#/evaluation/reconciliation/0` shows reconciliation record 0 with a link to its claim; `#/paper/references/<id>` for the first reference shows that reference's `raw` text. |
| X71 | X36's site. | `#/provenance` shows `S-AI` as the run ID and `J-AI` labeled as the judge's run ID. |

## 7.7 Scenario counts

| Level | Scenarios |
|-------|-----------|
| L1 | X1–X35 (35) |
| L2 | X36–X49 (14) |
| L2 +C | X50–X56 (7) |
| L3 | X57–X71 (15) |
