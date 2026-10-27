# Example review: Beyond Language Models: Byte Models are Digital World Simulators

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

- Paper: Shangda Wu, Xu Tan, Zili Wang, Rui Wang, Xiaobing Li, Maosong Sun. *Beyond Language Models: Byte Models are Digital World Simulators.* arXiv:2402.19155v1,
  <https://arxiv.org/abs/2402.19155v1>. Licensed
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). PDF SHA-256
  `999e3d81d95ab455856fdbf602d48a8f6433568e19413dae1589b372f83d7b81` (spec §8.7 conformance paper `bgpt`).
- Path: the paper adapter (spec §3) converted the PDF to an attested, paper-only evaluable
  artifact (`artifact/`); the judge (§4) and the reviewer (§5) then ran in the
  `artifact-informed` scope with an LLM provider. Run `20261026T230005.218Z-5e8a`.

## Files

| File | What it is |
|------|------------|
| `review-draft.md` | The review draft a human reviewer would start from (§5.12) |
| `paper-review.md` | The paper-review section on its own |
| `findings.json` | Reviewer findings with paper citations (§5.5) |
| `judge.json` | Deterministic judge result: findings, verdicts, rubric (§4) |
| `contributions.json` | Advisory assessment of the paper's contributions |
| `run.json` | Run record: stages, configuration, human-owned fields (§6) |
| `artifact/` | The adapter's output: `manifest.yml`, `claims.yml`, `results.yml`, `contributions.yml`, `paper_references.yml` |

## Changes made for publication

- A disclaimer banner was added to the top of `review-draft.md` and `paper-review.md`.
- The paper PDF, page images, and figure crops are omitted; download the paper from arXiv.
- Raw model responses, the evidence packet, intermediate coverage files, the human-decision
  file, and the sealed run manifest (`manifest.json`) are omitted. Because files were edited and
  omitted, this copy is **not** a sealed run and will not pass §6 seal verification.
- The LLM provider and model identifiers are replaced with `redacted-provider` and
  `redacted-model`; tool names are replaced with `reference-reviewer` and `reference-judge`;
  local paths are replaced with relative ones; an internal build hash is removed from version
  strings. Nothing else was changed.
