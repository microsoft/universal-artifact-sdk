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
3. `input_digest`: computed from `inputs` exactly as JR §6.3 specifies. Fixture paths are
   ASCII-only, so the open non-ASCII question of §2.4 does not arise.
4. Write the output files listed (with `run.json.input_provenance` carrying the values of
   steps 2–3), then `outputs`: SHA-256 of each, keyed by run-relative path.
5. Write `manifest.json` with the values listed and the maps from steps 2–4.

**Empty values.** Where this section says a key is *empty*, it means: `null` for a key whose
value is an object or a scalar, `[]` for a key whose value is a list, and, for `run.json.groups`,
an object with the seven JR §6.5 group keys, each `[]`. Every key of the JR skeletons is written;
none is omitted.

**Common values.**

- `manifest.json`: `format_version` `artifact-review-run/v1`, `status` `completed`, `error`
  `null`, `reviewer_version` `fixture/0`, `created_at` `2026-01-01T00:00:00Z`, `options`
  `{model: null, provider: null, reference_lookup_requested: false, reproduction_requested:
  false, visual_page_limit: null}`, `stage_notes` `{}`, `files` `{run: run.json, findings:
  findings.json, draft: review-draft.md, paper_review: paper-review.md}`.
- `run.json`: `_generated` `fixture`; `run_id`, `reviewer_version`, and `configuration` equal to
  the manifest's; `created_at` `2026-01-01T00:00:00Z`; `completed_at` `2026-01-01T00:05:00Z`;
  `input_provenance` with `kind` = scope and `input_digest`, `stages`, `judge`, `artifact_paper`
  equal to the manifest's, other keys empty; `contribution_review` equal to the parsed content of
  `contributions.json` when that file is written, else `null`; `human_owned` all three `null`;
  every other key empty.
- `findings.json`: `{"_generated": "fixture", "run_id": <run_id>, "findings": <list>}` (JR §6.2).
  Scenario-added review findings carry `id` and only the keys the scenario names; the explorer
  copies findings verbatim and MUST NOT require other JR §5.5 keys.
- `judge.json` (when written): `_generated` `fixture`, `format_version` `evaluable-artifact/v3`,
  `run_id` = the judge block's, `generated_at` `2026-01-01T00:01:00Z`, `judge_version`
  `fixture/0`, `rubric` `PARTIAL`, `findings` as listed, `warnings` and
  `contribution_diagnostics` `[]`, every other JR §6.6.1 key `null`. Each listed judge finding
  has the keys named, `message` `fixture`, `display` `{}`, and every other JR §4.2 key `null`.
- `review-draft.md` and `paper-review.md`: the single line `Fixture draft.` (S-JO: `No review was
  requested.`), followed by a newline.
- A file "with status `unavailable`" is `{"_generated": "fixture", "status": "unavailable",
  "reason": "no LLM provider configured"}`. In S-AI and S-PO this includes `contributions.json`,
  so `run.json.contribution_review` is that same object and no "differs" warning (§4.3) arises.
- The paper: any valid PDF file; scenarios that depend on its metadata say so.

| Fixture | `run_id`; scope | Snapshot | Stages (JR §6.4) | Outputs and other values |
|---------|-----------------|----------|------------------|--------------------------|
| **S-AI** artifact-informed, no LLM | `S-AI`; `artifact-informed` | `snapshot/artifact/` = the default fixture; `snapshot/paper/paper.pdf` = its `paper.pdf` | `artifact_checks` `completed`; `reproduction` and `reference_lookup` `not-requested`; every other stage `unavailable` | `paper` `snapshot/paper/paper.pdf`, `artifact_paper` `paper.pdf`; `configuration` `{digest: "fixture"}`; `judge` block `{path: judge.json, run_id: J-AI, judge_version: fixture/0, checks: [claim_validators], activity: inspection, submission_executed: false}`; `judge.json` with one finding `claim_validators/C1.v1` (`check` `claim_validators`, `verdict` `advisory`, `evidence` `[claims.yml#C1, results.yml#R1]`); `findings.json` with `findings: []`; `review-draft.md` and `paper-review.md` one line each; every other file of the artifact-informed row of JR §6.2 with status `unavailable` |
| **S-JO** judge-only | `S-JO`; `artifact-informed` | as S-AI | `artifact_checks` `completed`; every other stage `not-requested` (JR §6.4, judge-only) | as S-AI, except the judge `run_id` is `J-JO`, `configuration` is the judge-only value of JR §6.5, and `run.json.contribution_review` is `null`; `review-draft.md` and `paper-review.md` say "No review was requested."; only the "All" and "Judge-only" rows of JR §6.2 are written |
| **S-PO** paper-only | `S-PO`; `paper-only` | `snapshot/paper/paper.pdf` only | the four artifact stages, `reproduction`, and `reference_lookup` `not-requested`; every other stage `unavailable` | `paper` `snapshot/paper/paper.pdf`, `artifact_paper` `null`, `judge` `null`; `configuration` `{digest: "fixture"}`; `findings.json` with `findings: []`; files of the paper-only row of JR §6.2 with status `unavailable` |

Scenarios that change a fixture re-seal it, unless the scenario is about a broken seal: a change
to an output file only (for example an added finding) re-runs steps 4–5; a change to any
snapshot file (for example an added contribution in the artifact) re-runs steps 2–5, which also
changes `input_digest` and `run.json.input_provenance`.

## 7.4 L1 — data model

| ID | Fixture / action | Expected |
|----|------------------|----------|
| X1 | Default fixture; build. | Exit `0`. `data.json` has every key of §3.2; `schema` is `artifact-explorer/data/v1`; `identity.id` `demo`; `counts.claims` `1`; `claims[0].result_ids` `[R1]`; `results[0].evidence` `evidence/metrics.csv`; `results[0].evidence_asset.url` `assets/evidence/metrics.csv`, and that file exists in the output with identical bytes; `evaluation` `null`; `warnings` `[]` (undeclared, absent default indexes such as `exhibits.yml` are silent, §2.3). |
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
| X18 | X15 with `claim_link_sources` replaced by legacy `claim_links: {kind: extractor-inference, method: contribution-digest/v1}`. | `sources` `[reviewer-inference]` (the legacy form is always reviewer-inference, JR §5.13.2). |
| X19 | X15 plus `supporting_claims: [C1]`. | `link_basis` `declared`; `inferred_claims` `[]` (declared wins). |
| X20 | Claim `C1` carries `contributions: [K1]` and the claims index carries a `contribution_links` object; K1 has no `inferred_supporting_claims`. | No inferred link (`claims[0].inferred_contribution_links` `[]`); the claim's `extra.contributions` is `[K1]` (§3.5.1). |
| X21 | X15 plus a claims-index key `contribution_links: {provenance: reviewer-inference, method: m/v1}`. | `sources` still `[extractor-inference]`; no key of `data.json` carries `contribution_links` (§3.5.1). |
| X22 | `C1.paper_ref` is `{page: 0, section: "4"}`; separately `{section: "4"}`; separately `{page: "6"}`. | `claims[0].paper_location.page` `null` each time (page unknown); `section` `"4"` in the first two; `claims[0].paper_ref` keeps the original value (`page: 0` in the first case). |
| X23 | Default fixture plus `paper: {pdf: paper.pdf, source: paper.tex}`, `paper.tex` containing `\title{Streaming Parsers}`, and `paper.pdf` with document-metadata title `Untitled`. | `paper.title` `Streaming Parsers`; `paper.metadata_title` `Untitled`; `identity.display_title` `Streaming Parsers`; `display_title_source` `paper-source`. |
| X24 | X23 without `paper.tex` (and without `source`); separately with a metadata title of only spaces. | First: `display_title` `Untitled`, `display_title_source` `pdf-metadata`. Second: `display_title` `Demo`, `display_title_source` `manifest-title`, `paper.metadata_title` `null`. |
| X25 | Default fixture plus a root `related_work.yml` (top-level `related_work`, one entry) declared as `paths.related_work`. | `data.json` has no `related_work` key and `counts` has no `related_work` entry; the file is not copied; no warning is required. |
| X26 | bgpt `artifact/`; build. | `counts`: `claims` 20, `contributions` 6, `results` 38, `references` 58, `experiments` 0. Claims in file order (`claim-1`, `claim-2`, `claim-3`, `claim-5`, `claim-17`, `claim-4`, …, `claim-21`). `identity.display_title` `Beyond Language Models: Byte Models are Digital World Simulators` (`manifest-title`). `claim-4.paper_location.page` `6`; `claim-3.paper_location.page` `1`. `contributions[3].link_basis` `none`. `claim-1` has 4 inferred links, each with `sources` `[extractor-inference]`. `paths.figures` declared but no file: `figures` `[]` and a warning (no probe). `paper.pdf` `null` (declared, absent). `identity.origin.kind` `paper`. |
| X27 | lfmu `artifact/`; build. | `identity.title` `paper`; `identity.display_title` `paper` with `display_title_source` `manifest-title` (the example ships no paper file); `counts.claims` 9; `counts.contributions` 3; `counts.results` 54. |
| X28 | Default fixture plus `manifest.producer: {tool: x, anything: [1, 2]}` and an unknown claim field `foo: bar`. | `identity.producer` copied verbatim; `claims[0].extra` `{foo: bar}`. |
| X29 | Output directory equal to the artifact directory; separately inside it. | Exit `2`; nothing written. |
| X30 | Output directory exists and holds `keep.txt`; build without, then with, the explicit replace option. | Without: exit `2`, `keep.txt` untouched. With: exit `0`, `keep.txt` gone. An existing empty output directory is used without the option. |
| X31 | `C1` has `added: 2026-10-27`, `score: .nan`, and `notes: {1: a}`. | `claims[0].extra` `{added: "2026-10-27", notes: {"1": "a"}, score: "nan"}`. |
| X32 | `C1` has `stance: maybe` and `validators: [{id: v1, kind: builtin, name: monotonic, validation_mode: re-analyze, inputs: [R1]}]`; the manifest has root keys `_generated: x` and `source_format: latex`; the references export holds `{id: r1, raw: "A. B. 2020.", title: T, year: 2020}`. | `claims[0].stance` `maybe` with a warning; `claims[0].validators` `[{id: v1, kind: builtin, name: monotonic, gated_by: null, validation_mode: re-analyze, extra: {inputs: [R1]}}]`; `identity.extra` `{source_format: latex}` (no `_generated`); `references[0].extra` `{title: T, year: 2020}`. |
| X33 | `README.md` contains `![p](img/p.png)` and `![q](img/missing.png)`; `img/p.png` exists. | `readme.embedded` `{"img/p.png": {path: img/p.png, url: assets/img/p.png, kind: image}, "img/missing.png": null}`; `assets/img/p.png` is written. |
| X34 | `paper: {source: tex}` where `tex/` holds `main.tex` with `\title{Streaming Parsers}`; separately an empty `tex/`. | First: `paper.source.path` `tex/main.tex`; `paper.declared.source` `tex`; `paper.title` `Streaming Parsers`. Second: `paper.source` `null` and a warning. |
| X35 | No `paths.figures` and no `paths.exhibits`; `exhibits.yml` at its default name with `E1` (`type: figure`, `path: fig/a.png`, file present) and `E2` (`type: table`). Separately: `paths.exhibits: ex.yml` declared, `ex.yml` absent, and `figures/b.png` present. | First: `figures` has one entry, `id` `E1`, `path` `fig/a.png`, `path_asset.url` `assets/fig/a.png`; `exhibits[0].path` `fig/a.png` and `exhibits[0].path_asset` set. Second: `figures` `[]`, a warning naming `ex.yml`, and no figure from `figures/b.png` (no probing when an exhibits index is declared). |
| X36 | `R1.evidence` is `evidence/a b#1.csv`; separately `evidence/é.csv`; each file present. | `results[0].evidence_asset.url` `assets/evidence/a%20b%231.csv` (the file is written at `assets/evidence/a b#1.csv`); second: `assets/evidence/%C3%A9.csv`. Following either URL in the site loads the file. |
| X37 | `C1` has `checked: 2026-10-27 21:40:00`, `seen: 2026-10-27T23:40:00.500+02:00`, and `notes: {true: a, 1.0: b, null: c}`. | `claims[0].extra.checked` `"2026-10-27T21:40:00Z"`; `seen` `"2026-10-27T21:40:00.5Z"`; `notes` `{"1.0": "b", "null": "c", "true": "a"}`. |
| X38 | `README.md` with: `![a](./img/p.png)`, `[b](img/../img/p.png#s)`, `` `![c](img/q.png)` `` (a code span), `<img src="img/q.png">` (raw HTML), a reference definition `[r]: img/p.png`, `![d](https://example.org/x.png)`, and `![e](../../x.png)`; `img/p.png` and `img/q.png` exist. | `readme.embedded` has exactly the keys `./img/p.png`, `img/../img/p.png#s`, `img/p.png`, `https://example.org/x.png`, `../../x.png`; the first three map to the asset reference of `img/p.png`; the last two are `null`. `img/q.png` is not copied. |
| X39 | Figures index (`paths.figures`) with `{id: F1, path: fig/a.png, claims: [C1]}` and `R1.evidence: fig/a.png`; the file is present. | `figures[0].claim_links` `[{claim_id: C1, method: declared}, {claim_id: C1, method: adapter-suggested}]`. |
| X40 | An assessments index whose one assessment declares `evidence: [evidence/metrics.csv, missing.csv]`. | `assessments[0].evidence` kept; `assessments[0].evidence_asset` is a two-element list: the asset reference of `evidence/metrics.csv`, then `null`. |
| X41 | Claims index with two claims both `id: C1` (statements "A" then "B"). | Both kept in order with a warning naming `C1`; `claims[0].result_ids` `[R1]`, `claims[1].result_ids` `[]`; `#/claims/C1` (L3) shows "A". |

## 7.5 L2 — run overlay

| ID | Fixture / action | Expected |
|----|------------------|----------|
| X42 | S-AI; build with the run only. | Exit `0`. `evaluation.run.sealed` `true`; `run_id` `S-AI`, `scope`, `input_digest` equal the manifest's; `completed_at` `2026-01-01T00:05:00Z` (from `run.json`); `evaluation.judge.rubric` `PARTIAL`; `evaluation.judge.run_id` `J-AI`; `evaluation.review.human_owned` all `null`; `identity.id` `demo` (read from `snapshot/artifact/`). |
| X43 | X42 with one byte of `findings.json` changed. | Exit `2` (JR §6.7 rule 2); nothing written; the message names `findings.json`. |
| X44 | X42 with `status: failed` in the manifest; separately with `manifest.json` removed. | Exit `2` both times. |
| X45 | X42 plus the artifact directory as a second input. | Exit `2` (§1.2). |
| X46 | X42 with an extra file `notes.txt` in the run directory, not in `outputs`. | Exit `0`; `notes.txt` is not read and not copied. |
| X47 | X42. | Judge finding `claim_validators/C1.v1` has `joins` `[{kind: claim, id: C1, via: evidence-anchor, resolved: true}, {kind: result, id: R1, via: evidence-anchor, resolved: true}]`; `claims[0].judge_finding_ids` and `results[0].judge_finding_ids` are `[claim_validators/C1.v1]`. No key on `claims[0]` holds a verdict. |
| X48 | S-PO. | Exit `0`; `identity.id` `null`; `claims` `[]`; `paper.declared` `{pdf: snapshot/paper/paper.pdf, source: null}`; `paper.pdf.url` `run/snapshot/paper/paper.pdf`; `paper.source` `null`; `evaluation.judge` `null`. |
| X49 | X42 where `contributions.json` and `run.json.contribution_review` differ. | `evaluation.review.contribution_review` equals `contributions.json`; `warnings` notes the difference. |
| X50 | S-AI with `findings.json` holding, written by hand: `F1` with `target` `C1`, `evidence` `[judge:claim_validators/C1.v1]`, and its own `judge_finding_ids` `[claim_validators/C1.v1]`; `F2` with only `evidence` `[judge:claim_validators/C1.v1]`; re-sealed. | `F1.joins` `[{kind: claim, id: C1, via: target, resolved: true}, {kind: judge_finding, id: claim_validators/C1.v1, via: citation, resolved: true}, {kind: judge_finding, id: claim_validators/C1.v1, via: judge-ref, resolved: true}]`; `F1.judge_finding_ids` is still exactly the copied `[claim_validators/C1.v1]`. `F2.joins` has only the `judge_finding` entry (`via` `citation`); `claims[0].review_finding_ids` `[F1]`. |
| X51 | X42 where a copied run file is changed after validation and before copy (simulated); separately, a snapshot artifact file (`snapshot/artifact/evidence/metrics.csv`). | Exit `2` both times; no partial site. |
| X52 | S-JO. | Exit `0` (the run passes JR §6.7 like any other). `evaluation.run.judge_only` `true`; `evaluation.judge` present with `rubric` equal to `judge.json.rubric`; `evaluation.review` `null`; `run/review-draft.md` copied. |
| X53 | X42 (not judge-only). | `evaluation.run.judge_only` `false`; `evaluation.review` present even though no LLM provider was used (`paper_review` `unavailable`). |
| X54 | S-AI with the artifact also declaring contribution `K1`, and `findings.json` holding findings with `target`: `F3` `abstract`, `F4` `K1`, `F5` `contribution:K9`, `F6` `claim: overstated`, `F7` `""`, `F8` `claim_validators/C1.v1`, `F9` `Table 3 / Section 5.2.2`; re-sealed (steps 2–5). | `F3.joins` `[]`, `F7.joins` `[]`, `F9.joins` `[]`, and no warning mentions `F3`, `F7`, or `F9`. `F4.joins` `[{kind: contribution, id: K1, via: target, resolved: true}]`; `contributions[0].review_finding_ids` `[F4]`. `F5.joins` `[{kind: contribution, id: K9, via: target, resolved: false}]` and a warning names `K9`. `F6.joins` `[]` and a warning names `F6` (malformed reference). `F8.joins` `[{kind: judge_finding, id: claim_validators/C1.v1, via: target, resolved: true}]`. |
| X55 | S-AI with `findings.json` holding `F5` with `evidence` `[artifact:evidence/metrics.csv, artifact:missing.txt]`, and `run.json.synthesis.contribution_evidence` `[artifact:evidence/metrics.csv#L2]` (other synthesis keys empty); re-sealed. | `evaluation.citation_assets["artifact:evidence/metrics.csv"].url` `assets/evidence/metrics.csv`; `["artifact:missing.txt"]` `null`; `["artifact:evidence/metrics.csv#L2"].url` `assets/evidence/metrics.csv`. |
| X56 | S-AI with `review-draft.md` containing `![v](visuals/p1.png)` and `![w](visuals/p2.png)`; `visuals/p1.png` written and listed in `outputs`, `visuals/p2.png` present in the run directory but not listed; re-sealed. | `run/visuals/p1.png` is copied and `evaluation.run.files.draft.embedded["visuals/p1.png"].url` is `run/visuals/p1.png`; `["visuals/p2.png"]` `null`; `p2.png` is not read or copied. |
| X57 | S-AI plus a references export holding `{id: r1, raw: x}`; `judge.json.reference_check` `null`; an output `reference-check.json` with `available: true`, `resolver: fixture`, verdict `{id: r1, status: verified}`, and `counts`; re-sealed (steps 2–5). | `evaluation.judge.reference_check.available` `true`; `references[0].check.status` `verified`. |
| X58 | S-AI with one snapshot file renamed to `snapshot/artifact/evidence/é.csv` (and `R1.evidence` changed to match), sealed twice: once with `input_digest` over the literal UTF-8 serialization, once over the `\u00e9`-escaped one. | Exit `0` both times (§2.4). A third copy with an `input_digest` matching neither: exit `2`. |

**L2 +C (mode C).**

| ID | Fixture / action | Expected |
|----|------------------|----------|
| X59 | bgpt: artifact `bgpt/artifact`, outputs `bgpt/` without the opt-in flag. | Exit `2`. |
| X60 | Same with the opt-in flag. | Exit `0`. `evaluation.run.sealed` `false`; `run_id` `20261028T213946.517Z-1083`; `input_digest` equals `run.json.input_provenance.input_digest`; `status`, `options`, `stage_notes` `null`; `stages.visual_inspection` `incomplete`. `evaluation.judge.rubric` `PARTIAL`; `badges` all `unverifiable`. `contribution_diagnostics` is the judge's single entry, path `contributions[3].supporting_claims`, severity `warning`. `evaluation.review.findings` has 129 entries; `evaluation.judge.findings` has 36. |
| X61 | X60. | Judge finding `claim_validators/claim-4.v1` has a `joins` entry `{kind: claim, id: claim-4, via: evidence-anchor, resolved: true}` and `result` entries for `R9`, `R10`, `R11`, `R40`, `R41`, `R44`, `R45`, `R46`, in that order; `claim-4.judge_finding_ids` contains it and `R9.judge_finding_ids` contains it. The comparison finding whose `evidence_details.claim_id` is `claim-1` has a `joins` entry `{kind: claim, id: claim-1, via: reconciliation, resolved: true}` and appears in `claim-1.review_finding_ids`. |
| X62 | X60. | `evaluation.judge.run_id` `20261028T215337.690Z-e243` while `evaluation.run.run_id` is `20261028T213946.517Z-1083`; no warning about the difference (§4.2). |
| X63 | lfmu with the opt-in flag. | `run_id` `20261028T213907.918Z-9102`; review findings 100; judge findings 25; `evaluation.judge.contribution_diagnostics` `[]`. `evaluation.review.contribution_review` equals `contributions.json` as copied (its `declarations` in file order), and `contributions` equals the artifact's 3 records unchanged; the two lists are kept separately and neither is rewritten from the other, whatever their IDs and `derived_from` values (§4.5 item 9). |
| X64 | A hand-written outputs directory (opt-in flag) over the default fixture with `run.json` (minimal, JR §6.5 skeleton) and `findings.json` holding one finding with `target` `contribution:K9` and evidence `[claim:C9]`; neither ID exists. | Exit `0`; the finding's `joins` `[{kind: contribution, id: K9, via: target, resolved: false}, {kind: claim, id: C9, via: citation, resolved: false}]`; `warnings` names both as unresolved; `judge` `null`. |
| X65 | Hand-written outputs directory (opt-in flag) over the default fixture: `judge.json` with one finding `claim_validators/C1.v1` whose `evidence` is `[claims.yml#C1, results.yml#R1]`; `findings.json` with finding `F1` (evidence `[judge:claim_validators/C1.v1]`, no `target`, no `evidence_details`) and finding `F2` (evidence `[claim:C1]`). | `F1.joins` `[{kind: judge_finding, id: claim_validators/C1.v1, via: citation, resolved: true}]` (no claim or result entry: joins are direct only). `F2.joins` `[{kind: claim, id: C1, via: citation, resolved: true}]`. `claims[0].review_finding_ids` `[F2]`; `claims[0].judge_finding_ids` `[claim_validators/C1.v1]`. |

## 7.6 L3 — static site

| ID | Fixture / action | Expected |
|----|------------------|----------|
| X66 | X1's site served from a sub-path. | `#/overview` shows "Demo"; `#/claims/C1` shows "Accuracy is 0.91." and links to `R1`; following that link shows `R1` with a working link to the CSV. No request leaves the site's origin (verified with the browser's network log). |
| X67 | X26's site. | Every page shows "Derived from the paper by a paper adapter" and `attested`. `#/contributions` shows contribution 4 with "No claims linked". `#/claims/claim-1` shows four contribution links, each with "inferred by the paper adapter's extractor". |
| X68 | X16's site. | `#/claims/C1` shows "inferred by the paper adapter's extractor and inferred by the reviewer"; X17's site shows "inferred (source not recorded)". |
| X69 | X12's site. | `#/contributions` shows "No contribution declaration was provided" and "not evidence that the work makes no contribution". |
| X70 | Default fixture with `README.md` containing `<script>alert(1)</script>`, `<img src=x onerror=alert(1)>`, `[a](javascript:alert(1))`, and `![r](https://example.org/i.png)`. | `#/provenance` renders the README; no script runs; no `onerror` attribute and no `javascript:` link remain in the DOM; no request is made to `example.org`. A claim statement `<b>x</b>` renders as the literal text. |
| X71 | X60's site. | Every page shows "Unsealed analysis". `#/evaluation` shows exactly the three lines "Overall recommendation: unset", "Criterion scores: unset", "Reviewer confidence: unset"; shows `visual_inspection`: `incomplete`; labels judge findings "Judge (deterministic)" and reviewer findings "Reviewer (advisory)"; shows no combined score for any contribution; shows "not yet qualified by a human" for each reviewed candidate; shows the diagnostics block "Contribution declaration checks (structural)" with "Warning, contribution 4: claim support not declared or inferred." |
| X72 | X42's site. | `#/evaluation` shows the run ID in full and `input_digest`; states that no code was executed (`activity` `inspection`); `run/review-draft.md` is reachable from the page. |
| X73 | Any site; route `#/claims/does-not-exist`. | A "not found" notice with a link to the overview. |
| X74 | A contribution with ID `contribution/` + 64 hex digits. | Its route uses the full, percent-encoded ID and resolves; the page shows the full ID. |
| X75 | X22's site (first case), `#/claims/C1`; and X26's site, `#/claims/claim-4`. | `C1` shows "page unknown" with no page link and no "page 0"; `claim-4` shows page 6 as plain text, because a page links to the PDF only when a PDF asset exists and bgpt ships none. |
| X76 | X24's first site. | The header shows "Untitled" with "title from PDF metadata". X23's site shows "Streaming Parsers" without that label. |
| X77 | X52's site. | Overview and `#/evaluation` show "No review was requested in this run (judge-only)." and "Human-owned assessment: not applicable (no review was requested)."; the three "unset" lines are absent; judge findings are shown; no reviewer finding bucket is shown. |
| X78 | X65's site. | `#/claims/C1` lists `F2` and `claim_validators/C1.v1` but not `F1`; `#/findings/F1` links to `claim_validators/C1.v1`. |
| X79 | X60's site. | `#/evaluation/reconciliation/0` shows reconciliation record 0 with a link to its claim; `#/paper/references/<id>` for the first reference shows that reference's `raw` text. |
| X80 | X42's site. | `#/provenance` shows `S-AI` as the run ID and `J-AI` labeled as the judge's run ID. |

## 7.7 Scenario counts

| Level | Scenarios |
|-------|-----------|
| L1 | X1–X41 (41) |
| L2 | X42–X58 (17) |
| L2 +C | X59–X65 (7) |
| L3 | X66–X80 (15) |
