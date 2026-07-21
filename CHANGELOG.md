# Changelog

All notable changes to `@microsoft/universal-artifact-sdk` (the TypeScript binding of
`artifact-sdk/v1`, emitting the `evaluable-artifact/v2` format).

The format follows [Keep a Changelog](https://keepachangelog.com/); versions are
pre-1.0, so minor bumps carry additive, backward-compatible features. The emitted
**format id (`evaluable-artifact/v2`) is unchanged** across these releases — every
addition is optional and absence-tolerant, so a submission that uses none of the new
elements is behaviorally identical to `0.1.0` output.

## [0.6.0]

Release-infrastructure, documentation, and toolchain hardening for the public
open-source release. **No runtime or public-API changes** and **no change to the
emitted `evaluable-artifact/v2` format** — output is byte-for-byte identical to
`0.5.0`. This release exists to publish the first npm build from the public repo
through the release-gated pipeline.

### Added
- **Release-gated npm publish pipeline** (`.github/workflows/publish.yml`): builds,
  type-checks, tests, verifies the git tag matches `package.json`, and publishes
  `@microsoft/universal-artifact-sdk` with npm provenance on GitHub Release.
- **CodeQL scanning**, **Dependabot** (npm + GitHub Actions), and **`CODEOWNERS`**.
- **`MOTIVATION.md`** explaining why the SDK exists, linked from the README; authors
  named in the `SPEC.md` byline.

### Changed (toolchain / metadata — no runtime or API impact)
- Package metadata polished for npm publish.
- Dev/CI dependencies bumped: `typescript` 6.0.3 → 7.0.2, `@types/node`,
  `actions/checkout`, `actions/setup-node`, `github/codeql-action`.

## [0.5.0]

### Added
- **`human_interaction` trace kind.** `Trace.kind` gains a dedicated `human_interaction` value for
  human-in-the-loop logs (reviewer clarifications + stage-gate decisions) — a record of *oversight*,
  not of a *run*. It carries no `terminal_state`. Consumers **MUST exclude** it from run-oriented
  dimensions (execution authenticity, trace-report faithfulness); it is instead auditable
  human-oversight evidence for interactive review. Producers should set
  `kind: "human_interaction"` (previously such logs were filed under `other`, which a consumer could
  not distinguish from a run trace). The emitted format id is unchanged; the value is additive and
  the union stays open. See SPEC §2.2.1.

### Changed (toolchain — no runtime/API impact)
- **Dev dependencies bumped** to `typescript@^6.0.3`, `vitest@^4.1.9`, `@vitest/coverage-v8@^4.1.9`.
  TypeScript 6.0 no longer auto-includes ambient `@types/node`, so `tsconfig.json` now sets
  `compilerOptions.types: ["node"]` (fixes `TS2591: Cannot find name 'node:fs'` under the new
  compiler). No change to emitted output or the public API.

## [0.4.0]

### Security
- **Safe relative paths enforced on all producer-declared blob paths.** Every path a producer
  declares — `result.evidence`, `dataset.location.path`/`sample.path`, `trace.path`,
  `paper.pdf`/`source`/`claims_export`/`references_export`, `experiment.directory`,
  `research_agent.path`/`grounding_sources` — is now validated (in `validateStructure`) and
  re-checked at write time (`writeSubmission`). Absolute paths, drive-letter/backslash forms,
  `.`/`..` segments, paths inside `.sdk/`, and collisions with SDK-generated files
  (`manifest.yml`, `claims.yml`, `results.yml`, `datasets.yml`, `traces.yml`, `assessments.yml`,
  `journal.yml`, `reflection.md`, `SHA256SUMS`) are rejected. Previously these flowed unvalidated
  into `join(outDir, rel)` / `cpSync`, so a `..`/absolute path could write or copy **outside** the
  submission directory — a real risk when path fields are LLM/agent-derived. Backward-compatible for
  well-formed submissions.

### Changed
- **Paper: `pdf` or `source` (SPEC §2.6)** — a paper may now be carried as a compiled `pdf`, as
  `source` (LaTeX/Markdown — a single file or a multi-file directory staged verbatim), or **both**;
  a `paper` block requires at least one (previously `pdf` was mandatory). `attachPaper({ source })`
  with no `pdf` is now valid. Prompted by a real submission that shipped multi-file `.tex` and no
  compiled PDF. Backward-compatible: existing `pdf`-only papers are unaffected.

## [0.2.0]

First republish since `0.1.0`, folding in the process-transparency and evidence-source
work plus two correctness fixes. All additions are optional and backward-compatible.

### Added
- **Experiment disposition + provenance journal** (`abandonExperiment`, `failExperiment`,
  `supersedeExperiment`, `purgeExperiment`, `configureJournal`, `listJournal`): retain what
  was tried and *why* — attempted/failed/superseded experiments and a narrated, append-only
  edit history (`journal.yml`), so a refuted attempt reads as an honest negative result.
- **Claim stance** (`stance: "hypothesis" | "finding"` + `tested_by`): distinguish a proposed
  statement under test from a demonstrated result.
- **Research agent** (`attachResearchAgent`): an optional producer-shipped, evidence-grounded
  Q&A witness (`research-agent.md`) with a pinned `model` + `grounding_sources`.
- **Environment digest pinning**: `addEnvironment` auto-fills `image.digest` from a reference
  that already embeds one (`repo@sha256:…`, offline); `writeSubmission` warns (never errors)
  when an image has no effective digest. New `pinnedDigest(reference)` helper.
- **Runnable example**: `examples/quickstart.mjs` — a standalone script that writes a minimal
  submission. Now shipped in the package.

### Fixed
- **Authored-vs-generated ledger** (`.sdk/state.json`): staged producer blobs (paper, evidence,
  traces, research agent) are now classified `authored_files`, not `generated_files`, independent
  of whether `stageFrom` was passed — making the "never clobber authored blobs on re-emit"
  invariant enforceable. Internal bookkeeping only; no API change.
- **Rationale enforcement**: `abandonExperiment` and `supersedeExperiment` now correctly require
  a rationale (SPEC §2.2.2 / §4.2).

## [0.1.0]

Initial release: the core authoring API (`createArtifact`, `addEnvironment`, `addDataset`,
`addExperiment`, `addTrace`, `addResult`, `addClaim`, `addAssessment`, `attachPaper`,
`openSubmission`, `writeSubmission`), the builtin validator catalog, structural validation from
the generated JSON Schema, and serialization to the `evaluable-artifact/v2` layout.
