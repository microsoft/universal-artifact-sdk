"""Object model for the Universal Artifact SDK (``artifact-sdk/v1``).

These dataclasses are the in-memory shape a producer builds; :func:`write_submission`
serializes them into the on-disk ``evaluable-artifact/v2`` format. Field names track the
canonical schema, so the serialized names stay ``snake_case`` in every binding.

Nested schema models carry an *extension bucket*: a mapping used to round-trip legal
extension keys this binding does not understand. Serialization merges the bucket first
and known fields second, so an extension can never override a contract field. The bucket
is named ``extra`` on every model except :class:`StudyMetadata`, where ``extra`` is
itself a contract field (spec §2.7); that model overflows into ``extensions`` instead.
Each model names its own bucket through :data:`EXTENSION_FIELD`.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from dataclasses import MISSING, dataclass, field, fields, is_dataclass
from pathlib import Path
from typing import Any, ClassVar, Literal, TypeVar

SDK_VERSION = "artifact-sdk/v1"
FORMAT_VERSION = "evaluable-artifact/v2"

#: Closed vocabulary: how a claim is validated from evidence (spec §3.1).
VALIDATION_MODES: tuple[str, ...] = ("re-execute", "re-analyze", "inspect", "attest")
#: Closed vocabulary: lifecycle status of a retained experiment (spec §2.2.2).
DISPOSITION_STATUSES: tuple[str, ...] = ("active", "superseded", "abandoned", "failed")
#: Open vocabulary: the known exhibit genres (spec §2.3.1).
EXHIBIT_TYPES: tuple[str, ...] = ("figure", "table", "proof", "derivation", "listing")
#: Closed vocabulary: author-declared standing of a claim (spec §2.4.1).
CLAIM_STANCES: tuple[str, ...] = ("hypothesis", "finding")
#: The stance of a claim that does not declare one (spec §2.4.1).
DEFAULT_CLAIM_STANCE = "finding"
#: Open vocabulary: the known evidence kinds carried by a result (spec §2.3).
RESULT_KINDS: tuple[str, ...] = (
    "metrics",
    "figure",
    "table",
    "log",
    "proof",
    "artifact",
    "transcript",
    "survey",
    "codebook",
    "argument",
    "external_reference",
)
#: Open vocabulary: the known trace kinds (spec §2.2.1).
TRACE_KINDS: tuple[str, ...] = (
    "agent_session",
    "execution_log",
    "build_log",
    "notebook",
    "human_interaction",
    "other",
)
#: Names in the builtin validator catalog shipped in v1 (spec §3.2).
BUILTIN_CHECKS: tuple[str, ...] = (
    "numeric_close",
    "numeric_threshold",
    "monotonic",
    "exact_match",
    "contains",
    "output_present",
)

ValidationMode = Literal["re-execute", "re-analyze", "inspect", "attest"]
DispositionStatus = Literal["active", "superseded", "abandoned", "failed"]
ClaimStance = Literal["hypothesis", "finding"]
RationalePolicy = Literal["required", "prompt", "warn"]
JournalOp = Literal["add", "replace", "remove", "abandon", "attach", "set"]
#: Open vocabulary (spec §2.3): any string; :data:`RESULT_KINDS` lists the known values.
ResultKind = str
#: Open vocabulary (spec §2.3.1): any string; :data:`EXHIBIT_TYPES` lists the known values.
ExhibitType = str
#: Open vocabulary (spec §2.2.1): any string; :data:`TRACE_KINDS` lists the known values.
TraceKind = str
#: Open vocabulary (spec §3.2): any string; :data:`BUILTIN_CHECKS` lists the shipped catalog.
BuiltinCheck = str
#: Named cell-level handle into evidence, used by numeric validators (spec §2.3).
Locator = dict[str, Any]

#: The attribute a nested model overflows unknown extension keys into, unless the model
#: declares its own :data:`EXTENSION_FIELD` class variable (see :class:`StudyMetadata`).
DEFAULT_EXTENSION_FIELD = "extra"


def extension_field(model: Any) -> str:
    """Name the attribute holding ``model``'s unknown-key extension bucket.

    ``model`` may be a model class or an instance of one. The bucket is flattened into
    sibling keys by :func:`to_dict` and refilled from unrecognized sibling keys by
    :func:`_build`, so it must never name a contract field.
    """
    name = getattr(model, "EXTENSION_FIELD", DEFAULT_EXTENSION_FIELD)
    return name if isinstance(name, str) else DEFAULT_EXTENSION_FIELD


@dataclass
class Image:
    """Container image a run environment is built from (spec §2.5)."""

    reference: str
    digest: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Hardware:
    cpu: str | None = None
    gpu: str | None = None
    min_ram_gb: float | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Environment:
    name: str
    image: Image
    os: str | None = None
    hardware: Hardware | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class StudyMetadata:
    """Human-subjects / study provenance (spec §2.7). All fields advisory.

    ``extra`` is a *contract* field here, not this binding's extension bucket: spec §2.7
    defines it as an open sub-map of venue-specific study metadata (``data_use_agreement``
    and the like), so it serializes as a nested ``extra:`` mapping. Unknown sibling keys
    overflow into :attr:`extensions` instead, which is flattened into siblings on write
    exactly like the ``extra`` bucket every other nested model carries.
    """

    #: Overrides the model-wide default so ``extra`` stays a serialized contract field.
    EXTENSION_FIELD: ClassVar[str] = "extensions"

    ethics_approval: str | None = None
    consent_basis: str | None = None
    deidentification: str | None = None
    redaction_note: str | None = None
    sampling: str | None = None
    #: Open sub-map for venue-specific fields (spec §2.7); ``None`` when unauthored.
    extra: dict[str, Any] | None = None
    #: Unknown sibling keys, round-tripped as siblings of the declared fields.
    extensions: dict[str, Any] = field(default_factory=dict)


@dataclass
class InArtifactLocation:
    path: str
    kind: str = "in_artifact"
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class InContainerLocation:
    path: str
    in_environment: str
    kind: str = "in_container"
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExternalLocation:
    uri: str
    sha256: str
    bytes: int | None = None
    access: str | None = None
    license: str | None = None
    kind: str = "external"
    extra: dict[str, Any] = field(default_factory=dict)


DatasetLocation = InArtifactLocation | InContainerLocation | ExternalLocation


@dataclass
class Sample:
    path: str
    sha256: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Dataset:
    id: str
    location: DatasetLocation | dict[str, Any]
    description: str | None = None
    prepare: str | None = None
    sample: Sample | None = None
    study: StudyMetadata | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class RunSpec:
    command: str
    entrypoint: str | None = None
    working_dir: str | None = None
    args: list[str] | None = None
    env: dict[str, str] | None = None
    seed: int | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class DataUse:
    dataset: str
    at: str
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Failure:
    stage: str
    summary: str
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Disposition:
    """Why an attempted experiment is not in the reported set (spec §2.2.2)."""

    status: str
    #: Absent when the producer recorded none — never defaulted to an empty string, so a
    #: reopened disposition is written back exactly as authored (validation warns instead).
    rationale: str | None = None
    superseded_by: str | None = None
    failure: Failure | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Experiment:
    slug: str
    directory: str
    run: RunSpec
    uses_data: list[DataUse] | None = None
    depends_on: list[str] | None = None
    expected_runtime: str | None = None
    runs_in: str | None = None
    disposition: Disposition | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Trace:
    """The record of what actually ran (spec §2.2.1). Envelope only; body opaque."""

    id: str
    kind: str
    path: str
    covers: list[str] | None = None
    terminal_state: str | None = None
    counters: dict[str, float] | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class QualitativeExcerpt:
    file: str
    lines: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class InterRaterReliability:
    metric: str
    value: float
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class QualitativeSupport:
    """Qualitative support, in lieu of numeric locators (spec §2.3)."""

    excerpts: list[QualitativeExcerpt] | None = None
    codebook: str | None = None
    inter_rater_reliability: InterRaterReliability | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Result:
    id: str
    validates: list[str]
    evidence: str
    kind: str
    produced_by: str | None = None
    validation_mode: str | None = None
    locators: dict[str, Locator] | None = None
    support: QualitativeSupport | None = None
    supersedes: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Exhibit:
    """A typed, captioned evidence artifact that substantiates claims (spec §2.3.1)."""

    id: str
    type: str
    caption: str
    validates: list[str]
    path: str | None = None
    produced_by: str | None = None
    validation_mode: str | None = None
    source: str | None = None
    alt_text: str | None = None
    order: int | None = None
    from_result: str | None = None
    statement: str | None = None
    depends_on: list[str] | None = None
    language: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class PaperReference:
    section: str | None = None
    figure: str | None = None
    page: int | str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class BuiltinValidator:
    """Catalog check run by the evaluator (spec §3.2)."""

    name: str
    id: str | None = None
    input: dict[str, Any] | None = None
    params: dict[str, Any] | None = None
    gated_by: str | None = None
    kind: str = "builtin"
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class ProcedureTool:
    name: str
    version: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class ProcedureValidator:
    """Executable natural-language procedure (spec §3.3)."""

    instructions: str
    id: str | None = None
    tools: list[ProcedureTool] | None = None
    inputs: list[str] | None = None
    success_criteria: str | None = None
    timeout: str | None = None
    gated_by: str | None = None
    kind: str = "procedure"
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class AttestValidator:
    """Provenance / integrity / ethics attestation — gates inspect (spec §3.5)."""

    checks: str
    id: str | None = None
    inputs: list[str] | None = None
    kind: str = "attest"
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class LlmJudgeValidator:
    """Advisory natural-language rubric — the ``inspect`` mode (spec §3.4)."""

    criteria: str
    id: str | None = None
    inputs: list[str] | None = None
    gated_by: str | None = None
    kind: str = "llm_judge"
    extra: dict[str, Any] = field(default_factory=dict)


Validator = BuiltinValidator | ProcedureValidator | AttestValidator | LlmJudgeValidator


@dataclass
class Claim:
    id: str
    statement: str
    #: A malformed validator reopened from disk is carried verbatim as plain data, so
    #: `validate_structure` still reports it (see `validator_from_dict`).
    validators: list[Validator | dict[str, Any]] = field(default_factory=list)
    stance: str | None = None
    tested_by: list[str] | None = None
    paper_ref: PaperReference | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class AddClaimInput:
    """``validators`` list OR singular ``validator`` sugar (spec §2.4).

    When both are supplied ``validators`` wins, matching the frozen TypeScript binding.
    """

    id: str
    statement: str
    validators: list[Validator | dict[str, Any]] | None = None
    validator: Validator | dict[str, Any] | None = None
    stance: str | None = None
    tested_by: list[str] | None = None
    paper_ref: PaperReference | None = None


@dataclass
class Assessment:
    """Whole-submission evaluation dimension (spec §2.1.1)."""

    id: str
    dimension: str
    scope: str
    evidence: list[str] | None = None
    validator: Validator | dict[str, Any] | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Paper:
    """Compiled paper. At least one of ``pdf`` / ``source`` is required (spec §2.6)."""

    pdf: str | None = None
    source: str | None = None
    claims_export: str | None = None
    references_export: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class ResearchAgent:
    """Optional producer-shipped Q&A witness (spec §2.9)."""

    path: str
    model: str
    grounding_sources: list[str]
    scope: list[str] | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class JournalTarget:
    """The element a journal entry is about (spec §2.8)."""

    kind: str
    id: str
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class JournalEntry:
    """One append-only entry in the artifact's edit history (spec §2.8)."""

    seq: int
    timestamp: str
    actor: str
    op: str
    target: JournalTarget
    rationale: str
    before: Any = None
    after: Any = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class ChangeContext:
    """Optional per-mutation context carrying who made the change and why (spec §4.2)."""

    actor: str | None = None
    rationale: str | None = None


@dataclass
class PendingChange:
    """The change handed to ``on_missing_rationale`` before it commits (spec §4.2)."""

    op: str
    target: JournalTarget


@dataclass
class JournalConfig:
    """Per-session journaling configuration (spec §4.2). Never serialized."""

    policy: str = "warn"
    actor: str = "unknown"
    on_missing_rationale: Callable[[PendingChange], str] | None = None
    now: Callable[[], str] | None = None


@dataclass
class Artifact:
    """The root in-memory model a producer builds and serializes (spec §2)."""

    id: str
    title: str
    format_version: str = FORMAT_VERSION
    sdk_version: str = SDK_VERSION
    producer: dict[str, Any] | None = None
    environment: Environment | None = None
    datasets: list[Dataset] = field(default_factory=list)
    experiments: list[Experiment] = field(default_factory=list)
    traces: list[Trace] = field(default_factory=list)
    results: list[Result] = field(default_factory=list)
    claims: list[Claim] = field(default_factory=list)
    exhibits: list[Exhibit] = field(default_factory=list)
    assessments: list[Assessment] = field(default_factory=list)
    paper: Paper | None = None
    research_agent: ResearchAgent | None = None
    reflection: str | None = None
    journal: list[JournalEntry] = field(default_factory=list)
    #: Transient journaling config (spec §4.2); never serialized.
    journal_config: JournalConfig | None = field(default=None, repr=False, compare=False)


_PINNED_DIGEST = re.compile(r"@(sha256:[a-f0-9]{64})$", re.IGNORECASE)


def pinned_digest(reference: str | None) -> str | None:
    """Return the immutable ``sha256:…`` digest embedded in a pinned image reference.

    Returns ``None`` when the reference is a bare, mutable tag. Pure and offline: the
    SDK never contacts a registry.
    """
    match = _PINNED_DIGEST.search(reference or "")
    return match.group(1).lower() if match else None


def default_validation_mode(kind: str) -> str:
    """Default ``validation_mode`` inferred from a result's ``kind`` (spec §2.3)."""
    if kind in ("metrics", "table", "figure"):
        return "re-analyze"
    if kind in ("proof", "log"):
        return "re-execute"
    if kind == "external_reference":
        return "attest"
    return "inspect"


def default_exhibit_validation_mode(type: str) -> str:
    """Default ``validation_mode`` inferred from an exhibit's ``type`` (spec §2.3.1)."""
    return "re-execute" if type == "proof" else "inspect"


def canonical_schema_path() -> Path:
    """Locate the canonical schema in an installed package or an editable checkout."""
    packaged = Path(__file__).resolve().parent / "schema" / "evaluable-artifact-v2.schema.json"
    if packaged.is_file():
        return packaged
    return Path(__file__).resolve().parents[3] / "schema" / "evaluable-artifact-v2.schema.json"


def to_dict(value: Any) -> Any:
    """Convert a model graph to schema-shaped plain data.

    An optional *model field* that is ``None`` is omitted, declared list order is
    preserved, a nested model's extension bucket (:func:`extension_field`) is merged first
    so an extension can never shadow a contract field, and the transient journal
    configuration is never emitted.

    A ``None`` *value inside a mapping* is a different thing: mappings such as
    ``producer``, ``run.env``, ``trace.counters``, ``result.locators`` and a validator's
    ``input``/``params`` are opaque producer-authored data, so their nulls are preserved
    verbatim rather than treated as absent fields (``PYTHON_BINDING.md`` §4.2).
    """
    if is_dataclass(value) and not isinstance(value, type):
        overflow = extension_field(value)
        bucket = getattr(value, overflow, None)
        result: dict[str, Any] = dict(bucket) if isinstance(bucket, dict) else {}
        for item in fields(value):
            if item.name in (overflow, "journal_config"):
                continue
            current = getattr(value, item.name)
            if current is not None:
                result[item.name] = to_dict(current)
        return result
    if isinstance(value, list):
        return [to_dict(item) for item in value]
    if isinstance(value, tuple):
        return [to_dict(item) for item in value]
    if isinstance(value, dict):
        return {key: to_dict(item) for key, item in value.items()}
    return value


T = TypeVar("T")

_Converter = Callable[[Any], Any]


def _build(cls: type[T], data: Any, nested: Mapping[str, _Converter] | None = None) -> T:
    """Instantiate ``cls`` from plain data, routing unknown keys into its extension bucket.

    The bucket is named by :func:`extension_field` — ``extra`` for every model but
    :class:`StudyMetadata`, whose ``extra`` is a declared contract field and is therefore
    rebuilt like any other field.

    Reconstruction is deliberately lenient: a contract field absent from the source data
    is materialized as ``None`` rather than raising, so a malformed submission reaches
    :func:`validate_structure` and is reported as a structural issue. This mirrors the
    frozen TypeScript binding, where ``openSubmission`` casts raw YAML into the model.
    """
    if not isinstance(data, dict):
        raise ValueError(f"{cls.__name__}: expected a mapping, got {type(data).__name__}")
    converters = nested or {}
    overflow = extension_field(cls)
    declared = fields(cls)  # type: ignore[arg-type]
    names = {item.name for item in declared}
    values: dict[str, Any] = {}
    for key, value in data.items():
        if key == overflow or key not in names:
            continue
        convert = converters.get(key)
        values[key] = convert(value) if convert is not None and value is not None else value
    for item in declared:
        if item.name in values or item.name == overflow:
            continue
        if item.default is MISSING and item.default_factory is MISSING:
            values[item.name] = None
    if overflow in names:
        values[overflow] = {key: value for key, value in data.items() if key not in names}
    return cls(**values)


_VALIDATOR_CLASSES: dict[str, type[Any]] = {
    "builtin": BuiltinValidator,
    "procedure": ProcedureValidator,
    "attest": AttestValidator,
    "llm_judge": LlmJudgeValidator,
}


def validator_from_dict(data: dict[str, Any]) -> Validator | dict[str, Any]:
    """Reconstruct the validator variant named by ``kind`` (spec §3).

    A validator whose ``kind`` is missing or unrecognized is carried verbatim rather than
    coerced into a variant: inventing a ``kind`` would hide the malformed validator from
    :func:`validate_structure` and write a ``kind`` the producer never authored. This is
    the same treatment :func:`_location_from_dict` gives an unknown dataset location.
    """
    kind = data.get("kind")
    cls = _VALIDATOR_CLASSES.get(kind) if isinstance(kind, str) else None
    if cls is None:
        return dict(data)
    nested: dict[str, _Converter] = {
        "tools": lambda items: [_build(ProcedureTool, item) for item in items],
    }
    validator: Validator = _build(cls, data, nested)
    return validator


_LOCATION_CLASSES: dict[str, type[Any]] = {
    "in_artifact": InArtifactLocation,
    "in_container": InContainerLocation,
    "external": ExternalLocation,
}


def _location_from_dict(data: Any) -> Any:
    if not isinstance(data, dict):
        return data
    cls = _LOCATION_CLASSES.get(str(data.get("kind", "")))
    if cls is None:
        # An unknown location kind is carried verbatim rather than rejected here;
        # `validate_structure` is the authority on legality.
        return data
    return _build(cls, data)


def _dataset_from_dict(data: Any) -> Dataset:
    return _build(
        Dataset,
        data,
        {
            "location": _location_from_dict,
            "sample": lambda value: _build(Sample, value),
            "study": lambda value: _build(StudyMetadata, value),
        },
    )


def _experiment_from_dict(data: Any) -> Experiment:
    return _build(
        Experiment,
        data,
        {
            "run": lambda value: _build(RunSpec, value),
            "uses_data": lambda items: [_build(DataUse, item) for item in items],
            "disposition": lambda value: _build(
                Disposition, value, {"failure": lambda inner: _build(Failure, inner)}
            ),
        },
    )


def _result_from_dict(data: Any) -> Result:
    return _build(
        Result,
        data,
        {
            "support": lambda value: _build(
                QualitativeSupport,
                value,
                {
                    "excerpts": lambda items: [_build(QualitativeExcerpt, i) for i in items],
                    "inter_rater_reliability": lambda inner: _build(InterRaterReliability, inner),
                },
            )
        },
    )


def _claim_from_dict(data: Any) -> Claim:
    return _build(
        Claim,
        data,
        {
            "validators": lambda items: [validator_from_dict(item) for item in items],
            "paper_ref": lambda value: _build(PaperReference, value),
        },
    )


def _journal_entry_from_dict(data: Any) -> JournalEntry:
    return _build(
        JournalEntry, data, {"target": lambda value: _build(JournalTarget, value)}
    )


def artifact_from_dict(data: dict[str, Any]) -> Artifact:
    """Build an :class:`Artifact` from schema-shaped data, keeping nested extensions.

    Unknown top-level manifest keys are dropped, matching the frozen TypeScript
    implementation (see ``PYTHON_BINDING.md`` §4.2).
    """
    return _build(
        Artifact,
        data,
        {
            "environment": lambda value: _build(
                Environment,
                value,
                {
                    "image": lambda inner: _build(Image, inner),
                    "hardware": lambda inner: _build(Hardware, inner),
                },
            ),
            "datasets": lambda items: [_dataset_from_dict(item) for item in items],
            "experiments": lambda items: [_experiment_from_dict(item) for item in items],
            "traces": lambda items: [_build(Trace, item) for item in items],
            "results": lambda items: [_result_from_dict(item) for item in items],
            "claims": lambda items: [_claim_from_dict(item) for item in items],
            "exhibits": lambda items: [_build(Exhibit, item) for item in items],
            "assessments": lambda items: [
                _build(Assessment, item, {"validator": validator_from_dict}) for item in items
            ],
            "paper": lambda value: _build(Paper, value),
            "research_agent": lambda value: _build(ResearchAgent, value),
            "journal": lambda items: [_journal_entry_from_dict(item) for item in items],
        },
    )
