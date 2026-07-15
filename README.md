# Universal Artifact SDK

> **Implements:** `artifact-sdk/v1` · **Emits:** `evaluable-artifact/v2` · **Spec:** [`SPEC.md`](SPEC.md)

A small, vendor-neutral authoring API for research artifacts. A producer that already *has* the
structured facts about its run — which experiments it ran, what each produced, which claim each
result supports, the container it ran in, the paper — **declares them directly**, and the SDK
**writes a conforming submission**: no prose round-trip, no scraping. A downstream evaluator then
reads that submission.

## Install

```bash
npm install @microsoft/universal-artifact-sdk
```

`dist/` is built automatically on publish (via the `prepare` script), so the installed package is
ready to import — no build step on your side.

### Import (ESM)

```ts
import {
  createArtifact, addEnvironment, addDataset, addExperiment,
  addTrace, addResult, addClaim, attachPaper, writeSubmission,
} from "@microsoft/universal-artifact-sdk";
```

## Quickstart

```ts
import {
  createArtifact, addEnvironment, addDataset, addExperiment,
  addResult, addClaim, writeSubmission,
} from "@microsoft/universal-artifact-sdk";

const a = createArtifact({ id: "expt-42", title: "Feedback-driven contraction" });

addEnvironment(a, {
  name: "primary",
  image: { reference: "reg/artifact:1.2", digest: "sha256:abc…" },
});

addDataset(a, {
  id: "sample_corpus",
  location: { kind: "external", uri: "https://example.org/corpus.tar.gz", sha256: "def…", access: "public" },
  prepare: "tar -xzf corpus.tar.gz -C ./data",
});

addExperiment(a, {
  slug: "posterior_contraction",
  directory: "experiments/posterior_contraction",
  run: { command: "python run.py --seed 0", entrypoint: "run.py", seed: 0 },
  uses_data: [{ dataset: "sample_corpus", at: "data/corpus.parquet" }],
  runs_in: "primary",
});

addResult(a, {
  id: "R1",
  produced_by: "posterior_contraction",
  validates: ["C1"],
  evidence: "experiments/posterior_contraction/contraction.csv",
  kind: "metrics",
  locators: {
    kl_final:   { column: "kl_divergence", row: "final" },
    kl_initial: { column: "kl_divergence", row: "0" },
  },
});

addClaim(a, {
  id: "C1",
  statement: "Posterior contraction improves with more feedback rounds.",
  paper_ref: { section: "5.2", figure: "3" },
  // `validator` (singular) is sugar for a one-element `validators` list
  validator: {
    kind: "builtin", name: "monotonic",
    input: { result: "R1", series: ["kl_initial", "kl_final"] },
    params: { direction: "decreasing" },
  },
});

const report = writeSubmission(a, "./out", { stageFrom: "." });
// → ./out/{manifest.yml, claims.yml, results.yml, datasets.yml, SHA256SUMS, .sdk/state.json, …}
if (report.incomplete) console.warn("incomplete:", report.warnings);
```

A fuller example — a qualitative claim with a trace and **attest-gates-inspect** validators — is
in [`test/worked-example.test.ts`](test/worked-example.test.ts) (mirrors SPEC Appendix A).

## Runnable example

[`examples/quickstart.mjs`](examples/quickstart.mjs) is a standalone, copy-pasteable script that
builds the minimal artifact above and writes a conforming submission. After building the SDK, run it:

```bash
npm install && npm run build
node examples/quickstart.mjs
```

It prints the files written and the generated `manifest.yml`.

## The API

| Call | What it declares |
|------|------------------|
| `createArtifact({ id, title })` | new, empty artifact (in memory) |
| `openSubmission(dir)` | reopen an existing submission to iterate (§4.1) |
| `addEnvironment(a, {…})` | the container image, by reference (§2.5) |
| `addDataset(a, {…})` | an input data source: `in_artifact` \| `in_container` \| `external`, optional `study` ethics block (§2.7) |
| `addExperiment(a, {…})` | a runnable unit + exact run instructions (§2.2) |
| `addTrace(a, {…})` | the record of what actually ran (§2.2.1) |
| `addResult(a, {…})` | an output: `produced_by` + `validates` + evidence + `locators`/`support` (§2.3) |
| `addClaim(a, {…})` | a statement + one or more `validators`; optional `stance` (`hypothesis`\|`finding`) + `tested_by` (§2.4, §2.4.1, §3) |
| `addAssessment(a, {…})` | a whole-submission dimension (usually evaluator-written) (§2.1.1) |
| `attachPaper(a, {…})` | the paper PDF + optional source / claims / references export (§2.6) |
| `attachResearchAgent(a, {…})` | optional producer Q&A witness: pinned `model` + `grounding_sources` (§2.9) |
| `configureJournal(a, { policy, actor, onMissingRationale? })` | set the rationale-elicitation policy for the edit history (§2.8, §4.2) |
| `abandonExperiment` / `failExperiment` / `supersedeExperiment` / `purgeExperiment` | record an experiment's disposition — what was tried and why it was dropped (§2.2.2) |
| `listAbandonedExperiments(a)` / `listJournal(a)` | inspect the retained non-active experiments + the edit history |
| `writeSubmission(a, dir, opts?)` | structural validation + serialize to `evaluable-artifact/v2` (§5, §7) |

- **`add*` is upsert-by-id**: calling it with an existing id/slug **replaces** that element, so an
  artifact is edited across iterations, not rebuilt. `remove*` / `get*` / `list*` complete the
  editor surface.
- **Every mutation is journaled with a rationale (§2.8, §4.2).** Each mutating call accepts an
  optional `ctx = { actor?, rationale? }`; `configureJournal` sets whether a missing rationale is
  `required` (throw), `prompt` (ask an `onMissingRationale` callback — the seam a producing harness
  wires its agent into), or `warn` (default: record + flag). This captures **why** an experiment was
  added or dropped — intent a VCS diff cannot recover.
- **`removeExperiment` is a soft-remove**: it tags the experiment `abandoned` and **retains** it (with
  a `DISPOSITION.md` marker) so what was tried is never lost; `purgeExperiment` is the rationale-gated
  hard delete.
- **Claims carry an author `stance` (§2.4.1)**: `finding` (default) asserts a demonstrated result and
  is assessed on substantiation; `hypothesis` is a proposed statement — pair it with `tested_by` +
  experiment disposition so a *refuted* hypothesis reads as an honest **negative result**, not an
  unsubstantiated claim.
- **A submission may ship a research agent (§2.9)**: `attachResearchAgent` records an optional
  producer Q&A witness (persona file `research-agent.md` + a pinned `model` and `grounding_sources`
  in the manifest). It is advisory and **audited** by a downstream evaluator — an evidence source,
  never an authority. Optional: omit it and the corresponding `agent_faithfulness` dimension is
  simply unassessable.
- **`writeSubmission` is idempotent**: re-emitting an unchanged artifact rewrites the same bytes;
  it never clobbers producer-authored blobs (paper, evidence, traces, reflection).
- **`stageFrom`** (optional): a root the SDK copies referenced blob files from into the submission.
  Omit it if you place blobs into the output directory yourself.

## What the SDK checks (and what it doesn't)

The SDK does **structural** validation only (SPEC §7): required fields, legal enums, and
referential integrity (result→experiment/claim, experiment→dataset, trace `covers`→experiment,
claim `tested_by`→experiment, validator `gated_by`→an `attest` validator on the same claim), and
that `external` datasets carry a `sha256`. Hard problems throw `StructuralError`; "incomplete but
legal" cases (a claim with no validator, a not-yet-present evidence file) are **warnings** in the
returned report.

**Semantic** judgment — do results actually support claims, do validators pass — stays with a
downstream evaluator. Keeping the SDK's checks structural (schema-derived, identical across
bindings) avoids cross-language drift.

## Scope

Implemented: the full object model, the builder API, `writeSubmission` (serialization + evidence
inventory + `SHA256SUMS` + `.sdk/state.json`), structural validation, and `openSubmission`.

The canonical [JSON Schema](schema/evaluable-artifact-v2.schema.json) is authored here and the
emitted model is tested against it. The SDK only *declares* validators; *executing* them is the job
of a downstream evaluator.

## Develop

```bash
npm run typecheck     # tsc --noEmit
npm test              # vitest (114 tests)
npm run test:coverage # vitest + v8 coverage
npm run build         # emit dist/
```

## Contributing

This project welcomes contributions and suggestions. See [`CONTRIBUTING.md`](CONTRIBUTING.md)
for details, including the Contributor License Agreement (CLA). See [`SECURITY.md`](SECURITY.md)
for reporting security issues, and [`SUPPORT.md`](SUPPORT.md) for how to get help.

## Code of Conduct

This project has adopted the
[Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more
information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or
comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of
Microsoft trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion
or imply Microsoft sponsorship.

## License

[MIT](LICENSE) © Microsoft Corporation
