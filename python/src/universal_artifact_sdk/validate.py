"""Structural validation (spec §7): the SDK's half of the validation split.

The SDK checks that a submission is *well-formed* — required fields, legal enums, safe
paths, and referential integrity. It does not check whether results actually support
claims; that semantic judgment stays with the evaluator. Hard problems are **errors**
that block emission; "incomplete but legal" situations are **warnings**, because a
partial artifact is not malformed (spec §4.1).

Issues are returned in deterministic traversal order. Issue ``path`` and severity are a
cross-binding contract; message prose is not.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from .model import (
    CLAIM_STANCES,
    DISPOSITION_STATUSES,
    EXHIBIT_TYPES,
    VALIDATION_MODES,
    Artifact,
    Claim,
    extension_field,
    pinned_digest,
)

GENERATED_RESERVED_PATHS: tuple[str, ...] = (
    "manifest.yml",
    "claims.yml",
    "results.yml",
    "datasets.yml",
    "exhibits.yml",
    "traces.yml",
    "assessments.yml",
    "journal.yml",
    "reflection.md",
    "SHA256SUMS",
)

_DRIVE_LETTER = re.compile(r"^[A-Za-z]:")

_REQUIRED_VALIDATOR_FIELD = {
    "builtin": "name",
    "procedure": "instructions",
    "attest": "checks",
    "llm_judge": "criteria",
}

#: Sentinel telling "attribute absent" apart from "attribute present and ``None``".
_ABSENT = object()


@dataclass
class Issue:
    """A single structural finding: where it is, and what is wrong."""

    path: str
    message: str


@dataclass
class ValidationReport:
    ok: bool
    errors: list[Issue] = field(default_factory=list)
    warnings: list[Issue] = field(default_factory=list)


class StructuralError(ValueError):
    """Raised by :func:`write_submission` when structural errors block emission."""

    def __init__(self, issues: list[Issue]) -> None:
        self.issues = issues
        detail = "\n".join(f"  - {issue.path}: {issue.message}" for issue in issues)
        super().__init__(f"structural validation failed:\n{detail}")


def _attr(obj: Any, key: str, default: Any = None) -> Any:
    """Read ``key`` from a dataclass model, its extension bucket, or an equivalent mapping.

    A legal field that a particular variant does not declare — ``gated_by`` on an
    ``attest`` validator, say — is carried in the model's extension bucket (see
    ``model._build`` and ``model.extension_field``). The frozen TypeScript binding reads
    such a field structurally off *every* validator, so validation here must see the
    bucket-backed value too; declared fields always win.
    """
    if isinstance(obj, dict):
        return obj.get(key, default)
    value = getattr(obj, key, _ABSENT)
    if value is not _ABSENT:
        return value
    bucket = getattr(obj, extension_field(obj), None)
    if isinstance(bucket, dict) and key in bucket:
        return bucket[key]
    return default


def _path_problem(
    value: Any,
    *,
    allow_directory: bool,
    reserve_generated: bool = False,
    reserve_generated_descendants: bool = False,
) -> str | None:
    """Describe why ``value`` is not a safe artifact-relative path, or ``None`` if it is."""
    if not isinstance(value, str):
        return "must be a string"
    trimmed = value.strip()
    if not trimmed:
        return "must be non-empty"
    if trimmed != value:
        return "must not have leading or trailing whitespace"
    slash_path = value.replace("\\", "/")
    if slash_path in (".", ""):
        return "must not point at the artifact root"
    if slash_path.startswith("/") or _DRIVE_LETTER.match(slash_path):
        return "must be relative to the artifact root"
    if any(part in (".", "..") for part in slash_path.split("/")):
        return "must not contain . or .. path segments"
    if not allow_directory and slash_path.endswith("/"):
        return "must name a file, not a directory"
    lower = slash_path.lower()
    for reserved in GENERATED_RESERVED_PATHS:
        lower_reserved = reserved.lower()
        if reserve_generated and (
            lower == lower_reserved or lower.startswith(f"{lower_reserved}/")
        ):
            return "must not collide with SDK-generated files"
        if reserve_generated_descendants and lower.startswith(f"{lower_reserved}/"):
            return "must not collide with SDK-generated files"
    if lower == ".sdk" or lower.startswith(".sdk/"):
        return "must not be inside .sdk"
    return None


def _push_blob_path_error(errors: list[Issue], path: str, value: Any) -> None:
    problem = _path_problem(value, allow_directory=True, reserve_generated=True)
    if problem:
        errors.append(Issue(path, f"referenced blob path {problem}"))


def _artifact_path_key(value: Any) -> str | None:
    """Case- and separator-insensitive key used to detect on-disk path collisions."""
    if not isinstance(value, str):
        return None
    trimmed = value.strip()
    if not trimmed or trimmed != value:
        return None
    return trimmed.replace("\\", "/").lower()


def _authored_blob_refs(artifact: Artifact) -> list[tuple[str, str]]:
    """Every producer-authored blob reference, as ``(issue_path, value)`` pairs."""
    refs: list[tuple[str, str]] = []
    for dataset in artifact.datasets:
        location = dataset.location
        location_path = _attr(location, "path")
        if _attr(location, "kind") == "in_artifact" and isinstance(location_path, str):
            refs.append((f"dataset[{dataset.id}].location.path", location_path))
        if dataset.sample is not None and isinstance(dataset.sample.path, str):
            refs.append((f"dataset[{dataset.id}].sample.path", dataset.sample.path))
    for trace in artifact.traces:
        if isinstance(trace.path, str):
            refs.append((f"trace[{trace.id}].path", trace.path))
    for result in artifact.results:
        if isinstance(result.evidence, str):
            refs.append((f"result[{result.id}].evidence", result.evidence))
    for exhibit in artifact.exhibits:
        if isinstance(exhibit.path, str):
            refs.append((f"exhibit[{exhibit.id}].path", exhibit.path))
        if isinstance(exhibit.source, str):
            refs.append((f"exhibit[{exhibit.id}].source", exhibit.source))
    if artifact.paper is not None:
        for key in ("pdf", "source", "claims_export", "references_export"):
            value = getattr(artifact.paper, key)
            if isinstance(value, str):
                refs.append((f"paper.{key}", value))
    if artifact.research_agent is not None and isinstance(artifact.research_agent.path, str):
        refs.append(("research_agent.path", artifact.research_agent.path))
    return refs


def _validator_ids(claim: Claim) -> set[str]:
    ids: set[str] = set()
    for validator in claim.validators or []:
        validator_id = _attr(validator, "id")
        if isinstance(validator_id, str) and validator_id:
            ids.add(validator_id)
    return ids


def _exhibit_dependency_cycles(artifact: Artifact) -> list[list[str]]:
    """Detect cycles in the exhibit ``depends_on`` DAG (spec §2.3.1).

    Returns one representative path per distinct cycle, e.g. ``["X1", "X2", "X1"]``.
    """
    adjacency: dict[str, list[str]] = {
        exhibit.id: [dep for dep in (exhibit.depends_on or []) if dep != exhibit.id]
        for exhibit in artifact.exhibits
    }
    state: dict[str, str] = {}
    cycles: list[list[str]] = []
    seen: set[str] = set()

    def visit(node: str, stack: list[str]) -> None:
        state[node] = "visiting"
        stack.append(node)
        for next_node in adjacency.get(node, []):
            if next_node not in adjacency:
                continue  # a dangling reference is already reported as an error
            if state.get(next_node) == "visiting":
                cycle = stack[stack.index(next_node) :] + [next_node]
                key = "|".join(sorted(cycle))
                if key not in seen:
                    seen.add(key)
                    cycles.append(cycle)
            elif state.get(next_node) != "done":
                visit(next_node, stack)
        stack.pop()
        state[node] = "done"

    for exhibit in artifact.exhibits:
        if exhibit.id not in state:
            visit(exhibit.id, [])
    return cycles


def _check_validator_well_formed(validator: Any, path: str, errors: list[Issue]) -> None:
    kind = _attr(validator, "kind")
    required = _REQUIRED_VALIDATOR_FIELD.get(kind) if isinstance(kind, str) else None
    if required is None:
        errors.append(Issue(path, f"unknown validator kind {kind or '<missing>'}"))
        return
    if not _attr(validator, required):
        errors.append(Issue(path, f"{kind} validator requires `{required}`"))


def _check_root(artifact: Artifact, errors: list[Issue], warnings: list[Issue]) -> None:
    if not artifact.id:
        errors.append(Issue("artifact.id", "`id` is required"))
    if not artifact.title:
        errors.append(Issue("artifact.title", "`title` is required"))
    # A bare tag is mutable, so an unpinned image is "incomplete but legal" (spec §4).
    environment = artifact.environment
    if environment is not None and environment.image is not None:
        image = environment.image
        if not image.digest and not pinned_digest(image.reference):
            warnings.append(
                Issue(
                    f"environment[{environment.name}].image",
                    "image is not pinned to a digest — `reference` is a mutable tag; "
                    "set `image.digest` (sha256:…) so the exact environment is reproducible",
                )
            )
    paper = artifact.paper
    if paper is not None:
        pdf = paper.pdf.strip() if isinstance(paper.pdf, str) else ""
        source = paper.source.strip() if isinstance(paper.source, str) else ""
        if not pdf and not source:
            errors.append(
                Issue("paper", "paper requires at least one of `pdf` or `source` (spec §2.6)")
            )
        for key in ("pdf", "source", "claims_export", "references_export"):
            value = getattr(paper, key)
            if value is not None:
                _push_blob_path_error(errors, f"paper.{key}", value)


def _check_datasets(
    artifact: Artifact, errors: list[Issue], warnings: list[Issue]
) -> None:
    for dataset in artifact.datasets:
        prefix = f"dataset[{dataset.id}]"
        if not dataset.id:
            errors.append(Issue(prefix, "dataset requires `id`"))
        location = dataset.location
        kind = _attr(location, "kind")
        if not location or not kind:
            errors.append(Issue(prefix, "dataset requires `location.kind`"))
            continue
        if kind == "in_artifact":
            _push_blob_path_error(errors, f"{prefix}.location.path", _attr(location, "path"))
        if dataset.sample is not None and dataset.sample.path is not None:
            _push_blob_path_error(errors, f"{prefix}.sample.path", dataset.sample.path)
        if kind == "external" and not _attr(location, "sha256"):
            errors.append(
                Issue(f"{prefix}.location", "external dataset requires a `sha256` checksum")
            )
        if kind == "in_container" and not _attr(location, "in_environment"):
            errors.append(
                Issue(f"{prefix}.location", "in_container dataset requires `in_environment`")
            )
        if kind == "in_container" and not artifact.environment:
            warnings.append(
                Issue(f"{prefix}.location", "in_container dataset but no environment declared")
            )


def _check_experiments(
    artifact: Artifact,
    dataset_ids: set[str],
    experiment_slugs: set[str],
    errors: list[Issue],
    warnings: list[Issue],
) -> None:
    for experiment in artifact.experiments:
        prefix = f"experiment[{experiment.slug}]"
        if not experiment.slug:
            errors.append(Issue(prefix, "experiment requires `slug`"))
        directory_problem = _path_problem(
            experiment.directory, allow_directory=True, reserve_generated=True
        )
        if not experiment.directory:
            errors.append(Issue(prefix, "experiment requires `directory`"))
        elif directory_problem:
            errors.append(
                Issue(f"{prefix}.directory", f"experiment directory {directory_problem}")
            )
        if not experiment.run or not experiment.run.command:
            errors.append(Issue(prefix, "experiment requires `run.command`"))
        for use in experiment.uses_data or []:
            if _attr(use, "dataset") not in dataset_ids:
                errors.append(
                    Issue(
                        f"{prefix}.uses_data",
                        f"references unknown dataset '{_attr(use, 'dataset')}'",
                    )
                )
        for dependency in experiment.depends_on or []:
            if dependency not in experiment_slugs:
                errors.append(
                    Issue(
                        f"{prefix}.depends_on",
                        f"references unknown experiment '{dependency}'",
                    )
                )
        if (
            experiment.runs_in
            and artifact.environment
            and experiment.runs_in != artifact.environment.name
        ):
            errors.append(
                Issue(
                    f"{prefix}.runs_in",
                    f"references unknown environment '{experiment.runs_in}'",
                )
            )
        disposition = experiment.disposition
        if disposition is None:
            continue
        if disposition.status not in DISPOSITION_STATUSES:
            errors.append(
                Issue(
                    f"{prefix}.disposition",
                    f"illegal disposition status '{disposition.status}'",
                )
            )
        rationale = disposition.rationale if isinstance(disposition.rationale, str) else ""
        if disposition.status != "active" and not rationale.strip():
            warnings.append(
                Issue(
                    f"{prefix}.disposition",
                    f"{disposition.status} experiment has no rationale — "
                    "the process record is incomplete",
                )
            )
        if disposition.superseded_by and disposition.superseded_by not in experiment_slugs:
            errors.append(
                Issue(
                    f"{prefix}.disposition.superseded_by",
                    f"references unknown experiment '{disposition.superseded_by}'",
                )
            )
        if disposition.status == "failed" and not disposition.failure:
            warnings.append(
                Issue(
                    f"{prefix}.disposition",
                    "failed experiment has no `failure` detail (stage/summary)",
                )
            )


def _check_traces(
    artifact: Artifact, experiment_slugs: set[str], errors: list[Issue]
) -> None:
    for trace in artifact.traces:
        prefix = f"trace[{trace.id}]"
        if not trace.id:
            errors.append(Issue(prefix, "trace requires `id`"))
        if not trace.path:
            errors.append(Issue(prefix, "trace requires `path`"))
        else:
            _push_blob_path_error(errors, f"{prefix}.path", trace.path)
        for slug in trace.covers or []:
            if slug not in experiment_slugs:
                errors.append(
                    Issue(f"{prefix}.covers", f"references unknown experiment '{slug}'")
                )


def _check_results(
    artifact: Artifact,
    experiment_slugs: set[str],
    claim_ids: set[str],
    errors: list[Issue],
) -> None:
    for result in artifact.results:
        prefix = f"result[{result.id}]"
        if not result.id:
            errors.append(Issue(prefix, "result requires `id`"))
        if not result.evidence:
            errors.append(Issue(prefix, "result requires `evidence`"))
        else:
            _push_blob_path_error(errors, f"{prefix}.evidence", result.evidence)
        if not result.kind:
            errors.append(Issue(prefix, "result requires `kind`"))
        if result.validation_mode and result.validation_mode not in VALIDATION_MODES:
            errors.append(
                Issue(
                    f"{prefix}.validation_mode",
                    f"illegal validation_mode '{result.validation_mode}'",
                )
            )
        if result.produced_by and result.produced_by not in experiment_slugs:
            errors.append(
                Issue(
                    f"{prefix}.produced_by",
                    f"references unknown experiment '{result.produced_by}'",
                )
            )
        for claim_id in result.validates or []:
            if claim_id not in claim_ids:
                errors.append(
                    Issue(f"{prefix}.validates", f"references unknown claim '{claim_id}'")
                )


def _check_exhibits(
    artifact: Artifact,
    experiment_slugs: set[str],
    claim_ids: set[str],
    result_ids: set[str],
    exhibit_ids: set[str],
    errors: list[Issue],
    warnings: list[Issue],
) -> None:
    for exhibit in artifact.exhibits:
        prefix = f"exhibit[{exhibit.id}]"
        if not exhibit.id:
            errors.append(Issue(prefix, "exhibit requires `id`"))
        if not exhibit.type:
            errors.append(Issue(prefix, "exhibit requires `type`"))
        elif exhibit.type not in EXHIBIT_TYPES:
            # Open/extensible enum: an unrecognized type is legal but flagged for review.
            warnings.append(
                Issue(
                    f"{prefix}.type",
                    f"unrecognized exhibit type '{exhibit.type}' "
                    f"(known: {' | '.join(EXHIBIT_TYPES)})",
                )
            )
        if not exhibit.caption or not exhibit.caption.strip():
            errors.append(Issue(prefix, "exhibit requires a non-empty `caption`"))
        # `path` is required, except a proof/derivation may substitute a formal `statement`.
        statement_only = exhibit.type in ("proof", "derivation") and bool(
            exhibit.statement and exhibit.statement.strip()
        )
        if not exhibit.path and not statement_only:
            errors.append(
                Issue(
                    prefix,
                    "exhibit requires `path` (a proof/derivation may instead carry a `statement`)",
                )
            )
        if exhibit.path:
            _push_blob_path_error(errors, f"{prefix}.path", exhibit.path)
        if exhibit.source is not None:
            _push_blob_path_error(errors, f"{prefix}.source", exhibit.source)
        if exhibit.validation_mode and exhibit.validation_mode not in VALIDATION_MODES:
            errors.append(
                Issue(
                    f"{prefix}.validation_mode",
                    f"illegal validation_mode '{exhibit.validation_mode}'",
                )
            )
        if exhibit.produced_by and exhibit.produced_by not in experiment_slugs:
            errors.append(
                Issue(
                    f"{prefix}.produced_by",
                    f"references unknown experiment '{exhibit.produced_by}'",
                )
            )
        if exhibit.from_result and exhibit.from_result not in result_ids:
            errors.append(
                Issue(
                    f"{prefix}.from_result",
                    f"references unknown result '{exhibit.from_result}'",
                )
            )
        for claim_id in exhibit.validates or []:
            if claim_id not in claim_ids:
                errors.append(
                    Issue(f"{prefix}.validates", f"references unknown claim '{claim_id}'")
                )
        for dependency in exhibit.depends_on or []:
            if dependency == exhibit.id:
                errors.append(
                    Issue(f"{prefix}.depends_on", "exhibit cannot depend on itself")
                )
            elif dependency not in exhibit_ids:
                errors.append(
                    Issue(
                        f"{prefix}.depends_on",
                        f"references unknown exhibit '{dependency}'",
                    )
                )
    for cycle in _exhibit_dependency_cycles(artifact):
        errors.append(
            Issue(
                f"exhibit[{cycle[0]}].depends_on",
                f"exhibit dependency cycle: {' -> '.join(cycle)}",
            )
        )


def _check_claims(
    artifact: Artifact,
    experiment_slugs: set[str],
    result_ids: set[str],
    errors: list[Issue],
    warnings: list[Issue],
) -> None:
    for claim in artifact.claims:
        prefix = f"claim[{claim.id}]"
        if not claim.id:
            errors.append(Issue(prefix, "claim requires `id`"))
        if not claim.statement:
            errors.append(Issue(prefix, "claim requires `statement`"))
        if claim.stance is not None and claim.stance not in CLAIM_STANCES:
            errors.append(
                Issue(
                    f"{prefix}.stance",
                    f"invalid stance '{claim.stance}' (expected {' | '.join(CLAIM_STANCES)})",
                )
            )
        for slug in claim.tested_by or []:
            if slug not in experiment_slugs:
                errors.append(
                    Issue(f"{prefix}.tested_by", f"references unknown experiment '{slug}'")
                )
        validators = claim.validators or []
        if len(validators) == 0 and claim.stance != "hypothesis":
            warnings.append(
                Issue(
                    prefix,
                    "claim has no validator — the evaluator will treat it as unverifiable",
                )
            )
        local_validator_ids = _validator_ids(claim)
        for index, validator in enumerate(validators):
            validator_id = _attr(validator, "id")
            # An absent id falls back to the position; an empty id is kept verbatim.
            key = index if validator_id is None else validator_id
            validator_path = f"{prefix}.validators[{key}]"
            _check_validator_well_formed(validator, validator_path, errors)
            # `gated_by` must resolve to an attest validator on the SAME claim (spec §3.5).
            gated_by = _attr(validator, "gated_by")
            if gated_by:
                if gated_by not in local_validator_ids:
                    errors.append(
                        Issue(
                            f"{validator_path}.gated_by",
                            f"references unknown validator '{gated_by}' on this claim",
                        )
                    )
                else:
                    target = next(
                        (v for v in validators if _attr(v, "id") == gated_by), None
                    )
                    if target is not None and _attr(target, "kind") != "attest":
                        errors.append(
                            Issue(
                                f"{validator_path}.gated_by",
                                "gated_by must reference an attest validator, "
                                f"got '{_attr(target, 'kind')}'",
                            )
                        )
            # Field shape is kind-dependent (spec §3, audit A2): `builtin` uses singular
            # `input` naming one result; the other kinds use a plural `inputs` list.
            if _attr(validator, "kind") == "builtin":
                validator_input = _attr(validator, "input")
                referenced = (
                    validator_input.get("result") if isinstance(validator_input, dict) else None
                )
                if referenced and referenced not in result_ids:
                    errors.append(
                        Issue(
                            f"{validator_path}.input.result",
                            f"references unknown result '{referenced}'",
                        )
                    )
            else:
                for referenced in _attr(validator, "inputs") or []:
                    if referenced not in result_ids:
                        errors.append(
                            Issue(
                                f"{validator_path}.inputs",
                                f"references unknown result '{referenced}'",
                            )
                        )


def _check_assessments(artifact: Artifact, errors: list[Issue]) -> None:
    for assessment in artifact.assessments:
        prefix = f"assessment[{assessment.id}]"
        if not assessment.id:
            errors.append(Issue(prefix, "assessment requires `id`"))
        if not assessment.dimension:
            errors.append(Issue(prefix, "assessment requires `dimension`"))
        if assessment.scope not in ("artifact", "paper"):
            errors.append(Issue(f"{prefix}.scope", "scope must be 'artifact' or 'paper'"))


def _check_research_agent(artifact: Artifact, errors: list[Issue]) -> None:
    """The SDK only checks well-formedness; resolving sources on disk is the evaluator's job."""
    agent = artifact.research_agent
    if agent is None:
        return
    path_problem = _path_problem(agent.path, allow_directory=False, reserve_generated=True)
    if path_problem:
        errors.append(
            Issue("research_agent.path", f"research agent path {path_problem} (spec §2.9)")
        )
    if not isinstance(agent.model, str) or not agent.model.strip():
        errors.append(
            Issue("research_agent.model", "research agent requires a pinned `model` (spec §2.9)")
        )
    sources = agent.grounding_sources
    if not isinstance(sources, (list, tuple)) or len(sources) == 0:
        errors.append(
            Issue(
                "research_agent.grounding_sources",
                "research agent requires at least one `grounding_source` (spec §2.9)",
            )
        )
        return
    for index, source in enumerate(sources):
        problem = _path_problem(
            source, allow_directory=True, reserve_generated_descendants=True
        )
        if problem:
            errors.append(
                Issue(
                    f"research_agent.grounding_sources[{index}]",
                    f"research agent grounding_source {problem} (spec §2.9)",
                )
            )


def _check_generated_path_collisions(artifact: Artifact, errors: list[Issue]) -> None:
    """Generated disposition markers and authored blobs must not overwrite each other."""
    authored_refs = _authored_blob_refs(artifact)
    authored_keys: dict[str, str] = {}
    for issue_path, value in authored_refs:
        if value.endswith("/") or value.endswith("\\"):
            continue
        key = _artifact_path_key(value)
        if key:
            authored_keys[key] = issue_path
    markers: dict[str, str] = {}
    for experiment in artifact.experiments:
        if not experiment.disposition or experiment.disposition.status == "active":
            continue
        directory_key = _artifact_path_key(experiment.directory)
        if not directory_key:
            continue
        markers[f"{directory_key}/disposition.md"] = experiment.slug
        shadowed = authored_keys.get(directory_key)
        if shadowed:
            errors.append(
                Issue(
                    f"experiment[{experiment.slug}].directory",
                    f"experiment directory collides with authored blob {shadowed}",
                )
            )
    for issue_path, value in authored_refs:
        key = _artifact_path_key(value)
        if key is None:
            continue
        marker_slug = markers.get(key)
        if marker_slug:
            errors.append(
                Issue(
                    issue_path,
                    "referenced blob path collides with generated disposition marker "
                    f"for experiment '{marker_slug}'",
                )
            )


def _check_journal(artifact: Artifact, warnings: list[Issue]) -> None:
    """Every recorded mutation should carry a rationale (spec §2.8, §4.2)."""
    for entry in artifact.journal:
        rationale = entry.rationale if isinstance(entry.rationale, str) else ""
        if not rationale.strip():
            warnings.append(
                Issue(
                    f"journal[#{entry.seq}]",
                    f"mutation '{entry.op}' on {entry.target.kind}[{entry.target.id}] "
                    "has no rationale",
                )
            )


def _ids(values: Iterable[Any], key: str) -> set[str]:
    return {getattr(value, key) for value in values}


def validate_structure(artifact: Artifact) -> ValidationReport:
    """Validate an artifact's structure (spec §7). Pure — does not touch disk."""
    errors: list[Issue] = []
    warnings: list[Issue] = []

    _check_root(artifact, errors, warnings)

    experiment_slugs = _ids(artifact.experiments, "slug")
    dataset_ids = _ids(artifact.datasets, "id")
    claim_ids = _ids(artifact.claims, "id")
    result_ids = _ids(artifact.results, "id")
    exhibit_ids = _ids(artifact.exhibits, "id")

    _check_datasets(artifact, errors, warnings)
    _check_experiments(artifact, dataset_ids, experiment_slugs, errors, warnings)
    _check_traces(artifact, experiment_slugs, errors)
    _check_results(artifact, experiment_slugs, claim_ids, errors)
    _check_exhibits(
        artifact, experiment_slugs, claim_ids, result_ids, exhibit_ids, errors, warnings
    )
    _check_claims(artifact, experiment_slugs, result_ids, errors, warnings)
    _check_assessments(artifact, errors)
    _check_research_agent(artifact, errors)
    _check_generated_path_collisions(artifact, errors)
    _check_journal(artifact, warnings)

    return ValidationReport(ok=len(errors) == 0, errors=errors, warnings=warnings)
