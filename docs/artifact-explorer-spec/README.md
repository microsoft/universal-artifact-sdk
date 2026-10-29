> **Audience**: Builders of research-artifact viewers (humans and AI agents).
> **Source of truth for**: The behavioral specification of a static, read-only explorer that
> renders Universal Artifact SDK artifacts and, optionally, a sealed judge/reviewer run.

# Artifact Explorer — Specification

**Spec ID:** `artifact-explorer/v1` · **Status:** DRAFT · **Data contract:**
`artifact-explorer/data/v1` · **Input contracts:** `evaluable-artifact/v3` (SDK
[`SPEC.md`](../../SPEC.md)); `evaluable-artifact/v2` is still read (§2.2); optionally one sealed
`artifact-review-run/v1` run ([judge/reviewer specification](../judge-reviewer-spec/README.md),
§6)

This specification describes a tool, **the explorer**, that turns a research **artifact** into a
**self-contained static website** a person can browse: the paper, its claims, the results and
evidence behind them, the experiments, datasets, traces, and candidate contributions — and, when
supplied, the read-only analysis that a conforming judge/reviewer produced for that artifact.

It is written so that a competent team (or AI coding agent) can build a conforming explorer from
this document set alone, in any language and with any front-end framework. It specifies
**observable behavior and contracts** — what is read, what the intermediate data document
contains, what the site must show and must never show — not internal design. Where a value is a
presentation choice rather than a contract (ordering heuristics, labels, layout), it is marked
*reference value (non-normative)*.

The explorer is a **consumer** in two directions. It reads artifacts exactly as the SDK
specification defines them, and it reads judge/reviewer runs exactly as
`artifact-judge-reviewer/v1` (hereafter **JR**) §6 defines them. It restates neither contract:
where this document needs a field, it cites the section that defines it.

## What the explorer is — and is not

| It is | It is not |
|-------|-----------|
| A **renderer**: a pure function from (artifact, optional run) to a static site | An evaluator: it computes no verdict, badge, rubric, score, or recommendation |
| **Static and read-only**: the output is files any static web server can host; nothing is written back to the inputs | A server, an editor, a job runner, or a place to record human decisions |
| **Graceful**: every input beyond the artifact manifest is optional; absent content is shown as absent, never as negative | A validator of the artifact: malformed optional content is reported and skipped, not judged |
| **Attribution-preserving**: every advisory or inferred statement is shown with the tool or role that produced it | A place where tool output can be mistaken for the authors' declarations |
| **Neutral**: no assumption about venue, field, model vendor, execution platform, or artifact producer | Tied to any particular judge, reviewer, or front-end framework |

## Non-goals of v1

- **Human-in-the-loop** review, annotation, scoring, and approval. An implementation MAY offer
  them as a separate component, but that component is not part of a conforming static build and
  MUST NOT change what the static site shows (§1.4, I6). A static site MAY show an existing,
  explicitly supplied publication approval, read-only (§4.8, OPTIONAL).
- **Serving, jobs, and workspaces**: running the judge or reviewer, hosting several artifacts, or
  any server-side behavior.
- **Non-SDK indexes.** v1 reads only the SDK contract, the figures index of JR §3.6.1, the
  related-work export of JR §3.6.3 (§3.14), one run (sealed, or an unsealed preview), and the
  two OPTIONAL explicitly named files of §4.8 and §4.9.

## Reading order

| # | Document | Contents |
|---|----------|----------|
| 1 | [01-architecture.md](01-architecture.md) | Pipeline, build modes, invariants every conforming explorer keeps |
| 2 | [02-inputs.md](02-inputs.md) | Accepted inputs, the format gate, the run gate, path safety, discovery probes |
| 3 | [03-data-model.md](03-data-model.md) | The `artifact-explorer/data/v1` document: every top-level key and how it is derived |
| 4 | [04-run-overlay.md](04-run-overlay.md) | How a sealed run is read, joined to claims and contributions, and presented without promotion |
| 5 | [05-site.md](05-site.md) | Site layout, sections, routes, rendering rules, required labels and phrases |
| 6 | [06-security.md](06-security.md) | Untrusted input: path containment, sanitization, no network, output isolation |
| 7 | [07-conformance.md](07-conformance.md) | Conformance levels and acceptance scenarios |
| 8 | [08-glossary.md](08-glossary.md) | Terms used in this specification |

## Conventions

- MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are used as in RFC 2119.
- "SDK §N" refers to the Universal Artifact SDK specification ([`SPEC.md`](../../SPEC.md)).
  "JR §N" refers to the judge/reviewer specification. A bare "§N" refers to this document set.
- *Reference value (non-normative)* marks a choice conforming explorers may make differently.
  Everything else is normative.
- Example values are taken from the two worked review examples published with the judge/reviewer
  specification ([`docs/examples/reviews/`](../examples/reviews/README.md), hereafter **bgpt** and
  **lfmu**).
