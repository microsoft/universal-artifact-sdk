# Example review: Loss-Free Machine Unlearning

> [!WARNING]
> **Experimental, AI-generated example. No human judgement.** This review was produced
> automatically by an experimental reference implementation of the judge/reviewer
> specification. No person reviewed, edited, or endorsed it. It does not represent the
> opinion of the SDK maintainers, Microsoft, or any reviewer, and it is not an assessment of
> the paper or its authors. It may contain errors. It is published only to show what the
> tool's output looks like.


> **Audience**: Readers of the judge/reviewer specification who want to see real output.
> **Source of truth for**: Nothing normative; this is an illustrative example. The
> specification in [`docs/judge-reviewer-spec/`](../../../judge-reviewer-spec/README.md) governs.

A reference implementation of `artifact-judge-reviewer/v1`
produced this review automatically from the paper alone. No human reviewer has edited or
endorsed it. The recommendation, scores, and confidence are deliberately `unset`: they belong
to a human reviewer. The review says nothing about the authors' views and is not an
assessment by the SDK maintainers.

## Input

- Paper: Jack Foster, Stefan Schoepf, Alexandra Brintrup. *Loss-Free Machine Unlearning.* arXiv:2402.19308v1,
  <https://arxiv.org/abs/2402.19308v1>. Licensed
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). PDF SHA-256
  `005179f8c64043b9c7e0b5f3d3b642d4c6a482806328554a153659434b50ce50` (spec §8.7 conformance paper `lfmu`).
- Path: the paper adapter (spec §3) converted the PDF to an attested, paper-only evaluable
  artifact ([`artifact/`](artifact/)); the judge (§4) and the reviewer (§5) then ran in the
  `artifact-informed` scope with an LLM provider. Run `20261027T212642.530Z-3a86`.

## Where to start

- **Judge result:** [`judge-summary.md`](judge-summary.md) shows the overall rubric, each
  claim with its evidence and verdict, and every check, in one short page.
- **Review:** [`review-draft.md`](review-draft.md) is long because it lists every finding with
  its quotes. Read it by section rather than top to bottom:

1. [Questions for the authors](review-draft.md#questions-for-the-authors): Start here: concrete questions, each quoting the page it is about.
2. [Decision-critical concerns](review-draft.md#decision-critical-concerns): Issues that could change a decision, with their evidence.
3. [Reasons to accept](review-draft.md#reasons-to-accept): Strengths, each tied to the paper.
4. [Contributions](review-draft.md#contributions): What the paper claims to contribute, and how well each is supported.
5. [Additional improvements (non-blocking)](review-draft.md#additional-improvements-non-blocking): Smaller fixes that would not change a decision.
6. [Evidence to examine (advisory)](review-draft.md#evidence-to-examine-advisory): Long list of specific passages a reviewer may want to check.
7. [Direct visual evidence (advisory)](review-draft.md#direct-visual-evidence-advisory): Observations from page images, linked to the images in `visual/`.
8. [Review scope and coverage](review-draft.md#review-scope-and-coverage): What was and was not examined.

## Why there are two review files

The spec (§5.12) requires two renderings of the same findings:

- [`review-draft.md`](review-draft.md) is the **complete** draft for the human reviewer. It adds
  the evidence lists, the visual audit, and the artifact and coverage sections.
- [`paper-review.md`](paper-review.md) is the **paper-facing subset**: only the sections that
  could be shared with authors (sections 1–11 of the draft, without artifact sections or
  coverage notes). Every section in it also appears in `review-draft.md`.

## Files

| File | What it is |
|------|------------|
| [`judge-summary.md`](judge-summary.md) | Readable summary of `judge.json` with the claims and results (generated for this example; not a spec output) |
| [`review-draft.md`](review-draft.md) | Complete review draft for the human reviewer (§5.12) |
| [`paper-review.md`](paper-review.md) | Paper-facing subset of the draft (§5.12) |
| [`findings.json`](findings.json) | All reviewer findings with paper citations (§5.5) |
| [`judge.json`](judge.json) | Deterministic judge result: findings, verdicts, rubric (§4, §6.6) |
| [`contributions.json`](contributions.json) | Advisory review of the paper's contributions (§5.13.4) |
| [`visual-integration.json`](visual-integration.json) | How page-image observations were folded into the findings (§5.9) |
| [`artifact-reconciliation.json`](artifact-reconciliation.json) | Literal checks of claims against linked artifact evidence (§5.10.2) |
| [`artifact-visual-coverage.json`](artifact-visual-coverage.json) | Which artifact figures were inspected (§5.10.3) |
| [`run-evidence.json`](run-evidence.json) | Evidence from the artifact's own run records, if any (§5.10.4) |
| [`run.json`](run.json) | Run record: stages, configuration, human-owned fields (§6.5) |
| [`visual/`](visual/) | The 7 page images the review cites as `review-output:visual/…` |
| [`artifact/`](artifact/) | The adapter's output: `manifest.yml`, `claims.yml`, `results.yml`, `contributions.yml`, `paper_references.yml` |

## Changes made for publication

- A disclaimer banner was added to the top of every Markdown file.
- `judge-summary.md` and this README were added; they are not run outputs.
- Citations of the form `review-output:visual/…` in the Markdown files were turned into links
  to the images in `visual/`. Only cited page images are included.
- The paper PDF and uncited page images are omitted; download the paper from arXiv.
- Omitted run files: the raw model responses, the evidence packet
  (`evidence-packet.json`), page-level visual coverage (`visual-coverage.json`), the
  human-decision file, and the sealed run manifest (`manifest.json`). Because files were edited
  and omitted, this copy is **not** a sealed run and will not pass §6 seal verification.
- The LLM provider and model identifiers are replaced with `redacted-provider`,
  `redacted-model`, and `redacted-verifier-model`; tool names are replaced with `reference-reviewer` and `reference-judge`;
  local paths are replaced with relative ones; an internal build hash is removed from version
  strings. Nothing else was changed.
