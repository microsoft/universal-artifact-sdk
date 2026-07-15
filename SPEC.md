# Universal Artifact SDK — Specification (DRAFT for review)

> **Authors:** Microsoft Corporation.
> **Status:** DRAFT — prose-first, for a round of human review before we generate the JSON Schema.
> **Spec ID:** `artifact-sdk/v1` (this document, the API + object model)
> **Emits format:** `evaluable-artifact/v2` (the on-disk *submission* the SDK writes; see §6)
> **Audience:** producers integrating the SDK, SDK binding authors (Python + TypeScript), and
> authors of tools that consume the emitted format.
> **Source of truth for:** the language-neutral authoring API, the artifact object model, the
> validator model, and the on-disk submission layout the SDK produces.
> **Neutrality:** this spec is **vendor-neutral by construction**. No producer-specific concept is
> baked into the model; where a producer needs its own metadata it uses open/extensible blocks.
>
> **Revision note (this draft).** This revision folds in a **unified evaluation model** that
> generalizes the model to research whose evidence **cannot be recomputed by running code**
> (human-subjects, design, conceptual, and interpretive work). The additions are **evolutions along
> the existing grain** — the validator `kind` was already a max-verdict-strength trust ordering — not
> a rewrite. Version stamps are unchanged (`artifact-sdk/v1` → `evaluable-artifact/v2`): nothing has
> shipped yet, so this is a draft revision, not a version bump. **New/changed elements are marked
> `[NEW]`; the design forks surfaced by this revision have been **resolved** this round — each is
> marked `[resolved §11 Qn]` inline, with the decision and rationale recorded in §11.**
>
> **Addendum (post-lock).** §2.6 Paper: a paper may now be carried as `pdf`, as `source`
> (LaTeX/Markdown — a file or multi-file directory), or **both** — at least one is required
> (`[CHANGED]`; previously `pdf` was mandatory). Prompted by a real submission that shipped
> multi-file `.tex` and no compiled PDF. `source` is preferred for machine extraction; `pdf` for
> as-published locators.

---

## 0. What this is (and what it replaces)

Historically a producer ships a **prose submission** (`ARTIFACT.md`, `experiment_list.md`, a
compiled PDF, …) and downstream tooling has to **reverse-engineer structure** out of it into a
structured contract for evaluation. That inference is lossy and only needed because the producer's
structured knowledge was flattened into prose.

The **Artifact SDK inverts that**: a producer that already *has* the structured facts at
generation time (which experiments it ran, what each produced, which claim each result supports,
the container it ran in, the paper) **calls a small set of functions to declare them directly**,
and the SDK **writes a conforming submission** — no prose round-trip, no scraping.

- The **"submission" is the artifact format** (§6). There is no separate submission format to
  convert; the SDK emits `evaluable-artifact/v2` directly.
- The SDK is the **authoring** half. The **review** half is a downstream evaluator that reads the
  emitted format.
- The SDK is **spec-first** and ships **two bindings** — **TypeScript (primary)** and **Python (for
  generality)** — generated against one canonical JSON Schema (§8).

> **Non-goal:** the SDK does **not** evaluate, run experiments, or capture container images. It
> *records declarations* and *serializes* them. Validation of *meaning* stays with a downstream
> evaluator (§7); image capture is the producer's (§2.5).

---

## 1. Goals & principles

1. **Declare, don't infer.** The producer records what it already knows; the SDK never guesses.
2. **Neutral core, logged exceptions.** The model is generic to *any* research artifact. Producer
   specifics are pushed out to the producer via open/extensible blocks and, if truly unavoidable in
   the SDK, recorded in the exceptions register (§9).
3. **Spec-first, schema-canonical.** Prose (this doc) → reviewed → **JSON Schema** (the machine
   contract) → thin bindings that build + *structurally* validate + serialize (§8).
4. **Thin producer, authoritative evaluator.** The SDK does cheap structural checks; the evaluator remains
   the semantic validator and the sole verdict authority (§7).
5. **Deterministic-first, trust-ordered verification.** Every claim carries one or more *validators*
   whose **kind + validation mode determine the strength of verdict they can earn** (§3):
   deterministic checks (re-execute, re-analyze) can reproduce; provenance/integrity checks *attest*;
   an LLM rubric *inspects* and is advisory only. Strength is **relative to the validation mode
   appropriate to the evidence**, not to whether code ran (`[NEW]` — see §3, §11 Q9).
6. **Versioned, stable interface.** Both the API (`artifact-sdk/vN`) and the emitted format
   (`evaluable-artifact/vM`) are versioned; the evaluator hard-gates on the format version (§6).
7. **Iterative, not one-shot.** An artifact is built up and revised over many rounds (add an
   experiment, rerun it, edit a claim, re-evaluate). The SDK is a **re-entrant editor** over a durable,
   diffable submission — idempotent re-writes, authored edits preserved (§4.1).

---

## 2. The object model

A **submission** is a directed graph rooted at an **Artifact**:

```
Artifact
├── experiments[]     Experiment   — a runnable unit + exact run instructions
├── traces[]          Trace        — [NEW] 0..n records of what actually ran (agent/session logs)
├── results[]         Result       — an output of an experiment; names the claim(s) it validates
├── claims[]          Claim        — a statement about the paper's results + how to validate it
├── datasets[]        Dataset      — an input data source (in-container or external) + how to use it
├── assessments[]     Assessment   — [NEW] artifact-level (whole-submission) evaluation dimensions
├── environment       Environment  — reference to the container image the work ran in
├── paper             Paper        — the paper (PDF) + optional source + optional citations export
└── research_agent    ResearchAgent — [NEW] optional producer Q&A agent (persona + pinned model), evidence-grounded (§2.9)
```

Illustrative shapes below are **prose sketches**, not the final schema (that comes in §8). Field
names are provisional and open to the review round (§11).

> **Why the `[NEW]` objects.** Traces, Assessments, evidence-`kind`/`validation_mode` typing, and the
> ethics/citation blocks come from integrating research-execution-quality dimensions and generalizing beyond recomputable evidence
> (the unified evaluation model §9). They are **all optional and
> evidence-conditioned**: a submission that omits them is *not* malformed — the evaluator simply records
> the corresponding dimension as `unassessable` (a coverage note), never a failure. This is the same
> advisory-absence rule the format already applies to licenses and credential-gated datasets.

### 2.1 Artifact (root)

```yaml
artifact:
  format_version: "evaluable-artifact/v2"   # SDK-stamped; evaluator hard-gates on this
  sdk_version: "artifact-sdk/v1"            # which SDK/spec produced it (provenance)
  id: "<opaque producer id>"                # producer-owned; never truncated
  title: "..."
  # NOTE: no producer/framework field in the neutral core. A producer that needs to record its
  # identity uses an open `producer` block, keeping the neutral core producer-agnostic.
```

#### 2.1.1 Assessment — *whole-submission evaluation dimensions* `[NEW]`

Most validation is **claim-scoped** (a Result supports a Claim). But some evaluation dimensions are
about the **artifact or paper as a whole** and have no single claim to attach to — e.g. *did the
reported work actually happen* (**execution authenticity**), *does the paper's account match the
record* (**Trace-Report Faithfulness**), *are the citations real and correctly attributed*
(**Citation Integrity**), *are limitations disclosed honestly* (**Limitation Transparency**). An
**Assessment** is the object those dimensions bind to.

```yaml
assessment:
  id: "A1"
  dimension: "execution_authenticity"      # controlled vocab (resolved §11 Q10 — reconciled set below)
  scope: "artifact"                         # artifact | paper
  evidence: ["traces/run_0007.jsonl", "results.yml"]   # what the dimension is evaluated against
  validator: { kind: "attest", ... }        # [NEW] usually attest or llm_judge (§3)
```

> **Producers rarely author Assessments directly** — they mostly *declare the evidence* (ship the
> trace, the references export) and the **evaluator instantiates the artifact-level dimensions** from the
> evidence inventory (§5.1). The object exists so a producer *may* pre-declare or annotate one, and so
> the emitted format has a stable place for the evaluator to write them. **Resolved (§11 Q10):** authorship
> is **both, evaluator-primary**; the dimension vocabulary is a **reconciled set**, not the full set
> verbatim — the artifact-level dimensions are the ones that add coverage not already checked
> per-claim: **`execution_authenticity`, `trace_report_faithfulness`, `citation_integrity`** (and
> **`limitation_transparency`** when reflection is in scope — §11 Q5). Per-claim axes (substantiation,
> calibration, evidence completeness) stay per-claim and are **not** duplicated as artifact-level
> dimensions.

### 2.2 Experiment — *capturing the exact instructions for running*

```yaml
experiment:
  slug: "posterior_contraction"            # stable id, referenced by results
  directory: "experiments/posterior_contraction"
  run:
    command: "python run.py --seed 0"      # the exact invocation
    entrypoint: "run.py"
    working_dir: "experiments/posterior_contraction"
    args: ["--seed", "0"]
    env: { PYTHONHASHSEED: "0" }           # run-affecting env
    seed: 0
  uses_data:                               # inputs by reference to declared Datasets (§2.7)
    - dataset: "sample_corpus"             # → dataset id
      at: "data/derived/sample.parquet"    # where the experiment reads it at run time (path or mount)
  depends_on: []                           # explicit DAG edges over slugs
  expected_runtime: "4m"
  runs_in: "primary"                       # which Environment (§2.5) it runs in
```

The `run` block is the machine-readable form of "how do I run this experiment" — today recovered
heuristically from prose. It is what makes the artifact *executable* under the evaluator's `--reproduce`
milestone.

### 2.2.2 Experiment disposition — *what was tried, and why it was dropped* `[NEW]`

A research agent typically **attempts many more experiments than it reports**: dead ends, failed
runs, and variants superseded by a better design. Deleting those on the way to the paper discards
first-class scientific evidence — "what didn't work" — and erases the **selective-reporting** signal a
reviewer needs. So an experiment is **retained**, tagged with a `disposition`, rather than removed.

```yaml
experiment:
  slug: "posterior_contraction_v0"
  directory: "experiments/posterior_contraction_v0"
  run: { command: "python run.py --seed 0" }
  disposition:
    status: "superseded"                   # active | superseded | abandoned | failed
    rationale: "v1 fixes a data-leakage bug in the split"   # REQUIRED when status != active
    superseded_by: "posterior_contraction" # when status == superseded
    # failure: { stage: "run", summary: "OOM at 40k steps" }  # when status == failed
```

- `active` — in the reported set (the default; **absent `disposition` ⇒ `active`**, back-compatible).
- `superseded` — replaced by a later variant (`superseded_by` keeps the lineage).
- `abandoned` — deliberately dropped by the agent; `rationale` says why.
- `failed` — could not produce usable evidence; `failure` records where/why.

**`removeExperiment` is a soft-remove** (§4): it sets `status: "abandoned"` and keeps the directory,
so the attempt survives. A true hard delete (`purgeExperiment`) exists but is itself journaled (§2.8)
and requires a rationale. Non-active experiment directories ship a generated `DISPOSITION.md` marker.
The evaluator reads dispositions for the advisory **process-transparency** dimensions (§ *Assessment*),
surfacing the *attempted N → reported M* funnel; a missing/empty rationale is a coverage note, never a
hard failure.

### 2.2.1 Trace — *the record of what actually ran* `[NEW]`

`Experiment` captures the *instructions* for running; a **Trace** captures the **record of an actual
run** — the agent/session log, tool calls, execution events, terminal state. It is the primary
input: it is what lets an evaluator ask *did the reported work actually happen* (Execution
Authenticity) and *does the paper match the record* (Trace-Report Faithfulness), rather than taking
the paper's word for it.

```yaml
trace:
  id: "T1"
  kind: "agent_session"                    # agent_session | execution_log | build_log | notebook | human_interaction | other
  path: "traces/run_0007.jsonl"            # the record itself (in-artifact)
  covers: ["posterior_contraction"]        # optional: experiment slug(s) this trace pertains to
  terminal_state: "completed_with_outputs" # optional producer-declared; evaluator re-derives (see below)
  # terminal_state ∈ completed_with_outputs | planning_only | debugging_no_run | aborted | unknown
  counters: { num_steps: 214, error_count: 3 }   # optional normalized counters; never required
```

Design points (all follow the **evidence-conditioned, no-input-assumptions** rule —
the unified evaluation model §2):

- **0..n, never required.** A submission may ship no trace, one, or many. "No trace" is a **legal,
  non-punitive** outcome: trace-dependent dimensions become `unassessable`, not failures. This is the
  deliberate resolution of an implicit *single-trace* assumption (unified model §2).
- **`covers` is the trace↔experiment join.** With many traces, each dimension is evaluated against
  the trace subset that `covers` the relevant unit; a per-trace `terminal_state` is rolled up rather
  than assuming one global state.
- **`terminal_state` is producer-*declared but evaluator-*owned.** If shipped it is advisory; the evaluator
  re-derives it from the trace and flags disagreement (a Trace-Report Faithfulness signal).
- **`human_interaction` traces are not run records `[NEW]`.** A `human_interaction` trace is a
  human-in-the-loop log — reviewer clarifications and stage-gate decisions (approve/revise/abort) —
  not evidence that the work *ran*. It carries no `terminal_state`. The evaluator **MUST exclude it** from
  run-oriented dimensions (Execution Authenticity, Trace-Report Faithfulness) so a HITL log never
  dilutes the "did the reported work actually run?" signal; it is instead an auditable
  human-oversight evidence source for the interactive review
  ([interactive-review-v1](interactive-review-v1.md) §1). For submissions that predate this kind, a
  evaluator MAY fall back to the producer convention (a `human-in-the-loop` id or a
  `…human_interactions.md` path).
- **The trace body stays opaque (resolved §11 Q12).** We standardize only this envelope
  (`id`/`kind`/`path`/`covers`/`terminal_state`, + optional `counters`); the record's *contents* are
  producer-native and unparsed. An `inspect`-mode validator reads into it cite-addressably when a claim
  needs it. We deliberately do **not** impose a canonical tool-call/event schema — that would force
  every producer's trace format through a lossy mapping and recreate the prose-scraping problem the
  SDK exists to eliminate.

### 2.3 Result — *which experiment produced it, which claim it validates*

A Result is a **first-class object** (in v1 the contract only had a `has_shipped_evidence` boolean).
It carries **both edges**: provenance (which experiment) and intent (which claim(s) it is meant to
validate).

```yaml
result:
  id: "R1"
  produced_by: "posterior_contraction"     # → experiment slug (provenance); may be null for non-executed evidence
  validates: ["C1"]                         # → claim id(s) this result is intended to support
  evidence: "experiments/posterior_contraction/contraction.csv"
  kind: "metrics"                           # [EXPANDED] see enum below
  validation_mode: "re-analyze"            # [NEW] re-execute | re-analyze | inspect | attest (default inferred from kind)
  locators:                                 # named handles into the evidence, used by validators
    kl_final:   { column: "kl_divergence", row: "final" }
    kl_initial: { column: "kl_divergence", row: "0" }
```

**`kind` (expanded) `[NEW]`.** The v1 enum (`metrics | figure | table | log | proof | artifact`) only
covered *execution outputs*. To carry qualitative/interpretive evidence it gains:
`transcript | survey | codebook | argument | external_reference` (and stays open/extensible).

**`validation_mode` `[NEW]`** names *how a claim can be validated from this evidence* — the axis the
whole unified model turns on. It defaults from `kind` (e.g. `metrics`→`re-analyze`,
`transcript`→`inspect`, `external_reference`→`attest`) and may be set explicitly.

**Qualitative support `[NEW]`.** For non-numeric evidence, a Result may replace cell-`locators` with a
`support` block — the qualitative analog of a reported number:

```yaml
result:
  id: "R2"
  validates: ["C7"]
  evidence: "data/interviews/"
  kind: "transcript"
  validation_mode: "inspect"
  support:                                  # [NEW] qualitative support, in lieu of numeric locators
    excerpts:                               # span-addressable citations into the evidence
      - { file: "data/interviews/P07.txt", lines: "40-55" }
    codebook: "data/coding/codebook.yml"    # optional: the coding scheme
    inter_rater_reliability: { metric: "cohen_kappa", value: 0.81 }   # optional
```

`locators` give validators (§3) a stable, cell-level way to read a specific value out of the
evidence — a reported number is just a `locator` a numeric validator compares against. `support` is
its qualitative counterpart, cite-addressable for an `inspect`-mode validator (§3.4).

### 2.4 Claim — *statement + how to validate it*

The claim is the heart of the model. It states something about the paper's results **and carries one
or more validators** (§3). A claim's validators operate over the Result(s) that `validates` it.

```yaml
claim:
  id: "C1"
  statement: "Posterior contraction improves with more feedback rounds."
  paper_ref: { section: "5.2", figure: "3" }   # anchor into the paper
  validators:                                    # [NEW] a LIST — see §3 (builtin|procedure|attest|llm_judge)
    - { kind: "builtin", ... }
```

**Why a validator *list* now `[NEW — resolved §11 Q13]`.** A single claim can need more than one
check — most importantly an **attest** validator (is the evidence authentic/intact?) *gating* an
**inspect** validator (does it support the claim?). Attest and inspect are **orthogonal and
ordered**: a failed attestation must **block or heavily caveat** the inspect verdict, not sit beside
it (unified model §3). The list makes that explicit via an optional `gated_by` edge:

```yaml
claim:
  id: "C7"
  statement: "Participants distrusted the tool's suggestions."
  paper_ref: { section: "6.1" }
  validators:
    - { id: "v_attest", kind: "attest", checks: "provenance", inputs: ["R2"] }
    - { id: "v_inspect", kind: "llm_judge", gated_by: "v_attest",   # [NEW] attest gates inspect
        criteria: "The cited excerpts express distrust of the tool's suggestions.", inputs: ["R2"] }
```

A single `validator: {…}` (singular) remains accepted as sugar for a one-element list, so existing
one-validator claims are unchanged. **Resolved (§11 Q13):** `gated_by` is a **single** validator id in
v1 (one attest gates one inspect); no multiple-gate lists and no inspect→inspect ordering. A concrete
multi-gate need is met by having the attest validator check several things; the field is a candidate
to widen to a list in a later revision only if a real case appears.

> **Coverage note.** Claims here are **producer-declared** — generated via the API (§5), not a
> hand-edited file; the SDK regenerates `claims.yml` from the producer's model on every write. The
> evaluator still reconciles the declared claim set against the claims **extracted from the paper**:
> declaring a claim in the SDK does
> not exempt the artifact from a paper-coverage check. Shipping the paper source (§2.6) is what
> makes that reconciliation machine-checkable.

#### 2.4.1 Claim stance — *hypothesis vs. finding* `[NEW]`

The word "claim" quietly asserts a standing the author may not have earned. Before a result is a
**finding**, it begins as a **hypothesis** — a proposed statement the research agent set out to
test. An optional **`stance`** makes that distinction author-declared:

```yaml
claim:
  id: "H2"
  stance: "hypothesis"                 # [NEW] — absent ⇒ "finding" (default, back-compat)
  statement: "Caching will improve end-to-end throughput."
  tested_by: ["exp-cache-bench"]       # [NEW] — experiment slug(s) that resolve this claim
  validators: []                        # a hypothesis may carry no passing validator yet
```

`stance` is **not** a verdict — the evaluator still decides *substantiation* (§3.5). It is the axis the
verdict is read against:

| `stance` | what the author is asserting | the bar the evaluator holds it to |
| --- | --- | --- |
| `finding` (default) | "the evidence demonstrates this" | **substantiation** — is it supported? An unsupported `finding` is an **overclaim**. |
| `hypothesis` | "we proposed and tested this" | **honest testing/reporting** — was it fairly tested, and is the outcome disclosed? |

**Why this matters.** Without stance, an honestly-reported *negative result* ("we hypothesized X;
experiments did not support it") is indistinguishable from an *overclaim* ("X is true", no support):
both surface as "unsubstantiated claim." Pairing `stance: "hypothesis"` with `tested_by` and the
experiment's **disposition** (§2.2.2) makes a refuted hypothesis a first-class **preserved negative
result** — the evaluator rewards the honesty instead of penalizing a phantom claim. `tested_by` slugs
must resolve to declared experiments (§7).

**Lifecycle.** Because `addClaim` is upsert-by-id and every mutation is journaled (§2.8), *resolving*
a hypothesis is itself a recorded edit: re-`addClaim` the same id with `stance: "finding"` (+ a
passing validator) once an experiment supports it — the journal captures *why* — or leave it a
`hypothesis` and mark its experiment `failed`/`abandoned` (§4.2 rationale applies) when it does not.

### 2.5 Environment — *the container image, by reference*

Producers already build and capture a container image; the SDK **references** it (it does not build
or capture images).

```yaml
environment:
  name: "primary"
  image:
    reference: "registry.example.com/artifact:1.2@sha256:…"  # pin the identity of the image
    digest: "sha256:…"                     # optional if already embedded in `reference` (auto-filled)
  # optional descriptive context (advisory, for the human/badge):
  os: "ubuntu-22.04"
  hardware: { cpu: "x86_64", gpu: "none", min_ram_gb: 8 }
```

By-reference + digest is deliberate: images are large; the submission records *identity*, and the
evaluator's reproduction milestone pulls the pinned image. How the image bytes are stored/transported is
out of scope for the SDK.

**Digest pinning is strongly recommended, not required.** A bare tag (`artifact:1.2`) is *mutable* —
it can be repointed at different bytes later — so only a `sha256:…` **digest** pins the exact image.
The SDK does not *require* a digest (a producer may not have resolved one at authoring time — e.g. a
locally-built or not-yet-pushed image, or offline authoring), and it never contacts a registry. But
it makes pinning easy and visible, consistent with graceful-degradation (absence is a flag, never a
hard failure — like §2.6 license):

- **Auto-fill:** if `image.reference` already embeds a digest (`repo[:tag]@sha256:<64-hex>`),
  `addEnvironment` lifts it into `image.digest` so the pin is explicit and machine-readable.
- **Warn on emit:** `validateStructure` emits a **warning** (never an error) when an image is
  declared with neither an `image.digest` nor a digest embedded in the reference.
- **Evaluator advisory:** the evaluator's `structure/environment_pinned` finding is `VERIFIED` when the image
  is pinned and `ADVISORY` (a reproducibility risk, never a failure) when it is a bare mutable tag.

### 2.6 Paper

```yaml
paper:
  pdf: "paper.pdf"                          # compiled paper — see rule below
  source: "paper/"                          # LaTeX/Markdown source — see rule below
  claims_export: "paper_claims.yml"         # optional: structured result-claims export
  references_export: "paper_references.yml" # [NEW] optional: structured citation list (see below)
```

**At least one of `pdf` / `source` `[CHANGED]`.** A paper may be carried as a compiled `pdf`, as
`source`, or as **both** — but a `paper` block with neither is meaningless and is rejected. Neither
is individually required; `source` alone is fully valid (e.g. a producer that ships LaTeX without
compiling it). `source` **may be a directory** (`"paper/"`) — multi-file LaTeX projects (a `main.tex`
with `\input{}`-ed sections, a `.bib`, figures) are staged verbatim as a tree; it may also be a
single file (`"paper.md"`).

`source` is **preferred for machine reading**: literal numbers, structured `tabular`, and explicit
`\cite{}` extract far more reliably than scraping a PDF, so where both are present the evaluator reads
`source` for number/claim/citation extraction and keeps `pdf` for as-published, human-facing
locators. `source`/`claims_export` are **strongly recommended**: they let the evaluator enumerate the
paper's result-claims and reconcile coverage (§2.4 note) instead of scraping the PDF.

**`references_export` `[NEW]`** is the binding target for **citation integrity** (are cited
sources real, correctly attributed, and actually supportive?). Without it, citation checking has
nothing structured to act on and the dimension is `unassessable`. Shape (open):

```yaml
# paper_references.yml
references:
  - id: "cite12"
    raw: "Smith et al., 2024, Foo Bar, arXiv:2401.00001"
    doi: "10.1145/..."            # optional identifiers that make existence checkable
    cited_for: ["C3"]             # optional: which claim(s) rely on this citation
```

### 2.7 Dataset — *input data: where it comes from and how to use it*

Some artifacts bundle their input data in the container/submission; others pull it from an **external
source** (a URL, cloud store, DOI, or data registry). A **Dataset** captures *both* cases uniformly,
so the evaluator can tell the difference, fetch + verify what it must, and know how each experiment
consumes it. Experiments reference datasets by id via `uses_data` (§2.2) — never by bare path.

```yaml
dataset:
  id: "sample_corpus"                       # referenced by experiment.uses_data[].dataset
  description: "Derived training subset used by the contraction experiment."
  location:
    kind: in_artifact | in_container | external
    # kind: in_artifact  — shipped inside the submission bundle
    path: "data/derived/sample.parquet"     #   path within the submission
    # kind: in_container — already present in the Environment image (§2.5); nothing to fetch
    path: "/opt/data/corpus"                #   absolute path inside the image
    in_environment: "primary"               #   which Environment holds it
    # kind: external     — must be fetched from outside the artifact
    uri: "https://example.org/corpus-v3.tar.gz"   # or s3://…, gs://…, doi:…, a registry ref
    bytes: 294721271
    sha256: "…"                             #   integrity — required for external
    access: public | requires_credentials | license_gated   # how obtainable (default public)
    license: "CC-BY-4.0"                     #   optional; absence is advisory, never fatal
  # how to use it (the "how" the producer knows and the evaluator needs to reproduce):
  prepare: "tar -xzf corpus-v3.tar.gz -C ./data"   # optional: make it usable after fetch (NL or command)
  sample:                                    # optional small shipped subset for a smoke run
    path: "data/samples/corpus_tiny.parquet"
    sha256: "…"
```

**Human-subjects / study provenance `[NEW]`.** When a dataset is empirical data collected from
people (survey responses, interview transcripts, observation logs), the material questions are not
"can I re-fetch it" but *was it ethically obtained and responsibly released* — the **attest** mode
(§3.1). An optional `study` block carries that, advisory and absence-tolerant like license:

```yaml
dataset:
  id: "interview_corpus"
  # …location as above…
  study:                                    # [NEW] optional; all fields advisory, absence never fatal
    ethics_approval: "IRB-2025-0142"        # or a free-text basis; absence is a flag, not a failure
    consent_basis: "informed, opt-in"
    deidentification: "names + employers redacted; see redaction_note"
    redaction_note: "12 quotes withheld for re-identification risk"   # bounds what is reviewable
    sampling: "convenience; n=18 professional developers"
    extra: { data_use_agreement: "DUA-99" }   # open sub-map for venue-specific fields (resolved §11 Q14)
```

Design points:

- **`in_container` ties data to the Environment.** If the image already carries the data, the
  submission records *where* (path) and *which* image — no fetch, no duplication. This is the common
  "everything is in the container" case and is fully reproducible via the pinned image (§2.5).
- **`external` is fetch-and-verify.** `uri` + `sha256` (+ `bytes`) let the evaluator's reproduction
  milestone fetch, checksum, and mount the data deterministically. `access` tells the evaluator when it
  *cannot* fetch: `requires_credentials`/`license_gated` data the evaluator can't obtain yields a
  first-class **`unverifiable`** (not a failure), and an optional `sample` still enables a smoke run.
- **`prepare` is the "how to use it."** Unpacking, decompression, or placement that turns the fetched
  bytes into what the experiment's `at:` path expects. Kept flexible (a command or NL) like a
  `procedure` validator (§3.3).
- **License and study metadata are advisory.** Per repo policy, absence of license/access/ethics
  info is surfaced, never a hard failure. **Redaction is expected, not penalized:** `redaction_note`
  lets the evaluator score what is *reviewable-in-principle* rather than punishing responsible
  de-identification.

### 2.8 Provenance journal — *the narrated edit history* `[NEW]`

The elements above capture an artifact's **final state**. The **journal** captures how it got there:
an append-only log where **every mutation through the authoring API records what changed and — the
crux — *why***. Together with experiment dispositions (§2.2.2) it makes the *research process*
reviewable, not just the result.

```yaml
# journal.yml (generated, append-only)
journal:
  - seq: 1
    timestamp: "2026-01-01T00:00:00Z"
    actor: "agent:experiment"        # free-form; conventionally "<system>:<role>" or "human:<user>"
    op: "add"                              # add | replace | remove | abandon | attach | set
    target: { kind: "experiment", id: "posterior_contraction_v0" }
    rationale: "baseline sweep over feedback rounds"
    after: { … compact new value … }
  - seq: 2
    op: "abandon"
    target: { kind: "experiment", id: "posterior_contraction_v0" }
    rationale: "data-leakage bug found; superseded by v1"
    before: { … }
    after:  { … }
```

Design points:

- **Append-only, monotonic `seq`.** The journal is never rewritten; it is the process record.
- **Rationale is the point.** How aggressively it is required is the session's *elicitation policy*
  (§4.2): `required` (throw), `prompt` (ask a producer callback), or `warn` (record empty + flag).
- **Idempotent.** Re-emitting an unchanged artifact appends **no** entries; only real mutations do.
- **Back-compatible.** Absent journal ⇒ empty history; existing v2 artifacts and legacy submissions
  keep working. Serialized to `journal.yml`, indexed by the manifest `paths`.
- **Advisory to the evaluator.** It feeds process-transparency assessment dimensions; it is never a
  verdict.

### 2.9 Research agent — *an optional evidence-grounded Q&A witness* `[NEW]`

A producer **may** ship a `research-agent.md`: a persona + instructions that configure an LLM to
answer questions about *this* submission's research, methods, data, results — **and** its dead ends
(§2.2.2). It is an **additional evidence source the evaluator audits**, not an authority: a producer
agent describing its own work is an **advocate**, so it is advisory and sits at the **lowest trust**
tier (below deterministic findings and the neutral evaluator-agent — `interactive-review/v1` §1). The
element is **optional and absence-tolerant**: omit it and the corresponding dimension is
`unassessable`, never a failure.

```markdown
---
# research-agent.md — YAML frontmatter (structurally validated) + free-form guide below
research_agent: research-agent/v1
model: "copilot/gpt-5.5@2026-06-01"      # PINNED, in-file — reproducibility (like environment §2.5)
grounding_sources:                        # the artifact files it is authoritative over; MUST resolve
  - claims.yml
  - results.yml
  - traces/
  - paper/
scope: [research, methods, results, negative-results]   # declared capabilities (open vocab)
---

<!-- Free-form producer guide/persona: how to answer, what the study did, caveats.
     The SDK validates the frontmatter, NOT this prose. -->
```

**Behavioral contract** (the guarantees; how it reasons is left free):

- **Grounded — cite-or-say-"unverifiable".** Every answer MUST cite artifact evidence from
  `grounding_sources` or explicitly answer *unverifiable* — the same rule the evaluator-agent obeys
  (`interactive-review/v1` §1). No answer may assert beyond the shipped/regenerable evidence.
- **Faithful to the *executed* work.** It MUST answer honestly about **failed/abandoned**
  experiments and negative results (§2.2.2/§2.4.1), not only the paper's narrative — it reflects
  what was actually run.
- **Read-only & scoped.** It MUST NOT mutate the artifact, and SHOULD decline (as *out-of-scope*)
  questions outside its declared `scope`/`grounding_sources`.
- **Pinned & reproducible.** `model` is a concrete pinned reference in the file, so a review can
  re-run the agent deterministically enough to compare.

**How the evaluator uses it (§7, evaluator side).** Because the frontmatter is structured, the agent is
**auditable**: the evaluator can probe it with questions whose answers are already known from
`claims.yml`/`results`/dispositions and check the answers are grounded and *consistent* — a new
advisory `agent_faithfulness` dimension (agreement is a transparency signal; overclaim/contradiction
is an advisory finding). The agent **never sets a verdict**; the human remains final authority.

---

## 3. The validator model

A claim carries **one or more validators** (§2.4). Each validator's `kind` and **validation mode**
together fix *how* it runs and the **maximum verdict strength** it can earn — the trust ordering from
the agent-friendly memo, now made **relative to the validation mode appropriate to the evidence**
rather than to whether code executed.

| kind | validation mode (§3.1) | who produces the verdict | max verdict strength |
|------|------------------------|--------------------------|----------------------|
| **`builtin`** | re-execute / re-analyze | the evaluator, executing a catalog check | full (deterministic) |
| **`procedure`** | re-execute / re-analyze | an **external deterministic tool** (LLM/human only *orchestrates*) | full, once executed & human-confirmed |
| **`attest`** `[NEW]` | attest | the evaluator, checking provenance/integrity/ethics presence | full **for the integrity question**. As a *gate* it contributes no support verdict; when attest **is** the claim's own validation mode it yields the `attested` verdict (§3.5) |
| **`llm_judge`** | inspect | a model's judgment of a rubric | **advisory** — evidence-supported, not execution-strength |

A validator reads its inputs from the Result(s) linked to the claim (via `locators` or qualitative
`support`), and yields `pass` / `fail` / `unverifiable` + a message.

> **Field-shape caution (`input:` vs `inputs:`).** These are two *distinct* fields, not typos of one
> another. A `builtin` validator takes a singular **`input:`** — an *object* naming one Result and the
> series/columns within it (`{ result, series }`, §3.2). A `procedure` / `attest` / `llm_judge`
> validator takes a plural **`inputs:`** — a *list of Result/evidence ids* it consumes (§3.3–3.5).
> JSON-Schema generation (§11 Q1) will rename these to remove the collision; until then, match the
> field shape to the kind.

> **Max verdict strength is mode-relative `[NEW — resolved §11 Q9]`.** Previously `llm_judge`
> "caps at PARTIAL" — but that bakes in the category error that only *execution* earns the top
> outcome. Under the unified model, a claim whose *appropriate* validation mode is `inspect` reaches
> its ceiling ("evidence inspected and supports the claim, with attest passed") without ever running
> code. The **adopted** verdict vocabulary — `re-executed` / `re-analyzed` / `evidence-supported` /
> `attested` / `unverifiable` — rolls up into the familiar `REPRODUCED` / `PARTIAL` /
> `NOT_REPRODUCED` summary for the dashboard. The **human remains final**, and **attest gates
> inspect** (a failed `attest` validator blocks/caveats a `gated_by` inspect verdict). **Roll-up
> precedence is resolved:** `evidence-supported` is **capped below** `re-executed`/`re-analyzed` — a
> claim settled by inspection is strongly supported but not *reproduced* in the ACM "Results
> Reproduced" sense, so it never reaches the top reproduction tier automatically; the human reviewer
> may promote it (§11 Q9).
>
> **`REPRODUCED` carries a method badge `[resolved audit B2]`.** Both `re-executed` (pinned code
> re-ran) and `re-analyzed` (reported numbers recomputed from released data) roll up to `REPRODUCED` —
> recomputing the numbers reproduces the *results* in the ACM "Results Reproduced" sense. But the
> dashboard **badges which method was used** — *reproduced (re-executed)* vs *reproduced (from released
> data)* — so a reviewer sees that re-execution is the stronger demonstration. This **revises** the
> earlier evaluator rule that reserved `REPRODUCED` for actual re-execution.

### 3.1 Validation mode — the axis `[NEW]`

Every validator (and, by default, every Result — §2.3) carries a **validation mode** naming *how a
claim is validated from the evidence*, ordered by how much is settled deterministically:

| mode | the validator… | deterministic? |
|------|----------------|----------------|
| `re-execute` | re-runs pinned code → regenerates outputs, compares within tolerance | yes |
| `re-analyze` | treats released data as a frozen input; re-runs the *analysis* → reproduces reported numbers | yes |
| `inspect` | reads the record (transcript, argument, figure) and assesses whether it supports the claim | no — advisory, human-final |
| `attest` | verifies the evidence *is what it claims* and was properly obtained (provenance/integrity/ethics) | partly (structural) |

`re-execute` and `re-analyze` are the deterministic modes (today's `builtin`/`procedure`); `inspect`
is `llm_judge`; `attest` is the new kind below (§3.5). This axis is what lets the evaluator pick the right
check per claim instead of assuming everything re-runs.

### 3.2 `builtin` — named catalog + params (the default)

The producer picks a check by **name** from a spec-defined catalog and supplies params + a locator.
No producer code is shipped or run; semantics are defined **in this spec** so the TS emitter and the
Python evaluator agree.

```yaml
validator:
  kind: builtin
  name: monotonic                 # from the catalog below
  input: { result: "R1", series: ["kl_initial", "kl_final"] }
  params: { direction: "decreasing" }
```

**Initial catalog** — **resolved (§11 Q2):** ship the first six; the two `[proposed]` rows are staged
(corpus demand drives further additions — the catalog is deliberately kept small):

| name | checks | key params |
|------|--------|-----------|
| `numeric_close` | a value ≈ an expected value | `expected`, `rel_tol`, `abs_tol` (numpy-isclose semantics) |
| `numeric_threshold` | a value satisfies an inequality | `op` (`>=`,`<=`,`>`,`<`,`==`), `bound` |
| `monotonic` | a series is monotone | `direction` (`increasing`/`decreasing`) |
| `exact_match` | a value equals an expected literal | `expected` |
| `contains` | evidence contains an expected item/substring | `expected` |
| `output_present` | a declared output exists and is non-empty | — |
| `set_ranking` `[proposed §11 Q2]` | a set matches (membership) or a ranking matches (order) an expected list | `expected`, `mode` (`set`/`order`) |
| `distribution_close` `[proposed §11 Q2]` | two samples are drawn from the same distribution (two-sample test) | `test` (`ks`/`mannwhitney`), `alpha` |

> **Reported-number consistency** ("paper says 0.82; the artifact produced 0.82 ± 5%") is expressed
> as `numeric_close` over a Result locator — no separate mechanism needed.

### 3.3 `procedure` — natural-language orchestration, may invoke external tools

For verification the catalog can't express — **verify a proof with automation** (Lean/Coq/Isabelle),
run an SMT/model checker, or a custom harness. The **outcome is deterministic** (the tool decides);
only the *orchestration* is natural language, because these tools can't be pre-catalogued.

```yaml
validator:
  kind: procedure
  instructions: >
    In the primary image, run `lake build` in `proofs/`. Theorem 3 is verified iff the build
    exits 0 with no `sorry`/`admit` in the output.
  tools: [ { name: "lean", version: "4.x" } ]   # declared so they can be provisioned/sandboxed
  inputs: ["R1"]                                  # results/evidence the procedure consumes
  success_criteria: "exit code 0 and no 'sorry' in output"   # NL + optional machine hint
  timeout: "10m"
```

**Critical distinction — `procedure` is *not* `llm_judge`:** here the LLM/agent is the
**orchestrator**, not the evaluator. It reads the instructions, runs the tool in a sandbox, and reports
**the tool's** deterministic result; the verdict is the tool's, human-confirmed. That is why a
`procedure` can earn a real verdict while an `llm_judge` cannot. **Authoring guidance:** reach for
`procedure` whenever an external tool can *decide* the claim; reserve `llm_judge` for genuinely
subjective correctness.

Because it needs tool provisioning + a sandbox, in the static phase a `procedure` is **surfaced as
"declared, run-to-verify" (pending)** — the same milestone shape as `--reproduce` — rather than
auto-executed.

### 3.4 `llm_judge` — NL rubric measuring correctness (the `inspect` mode)

For qualitative/interpretive claims no deterministic tool can settle — the **`inspect`** validation
mode (§3.1).

```yaml
validator:
  kind: llm_judge
  gated_by: "v_attest"            # [NEW] optional: attest validator that must pass first (§3.5)
  criteria: >
    The generated summaries faithfully reflect the source documents with no fabricated claims.
  inputs: ["R2"]
```

Per the locked principle (LLM never sets a verdict —
[`interactive-review-v1.md`](./interactive-review-v1.md) §3), an `llm_judge` result is **advisory**:
it informs the human, who is final. Its **max verdict strength is `evidence-supported`** — the
ceiling for a claim whose appropriate mode is `inspect` — reached only when any `gated_by` `attest`
validator passes (§3.5). This **replaces** the older "caps at PARTIAL" rule, which conflated
"validated by inspection" with "couldn't reproduce" (`resolved §11 Q9`).

### 3.5 `attest` — provenance / integrity / ethics `[NEW]`

An `attest` validator answers *is this evidence authentic, intact, and legitimately obtained?* — it
**never** asserts a claim is *supported*. It is largely deterministic/structural (hashes, presence of
declared provenance, ethics-block presence) with advisory portions.

```yaml
validator:
  kind: attest
  checks: provenance                        # provenance | integrity | ethics | citations_exist
  inputs: ["R2"]                             # result(s) / evidence whose integrity is attested
```

**Attest gates inspect.** An `attest` validator is typically referenced by an `inspect`
(`llm_judge`) validator's `gated_by` field on the same claim (§2.4). Semantics: if the attest fails
or is `unverifiable`, the gated inspect verdict is **blocked or heavily caveated**, not reported as
an equal peer. Courtroom analogy: attest = chain of custody; inspect = probative value (unified model
§3).

**Two roles for `attest` — gate vs. verdict `[resolved audit B1]`.** The same kind serves two
distinct purposes, and they must not be conflated:

> - **Attest-as-gate.** When an `attest` validator is named by another validator's `gated_by`, it
>   contributes **no verdict of its own** — it only permits or blocks the gated inspect verdict (above).
> - **Attest-as-verdict.** When the claim's *own* question **is** an integrity/provenance/ethics
>   question (e.g. "the transcript is authentic and unaltered", "the consent basis is documented"),
>   the passing `attest` validator **is** the claim's verdict: **`attested`** — a first-class entry in
>   the verdict vocabulary (§3, Q9). In roll-up, `attested` maps to **at most `PARTIAL`** and is
>   **advisory for badging**: it evidences integrity, not that a *result* was reproduced.

---

## 4. The authoring API (language-neutral)

The bindings expose an ergonomic builder. Signatures below are **conceptual** — each binding renders
them idiomatically (TS Promises/objects, Python dataclasses), but all target the same JSON Schema.

```
# --- construct or reopen ---
createArtifact({ id, title }) -> Artifact                  # new, empty artifact (in memory)
openSubmission(dir) -> Artifact                            # reopen an existing submission to iterate (§4.1)

# --- declare / upsert (add* is create-or-replace by id) ---
addEnvironment(artifact, { name, image:{reference,digest}, os?, hardware? }) -> Environment
addDataset(artifact, { id, location:{kind,…}, prepare?, sample?, study? }) -> Dataset       # study? = [NEW] ethics/provenance
addExperiment(artifact, { slug, directory, run:{command,…,seed}, uses_data?, depends_on?, runs_in }) -> Experiment
addTrace(artifact, { id, kind, path, covers?, terminal_state? }) -> Trace                    # [NEW] §2.2.1
addResult(artifact, { id, produced_by?, validates, evidence, kind, validation_mode?, locators?, support?, supersedes? }) -> Result
addClaim(artifact, { id, statement, stance?, tested_by?, paper_ref, validators }) -> Claim    # validators = list (validator: singular sugar); stance/tested_by = [NEW] §2.4.1
addAssessment(artifact, { id, dimension, scope, evidence, validator }) -> Assessment          # [NEW] §2.1.1
attachPaper(artifact, { pdf, source?, claims_export?, references_export? }) -> Paper           # references_export = [NEW] §2.6
attachResearchAgent(artifact, { path, model, grounding_sources, scope? }) -> ResearchAgent     # [NEW] §2.9 — optional; model pinned in-file

# --- inspect / revise (enables iteration — §4.1) ---
getExperiment(artifact, slug) / listExperiments(artifact) -> …     # and get*/list* for each element (incl. traces, assessments)
removeExperiment(artifact, slug, ctx?) / removeResult(artifact, id, ctx?) / removeClaim / removeDataset
removeTrace(artifact, id, ctx?) / removeAssessment(artifact, id, ctx?)                         # [NEW]

# --- process provenance (journal + experiment lifecycle — §2.2.2, §2.8) [NEW] ---
configureJournal(artifact, { policy, actor, onMissingRationale? })   # rationale-elicitation policy (§4.2)
abandonExperiment(artifact, slug, ctx) / failExperiment(artifact, slug, {stage,summary}, ctx)  # soft, retained
supersedeExperiment(artifact, slug, supersededBy, ctx) / purgeExperiment(artifact, slug, ctx)  # purge = hard delete
listAbandonedExperiments(artifact) / listJournal(artifact) -> …      # inspect what was tried + the history
# every mutating call above accepts an optional ctx = { actor?, rationale? } (§4.2)

# --- serialize (idempotent; §4.1, §5, §7) ---
writeSubmission(artifact, outDir) -> SubmissionReport      # serialize + structural validation (§7)
```

Notes:
- `addResult` carries the two edges directly (`produced_by`, `validates`) — no separate "connect"
  call; the result *is* the connection. `produced_by` is **optional** `[NEW]`: evidence that was not
  produced by a declared experiment (a transcript, an external reference) simply omits it.
- `addClaim` takes `validators` (a list; a singular `validator` is accepted as one-element sugar —
  §2.4). A claim with no runnable validator is allowed but surfaced by the evaluator as `unverifiable`
  (except a `stance: "hypothesis"` claim, for which an empty validator list is expected — §2.4.1).
  An optional **`stance`** (`hypothesis` | `finding`, default `finding`) declares the claim's author
  standing, and **`tested_by`** links a hypothesis to the experiment slug(s) that resolve it.
- **`add*` is upsert-by-id**: calling it with an id/slug that already exists **replaces** that element
  (see §4.1); `remove*` deletes one. This is what makes the model editable across iterations, not
  write-once.
- `writeSubmission` lays out §5, stamps `format_version`, computes integrity hashes, and runs
  structural validation (§7). It returns a report (not a verdict). It is **idempotent and
  re-runnable** — not a one-shot terminal op (§4.1).
- **Ordering / referential integrity:** results reference experiment slugs and claim ids, experiments
  reference dataset ids (`uses_data`), traces optionally reference experiment slugs (`covers`), claims
  optionally reference experiment slugs (`tested_by`), and a validator's `gated_by` references another
  validator id on the same claim; the SDK checks these all resolve at `writeSubmission` time
  (structural only — §7).

### 4.1 Iteration & the authoring lifecycle

An artifact is **built up and revised over time** — a human (or agent) adds an experiment, reruns it,
edits a claim, ships more evidence, then re-submits for another round of judging. The SDK is a
**re-entrant editor over a durable submission**, not a one-shot builder. It inherits the two
load-bearing invariants of the format it emits: **idempotent re-writes** and the
**generated-vs-authored** separation (a central invariant of the emitted format, which the SDK
preserves).

- **Reopen, don't rebuild.** `openSubmission(dir)` reads an existing submission back into the model so
  the next change is a small edit, not a from-scratch reconstruction. (Producers whose *generator* is
  the source of truth — e.g. an experiment harness — may instead re-run their build program; both are
  supported. See §11 Q8.)
- **Edit by id.** `add*` is create-or-replace keyed on the element's id/slug; `remove*` deletes;
  `get*/list*` inspect. Ids are stable, producer-owned, and never truncated — so an edit targets
  exactly one element and leaves the rest untouched.
- **Idempotent, diff-friendly writes.** `writeSubmission` re-serializes with stable ordering and
  content hashes, so **only changed files are rewritten** and re-emitting an unchanged artifact is a
  no-op. This keeps the on-disk submission cleanly diffable under version control.
- **Authored files are never clobbered.** Re-emission regenerates *generated* files (manifest,
  claims, results, datasets, checksums) but preserves *authored* ones (`reflection.md`, the paper) —
  the same invariant that guarantees human edits survive re-runs.
- **Reruns are additive.** Re-running an experiment produces fresh evidence. Reusing a result id
  **replaces** it; minting a new id (optionally `supersedes: "<old id>"`) **keeps both**, so runs can
  be compared — mirroring the evaluator's additive *regenerated-evidence* rule.
- **Incomplete is legal.** A partial artifact (a new experiment with no result yet, a claim awaiting
  evidence) is **not malformed**: `writeSubmission` reports it as *incomplete* (warning) and the evaluator
  treats the unbacked claim as `unverifiable`, not a failure. This enables save-and-continue authoring.
- **Iteration history lives in *both* the journal and version control `[NEW — §2.8]`.** The SDK now
  keeps an **in-artifact provenance journal** — an append-only record of every mutation *and its
  rationale* (§2.8) — because "why was this experiment dropped" is not recoverable from a VCS diff.
  Version control remains complementary (the evaluator `git init`s the submission dir for file-level
  provenance); the journal adds the **intent** a diff cannot.

Together these make the real loop first-class:
**produce → evaluator → findings → iterate (add / rerun / revise) → re-emit → re-evaluate.**
The SDK owns the *iterate* and *re-emit* steps; the evaluator owns the rest.

### 4.2 Rationale elicitation — *asking "why" at each stage* `[NEW]`

Every mutating call (`add*`, `remove*`, `abandon*`, `attach*`, `set*`) accepts an optional
`ctx = { actor?, rationale? }` and appends one journal entry (§2.8). How hard the SDK insists on a
rationale is the **session policy**, set once via `configureJournal`:

| policy | behavior when a mutation omits a rationale |
|--------|--------------------------------------------|
| `required` | **throws** before the mutation is applied — the change is rejected (transactional). Best for high-integrity pipelines. |
| `prompt` | invokes the producer-supplied `onMissingRationale(change) => string` callback to obtain the explanation before committing. **This is the seam a producing harness wires its agent-prompting into** — "you just removed experiment X; why?" |
| `warn` *(default)* | records the entry with an empty rationale and surfaces it as a **coverage warning** at `writeSubmission` (never a hard failure). |

The callback keeps the core **phase-agnostic and vendor-neutral**: the SDK defines *when* a rationale
is needed; the producer decides *how* to obtain it. `abandonExperiment`/`failExperiment`/`purgeExperiment`
treat the rationale as **required** regardless of policy — dropping a tried experiment without saying
why defeats the point.

---

## 5. Serialization — the "submission" on disk

`writeSubmission` produces the `evaluable-artifact/v2` layout:

```
<submission>/
├── manifest.yml          # experiments, environment ref, paths, format_version, sdk_version, evidence inventory (§5.1)
├── claims.yml            # claims + their validator(s)
├── results.yml           # results: produced_by + validates + evidence + locators/support + kind + validation_mode
├── datasets.yml          # input data sources (in_artifact | in_container | external) + how to use + study? (ethics)
├── traces.yml            # [NEW] declared traces (id, kind, path, covers, terminal_state); omit if none
├── assessments.yml       # [NEW] artifact-level dimensions (mostly evaluator-written); omit if none
├── paper.pdf             # + optional paper/ source, paper_claims.yml, paper_references.yml [NEW]
├── data/…                # data shipped in the bundle (in_artifact datasets, samples)
├── evidence/…            # the shipped outputs referenced by results (or under experiments/<slug>/)
├── traces/…              # [NEW] the trace records themselves (referenced by traces.yml)
├── journal.yml           # [NEW] append-only edit history (§2.8); omit if no mutations recorded
├── experiments/<slug>/DISPOSITION.md   # [NEW] marker for a non-active (abandoned/failed/superseded) experiment (§2.2.2)
├── reflection.md         # optional authored reflection/limitations
├── research-agent.md     # [NEW] optional producer Q&A agent — pinned model + grounding_sources in frontmatter (§2.9)
├── .sdk/state.json       # GENERATED — authored-file registry + content hashes (idempotency; §4.1)
└── SHA256SUMS            # integrity over all shipped files (SDK-computed)
```

- **The generated-vs-authored split is *known by construction*.** Unlike prose reverse-engineering — which had
  to *reverse-engineer* which files were generated output vs human-authored seeds
  (`evaluable-artifact/v1` §1.1) — the SDK knows this directly: files it serializes from the model
  (manifest, claims, results, datasets, traces index, assessments, checksums) are **generated**;
  files the producer places (`reflection.md`, the paper, evidence + trace blobs) are **authored**. On
  re-emit (§4.1) the SDK rewrites the former and never clobbers the latter. The registry of authored
  files + their content hashes is recorded (as in `evaluable-artifact/v1`'s `state.json`) so
  idempotency survives across sessions.
- Every machine-generated file carries a generated marker naming the SDK
  (repo convention; e.g. `_generated:` / `> **Auto-generated**`).
- **New index files are omitted when empty.** `traces.yml` / `assessments.yml` / `journal.yml` /
  `paper_references.yml` appear only if the producer declared the corresponding content — their
  absence is the on-disk form of "this evidence was not provided" (see §5.1).
- **Producer-declared paths must be safe relative paths.** Every path a producer declares —
  `result.evidence`, `dataset.location.path` / `sample.path`, `trace.path`, `experiment.directory`,
  `paper.pdf` / `source` / `claims_export` / `references_export`, `research_agent.path` /
  `grounding_sources` — is a path **relative to the submission root**. It must not be absolute, must
  not contain `.`/`..` segments (nor drive-letter/backslash forms), must not live under `.sdk/`, and
  must not collide with an SDK-generated file (`manifest.yml`, `claims.yml`, `results.yml`,
  `datasets.yml`, `traces.yml`, `assessments.yml`, `journal.yml`, `reflection.md`, `SHA256SUMS`).
  The SDK enforces this on both `writeSubmission` and structural validation, so an unsafe path can
  never write or copy **outside** the submission directory — a real risk when path fields are
  LLM/agent-derived. **Consumers must mirror the check on read:** a submission is untrusted, so a
  reader resolving a declared path must refuse anything that escapes the root (the evaluator does this in
  `loader.safe_artifact_path`).

### 5.1 Evidence inventory & activation `[NEW]`

`manifest.yml` carries an **evidence inventory**: a machine-readable capability list of what the
submission actually contains — enabling **evidence-conditioned** evaluation
(the unified evaluation model §2, §5). This formalizes, in one place,
the optionality that is otherwise scattered field-by-field.

```yaml
# manifest.yml (excerpt)
evidence_inventory:                # [NEW] SDK-computed from what was declared
  has_runnable_experiments: true
  has_traces: true                 # ≥1 Trace declared
  trace_count: 3
  has_released_data: true          # ≥1 in_artifact/external Dataset
  has_paper_source: true
  has_research_agent: false        # [NEW §2.9] → agent_faithfulness is unassessable when absent
  has_citations_export: false      # → Citation Integrity is unassessable, not failed
  has_journal: true                # [NEW §2.8] an edit history was recorded
  experiments_attempted: 5         # [NEW §2.2.2] active + non-active
  experiments_reported: 3          # [NEW §2.2.2] active only → the attempted→reported funnel
  evidence_kinds: [metrics, transcript]      # union of Result.kind present
  validation_modes: [re-analyze, inspect, attest]   # union of modes present
```

**Activation contract.** The evaluator indexes each check/dimension by the evidence it needs and runs it
**iff** the inventory satisfies the precondition; otherwise it emits an explicit
`unassessable(reason)` — a **coverage note, never a failure and never a downgraded verdict**. The SDK
only *computes and records* the inventory (structural); the evaluator *acts* on it (semantic). This is
the mechanism by which the format assumes **nothing** about which inputs are present.

---

## 6. Versioning

Two independent axes, both explicit in every submission:

- **`artifact-sdk/vN`** — the API + this spec (bindings implement it).
- **`evaluable-artifact/vM`** — the emitted on-disk format (the evaluator hard-gates on it).

This spec defines **`artifact-sdk/v1`** emitting **`evaluable-artifact/v2`**. `v2` is a superset of
`v1`: it adds first-class **Results**, **Claim validators**, and **Environment-by-reference**, drops
prose-only inference (`flags.*` guessed from prose), and — in this revision — adds the
**evidence-conditioned** additions from the unified model: **Traces**, artifact-level
**Assessments**, the **`attest`** validator kind + **validation-mode** axis, expanded evidence
**`kind`** + qualitative **`support`**, dataset **`study`** (ethics) metadata, a paper
**`references_export`**, the **evidence inventory** (§5.1), and — in this revision — **experiment
dispositions** (§2.2.2) + the **provenance journal** (§2.8) that capture the research *process*
(what was tried and why), with a **rationale-elicitation policy** on the authoring API (§4.2). **All
additions are optional and absence-tolerant**, so a `v2` submission that uses none of them is
behaviorally the earlier `v1`. **Evaluator
support for `v2` is a required, separate milestone** — the evaluator continues to accept `v1` (legacy
output) and grows a `v2` reader. Nothing here breaks the current pipeline.

> **Naming caution** (see repo memory): `evaluable-artifact/vM` is *our contract version*; do not
> conflate it with any producer's own format-revision numbering.

---

## 7. Validation split — thin SDK, authoritative evaluator

| Layer | Runs where | Checks | On failure |
|-------|-----------|--------|------------|
| **Structural** | in the SDK (`writeSubmission`), both bindings, from the JSON Schema | required fields, types, referential integrity (result→experiment/claim ids resolve, experiment→dataset ids resolve, trace `covers`→experiment ids resolve, validator `gated_by`→a validator id on the same claim, claim `tested_by`→an experiment slug, experiment `disposition.superseded_by`→an experiment slug, research-agent `grounding_sources`→shipped paths that resolve), external datasets carry a `sha256`, a research-agent (when present) declares a pinned `model` and at least one `grounding_source`, a validator is well-formed for its `kind`, `validation_mode`/`disposition.status`/`claim.stance` are legal enum values, all producer-declared paths are safe relative paths (§5 — no absolute/`..`/`.sdk`/generated-file collision), a recorded mutation carries a rationale (§4.2 — warning), evidence inventory (§5.1) is computed | reject / report — the producer fixes before emitting |
| **Semantic** | in the **evaluator** | do results actually support claims; do validators pass (per validation mode; attest gates inspect); artifact-level assessments; paper-coverage (D8); citation integrity; consistency; external-data fetch + checksum + mount (reproduction milestone); structure/badges; **evidence-conditioned activation** (*no* evidence declaration → `unassessable`, a coverage note; a *declared-but-unresolved* pointer → `unverifiable` + integrity flag — never a silent pass, §5.1) | verdicts (mode-relative, rolling up to `REPRODUCED`/`PARTIAL`/`NOT_REPRODUCED`) + findings |

Rationale: **cross-language semantic validation would drift** between TS and Python. Keeping the
SDK's checks structural (and schema-derived, hence identical in both languages) while the single
Python evaluator owns semantics avoids duplicating — and diverging — the hard logic. The SDK's job is to
make a submission *well-formed*; the evaluator decides if it's *good*.

---

## 8. Language bindings & the spec→schema pipeline

1. **Prose spec (this doc)** → reviewed by humans (this round).
2. **JSON Schema** generated from the agreed model — the **canonical machine contract** for both the
   emitted format *and* the API's inputs. Validator-catalog semantics (§3.2) are pinned here in prose
   + schema so both languages agree.
3. **Bindings** (thin builders over the schema):
   - **TypeScript — primary.** TypeScript is the primary binding and first real consumer, so
     the TS binding is first-class, not a port.
   - **Python — for generality**, and it aligns with the reference evaluator / `emit_manifest` semantics,
     which serve as the reference implementation for the builtin catalog.
   Both: build → structurally validate (schema) → serialize (§5). No semantic logic; no shipped
   validator code executed.

---

## 9. Neutrality & the exceptions register

The SDK is **vendor-neutral by construction**: the object model, validators, and API contain nothing
producer-specific. Where a producer needs its own metadata, it uses open/extensible blocks (e.g. a
`producer` map) rather than first-class neutral fields.

If a producer-specific item *must* enter the SDK/spec itself, it is recorded — with rationale and a
generalization/removal plan — in an exceptions register. The register
should ideally stay **empty**; every entry is visible debt. This operationalizes the vendor-neutral
separation invariant.

---

## 10. Review side (deferred bindings)

The **review** half is the existing evaluator; it reads `evaluable-artifact/v2`. **Review-side bindings
are deferred** — for now the evaluator is invoked as today (Python / CLI). When we do add producer-facing
review access, it reuses this spec's schema for the findings/verdicts shapes.

---

## 11. Review decisions (resolved this round)

The forks below were **decided** in the review walkthrough (2026-07-07). Each is now reflected inline
in the relevant section via a `[resolved §11 Qn]` marker. Two items (Q1, Q6) are **deferred by
decision** — they don't block implementation and are settled at a later, well-defined point.

| # | Question | **Decision** | Rationale |
|---|----------|--------------|-----------|
| 1 | Field naming (§2) | **Deferred to JSON-Schema generation.** Names stay provisional in the prose spec. | Naming churns until the schema is written; no need to freeze now. |
| 2 | Builtin catalog (§3.2) | **Ship the six**; stage two `[proposed]` — `set_ranking`, `distribution_close`. Keep the catalog small; corpus demand drives more. | Avoid speculative surface; add checks when a real submission needs them. |
| 3 | `procedure` machine hints (§3.3) | **NL + optional machine hint** (`exit_code`/regex) for `success_criteria`. | Gives an agent an auto-run path without forcing structure onto every procedure. |
| 4 | Datasets (§2.7) | **Keep `in_artifact│in_container│external`.** DOIs/registry refs are first-class URIs; **single `prepare` step** for now (defer the preprocessing mini-DAG); `access` handling stays. | The model covers observed cases; a mini-DAG is unneeded complexity until a submission demands it. |
| 5 | Reflection/limitations | **Optional to emit.** When present, feeds the `limitation_transparency` assessment dimension (Q10). | Not all producers ship reflection; absence is a coverage note, not a failure. |
| 6 | Product/package name (OD1) | **Deferred (branding).** Keep the working name `universal-artifact-sdk` (PyPI `universal-artifact-sdk`, import `uas`) so consumers can build now. | Final name ties to org/open-source review (OD5); renameable before first publish without touching the model. |
| 7 | Format name | **Evolve `evaluable-artifact/v2`** (don't mint a new name). | Nothing has shipped; all additions are optional/absence-tolerant, so it's the same `v2`. |
| 8 | Canonical source (§4.1) | **Support both** build-program and on-disk submission; the producer's harness decides which it uses. `openSubmission` ships regardless. | No spec-level forced choice; keeps the human-in-the-loop reopen path available. |
| 9 | Verdict vocabulary & roll-up (§3, §3.4) | **Mode-keyed vocabulary** (`re-executed`/`re-analyzed`/`evidence-supported`/`attested`/`unverifiable`) **rolling up** to `REPRODUCED`/`PARTIAL`/`NOT_REPRODUCED`. **`evidence-supported` is capped below** `re-executed`/`re-analyzed`; the human may promote. | Keeps mode-native meaning honest and ACM-compatible; a claim settled by inspection isn't *reproduced* in the ACM sense. |
| 10 | Assessment authorship & dimension vocab (§2.1.1) | **Both, evaluator-primary.** **Reconciled set**, not the full set verbatim — artifact-level dimensions are `execution_authenticity`, `trace_report_faithfulness`, `citation_integrity` (+ `limitation_transparency` if reflection in scope). Per-claim axes stay per-claim. | Adopting all 8 double-counts checks we already run per-claim; producers mostly declare evidence, not dimensions. |
| 11 | Weighted aggregation | **Advisory / display-only.** Weights may order findings for the reviewer and render a display composite; **never a scored gating output.** | A weighted scalar collapses per-claim/per-mode nuance and fights evidence-conditioned `unassessable` handling. |
| 12 | Trace schema depth (§2.2.1) | **Terminal-state-only envelope** (`id`/`kind`/`path`/`covers`/`terminal_state`, + optional `counters`). Body stays opaque; no standardized event schema. | An event schema forces a lossy per-producer mapping — the prose-scraping problem the SDK exists to remove. |
| 13 | `gated_by` semantics (§2.4, §3.5) | **Single gate edge for v1** (one attest gates one inspect). No multi-gate lists, no inspect→inspect ordering. Candidate to widen later. | The concrete need is one-to-one (chain-of-custody); multi-gate is expressible by an attest that checks several things. |
| 14 | Ethics/study metadata (§2.7) | **Hybrid**: a few named fields (`ethics_approval`, `consent_basis`, `deidentification`, `sampling`) + an open `extra` sub-map. **Strictly advisory** — absence is a flag, never a hard failure. | Mirrors the license policy; reviewer legibility without over-fitting; the venue PC, not the evaluator, gates on ethics. |
| B1 | `attest`: gate or verdict? (§3, §3.5) | **Both, disambiguated.** As a `gated_by` gate it contributes no verdict; when attest **is** the claim's own mode it yields the `attested` verdict (≤ `PARTIAL`, advisory for badging). | One word hid two roles; conflating them either dropped a real integrity verdict or let a gate masquerade as support. |
| B2 | Does `re-analyze` reach `REPRODUCED`? (§3.1, roll-up) | **Yes, method-badged.** `re-executed` and `re-analyzed` both roll up to `REPRODUCED`; the dashboard badges *re-executed* vs *from released data*. **Revises D6.** | Recomputing reported numbers reproduces the *results* (ACM sense); badging preserves that re-execution is the stronger demonstration. |
| B3 | Missing vs. declared-but-absent evidence (§5.1) | **Distinguished.** *No* declaration → `unassessable` (coverage note). A *declared-but-unresolved* pointer → `unverifiable` + integrity flag — not a silent pass, not a hard `FAILED`. | A dangling pointer is a broken promise, strictly worse than shipping nothing; it must stay visible without tanking the whole rubric. |
| B4 | `claims.yml` authored or generated? (§4.1, §5) | **Generated**, single `validators` schema (producer-owned; regenerated on write). **Resolves A4.** | The producer is the format source of truth; `claims.yml` is regenerated on every write. |

**Still genuinely open** (need external input, tracked outside this spec): OD2–OD5 (tracked separately)
(repo strategy, CAIS profile openness, license, GitHub org). None blocks the object model.

## 12. Deferred / out of scope

- Evaluator support for `v2` (separate milestone; §6).
- Execution of `procedure` validators and `--reproduce` (reproduction milestone).
- Review-side bindings (§10).
- Container image capture/transport (producer-owned; §2.5).
- The open-source release mechanics (MS OSS gates — issue #10, run in parallel).

---

## Appendix A — worked example (API → submission)

```text
a = createArtifact({ id: "expt-42", title: "Feedback-driven contraction" })
addEnvironment(a, { name: "primary",
                    image: { reference: "reg/artifact:1.2", digest: "sha256:abc…" } })
addDataset(a, { id: "sample_corpus",
                location: { kind: "external", uri: "https://example.org/corpus-v3.tar.gz",
                            bytes: 294721271, sha256: "def…", access: "public" },
                prepare: "tar -xzf corpus-v3.tar.gz -C ./data",
                sample: { path: "data/samples/corpus_tiny.parquet", sha256: "aaa…" } })
addExperiment(a, { slug: "posterior_contraction", directory: "experiments/posterior_contraction",
                   run: { command: "python run.py --seed 0", entrypoint: "run.py", seed: 0 },
                   uses_data: [ { dataset: "sample_corpus", at: "data/corpus.parquet" } ],
                   runs_in: "primary" })
addResult(a, { id: "R1", produced_by: "posterior_contraction", validates: ["C1"],
               evidence: "experiments/posterior_contraction/contraction.csv", kind: "metrics",
               locators: { kl_final: { column: "kl_divergence", row: "final" },
                           kl_initial: { column: "kl_divergence", row: "0" } } })
addClaim(a, { id: "C1", statement: "Posterior contraction improves with more feedback rounds.",
              paper_ref: { section: "5.2", figure: "3" },
              validator: { kind: "builtin", name: "monotonic",
                           input: { result: "R1", series: ["kl_initial", "kl_final"] },
                           params: { direction: "decreasing" } } })

# --- [NEW] a qualitative claim: transcript evidence, attest-gates-inspect, a trace, ethics metadata ---
addDataset(a, { id: "interviews",
                location: { kind: "in_artifact", path: "data/interviews/" },
                study: { ethics_approval: "IRB-2025-0142", consent_basis: "informed, opt-in",
                         deidentification: "names redacted", sampling: "convenience; n=18" } })
addTrace(a, { id: "T1", kind: "agent_session", path: "traces/run_0007.jsonl",
              covers: ["posterior_contraction"], terminal_state: "completed_with_outputs" })
addResult(a, { id: "R2", validates: ["C7"], evidence: "data/interviews/",
               kind: "transcript", validation_mode: "inspect",
               support: { excerpts: [ { file: "data/interviews/P07.txt", lines: "40-55" } ],
                          inter_rater_reliability: { metric: "cohen_kappa", value: 0.81 } } })
addClaim(a, { id: "C7", statement: "Participants distrusted the tool's suggestions.",
              paper_ref: { section: "6.1" },
              validators: [
                { id: "v_attest", kind: "attest", checks: "provenance", inputs: ["R2"] },
                { id: "v_inspect", kind: "llm_judge", gated_by: "v_attest",
                  criteria: "The cited excerpts express distrust of the tool's suggestions.",
                  inputs: ["R2"] } ] })
attachPaper(a, { pdf: "paper.pdf", source: "paper/", references_export: "paper_references.yml" })
writeSubmission(a, "./out")     # → ./out/{manifest.yml (+evidence_inventory),claims.yml,results.yml,datasets.yml,traces.yml,paper.pdf,…,SHA256SUMS}
```

The evaluator then reads `./out` (as `evaluable-artifact/v2`): it runs the `monotonic` validator over
`R1` (mode `re-analyze`, deterministic → `re-analyzed`); for `C7` it runs `v_attest` first and, only
if provenance attests, the `v_inspect` rubric (mode `inspect`, advisory → `evidence-supported`, human
final); it re-derives `T1`'s terminal state and flags any disagreement (Trace-Report Faithfulness);
and any dimension whose evidence is absent (e.g. citation integrity if `paper_references.yml` were
missing) is reported as `unassessable` — a coverage note, not a failure. All verdicts reconcile `C1`
and `C7` against the paper's claims (D8) and roll up to the dashboard.
