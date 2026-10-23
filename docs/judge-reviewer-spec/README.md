> **Audience**: Builders of research-artifact evaluation tools (humans and AI agents).
> **Source of truth for**: The behavioral specification of a combined artifact judge and
> academic reviewer that consumes Universal Artifact SDK artifacts.

# Artifact Judge and Reviewer — Specification

**Spec ID:** `artifact-judge-reviewer/v1` · **Status:** DRAFT · **Input contract:**
`evaluable-artifact/v3` as defined by the SDK specification ([`SPEC.md`](../../SPEC.md));
`evaluable-artifact/v2` is still read (§2.2)

This specification describes a tool that takes a research **artifact** (or a bare research
**paper**) and produces a sealed, read-only **analysis** of it:

- a **judge** that deterministically checks whether the artifact's own contents support the
  paper's reported results, grounded in published artifact-evaluation standards; and
- a **reviewer** that drafts a two-sided, evidence-cited, conference-style review of the paper
  as research.

When the artifact declares **contributions** (the candidate advances the work claims to make,
SDK §2.4.2), the judge checks the declarations structurally and the reviewer assesses each
candidate along separate, independent axes (claim support, significance, originality) without
ever qualifying it on its own; qualification is left to a human.

It is written so that a competent team (or AI coding agent) can build a conforming tool from
this document set alone, in any language. It specifies **observable behavior and contracts**,
not internal design. Where a value is a tuning
choice rather than a contract (budgets, thresholds, prompt wording), it is marked
*reference value (non-normative)* so builders may do better.

The Universal Artifact SDK (this repository; [`README.md`](../../README.md),
[`SPEC.md`](../../SPEC.md)) is the *authoring* half of the artifact life-cycle; its `SPEC.md`
§10 leaves review-side bindings to downstream tools. This document is one such downstream tool: a roadmap for building evaluators
of SDK-produced artifacts.

## What this tool is — and is not

| It is | It is not |
|-------|-----------|
| A producer of **read-only analysis** for a human (or another tool) to consume | A decision-maker: it never sets scores, a recommendation, reviewer confidence, or acceptance |
| **Deterministic-first**: the judge's verdicts are computed without any LLM | Dependent on an LLM: with no model configured it still produces a complete judge result and an explicitly incomplete review |
| **Evidence-bound**: every statement it makes cites resolvable evidence or is labeled unassessed | A source of new scientific facts |
| **Pluggable** at defined seams: LLM provider, reproduction (execution) provider, reference resolver, venue profiles, downstream human workflow | Tied to any model vendor, execution platform, venue, or artifact producer |

Two capabilities are **specified as extension points** and are expected to be customized per
deployment ([07-extension-points.md](07-extension-points.md)):

1. **Reproduction** — actually executing an artifact's experiments. The judge's verdict model
   is fully specified for executed results; when no reproduction provider is configured, the
   tool reports reproduction as not run and caps its rubric accordingly.
2. **Human-in-the-loop** — editing, overriding, scoring, and approving. The tool's output is
   designed to be *consumed* by such a layer, which must never mutate the sealed analysis.

## Reading order

| # | Document | Contents |
|---|----------|----------|
| 1 | [01-architecture.md](01-architecture.md) | Components, data flow, run scopes, and the invariants every conforming tool keeps |
| 2 | [02-inputs.md](02-inputs.md) | Accepted inputs, the format gate (v3, v2), path safety, snapshotting, which artifact fields (including contributions) are read, quote locating |
| 3 | [03-paper-adapter.md](03-paper-adapter.md) | Turning a bare paper into a paper-origin artifact capped at `attested` evidence: output layout, result harvesting, claims, figures, candidate contributions |
| 4 | [04-judge.md](04-judge.md) | Finding and verdict model, every check, validators, contribution diagnostics, rubric aggregation, badge profile |
| 5 | [05-reviewer.md](05-reviewer.md) | Review configuration, pipeline, finding model, grounding rules, visual and artifact-informed analysis, contribution review, draft structure |
| 6 | [06-run-output.md](06-run-output.md) | The sealed `artifact-review-run/v1` output — the tool's public interface — and consumer obligations |
| 7 | [07-extension-points.md](07-extension-points.md) | LLM provider, reproduction provider, reference resolver, profiles/packs, custom checks, human-in-the-loop layer |
| 8 | [08-conformance.md](08-conformance.md) | Conformance levels and acceptance scenarios a rebuild must pass |
| 9 | [09-standards-and-glossary.md](09-standards-and-glossary.md) | Standards the criteria are grounded in; glossary |

## Conventions

- The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be
  interpreted as described in RFC 2119.
- Field and enum names are given in `code`; their spelling is normative.
- Tool outputs are JSON (UTF-8) plus Markdown renderings; input sketches use YAML as in the
  SDK's `SPEC.md`.
- Hashes are lowercase hexadecimal SHA-256 unless stated otherwise.
- Paths inside an artifact or run directory are relative and `/`-separated, never absolute.
- "§n" refers to a section of this specification; "SDK §n" refers to the SDK's
  [`SPEC.md`](../../SPEC.md) (the `evaluable-artifact/v3` revision).
