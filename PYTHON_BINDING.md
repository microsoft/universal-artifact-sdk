# Python binding design

> **Status:** Accepted for implementation
>
> **Audience:** SDK maintainers, Python contributors, and release owners
>
> **Source of truth for:** the Python package layout, API conventions, cross-binding
> conformance, testing strategy, and PyPI release process
>
> **Normative model:** [`SPEC.md`](SPEC.md) and
> [`schema/evaluable-artifact-v2.schema.json`](schema/evaluable-artifact-v2.schema.json)

## 1. Purpose

The Python package is a first-class producer binding for `artifact-sdk/v1`. It builds,
validates, writes, and reopens the same `evaluable-artifact/v2` submissions as the
TypeScript package.

The binding is not a wrapper around Node.js and does not invoke the TypeScript package.
It is a native Python implementation with an idiomatic API, tested against the same
language-neutral contract.

## 2. Decisions

| Topic | Decision |
|---|---|
| Distribution | PyPI `universal-artifact-sdk` |
| Import package | `universal_artifact_sdk` |
| Python support | Python 3.10 and later |
| Versioning | Lockstep with `@microsoft/universal-artifact-sdk` |
| Models | Authored Python dataclasses; no generated binding code |
| Public naming | Idiomatic `snake_case` functions and fields |
| Cross-binding parity | Semantic equivalence, not byte identity |
| Validation authority | Frozen TypeScript behavior initially; schema plus relational validation is the post-freeze target |
| YAML | YAML 1.2 through `ruamel.yaml` |
| Release | PyPI trusted publishing with provenance |

The TypeScript and Python distributions use the same release version because they
implement one SDK contract. A release is complete only when both packages pass their
independent package checks. The `sdk_version` written into submissions remains the
contract identifier `artifact-sdk/v1`, not the distribution version.

The current TypeScript API and implementation are frozen while an experiment depends
on their behavior. This effort MUST NOT modify files under `src/`, change TypeScript
exports, or intentionally change TypeScript output. Contract inconsistencies discovered
during the Python work are tracked in
[issue #32](https://github.com/microsoft/universal-artifact-sdk/issues/32) for
post-experiment correction.

## 3. Repository and package layout

The repository remains a single project with one canonical schema:

```text
.
├── schema/
│   └── evaluable-artifact-v2.schema.json
├── src/                         # TypeScript binding
├── test/                        # TypeScript tests and shared source fixtures
├── python/
│   ├── src/universal_artifact_sdk/
│   │   ├── __init__.py
│   │   ├── builder.py
│   │   ├── inventory.py
│   │   ├── model.py
│   │   ├── open.py
│   │   ├── serialize.py
│   │   ├── validate.py
│   │   └── py.typed
│   ├── tests/
│   └── examples/
│       └── quickstart.py
├── parity/                      # language-neutral conformance cases
│   ├── case.schema.json
│   ├── cases/
│   ├── expected/
│   └── fixtures/
└── pyproject.toml
```

`pyproject.toml` lives at the repository root so the wheel can include the root
canonical schema without copying it into a second source tree. The wheel installs that
schema as package data under
`universal_artifact_sdk/schema/`. The repository copy remains the only authored source.
Hatchling is the build backend; its force-include configuration maps the root schema
into wheels and source distributions. Editable installs resolve the schema from the
repository root when the packaged resource is absent.

## 4. Public API

### 4.1 Naming

Python uses `snake_case`:

| Language-neutral operation | Python |
|---|---|
| `createArtifact` | `create_artifact` |
| `openSubmission` | `open_submission` |
| `writeSubmission` | `write_submission` |
| `validateStructure` | `validate_structure` |
| `computeEvidenceInventory` | `compute_evidence_inventory` |
| `addEnvironment` | `add_environment` |
| `addDataset` | `add_dataset` |
| `addExperiment` | `add_experiment` |
| `addTrace` | `add_trace` |
| `addResult` | `add_result` |
| `addExhibit` | `add_exhibit` |
| `addClaim` | `add_claim` |
| `addAssessment` | `add_assessment` |
| `attachPaper` | `attach_paper` |
| `attachResearchAgent` | `attach_research_agent` |
| `configureJournal` | `configure_journal` |

The remaining `get*`, `list*`, `remove*`, experiment-lifecycle, journal, reflection,
default-mode, inventory, and digest helpers follow the same mechanical conversion.
CamelCase aliases are not exported.

Serialized field names remain the schema's `snake_case` names in both bindings.

### 4.2 Models and inputs

Public model objects are mutable `@dataclass` classes with type annotations. Nested
schema objects such as `Image`, `RunSpec`, `PaperReference`, and validator variants are
also dataclasses. Nested schema models carry an *extension bucket* — a
`dict[str, Any]` field used to round-trip legal extension keys that the binding does not
understand. Serialization merges the bucket first and known fields second so extensions
cannot override contract fields. The bucket is named `extra` on every model except
`StudyMetadata`: spec §2.7 defines `study.extra` as a real nested field (an open sub-map
of venue-specific study metadata), so that model serializes `extra` as a normal field and
overflows unknown sibling keys into `extensions` instead. `model.extension_field` names
each model's bucket, and `to_dict`/`artifact_from_dict` are generic over it, so the public
schema field name `extra` is unchanged in both roles. The initial root `Artifact` model
drops unknown top-level manifest keys when reopened, matching the frozen TypeScript
implementation; preserving those keys is deferred to issue #32.

Python treats an explicitly null *optional model field* as omitted. This is the one
documented freeze-period validation divergence: the frozen TypeScript validator rejects
null for some optional fields because it distinguishes null from undefined. Python does
not add hidden field-presence state solely to reproduce that inconsistency; issue #32
tracks post-freeze reconciliation.

That rule stops at the edge of an opaque map. A null **value inside a producer-authored
mapping** — `producer`, `run.env`, a trace's `counters`, a result's `locators`, a
validator's `input`/`params`, or any nested extension object — is producer data, not an
absent field, so `to_dict` and `write_submission` preserve it verbatim exactly as the
frozen TypeScript binding does. The same split governs default values: an optional field
the producer omitted, such as a non-active `disposition.rationale`, stays absent rather
than being materialized as an empty string on write.

Open vocabularies use `str` with documented known constants rather than closed Python
`Enum` classes. Open vocabularies include result kind, exhibit type, trace kind, and
assessment dimension. Closed vocabularies include validation mode, disposition status,
claim stance, validator kind, assessment scope, and the schema's trace terminal state.
An unknown exhibit type retains the frozen TypeScript warning behavior.

Builder functions accept model instances:

```python
artifact = create_artifact(id="expt-42", title="Feedback-driven contraction")

add_environment(
    artifact,
    Environment(
        name="primary",
        image=Image(reference="reg/artifact:1.2", digest="sha256:abc..."),
    ),
)
```

`add_claim` accepts `Claim` or `AddClaimInput`. The latter supports either
`validators=[...]` or singular `validator=...`, matching the language-neutral
convenience defined by `SPEC.md`. When both are supplied, `validators` wins, matching
the frozen TypeScript implementation. Like the TypeScript `addClaim` reconstruction,
this operation drops unknown input keys rather than carrying them into the stored
claim; reopen-and-write without re-adding the claim still preserves nested claim
extensions.

All mutating functions accept an optional keyword-only `ctx: ChangeContext | None`.
`configure_journal(..., on_missing_rationale=...)` accepts a synchronous callable. An
async callback is outside `artifact-sdk/v1`.

### 4.3 Return and exception behavior

- `get_*` returns the stored model object or `None`.
- `list_*` returns a new list containing the stored model objects.
- Ordinary `remove_*` returns `bool`.
- Invalid direct function arguments raise `ValueError`.
- `validate_structure` returns `ValidationReport`.
- `write_submission` raises `StructuralError` when structural errors exist and otherwise
  returns `SubmissionReport`, including warnings and incomplete status.
- A missing rationale under `required` policy or a rationale-required experiment
  lifecycle operation raises `ValueError`.
- A path rejected by the write-time safety guard raises `ValueError`.
- `open_submission` raises `FileNotFoundError` when `manifest.yml` is absent.
- Filesystem and YAML errors retain their specific underlying Python exceptions.

Exception message text is not a cross-language compatibility contract. Validation issue
paths, severity, and pass/fail behavior are.

`write_submission` accepts `stage_from` and `quiet`. `SubmissionReport` exposes
`out_dir`, `ok`, `incomplete`, `warnings`, `files_written`, and `missing_blobs`.
Missing referenced files always add `blob[<path>]` warnings. Matching the frozen
TypeScript behavior, `quiet=True` only forces `incomplete=False`; it does not remove
warnings or missing-blob entries, and neither binding prints them.

`configure_journal` also accepts an injectable `now` callable. Journal `before` and
`after` values for ordinary add/replace operations retain the same object references
as the artifact, matching the frozen TypeScript implementation. Disposition changes
use shallow before/after snapshots.

## 5. Modules and responsibilities

| Module | Responsibility |
|---|---|
| `model.py` | Constants, dataclasses, type aliases, validator variants, default-mode helpers, pinned-digest parsing |
| `builder.py` | Artifact creation, upserts, inspection, removal, experiment lifecycle, journaling, attachments |
| `validate.py` | Schema validation, relational invariants, path safety, warnings, `StructuralError` |
| `inventory.py` | Evidence inventory derived from an artifact |
| `serialize.py` | Stable YAML/JSON/Markdown output, staging, hashes, state ledger |
| `open.py` | Reconstruct an artifact from an existing submission |
| `__init__.py` | Deliberate re-export of the supported public API |

Internal conversion helpers map dataclasses to plain dictionaries and back. They omit
`None` fields, preserve declared list order, and never persist the transient journal
configuration.

## 6. Validation algorithm

### 6.1 Initial compatibility profile

The canonical JSON Schema remains a required conformance gate, but the frozen
TypeScript runtime does not currently execute it. Running schema validation only in
Python would reject structures accepted by TypeScript and violate the experiment
freeze. Therefore the initial Python `validate_structure` performs these stages:

1. Convert the artifact dataclass graph to its schema-shaped dictionary.
2. Apply the same authored validation rules and deterministic traversal order as the
   frozen TypeScript `validateStructure`, including:
   - referential integrity;
   - graph-cycle checks;
   - safe relative paths and generated-path collisions;
   - disposition and journal constraints;
   - evidence-pointer and research-agent rules.
3. Add advisory warnings for incomplete but legal artifacts.
4. Return errors and warnings in deterministic traversal order.

Both bindings separately validate every emitted conformance fixture against the
canonical draft-07 schema in tests. Python uses `Draft7Validator` with deterministically
sorted errors. Schema/runtime differences are explicit expected cases, never silently
discarded.

### 6.2 Post-freeze target

After the experiment freeze, issue #32 will reconcile the schema and authored rules,
define a stable schema-error-to-issue-path mapping and deduplication policy, and enable
schema plus relational runtime validation in both bindings. The Python implementation
must isolate schema validation so that transition does not require redesigning its
public API.

The TypeScript binding currently authors the same invariants directly. Shared
conformance cases, rather than duplicated implementation structure, prevent behavioral
drift.

`open_submission` mirrors the current compatibility behavior: it parses the submission
and reconstructs the model but does not reject incomplete or legacy-compatible content.
Callers may invoke `validate_structure`; `write_submission` always does so before
writing.

## 7. Serialization algorithm

`write_submission` follows the same observable stages in both bindings:

1. Validate before modifying the output directory.
2. Resolve every producer-declared path with the same portable, case-insensitive safety
   rules.
3. Stage referenced authored blobs.
4. Write `reflection.md` when the model carries reflection text.
5. Write the required generated indexes and optional indexes only when populated.
6. Write non-active experiment disposition markers.
7. Compute the evidence inventory.
8. Hash submission files and write `SHA256SUMS`.
9. Write `.sdk/state.json`, separating generated and authored files.
10. Return the complete write report.

Python writes UTF-8 with `\n` line endings, stable dictionary insertion order, stable
list order, and deterministic YAML settings. Re-emitting the same artifact with the
same Python package must be byte-idempotent.

Cross-binding byte identity is not required because compliant YAML emitters may differ
in quoting and wrapping. Consequently, binding-produced hashes may differ even when
the represented artifact is equivalent.

Python parses and emits YAML 1.2. `ruamel.yaml` runs in safe, pure-Python YAML 1.2 mode
with an explicit deterministic quoting policy so values such as `no`, `on`, `off`, and
`12:30` remain strings across bindings.

### 7.1 Frozen TypeScript compatibility behavior

Until issue #32 is resolved, Python deliberately matches these observable TypeScript
behaviors and locks them with compatibility tests:

- staged files replace an existing destination when `stage_from` is used;
- model-carried `reflection.md` is written and classified as generated;
- optional generated indexes left by an earlier write are not deleted when their
  collection later becomes empty; the stale files remain in `SHA256SUMS` and are
  reclassified as authored in `.sdk/state.json`;
- unknown nested extension keys survive open/write cycles; unknown top-level manifest
  keys retain the frozen drop behavior described in §4.2.

These are compatibility constraints, not endorsements of the behavior. They must not
be "fixed" in Python alone.

## 8. Cross-binding conformance

Semantic parity means that, for every shared case:

1. Both bindings accept or reject the same artifact, except for the documented
   explicit-null compatibility rule: Python treats null optional model fields as omitted.
2. Validation produces the same issue severity and logical path. Message prose may
   differ. A field a variant's model does not declare is still validated — `gated_by` on
   an `attest` validator, for example, which Python carries in the model's extension
   bucket (§4.2) and TypeScript reads structurally.
3. Both bindings emit the same set of generated and authored paths.
4. Parsing YAML and JSON outputs yields equivalent values after normalizing
   binding-byte-dependent hashes, treating numerically equal integral values such as
   `1` and `1.0` as equivalent, and treating an explicit `null` as equivalent to an
   omitted optional model field. That last equivalence covers optional model fields
   only: a null *value inside an opaque producer-authored map* is data both bindings must
   emit verbatim, so the harness `read_document` operation marks explicit nulls as
   `<null>` and compares them across bindings.
5. `SHA256SUMS` and `.sdk/state.json` cover the same paths and classifications; each
   binding's hashes must be correct for its own bytes.
6. Reopening either binding's output produces an equivalent in-memory model in both
   bindings.
7. A write-open-write round trip is idempotent within each binding.

Shared cases are data, not one binding invoking the other. Each language test runner
loads the same case manifests and expected normalized results. Cross-open tests run in
CI after both packages are built.

`parity/case.schema.json` defines two case forms:

- **Artifact cases** provide a final schema-shaped artifact, optional source fixtures,
  write options, and expected validation/report/output summaries.
- **Operation cases** provide an ordered, language-neutral operation script. Each step
  has a snake_case operation name, arguments, optional change context, and optional
  expected exception. The case may define journal policy, actor, a fixed sequence of
  `now` values, and prompt-rationale responses.

The TypeScript runner mechanically maps operation names to its frozen camelCase
exports; the Python runner calls the corresponding snake_case exports. Operation cases
cover builder defaults, upsert behavior, journaling, experiment lifecycle, attachments,
and removals that cannot be reconstructed from final-state data alone.

The initial corpus must cover:

- the complete worked example;
- every model collection and validator kind;
- empty/partial artifacts and warning behavior;
- all experiment dispositions and rationale policies;
- authored/generated file classification;
- safe-path rejection and reserved-path collisions;
- optional-index omission;
- schema and referential failures;
- TypeScript-output opened by Python and Python-output opened by TypeScript;
- unknown extension fields, including `study.extra` — a spec-defined nested field that
  coexists with an unknown sibling key on the same `study` block;
- ambiguous YAML scalars;
- fixed-clock journal snapshots;
- staging replacement and missing-blob warnings;
- frozen reflection and stale-index behavior;
- `gated_by` on every validator kind, including `attest`;
- a non-active disposition whose `rationale` is omitted entirely;
- null values inside opaque producer-authored maps.

The checked-in expected results are human-reviewed contract data. A maintainer may
regenerate candidates only through an explicit `--update` mode; regeneration never
turns one binding's current output into the contract automatically. Shared source blobs
live under `parity/fixtures/`, independently of TypeScript-only fixtures.

## 9. Python tests and quality gates

The Python suite uses `pytest` and mirrors the behavioral groupings under `test/`:

- builder and model defaults;
- structural validation;
- serialization and reopening;
- journaling and experiment lifecycle;
- claim stance;
- exhibits;
- research agent;
- worked example and schema conformance;
- cross-binding parity.

Quality gates:

```bash
python -m pytest python/tests
python -m mypy python/src/universal_artifact_sdk
python -m ruff check python
python -m build --outdir dist-python
python -m twine check dist-python/*
```

CI runs the Python suite on supported representative versions, including the minimum
Python 3.10 and the newest stable version available to GitHub Actions. The TypeScript
matrix remains unchanged. A separate parity job depends on both binding jobs.

## 10. Dependencies

Runtime dependencies are intentionally small:

- `ruamel.yaml` for safe YAML 1.2 parsing and deterministic emission.

The standard library supplies dataclasses, hashing, JSON, paths, copying, timestamps,
and filesystem operations. `jsonschema` is a development dependency for canonical
schema conformance tests during the TypeScript freeze; it becomes a runtime dependency
when issue #32 enables schema validation in both bindings. Development dependencies are
isolated in a `dev` optional extra.

## 11. Packaging and release

The wheel and source distribution include:

- `universal_artifact_sdk` and `py.typed`;
- the canonical JSON Schema as
  `universal_artifact_sdk/schema/evaluable-artifact-v2.schema.json`;
- the Python quickstart example;
- README, specification, changelog, and license metadata as appropriate.

Source distributions explicitly exclude Node dependencies, TypeScript build output,
coverage output, and scratch artifacts. Python build products use `dist-python/`, which
is ignored by git and is outside the npm package's `files` allowlist; Python tooling
must never write wheels or source archives into the TypeScript `dist/` directory.

The release workflow:

1. Verify the git tag matches both `package.json` and `pyproject.toml`.
2. Run all TypeScript, Python, and parity checks.
3. Build and inspect both distributions.
4. Publish npm with provenance.
5. Publish PyPI through GitHub Actions trusted publishing with provenance.

The PyPI project and trusted-publisher relationship must be configured by a repository
or PyPI administrator before the first release. No long-lived PyPI API token is stored
in GitHub.

## 12. Acceptance criteria

The Python binding is complete when:

- every public TypeScript export that represents language-neutral SDK behavior has an
  idiomatic Python equivalent, verified by a maintained export-parity inventory;
- Python validation covers every current TypeScript structural rule;
- both bindings pass the shared conformance corpus;
- each binding can reopen the other's output;
- Python build artifacts install and import in a clean environment;
- CI enforces Python 3.10+, typing, lint, tests, package build, and parity;
- release automation validates lockstep versions and is ready for PyPI trusted
  publishing;
- README, contributing instructions, examples, and changelog describe both bindings;
- no TypeScript API or implementation file changes as part of the frozen experiment.
