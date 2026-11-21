> **Audience**: Builders of tools that consume Universal Artifact SDK artifacts (judges,
> reviewers, explorers, benchmark writers), human or AI.
> **Source of truth for**: How a consumer opens an artifact: locating and parsing its files,
> the repairs it applies to imperfect input, when it may reject, the artifact kind, the content
> digest, the read-only rule, and the evaluation record that tells which stage an artifact is in.

# Artifact Reader — Specification

**Spec ID:** `artifact-reader/v1` · **Status:** DRAFT · **Input contract:** `evaluable-artifact/v3`
and `evaluable-artifact/v2` as defined by [`SPEC.md`](../../SPEC.md)

Artifacts are expensive to produce, and real ones are often slightly wrong: an index file with the
wrong top-level key, an evidence path with a typo, a stale evidence inventory, a version string
from a newer writer. A consumer that rejects such an artifact loses a whole evaluation over a
defect that should cost one finding. This specification defines **one forgiving reader** that
every consumer uses, so that all tools accept the same artifacts and report the same defects.

The SDK's writer stays strict: `writeSubmission` and structural validation (SPEC §4, §5) still
refuse to *produce* a malformed artifact. The reader is the other half: it *accepts* anything that
can still be evaluated, repairs what it can, and records every repair.

Example. An artifact's `results.yml` holds a bare list instead of `{results: [...]}`, and one
result's `evidence` is `Results/summary.json` while the file is `results/summary.json`. A strict
reader would refuse the artifact or drop every result. This reader reads the list (repair
`RD-INDEX-BARE-LIST`), resolves the evidence by its case-insensitive match (`RD-PATH-CASE`), and
returns both repairs as warnings. The judge then evaluates every result and reports the two
repairs as findings.

## 1. Principles

| # | Principle |
|---|-----------|
| P1 | **Accept what can be evaluated.** The reader rejects an input only under §5. Every other defect is repaired or recorded, never fatal. |
| P2 | **Every repair is visible.** Each repair produces a warning with a stable code (§4). Consumers report warnings; a judge reports them as findings. |
| P3 | **Leniency never weakens safety.** Path safety (§3.4) is not relaxed. An unsafe path is unresolved, not repaired. Leniency applies to shape, not to trust. |
| P4 | **Contents win over declarations.** Where the artifact declares a fact the reader can compute (evidence inventory, artifact kind), the computed value is used and a mismatch is a warning. |
| P5 | **The artifact is read-only.** The reader and every consumer never write inside the artifact and never need to copy it (§7). |
| P6 | **Same input, same read.** Given identical bytes, two conforming readers produce the same read model and the same warnings (§8). |

## 2. Inputs

| Form | Handling |
|------|----------|
| Directory | Read in place. |
| Archive (`.zip`, `.tar`, `.tar.gz`, `.tgz`) | Extracted to a private temporary directory owned by the consumer, then read as a directory. Members with unsafe names (§3.4), links, or special files are skipped (`RD-ARCHIVE-MEMBER-SKIPPED`). |
| Single paper file (any name ending `.pdf`, `.tex`, or `.md`) | Read as an artifact with no manifest whose only file is that paper; it is the paper of record and text source, whatever its name. Kind `paper-only`. Warnings: `RD-MANIFEST-ABSENT` only. |

**Root location.** The artifact root is the input directory, unless that directory holds no
`manifest.yml` (or §3.1 case B variant), holds exactly one subdirectory (ignoring `__MACOSX` and
names starting with `.`), and that subdirectory holds a manifest; then that subdirectory is the root
(`RD-ROOT-NESTED`). Loose files beside the subdirectory do not prevent this. This handles a zip that
wraps the artifact in a folder.

## 3. Reading

### 3.1 Manifest

| Case | Condition | Handling |
|------|-----------|----------|
| A | `manifest.yml` parses to a mapping | Normal read. |
| B | No `manifest.yml`, but `manifest.yaml` or a letter-case variant of either exists at the root | Read it (`RD-MANIFEST-NAME`). If several exist, the first in code-point order. |
| C | The manifest exists but is not UTF-8, does not parse, or is not a mapping | Treat as absent (`RD-MANIFEST-UNREADABLE`) and continue as case D. |
| D | No manifest | Use an empty manifest; find indexes and the paper by probing (§3.3) (`RD-MANIFEST-ABSENT`). |

**Version.**

| `format_version` | Handling |
|------------------|----------|
| `evaluable-artifact/v3`, `evaluable-artifact/v2` | Native rules for that version. |
| `evaluable-artifact/vN`, N > 3 | Read with the v3 rules; unknown fields preserved (`RD-VERSION-NEWER`). |
| `evaluable-artifact/v1`, missing, empty, or any other value | Read with the v3 rules (`RD-VERSION-UNKNOWN`). When the manifest itself is absent (case D) the declared version is `null` and only `RD-MANIFEST-ABSENT` is reported. |

The declared value is kept verbatim in the read model. `sdk_version`, `producer`, `origin`, and
unknown manifest keys are preserved and never change behavior, except where §6 or JR §3.3
(paper-origin artifacts) say otherwise.

### 3.2 Index files

Each index (`claims`, `results`, `exhibits`, `datasets`, `traces`, `assessments`, `journal`, and in
v3 `contributions`) is located as JR §2.3.1 says: through `paths.<name>`, else at its default file
name; contributions only through `paths.contributions`. A declared `paths.<name>` is first resolved
like any declared path (§3.4): `RD-PATH-CASE` may repair it; if it is unsafe (`RD-PATH-UNSAFE`) the
index is empty and the default name is **not** tried. The reader then applies these rules in order:

| Code | Condition | Repair |
|------|-----------|--------|
| `RD-INDEX-DECLARED-MISSING` | `paths.<name>` names a file that does not exist, and the default file exists | Read the default file. |
| `RD-INDEX-NAME` | Neither exists, but a `.yaml` or letter-case variant of the default name exists at the root | Read it. |
| `RD-INDEX-UNREADABLE` | The file is not UTF-8 or does not parse | Index is empty. |
| `RD-INDEX-BARE-LIST` | Top level is a list | Use the list. |
| `RD-INDEX-KEY` | Top level is a mapping without the expected key, and exactly one of its keys other than `_generated` holds a list | Use that list. |
| `RD-INDEX-NO-LIST` | None of the above yields a list (including an empty file and `claims: null`) | Index is empty. |
| `RD-RECORD-NOT-MAPPING` | A list element is not a mapping | Skip it. |

Absence is not a defect: an index that is neither declared nor found is empty with **no** warning
(JR §2.3). Journal entries (SPEC §2.8) have no IDs; the ID rules of §3.4 do not apply to them.

**YAML.** UTF-8, a leading byte-order mark ignored, YAML 1.2 core schema (SPEC §5). A repeated key
makes **that file** unparsable (`RD-INDEX-UNREADABLE`, or case C for the manifest); the rest of the
artifact is read normally. The reader does not guess at malformed YAML.

### 3.3 Discovery probes

The reader adopts the probes of explorer §2.6 unchanged (paper PDF, paper source, README), used
only when nothing declares the role. When the manifest is absent (case D), indexes are probed at
their default names (§3.2). Without a manifest an artifact has no experiments; code found on disk
appears in `unindexed_files` (§8) but is not treated as runnable.

### 3.4 Records, references, and paths

| Code | Condition | Repair |
|------|-----------|--------|
| `RD-ID-TYPE` | An `id`, `slug`, or reference is a number or boolean | Use its YAML 1.2 string form (`7` → `"7"`). |
| `RD-ID-MISSING` | A record lacks its `id` (`slug` for experiments) | Assign `<collection>#<1-based position in the file's list, counting skipped elements>`, e.g. `claims#3`; if that equals a declared ID, append `#2`, `#3`, … to it until unique. |
| `RD-ID-DUPLICATE` | Two records of one collection share an ID | Keep both in order; lookups resolve to the first (explorer §2.3). |
| `RD-FIELD-SINGULAR` | A list-valued field holds a scalar or a single mapping (`validates: C1`), or the singular key is used (`validator:` for `validators:`) | Wrap it in a one-element list. |
| `RD-FIELD-TYPE` | A known field has an unusable type (e.g. `statement` is a list) | Treat the field as absent; keep the raw value in `extra`. |
| `RD-REF-DANGLING` | A reference names no record of its target collection: `validates`, `supporting_claims` → claims; `produced_by`, `tested_by`, `depends_on` → experiments; validator `inputs` → results; `uses_data[].dataset` → datasets | Keep it; it resolves to nothing. |
| `RD-PATH-CASE` | A declared path does not exist, and exactly one existing path differs from it only in letter case | Resolve to that path. |
| `RD-PATH-UNRESOLVED` | A declared path does not exist (after `RD-PATH-CASE`) | Unresolved. |
| `RD-PATH-UNSAFE` | A declared path fails JR §2.4 (absolute, drive or backslash form, `.`/`..` segment, escapes the root, is or traverses a symbolic link) | Unresolved. **Never repaired** (P3). |
| `RD-SPECIAL-FILE` | A symbolic link, device, socket, or FIFO exists anywhere in the tree | Excluded from the read model and the content digest (§7.1); never followed. |

Unknown fields on any record are preserved in `extra` and never interpreted. `run.working_dir`
resolves against the artifact root; `run.entrypoint` resolves against `run.working_dir` when
declared, else the root. Neither is a declared path: they get no `paths` entry and no
`RD-PATH-*` warning, because a `spec-artifact`'s entrypoint does not exist until someone implements
it. They feed kind derivation (§6) only; the AEBench writer checks the entrypoint (Writer §7.2).

### 3.5 Evidence inventory

The reader **always computes** the evidence inventory (SPEC §5.1) from what it read, using the
meaning each key's comment gives there. A `has_*` key that names a file (`has_paper_source`,
`has_citations_export`, `has_research_agent`) is true only when the declared path resolves.
`validation_modes` collects the modes declared explicitly on results and exhibits; it is not inferred
from validator kinds. `has_runnable_experiments` is true when the derived kind
(§6) is `full-artifact`. A declared `evidence_inventory` is kept for display. Each declared key whose
value differs from the computed value yields `RD-INVENTORY-MISMATCH` naming the key; list values are
compared as sets, and declared keys the reader does not compute are ignored. Consumers act on the computed inventory only
(P4).

## 4. Warnings

A warning is `{code, path, message}`: `code` from §2, §3, or §6; `path` is the artifact-relative
file, followed for record-level warnings by `#` and the record locator (e.g.
`results.yml#R3.evidence`); `message` is free text. The record locator is `<id>.<field>` (experiments: `<slug>.<field>`); a
record without a usable ID uses `<collection>[<0-based index>]`. Warnings are sorted by `path`, then `code`,
then `message`, in code-point order.

Consumers MUST show every warning (P2). A judge reports each as a structure finding: severity
`warning` for `RD-PATH-*`, `RD-REF-DANGLING`, `RD-INVENTORY-MISMATCH`, and `RD-KIND-MISMATCH`,
severity `info` for the rest. A repair alone MUST NOT change a claim verdict: a result whose
evidence resolved through `RD-PATH-CASE` is judged on that evidence.

## 5. Rejection

The reader rejects an input (consumers map this to exit status 2) **only** when:

1. the input does not exist, cannot be read, or is an archive that cannot be opened; or
2. after reading, there is **nothing to evaluate**: no paper resolves, and claims, experiments,
   and results are all empty.

A rejection message lists every warning gathered before it. Nothing else rejects: not the version,
not a broken index, not an unsafe path, not a special file.

## 6. Artifact kind

The **artifact kind** says what an evaluator can do with an artifact. The reader derives it from
the read model, ignoring experiment `disposition`; the first matching row wins.

| Kind | Rule | Supports |
|------|------|----------|
| `full-artifact` | ≥1 experiment whose `implementation.kind` is `code` or absent, with a non-empty `run.command` and a `directory` that resolves to a directory containing at least one regular file (at any depth) | Re-executing shipped code. |
| `spec-artifact` | ≥1 experiment whose `implementation.kind` is `spec` and whose `implementation.spec` resolves to a file | Re-implementing from specification, then executing. |
| `paper+evidence` | ≥1 result, trace, or exhibit whose path resolves, or ≥1 dataset that is `external` or resolves `in_artifact` | Re-analysis and inspection; no execution. |
| `paper-only` | Anything else that passes §5 | Paper review only. |

`implementation` is an optional experiment field: `{kind: code | spec, spec?: <path>, check?:
<command>}`. `kind: spec` means the experiment's code is **not shipped**; the file at `spec` defines
what the code must do precisely enough to re-implement it, and `run.command` is the command to run
once it exists. `check` is a command that exits 0 if and only if the implementation is in place and
its specified tests pass.

A producer MAY declare `artifact_kind` at the manifest root (the SDK writer SHOULD compute it as
it computes the evidence inventory). If it differs from the derived kind, the reader records
`RD-KIND-MISMATCH` and consumers use the derived kind (P4).

Example. The Benford example artifact ([`examples/benford-e2e/artifact/`](../../examples/benford-e2e/artifact/))
ships no code. Each experiment declares `implementation: {kind: spec, spec: specs/<module>.md}`, so
its kind is `spec-artifact`. An AEBench case built from it asks the agent to implement the specs,
run the commands, and leave the outputs for the oracle
([AEBench writer](../aebench-writer-spec/README.md)).

## 7. Read-only use, identity, and stage

### 7.1 Content digest

The **content digest** identifies an artifact's bytes independent of where it is stored, so that
evaluations can refer to it without copying it.

1. List every regular file under the root, excluding the directories `.git`, `.hg`, `.svn`, and
   `__pycache__` at any depth (as JR §2.5 does) and the special files of `RD-SPECIAL-FILE`.
2. For each file form the line `<lowercase sha256 hex>␠␠<relative path, "/"-separated>\n`.
3. Sort the lines by the UTF-8 bytes of the path and concatenate them.
4. The content digest is `sha256:` followed by the SHA-256 hex of the concatenation.

The artifact's own `SHA256SUMS` is hashed like any other file; it is never trusted in place of
hashing.

### 7.2 No writes, no copies

A consumer MUST NOT create, modify, or delete anything inside the artifact root, including `.git`,
lock files, and caches. It SHOULD NOT copy the artifact. To show that it evaluated the bytes it
names, it records the per-file hashes of §7.1 when it starts and, when it finishes, re-verifies
that every file it read still has its recorded hash; a mismatch fails the evaluation. This is
**snapshot by reference**. Copying (JR §2.5) remains allowed for small artifacts, and a consumer
that copies MUST still record the content digest.

Large inputs belong outside the artifact as `external` datasets (SPEC §2.7) with `uri` and `sha256`.
Whoever runs the experiments fetches them into their own workspace, never into the artifact.

### 7.3 Evaluation record and stage

Every evaluation (a judge run, a review, an AEBench run, a human assessment) writes an
`evaluation-record.yml` **in its own output directory**:

```yaml
record_version: evaluation-record/v1
artifact:
  id: benford-population-conformity        # manifest id, or null
  content_digest: "sha256:…"                # §7.1
  location: examples/benford-e2e/artifact   # where it was read; informational only
  kind: spec-artifact                       # §6, derived
evaluator:
  type: aebench                             # judge | reviewer | aebench | human | <other>
  name: AEBench
  version: 0e93841
  config: {case: uas_benford_population, agent: example-agent, model: example-model}
started_at: "2026-11-20T21:00:00Z"
finished_at: "2026-11-20T21:40:00Z"
status: completed                           # completed | failed | aborted
outcome: {score: 4, expected_score: 4}      # evaluator-defined summary
outputs: [oracle/report.json]               # paths relative to this record
reader_warnings: 2                          # count of §4 warnings
```

An artifact's **stage** is derived, never written into the artifact:

- `pre-evaluation` — no known evaluation record carries its content digest;
- `evaluated` — at least one does; the stage lists their `evaluator.type` values, e.g.
  `evaluated: [judge, reviewer, aebench]`.

"Known" records are those a tool is pointed at (a runs directory, a results registry). Because the
digest depends only on content, an edited artifact is a new artifact at `pre-evaluation`, and
evaluations of the earlier bytes stay attached to them.

## 8. Read model

The reader returns one object. Its JSON form (keys sorted, UTF-8) is the conformance surface.

| Key | Content |
|-----|---------|
| `root` | `"."` or the nested directory name (§2). |
| `format_version` | `{declared: <string or null>, read_as: "v2" or "v3"}`. |
| `manifest` | The repaired manifest mapping without `experiments`; unknown keys preserved. |
| `collections` | `experiments`, `claims`, `results`, `exhibits`, `datasets`, `traces`, `assessments`, `journal`, `contributions`: repaired record lists in declaration order. Each record holds the fields its SDK object defines (SPEC §2, repaired) plus `extra`, a mapping of every other key. |
| `paths` | Every declared path by record locator → `{resolved: <relative path or null>, code?}`. A locator is `<index file>#<record id>.<field path>` (e.g. `results.yml#R1.evidence`, `manifest.yml#e1.directory`, `manifest.yml#paths.claims`); a record with a missing or duplicate ID uses `<index file>#[<0-based position>].<field path>`. List elements append `[<i>]` (e.g. `results.yml#R1.validators[0].input.path`). |
| `paper` | `{of_record, text_source}` as JR §2.3.2 defines them; each a relative path or `null`. |
| `evidence_inventory` | `{declared, computed}`. |
| `artifact_kind` | `{declared, derived}`. |
| `content_digest` | §7.1. |
| `unindexed_files` | Regular files that are not the manifest, an index file, a resolved declared path, inside a resolved experiment `directory`, or a probed paper or README; sorted. |
| `warnings` | §4. |

## 9. Conformance

Each scenario starts from the **base fixture**: a v3 artifact with `manifest.yml` (`id: demo`,
`title: Demo`, one experiment `{slug: e1, directory: e1, run: {command: python run.py, working_dir: e1}}`),
`e1/run.py`, `claims.yml` with claim `C1`, `results.yml` with `R1` (`validates: [C1]`,
`evidence: out/r1.json`, `kind: metrics`), `out/r1.json`, and `paper.pdf`.

| ID | Change to the base fixture | Expected |
|----|----------------------------|----------|
| RD1 | None | No warnings; kind `full-artifact`. |
| RD2 | `format_version: evaluable-artifact/v9` | Read; `RD-VERSION-NEWER`; collections as RD1. |
| RD3 | `format_version` removed | Read; `RD-VERSION-UNKNOWN`. |
| RD4 | `manifest.yml` contents replaced by `: : :` | `RD-MANIFEST-UNREADABLE` and `RD-MANIFEST-ABSENT`; `C1` and `R1` found by probing; no experiments; kind `paper+evidence`. |
| RD5 | Artifact zipped inside a folder `demo/` | `RD-ROOT-NESTED`; otherwise as RD1. |
| RD6 | `results.yml` holds a bare list | `RD-INDEX-BARE-LIST`; `R1` read. |
| RD7 | `claims.yml` top-level key is `claim` | `RD-INDEX-KEY`; `C1` read. |
| RD8 | `R1.evidence: OUT/r1.json` | `RD-PATH-CASE`; resolves to `out/r1.json`. |
| RD9 | `R1.evidence: ../secret.json` | `RD-PATH-UNSAFE`; unresolved. |
| RD10 | `R1.validates: C1` | `RD-FIELD-SINGULAR`; `validates` is `["C1"]`. |
| RD11 | `R1.validates: [C9]` | `RD-REF-DANGLING`. |
| RD12 | `C1` has no `id` | `RD-ID-MISSING`; ID `claims#1`; `R1.validates` dangles (`RD-REF-DANGLING`). |
| RD13 | Symbolic link `link` → `out/r1.json` added | `RD-SPECIAL-FILE`; content digest equals RD1's. |
| RD14 | `evidence_inventory: {has_traces: true}` declared | `RD-INVENTORY-MISMATCH` for `has_traces`; computed `false`. |
| RD15 | `e1` gets `implementation: {kind: spec, spec: specs/e1.md}`; `e1/run.py` removed; `e1/README.md` and `specs/e1.md` added | Kind `spec-artifact`. |
| RD16 | RD15 plus `artifact_kind: full-artifact` | `RD-KIND-MISMATCH`; derived `spec-artifact`. |
| RD17 | `paper.pdf`, `claims.yml`, `results.yml`, and the experiment removed | Rejected (§5). |
| RD18 | Input is a single `paper.pdf` | Kind `paper-only`. |
| RD19 | RD1 read twice, and from a copy at another location | Identical read models (except `artifact` location, which is not in the read model) and content digests. |
| RD20 | Every scenario | The artifact's file list and bytes are unchanged after reading. |

## 10. Relation to other specifications

- **SPEC.md** defines the format; this specification defines how consumers read imperfect
  instances of it. It introduces optional fields — experiment `implementation`, manifest
  `artifact_kind`, and (in the AEBench writer) result `output_path` — all additive (the v3 schema
  allows additional properties). *(Pending: SPEC.md §2.2, §2.3, §5.1 and the schema to document
  them.)*
- **Judge and reviewer** ([JR §2](../judge-reviewer-spec/02-inputs.md)) and **explorer**
  ([§2](../artifact-explorer-spec/02-inputs.md)) read artifacts through this reader. The
  version gates of JR §2.2 rule 1 and explorer §2.2, and the symbolic-link rejection of JR §2.5
  rule 1, are superseded by §3.1 and `RD-SPECIAL-FILE`; conformance scenarios JR J2 and explorer
  X3 change to expect a read with `RD-VERSION-NEWER`. Path safety, paper selection, and text
  extraction are unchanged. *(Pending: those documents are not yet edited to point here.)*
- **AEBench writer** ([`../aebench-writer-spec/README.md`](../aebench-writer-spec/README.md))
  consumes the read model.
