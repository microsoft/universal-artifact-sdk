> **Audience**: Builders of research-artifact evaluation tools.
> **Source of truth for**: Components, data flow, run scopes, and global invariants of
> `artifact-judge-reviewer/v1`.

# 1. Architecture and invariants

## 1.1 Components

```text
            ┌───────────────┐
 paper ───▶ │ Paper adapter │──┐   (optional: bare paper → paper-origin artifact, §3)
            └───────────────┘  │
                               ▼
 artifact ──────────▶ ┌──────────────────┐
 (evaluable-artifact/v3)│ Intake & snapshot│  format gate, path safety, immutable copy + hashes (§2)
                      └────────┬─────────┘
                               │ snapshot (read-only)
              ┌────────────────┼─────────────────────┐
              ▼                ▼                     ▼
        ┌──────────┐    ┌────────────┐      ┌─────────────────┐
        │  Judge   │    │  Reviewer  │      │ Optional services│
        │  (§4)    │───▶│   (§5)     │      │ LLM provider     │
        └────┬─────┘    └─────┬──────┘      │ Reproduction prov│
             │  judge result  │             │ Reference resolver│
             ▼                ▼             └─────────────────┘
        ┌─────────────────────────────┐
        │ Run writer & sealer (§6)    │──▶  sealed run directory (artifact-review-run/v1)
        └─────────────────────────────┘
                                             ▼
                          consumers: viewers, dashboards, CI gates, a future
                          human-in-the-loop layer (read-only; §6.7–6.8, §7.6)
```

| Component | Responsibility | Requires an LLM? |
|-----------|----------------|------------------|
| **Paper adapter** | Produce a paper-origin `evaluable-artifact/v3` directory from a paper, with every result capped at `attested`, plus source-bound candidate contributions and figures. | No (optional enrichment) |
| **Intake & snapshot** | Validate the input, select the paper, copy inputs into an immutable, hashed snapshot. | No |
| **Judge** | Run deterministic checks over the snapshot; aggregate into a rubric and badges; report structural contribution diagnostics separately from the rubric. Optionally attach advisory overlays (reference existence, LLM claim extraction). | No |
| **Reviewer** | Produce a two-sided, evidence-cited review draft; review candidate contributions along independent axes; in artifact-informed scope, incorporate the judge result, reconcile paper claims with shipped evidence, and review declared contributions. | Yes for the scientific analysis; without one it emits an explicitly incomplete draft |
| **Run writer & sealer** | Write all outputs, hash them, and seal a manifest that binds inputs, configuration, versions, stage statuses, and outputs. | No |

The judge and reviewer are separate analysis engines behind one run interface. They have
**strictly separated responsibilities**:

- the **judge** assesses the *artifact*: evidence, consistency, structure, integrity, and
  (when a reproduction provider exists) reproducibility;
- the **reviewer** assesses the *paper as research* and writes for a human reviewer;
- **scores, confidence, the recommendation, and all final decisions** belong to a human (or
  downstream process) and are **never** produced by this tool.

## 1.2 Run scopes

Every invocation produces exactly one **run**, with one of two scopes:

| Scope | Input | What runs | Artifact contents used as evidence? |
|-------|-------|-----------|-----------------------------|
| `paper-only` (default) | a paper file, **or** an artifact directory (only its paper pointer is read) | reviewer paper analysis; optional reference check | **No.** The reviewer reads only the manifest's paper pointer and the selected paper. It MUST NOT criticize the absence of code, data, or artifacts. |
| `artifact-informed` | an artifact directory | the judge over the snapshot, then the reviewer's paper analysis plus supplementary artifact analyses (reconciliation, artifact visuals, run evidence) | **Yes**, as *supplementary* evidence. The paper review is produced independently first; artifact analysis never displaces it. |

An implementation MAY additionally offer a **judge-only** invocation (useful in CI). In that
case it MUST still write a sealed run (§6) with scope `artifact-informed` and all reviewer
stages reported as `not-requested`.

## 1.3 Run lifecycle

1. **Create** the run directory and an initial manifest with `status: "running"`. A run ID
   that already exists MUST be rejected — runs are never overwritten.
2. **Snapshot** inputs (§2.5). From here on, only the snapshot is read.
3. **Resolve configuration** (venue profile, area pack, methodology pack; §5.2) and record its
   digest.
4. **Judge** (artifact-informed only): run checks, aggregate, attach overlays (§4).
5. **Review**: paper analysis, then optional supplementary analyses (§5).
6. **Write** outputs; **verify** the snapshot is unchanged; **hash** outputs; **seal** the
   manifest with `status: "completed"` (§6).
7. On any unrecoverable error, set `status: "failed"` with an `error` string. A failed run is
   never consumable as a completed analysis.

`completed` means the orchestration finished, **not** that every stage succeeded. Each stage's
own status (`completed`, `incomplete`, `unavailable`, `not-run`, …) is recorded separately and
consumers MUST read it (§6.4).

## 1.4 Global invariants

A conforming implementation MUST keep all of the following. They are the tool's identity;
everything else is detail.

| # | Invariant |
|---|-----------|
| I1 | **Read-only input.** The tool MUST NOT modify its input artifact or paper. All outputs go to the run directory. Any reproduction output is additive and lives in the run directory. |
| I2 | **Deterministic verdicts.** The judge's per-finding verdicts, rubric, and badges MUST be computable without an LLM and MUST NOT be changed by any LLM output. |
| I3 | **LLM output is advisory.** LLM-derived content is labeled as such, MUST cite evidence that resolves in the supplied material (or be labeled `unassessed`), and MUST NOT set a verdict, score, recommendation, or confidence. |
| I4 | **No decisions.** The tool MUST leave the overall recommendation, criterion scores, and reviewer confidence **unset** in every output. |
| I5 | **Evidence-conditioned activation.** When the evidence a check needs was *never declared*, the result is `unassessable` (a coverage note, excluded from aggregation) — never a failure. When evidence was *declared but does not resolve*, the result is `unverifiable` plus an integrity note — never a silent pass. |
| I6 | **Uncertainty is first-class.** `unverifiable`, `unassessable`, `unassessed`, `unavailable`, and `not-run` are explicit states that MUST be reported, never collapsed into pass or fail. |
| I7 | **Honest ceiling.** Without actual re-execution or re-analysis by the tool, the judge rubric MUST NOT exceed `PARTIAL`. Producer-declared intent (e.g. a claimed validation mode) MUST NOT raise a verdict. |
| I8 | **Producer neutrality.** The tool MUST NOT branch on producer identity, producer extension blocks, venue, or file-naming conventions of any particular producer. It reads only the SDK contract. |
| I9 | **Scope isolation.** In `paper-only` scope, no artifact content other than the manifest's paper pointer may be read or used. |
| I10 | **Sealed, verifiable output.** Every completed run binds every input and output by hash; consumers can verify the run without trusting the producer of the run (§6). |
| I11 | **Untrusted content.** Paper text, artifact files, traces, and model outputs are untrusted data. Text inside them MUST NOT be followed as instructions, and file paths in them MUST be resolved safely (§2.4). |
| I12 | **No silent degradation.** Every external dependency (LLM, reference resolver, reproduction provider) can be absent or fail; each such case MUST be reported as stage status and warnings, and MUST NOT change deterministic verdicts. |
| I13 | **Contributions are candidates, never qualified by the tool.** Declared or extracted contributions are assessed only along separate axes (claim support, significance, originality; §5.13); the tool MUST NOT combine them into one score or vote, MUST NOT mark a contribution established or qualified (`human_qualification` stays `null`), and contribution diagnostics MUST NOT change the rubric, badges, or exit status. |

## 1.5 Determinism and reproducibility of the tool itself

- For a fixed snapshot, configuration, tool version, and run ID, the judge's findings,
  rubric, and badges MUST be identical across runs (timestamps excepted).
- LLM-derived content cannot be bit-for-bit deterministic. The tool instead records what is
  needed to audit it: provider and model identifiers, a prompt-contract version, every raw
  model response, validation attempts, and the evidence packet each call consumed (§5.4, §6).
- Stable identifiers (finding IDs, evidence-packet IDs, configuration digest, input digest)
  are derived by hashing canonical content so that independent runs on identical inputs
  produce identical IDs.
