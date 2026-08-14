# Motivation

> **Companion to [`SPEC.md`](SPEC.md).** `SPEC.md` defines *what* the SDK emits and *how*; this
> document explains *why* the SDK exists and the principles behind its shape. It is distilled from a
> broader position paper on making artifact evaluation agent-friendly (see [References](#references)).

## The problem

Research artifacts were designed for an all-human world. A reviewer — human **or** automated — still
has to *infer* an artifact's structure from prose, hunt for "the evidence for claim X," and scrape
"the number for claim Y" out of a PDF. As research is increasingly produced *with* AI agents, that
per-submission guesswork is the bottleneck: today's best agents reproduce published results in only
~20–30% of cases [[6]](#references) [[7]](#references), and unstructured artifacts make that gap
hard to even *see*.

The facts a reviewer needs — where an experiment lives, which output backs which claim, what number
a table cell came from, the container it ran in — are **already in hand at production time**. They
are only lost because the producing toolchain flattens them into prose that a consumer must later
reverse-engineer.

## Goals

- **Deterministic-first, human-authoritative.** Maximize the share of review that can be settled
  *deterministically* — re-executing pipelines, recomputing reported numbers, checking that every
  claim resolves to declared evidence — and leave the rest to human judgment. A failed deterministic
  check is an **auditable signal**, not an opinion.
- **Tool-agnostic consumer; no verdict from a model.** A *consumer* of these declarations is anything
  that reads them — a human reviewer, a script, a CI job, or an agent. Verdicts come from
  **deterministic checks** or **the human**; if a model is used at all, it is an optional aid for
  summarization and triage and **never issues a verdict**. The value of the declarations does not
  depend on any one tool.
- **Verify to the strength the evidence allows.** Verification is graded, not a binary re-run:
  **re-executed / re-analyzed** (a runnable experiment — strongest) → **evidence-supported** (the
  artifact ships the dataset, output, derivation, or proof the claim points to; checked without
  execution) → **attested** (a documented qualitative analysis or design rationale a human judges,
  grounded in a locatable artifact). All are first-class, and **"unverifiable" is distinct from
  "failed."**
- **Serve more than experiments.** The same backbone serves **analysis papers, qualitative studies,
  and design/systems work**: the common invariant is *every claim resolves to locatable evidence in
  the artifact*, verified as strongly as its evidence allows.
- **Machine-legible by construction.** Structure the artifact so any consumer can parse content, run
  code where applicable, and retrieve each claim's evidence without per-submission heuristics.
- **Additive and backward compatible — never a flag day.** Every declaration is optional. A consumer
  prefers it when present and falls back to today's prose/PDF when absent. Absence is **advisory**,
  never an automatic failure.
- **Defensible by construction.** Every declaration maps onto **recognized, published practice**
  (see [References](#references)) — never an ad-hoc or model-invented notion of a "good artifact."

## The approach: the producer emits the format

The cleanest way to get machine-readable declarations is **not** to ask authors to hand-write
manifests, but to have the producing toolchain emit them through a **small typed authoring API**:

```
create artifact → add environment / dataset / experiment / result / claim / trace / paper → write
```

Because the producer already holds these facts, a typed API records them as a **byproduct** of
production and writes a version-stamped, self-describing submission. Producers that don't adopt the
API can ship the *same declarations* as additive manifest files by hand — a consumer treats either
form identically.

Two principles keep the model honest:

- **Claims are paper-grounded, not author-curated.** The claims under review are the ones the
  **paper** makes. A declared claim→evidence map is the author's *answer key*; a consumer reconciles
  it against claims extracted from the paper and treats any claim with no resolvable evidence as a
  first-class `unverifiable` finding, never a silent pass.
- **Vendor-neutral.** The API and the format it emits carry no venue-, tool-, or producer-specific
  assumptions. A producer's own metadata belongs in open, extensible blocks — not in first-class
  fields.

### Related agent-native work

[Ara (Agent-Native Research Artifacts)](https://github.com/ARA-Labs/Agent-Native-Research-Artifact)
is closely related, convergent work. Ara organizes research artifacts into scientific logic,
executable code and operational specifications, an exploration graph that preserves failures and
pivots, and evidence grounding claims in raw outputs [[9]](#references). Those layers correspond
conceptually to this SDK's paper-grounded claims and validators, experiments and environments,
retained experiment dispositions and provenance journal, and claim-to-result or claim-to-exhibit
bindings.

The systems have different scopes. Ara is a broader protocol and toolkit for managing, compiling,
reviewing, and extending agent-native research. This SDK is a small, vendor-neutral producer-side
typed API and canonical interchange contract. It deliberately does not review, score, or badge
artifacts: deterministic checks may produce machine verdicts, model-based inspection remains
advisory, and humans retain authority. Its evidence-relative validation model also covers research
beyond computational experiments. The conceptual overlap does not imply schema equivalence,
protocol implementation, or compatibility; those would require a separate mapping and conformance
analysis.

## What an artifact declares (the shape)

Whether emitted by the API or written as manifests, the essentials are:

| Priority | Declaration | Why review needs it |
|----------|-------------|---------------------|
| **P0** | **Experiments** (where applicable) — per experiment: a stable id, its location, the command/entrypoint, inputs, labeled expected outputs, dependencies. | Lets a consumer *enumerate* runnable experiments and locate each one's script + outputs deterministically. Papers with no experiments simply declare none. |
| **P0** | **Claim → evidence map** — each paper claim bound to what backs it: an experiment + output + expected outcome, *or* a dataset/derivation/proof, *or* a documented analysis. | Makes "do the artifact's contents support the paper's claims?" a locatable, checkable step, and surfaces omitted claims as coverage gaps. |
| **P0** | **Paper in extractable form** — the paper's `source` (LaTeX/Markdown) and/or a compiled `pdf` (at least one), optionally with a structured claims/results export. | Only if the paper's claims and numbers are machine-readable can a consumer reconcile them against what the author declared; a PDF alone forces lossy scraping. |
| **P1** | **Evidence + reported numbers** — shipped results in (or declared as) a structured form, each headline number tied to the file/cell it came from. | Turns "paper's number == produced number" from a fragile scrape into a deterministic lookup-and-compare. |
| **P1** | **Curated, pinned environment** — a single-root curated artifact (no raw workspace, no leaked paths), a digest-pinned base image, locked dependencies, seeds. | Re-running deterministically needs a buildable, pinned environment; raw-workspace dumps and floating dependencies defeat reproduction. |
| **P2** | **Governance** — a format-version stamp, an SPDX license, externalized large data (url + size + checksum), and a checksum/provenance manifest. | Lets the format evolve safely, unlocks the **Available** badge, and underpins trust that the evaluated artifact is the one the results came from. |

> **Start with the three P0 items** — they unblock the core claim-verification verdicts; everything
> else follows additively. Exact field names are defined in [`SPEC.md`](SPEC.md); the point is the
> *shape*: a declared, resolvable fact in place of a heuristic.

## Scope of this SDK

This SDK is the **producer side** only: a typed authoring binding that emits a conforming
`evaluable-artifact/v2` submission. It does **not** review, score, or badge an artifact — that is a
downstream *consumer's* job, and by design verdicts come from deterministic checks or a human, never
from a model. The declarations here are meant to *strengthen* the badge checklists venues already
award (e.g. ACM **Available / Functional / Reproduced** [[2]](#references)), not to replace them.

## Authors

Chad Atalla, Lef Ioannidis, Nick Pangakis, Tyler Sorensen, Hannah Washington,
Ben Zorn.

## Acknowledgements

We thank Jenn Wortman Vaughan for her valuable input and feedback.

## References

The SDK's design is grounded in established artifact-evaluation standards and the emerging
agent-native-artifact literature:

1. ACM CAIS 2026 — Artifact Evaluation call & process. <https://sysartifacts.github.io/cais2026/>
2. ACM, *Artifact Review and Badging v1.1*. <https://www.acm.org/publications/policies/artifact-review-and-badging-current>
3. NISO RP-31-2021, *Reproducibility Badging and Definitions*. <https://www.niso.org/standards-committees/reproducibility-badging>
4. ML Reproducibility Checklist (Pineau *et al.*). <https://www.cs.mcgill.ca/~jpineau/ReproducibilityChecklist.pdf>
5. de Halleux *et al.*, *Repositories are Human-Agent Knowledge Factories*, SIGPLAN Blog, 2026. <https://blog.sigplan.org/2026/04/21/repositories-are-human-agent-knowledge-factories/>
6. Siegel *et al.*, *CORE-Bench*, 2024. <https://arxiv.org/abs/2409.11363>
7. Hu *et al.*, *REPRO-Bench*, 2025. <https://arxiv.org/abs/2507.18901>
8. SIGPLAN — Review Policies (<https://www.sigplan.org/Resources/Policies/Review/>) and Empirical Evaluation Checklist (<https://www.sigplan.org/Resources/EmpiricalEvaluation/>).
9. Liu *et al.*, *The Last Human-Written Paper: Agent-Native Research Artifacts*, 2026.
   <https://arxiv.org/abs/2604.24658>; toolkit:
   <https://github.com/ARA-Labs/Agent-Native-Research-Artifact>.
