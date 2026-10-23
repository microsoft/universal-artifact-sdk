> **Audience**: Builders of research-artifact evaluation tools who want to plug in models,
> execution, bibliographic lookup, review profiles, extra checks, or a human decision layer.
> **Source of truth for**: The contracts of every pluggable component, and what each one may and
> may not change.

# 7. Extension points

All extensions share three rules:

- **E1, advisory boundary.** An extension can add evidence or advisory content. It can never
  override a deterministic verdict, set a decision, or write outside the run directory it is
  invoked for.
- **E2, failure is visible.** An extension failure becomes a stage status (`unavailable`,
  `incomplete`, `failed`), a warning, or an `unverifiable` finding. It never crashes the run and
  never becomes a silent pass (I12).
- **E3, recorded identity.** Every extension used in a run is identified by name and version in
  the manifest (`options`, `configuration`, `judge`, or the relevant output file), so two runs can
  be compared.

## 7.1 LLM provider

```text
complete(prompt: text, model: text, system: text | null, call: CallInfo) -> text | null
complete_images(prompt: text, images: [ImageInput], model: text, system: text | null,
                call: CallInfo)
    -> { content: text | null, unavailable_reason: text | null }
ImageInput = { name: text, mime_type: text, bytes: binary }
CallInfo   = { role: text, attempt: int }   # role: table below; attempt: 1-based within the role call
```

**Call roles and response shapes (normative).** The tool passes, with every call, the role that
is calling and the 1-based attempt number (a repair prompt, §5.6.1, is attempt 2, 3, …; it
keeps the role). A real provider MAY ignore `CallInfo`; a test double uses it to script
responses (§8.5.1). The response is JSON text whose top-level shape is fixed per role:

| Role ID | Caller | Response shape (JSON) |
|---------|--------|-----------------------|
| `specialist/contribution`, `specialist/originality-impact`, `specialist/soundness`, `specialist/author-guidance`, `specialist/presentation` | §5.4 | `{"findings": [F, …]}` |
| `contribution-review/contribution`, `contribution-review/originality-impact` | §5.13.4 (re-run over the artifact bundle) | `{"findings": [F, …]}` |
| `synthesis` | §5.8 | `{"contribution_summary": s, "originality": s, "likely_impact": s, "decision_synthesis": s, "contribution_evidence": [c, …], "originality_evidence": [c, …], "impact_evidence": [c, …]}` |
| `contribution-digest` | §5.13.2 | `{"contributions": [{"title": s, "summary": s, "quote": s, "candidate_ids": [id, …], "claim_ids": [id, …]}, …]}` |
| `visual/interpret`, `artifact-visual/interpret` (image calls) | §5.9 step 3, §5.10.3 | `{"observations": [{"check": s, "classification": "agreement" \| "mismatch" \| "unresolved", "visual_observation": s, "paper_quote": s, "explanation": s, "figure"?: s, "region"?: [x0, y0, x1, y1] \| null}, …]}` |
| `visual/confirm`, `artifact-visual/confirm` (image calls) | §5.9 step 4 | `{"comparisons": [{"index": int, "check": s, "classification": "agreement" \| "mismatch" \| "unresolved", "paper_quote": s, "visual_observation": s, "explanation": s}, …]}` |
| `run-evidence` | §5.10.4 | `{"observations": [{"claim_id": id, "result_id": id, "classification": "corroboration" \| "qualification" \| "contradiction" \| "unresolved", "summary": s, "reasoning": s, "paper_quote": s, "evidence_quotes": [{"citation": c, "quote": s}, …]}, …]}` |
| `adapter/extractor`, `adapter/verifier`, `judge/*` | §3.7, §4.10 | Implementation-defined (not scripted by conformance). |

`s` is a string, `c` a citation ID (§5.3.2), `id` a claim, result, or candidate ID. `F` is a
reviewer finding (§5.5) **as the model writes it**: the fields marked "model" in the §5.5 field
table. The fields marked "tool" there are assigned by the tool and overwrite any value the
model supplies; fields not in the table are dropped (§5.5). Unknown top-level keys are ignored; a missing
array key or a non-object response is a validation error that triggers recovery (§5.6.1). The
deterministic critique (§5.6.2) makes no model call; `critic` in the per-role model list below
is reserved for implementations that add one.

- `null`/`unavailable_reason` means "no usable response". Missing credentials, network errors,
  timeouts, malformed responses, and refusals all map to it. Providers MUST NOT raise to the
  caller.
- Transport retries, backoff, rate limiting, and timeouts belong **inside** the provider. The
  pipeline's own retry is only the response-recovery loop (§5.6), which re-asks after an
  **invalid** response.
- Images are passed as bytes, never as file-system paths. A provider without image support
  returns `unavailable_reason` for every image call; it MUST NOT fall back to describing an image
  from text.
- Each call is independent: no conversation state is carried between calls, so specialists
  cannot see each other's output (§5.4).
- Credentials are read from the environment or a secret store and are never written to the run.
  Only the provider ID and model ID are recorded.
- Model selection can be per role (extractor, verifier, substantiator, specialist, critic,
  synthesizer, contribution digest, visual). Precedence: explicit per-role option, then a general option, then the
  provider default.
- Every prompt MUST demand JSON-only output, and every parser MUST be defensive (§5.5). Model
  text is untrusted (I11).

**No provider configured** is a supported, first-class configuration (§5.11).

## 7.2 Reproduction provider

```text
reproduce(artifact_snapshot: path, experiment: Experiment, workdir: path, budget: Budget)
    -> ExecutionRecord
```

- The provider receives a **copy** of the snapshot inside `<run>/reproduction/<slug>/`, never the
  original artifact (I1).
- It MAY edit files in its copy to make an experiment run. Every such edit is a **repair**,
  recorded as a unified diff against the snapshot in `repairs/`, with a one-line reason each.
- Regenerated outputs go under `<run>/reproduction/<slug>/outputs/`. They never replace shipped
  evidence. The judge evaluates validators against regenerated outputs and compares them to the
  shipped evidence (§4.9).
- `ExecutionRecord` (written as `execution.json`): command, environment description (image or
  interpreter and dependency lock hash), start/end time, exit status, wall time, resource caps
  applied, repair count, output inventory with hashes, and `status` ∈ `completed`, `failed`,
  `timeout`, `skipped`.
- Execution MUST be sandboxed: no network unless the experiment declares it and the caller allows
  it; bounded time, memory, and disk; no access outside `workdir`.
- When used, the manifest's `judge.activity` becomes `reproduction` and
  `judge.submission_executed` becomes `true` (§6.3).

## 7.3 Reference resolver

```text
resolve(reference: { id, raw, title?, authors?, year?, doi?, url? }) -> {
  status: "verified" | "unverified" | "error",
  matched_title: text | null, matched_id: text | null, reason: text | null }
```

- Backed by one or more public bibliographic indexes. Matching rule: an identifier match (DOI,
  arXiv ID, or similar) verifies the reference. Otherwise, a normalized title match plus at least
  one agreeing author surname or year within ±1 verifies it.
- `unverified` means "searched and not found"; it is never proof of fabrication. `error` means
  the lookup failed. A resolver that is unreachable yields `unchecked` for everything (§6.6.2).
- Results are cacheable by reference text hash. The cache is not part of the run.

## 7.4 Review profiles and packs

Venue profiles, area packs, and methodology packs (§5.2) are data, not code. A profile or pack
is a versioned document (`<name>/v<N>`) containing:

- display name and short description;
- a list of criteria, each with ID, question, and the specialist(s) responsible;
- emphasis weights or ordering hints used by the critic's ranking (§5.7);
- for venues: the review-form section list used to lay out the draft (§5.12);
- standard references (§9.1) supporting each criterion.

Rules:

- A pack can **add** criteria and **reweight** ranking. It cannot remove the writing-quality
  criteria (§5.4), the citation rules (§5.3), the three contribution-axis criteria
  (`claim_support`, `significance_and_relevance`, `novelty_and_related_work`, §5.13.3), or any
  invariant.
- The resolved configuration and its digest are recorded in the run (§5.2), so a review can be
  traced to the exact profile text.
- Unknown profile names are a configuration error (exit status 2).

## 7.5 Custom checks and validators

**Custom check:**

```text
check(artifact: LoadedArtifact, context: { paper_text?, run_dir, options }) -> [Finding]
```

- Runs after the builtin checks, in a stable order (by registered name).
- Its findings MUST use its own check name as the ID prefix and MUST follow the finding schema
  (§4.2), including evidence pointers.
- A custom check MAY set a mode verdict only by evaluating artifact evidence deterministically.
  Anything model-based is advisory.
- A custom check MUST NOT modify other findings.

**Custom validator kind:**

```text
validate(params: map, evidence: ResolvedEvidence, result: Result) -> { passed: bool | null, detail: text }
```

- `null` means "cannot be evaluated" and maps to `unverifiable`.
- MUST NOT reuse any builtin catalog name (§4.6). An artifact that uses a validator kind the
  implementation does not know gets `unverifiable` for that claim, with the unknown kind named in
  `detail`.
- MUST be deterministic and side-effect free.

## 7.6 Human-in-the-loop layer

The tool deliberately stops at advisory analysis (I4). A decision layer, such as an interactive
review console, a program-committee workflow, or an artifact evaluation committee's badge sign-off,
is built **on top of** sealed runs:

- It reads a run only after consumer validation (§6.7).
- It MUST NOT modify any file in the run. Decisions, scores, comments, and accepted/rejected
  finding marks go to a **sidecar** keyed by `run_id` and `input_digest`, or into a new run.
- A sidecar SHOULD record who decided, when, and which finding IDs (finding IDs, §5.5) each
  decision refers to. Because finding IDs are stable across re-runs on identical input, decisions
  can be carried forward and their staleness detected when `input_digest` changes.
- Interactive question-answering about an artifact, if offered, MUST follow the same evidence
  rules as the reviewer: cite the snapshot or answer "unverifiable".
- The human layer, not the tool, fills `human_owned` (§6.5), and only in its own sidecar.
- **Contribution qualification** is human-owned too. The sealed run always has
  `human_qualification: null` (§5.13.4). A human layer MAY record, per contribution ID (full,
  never truncated) and per run, whether the contribution qualifies, together with its own
  originality search (sources inspected, cutoff, what was not inspected). That record lives in
  the sidecar, keeps the three axes separate, and MUST NOT be written back into the run or into
  the artifact's `contributions.yml` (the SDK has no qualification field).

## 7.7 Multi-reviewer panels (optional)

An implementation MAY run the reviewer pipeline several times with different provider/model
pairs ("arms") and present the drafts side by side. If it does:

- each arm is its own run directory, or a clearly separated sub-tree with its own findings;
- arms MUST use distinct provider/model pairs;
- any merge across arms is itself advisory and recorded with its method; disagreement between
  arms is surfaced, not averaged away.
