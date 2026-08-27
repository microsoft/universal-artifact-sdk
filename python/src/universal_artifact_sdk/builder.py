"""The authoring API (spec §4): an ergonomic builder over the object model.

``add_*`` is create-or-replace keyed on the element's id/slug (upsert), so an artifact is
edited across iterations rather than rebuilt (spec §4.1). ``remove_*`` / ``get_*`` /
``list_*`` complete the re-entrant editor surface. None of these serialize — that is
:func:`write_submission`.

Every mutation is recorded in the artifact's append-only journal (spec §2.8) with a
rationale elicited per the session's :class:`JournalConfig` (spec §4.2). Experiments are
soft-removed (tagged ``abandoned`` and retained) so what was tried is never lost.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import replace
from datetime import datetime, timezone
from typing import Any, TypeVar

from .model import (
    FORMAT_VERSION,
    SDK_VERSION,
    AddClaimInput,
    Artifact,
    Assessment,
    ChangeContext,
    Claim,
    Dataset,
    Disposition,
    Environment,
    Exhibit,
    Experiment,
    Failure,
    JournalConfig,
    JournalEntry,
    JournalTarget,
    Paper,
    PendingChange,
    ResearchAgent,
    Result,
    Trace,
    pinned_digest,
)

T = TypeVar("T")

_ALWAYS_REQUIRE_RATIONALE = True
"""Dropping a tried experiment always requires a rationale, whatever the policy."""


def create_artifact(
    *, id: str, title: str, producer: dict[str, Any] | None = None
) -> Artifact:
    """Create a new, empty artifact held in memory (spec §4)."""
    if not id:
        raise ValueError("create_artifact: `id` is required")
    if not title:
        raise ValueError("create_artifact: `title` is required")
    return Artifact(
        id=id,
        title=title,
        format_version=FORMAT_VERSION,
        sdk_version=SDK_VERSION,
        producer=producer,
    )


# --- journaling (spec §2.8, §4.2) -------------------------------------------


def configure_journal(
    artifact: Artifact,
    *,
    policy: str | None = None,
    actor: str | None = None,
    on_missing_rationale: Callable[[PendingChange], str] | None = None,
    now: Callable[[], str] | None = None,
) -> None:
    """Configure the session's journaling policy (spec §4.2). Transient, never serialized.

    Under ``policy="prompt"`` the SDK calls ``on_missing_rationale`` to obtain an
    explanation when a mutation omits one. Unspecified settings keep their current value.
    """
    current = artifact.journal_config
    artifact.journal_config = JournalConfig(
        policy=policy or (current.policy if current else "warn"),
        actor=actor or (current.actor if current else "unknown"),
        on_missing_rationale=on_missing_rationale
        or (current.on_missing_rationale if current else None),
        now=now or (current.now if current else None),
    )


def list_journal(artifact: Artifact) -> list[JournalEntry]:
    """Return the full edit history, oldest first (spec §2.8). Returns a copy."""
    return list(artifact.journal)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _resolve_rationale(
    artifact: Artifact,
    op: str,
    target: JournalTarget,
    ctx: ChangeContext | None,
    require_rationale: bool = False,
) -> str:
    """Elicit the rationale for a mutation *before* the model is touched (spec §4.2)."""
    config = artifact.journal_config
    rationale = (ctx.rationale if ctx and ctx.rationale else "").strip()
    policy = config.policy if config else "warn"
    if not rationale and policy == "prompt" and config and config.on_missing_rationale:
        rationale = (config.on_missing_rationale(PendingChange(op=op, target=target)) or "").strip()
    if not rationale and (require_rationale or policy == "required"):
        raise ValueError(
            f"journal: a rationale is required for '{op}' on {target.kind}[{target.id}]"
        )
    return rationale


def _push_entry(
    artifact: Artifact,
    op: str,
    target: JournalTarget,
    rationale: str,
    ctx: ChangeContext | None,
    *,
    before: Any = None,
    after: Any = None,
) -> None:
    config = artifact.journal_config
    clock = config.now if config and config.now else _utc_now
    artifact.journal.append(
        JournalEntry(
            seq=len(artifact.journal) + 1,
            timestamp=clock(),
            actor=(ctx.actor if ctx and ctx.actor else (config.actor if config else "unknown")),
            op=op,
            target=target,
            rationale=rationale,
            before=before,
            after=after,
        )
    )


def _add_element(
    artifact: Artifact,
    elements: list[T],
    element: T,
    key: Callable[[T], str],
    kind: str,
    ctx: ChangeContext | None,
) -> T:
    """Generic add/replace + journal for the simple element lists."""
    element_id = key(element)
    index = next((i for i, item in enumerate(elements) if key(item) == element_id), -1)
    previous = elements[index] if index >= 0 else None
    op = "replace" if previous is not None else "add"
    target = JournalTarget(kind=kind, id=element_id)
    rationale = _resolve_rationale(artifact, op, target, ctx)
    if index >= 0:
        elements[index] = element
    else:
        elements.append(element)
    _push_entry(artifact, op, target, rationale, ctx, before=previous, after=element)
    return element


def _remove_element(
    artifact: Artifact,
    elements: list[T],
    element_id: str,
    key: Callable[[T], str],
    kind: str,
    ctx: ChangeContext | None,
) -> bool:
    """Generic hard-remove + journal for the simple element lists."""
    index = next((i for i, item in enumerate(elements) if key(item) == element_id), -1)
    if index < 0:
        return False
    previous = elements[index]
    target = JournalTarget(kind=kind, id=element_id)
    rationale = _resolve_rationale(artifact, "remove", target, ctx)
    elements.pop(index)
    _push_entry(artifact, "remove", target, rationale, ctx, before=previous)
    return True


# --- environment ------------------------------------------------------------


def add_environment(
    artifact: Artifact, environment: Environment, *, ctx: ChangeContext | None = None
) -> Environment:
    """Set the run environment, lifting an embedded digest into ``image.digest``."""
    embedded = pinned_digest(environment.image.reference if environment.image else None)
    resolved = (
        replace(environment, image=replace(environment.image, digest=embedded))
        if embedded and environment.image and not environment.image.digest
        else environment
    )
    previous = artifact.environment
    op = "replace" if previous else "set"
    target = JournalTarget(kind="environment", id=resolved.name)
    rationale = _resolve_rationale(artifact, op, target, ctx)
    artifact.environment = resolved
    _push_entry(artifact, op, target, rationale, ctx, before=previous, after=resolved)
    return resolved


# --- datasets ---------------------------------------------------------------


def add_dataset(
    artifact: Artifact, dataset: Dataset, *, ctx: ChangeContext | None = None
) -> Dataset:
    return _add_element(artifact, artifact.datasets, dataset, lambda x: x.id, "dataset", ctx)


def get_dataset(artifact: Artifact, id: str) -> Dataset | None:
    return next((item for item in artifact.datasets if item.id == id), None)


def list_datasets(artifact: Artifact) -> list[Dataset]:
    return list(artifact.datasets)


def remove_dataset(artifact: Artifact, id: str, *, ctx: ChangeContext | None = None) -> bool:
    return _remove_element(artifact, artifact.datasets, id, lambda x: x.id, "dataset", ctx)


# --- experiments ------------------------------------------------------------


def add_experiment(
    artifact: Artifact, experiment: Experiment, *, ctx: ChangeContext | None = None
) -> Experiment:
    return _add_element(
        artifact, artifact.experiments, experiment, lambda x: x.slug, "experiment", ctx
    )


def get_experiment(artifact: Artifact, slug: str) -> Experiment | None:
    return next((item for item in artifact.experiments if item.slug == slug), None)


def list_experiments(artifact: Artifact) -> list[Experiment]:
    return list(artifact.experiments)


def list_abandoned_experiments(artifact: Artifact) -> list[Experiment]:
    """Experiments the producer tried but dropped, retained for transparency (spec §2.2.2)."""
    return [
        item
        for item in artifact.experiments
        if item.disposition and item.disposition.status != "active"
    ]


def _set_disposition(
    artifact: Artifact,
    slug: str,
    disposition: Disposition,
    op: str,
    ctx: ChangeContext | None,
    require_rationale: bool,
) -> Experiment | None:
    experiment = get_experiment(artifact, slug)
    if experiment is None:
        return None
    before = replace(experiment)
    target = JournalTarget(kind="experiment", id=slug)
    rationale = _resolve_rationale(artifact, op, target, ctx, require_rationale)
    experiment.disposition = replace(disposition, rationale=rationale)
    _push_entry(
        artifact, op, target, rationale, ctx, before=before, after=replace(experiment)
    )
    return experiment


def abandon_experiment(
    artifact: Artifact, slug: str, *, ctx: ChangeContext | None = None
) -> Experiment | None:
    """Mark an attempted experiment as deliberately dropped (spec §2.2.2, §4.2)."""
    return _set_disposition(
        artifact, slug, Disposition(status="abandoned"), "abandon", ctx, _ALWAYS_REQUIRE_RATIONALE
    )


def fail_experiment(
    artifact: Artifact,
    slug: str,
    failure: Failure | Mapping[str, str],
    *,
    ctx: ChangeContext | None = None,
) -> Experiment | None:
    """Record an attempted experiment that failed to produce usable evidence (spec §2.2.2)."""
    if isinstance(failure, Failure):
        resolved = failure
    else:
        values: dict[str, Any] = dict(failure)
        resolved = Failure(**values)
    return _set_disposition(
        artifact,
        slug,
        Disposition(status="failed", failure=resolved),
        "abandon",
        ctx,
        _ALWAYS_REQUIRE_RATIONALE,
    )


def supersede_experiment(
    artifact: Artifact, slug: str, superseded_by: str, *, ctx: ChangeContext | None = None
) -> Experiment | None:
    """Mark an experiment superseded by a later variant, keeping the lineage (spec §2.2.2)."""
    return _set_disposition(
        artifact,
        slug,
        Disposition(status="superseded", superseded_by=superseded_by),
        "replace",
        ctx,
        _ALWAYS_REQUIRE_RATIONALE,
    )


def remove_experiment(artifact: Artifact, slug: str, *, ctx: ChangeContext | None = None) -> bool:
    """Soft-remove an experiment: tag it ``abandoned`` and retain it (spec §2.2.2).

    A rationale is always required. Use :func:`purge_experiment` for a hard delete.
    """
    return abandon_experiment(artifact, slug, ctx=ctx) is not None


def purge_experiment(artifact: Artifact, slug: str, *, ctx: ChangeContext | None = None) -> bool:
    """Hard-delete an experiment (spec §2.2.2). Journaled; a rationale is required."""
    index = next((i for i, item in enumerate(artifact.experiments) if item.slug == slug), -1)
    if index < 0:
        return False
    previous = artifact.experiments[index]
    target = JournalTarget(kind="experiment", id=slug)
    rationale = _resolve_rationale(artifact, "remove", target, ctx, _ALWAYS_REQUIRE_RATIONALE)
    artifact.experiments.pop(index)
    _push_entry(artifact, "remove", target, rationale, ctx, before=previous)
    return True


# --- traces -----------------------------------------------------------------


def add_trace(artifact: Artifact, trace: Trace, *, ctx: ChangeContext | None = None) -> Trace:
    return _add_element(artifact, artifact.traces, trace, lambda x: x.id, "trace", ctx)


def get_trace(artifact: Artifact, id: str) -> Trace | None:
    return next((item for item in artifact.traces if item.id == id), None)


def list_traces(artifact: Artifact) -> list[Trace]:
    return list(artifact.traces)


def remove_trace(artifact: Artifact, id: str, *, ctx: ChangeContext | None = None) -> bool:
    return _remove_element(artifact, artifact.traces, id, lambda x: x.id, "trace", ctx)


# --- results ----------------------------------------------------------------


def add_result(artifact: Artifact, result: Result, *, ctx: ChangeContext | None = None) -> Result:
    return _add_element(artifact, artifact.results, result, lambda x: x.id, "result", ctx)


def get_result(artifact: Artifact, id: str) -> Result | None:
    return next((item for item in artifact.results if item.id == id), None)


def list_results(artifact: Artifact) -> list[Result]:
    return list(artifact.results)


def remove_result(artifact: Artifact, id: str, *, ctx: ChangeContext | None = None) -> bool:
    return _remove_element(artifact, artifact.results, id, lambda x: x.id, "result", ctx)


# --- exhibits ---------------------------------------------------------------


def add_exhibit(
    artifact: Artifact, exhibit: Exhibit, *, ctx: ChangeContext | None = None
) -> Exhibit:
    """Add or replace a typed exhibit that substantiates claims (spec §2.3.1)."""
    return _add_element(artifact, artifact.exhibits, exhibit, lambda x: x.id, "exhibit", ctx)


def get_exhibit(artifact: Artifact, id: str) -> Exhibit | None:
    return next((item for item in artifact.exhibits if item.id == id), None)


def list_exhibits(artifact: Artifact) -> list[Exhibit]:
    return list(artifact.exhibits)


def remove_exhibit(artifact: Artifact, id: str, *, ctx: ChangeContext | None = None) -> bool:
    return _remove_element(artifact, artifact.exhibits, id, lambda x: x.id, "exhibit", ctx)


# --- claims -----------------------------------------------------------------


def add_claim(
    artifact: Artifact, input: Claim | AddClaimInput, *, ctx: ChangeContext | None = None
) -> Claim:
    """Add or replace a claim, accepting the singular ``validator`` sugar (spec §2.4).

    Like the frozen TypeScript ``addClaim``, the claim is reconstructed from the known
    contract fields, so unknown input keys are dropped rather than stored.
    """
    if isinstance(input, Claim):
        validators = list(input.validators)
    elif input.validators is not None:
        validators = list(input.validators)
    else:
        validators = [input.validator] if input.validator else []
    claim = Claim(
        id=input.id,
        statement=input.statement,
        validators=validators,
        stance=input.stance,
        tested_by=input.tested_by,
        paper_ref=input.paper_ref,
    )
    return _add_element(artifact, artifact.claims, claim, lambda x: x.id, "claim", ctx)


def get_claim(artifact: Artifact, id: str) -> Claim | None:
    return next((item for item in artifact.claims if item.id == id), None)


def list_claims(artifact: Artifact) -> list[Claim]:
    return list(artifact.claims)


def remove_claim(artifact: Artifact, id: str, *, ctx: ChangeContext | None = None) -> bool:
    return _remove_element(artifact, artifact.claims, id, lambda x: x.id, "claim", ctx)


# --- assessments ------------------------------------------------------------


def add_assessment(
    artifact: Artifact, assessment: Assessment, *, ctx: ChangeContext | None = None
) -> Assessment:
    return _add_element(
        artifact, artifact.assessments, assessment, lambda x: x.id, "assessment", ctx
    )


def get_assessment(artifact: Artifact, id: str) -> Assessment | None:
    return next((item for item in artifact.assessments if item.id == id), None)


def list_assessments(artifact: Artifact) -> list[Assessment]:
    return list(artifact.assessments)


def remove_assessment(artifact: Artifact, id: str, *, ctx: ChangeContext | None = None) -> bool:
    return _remove_element(artifact, artifact.assessments, id, lambda x: x.id, "assessment", ctx)


# --- paper / research agent / reflection ------------------------------------


def attach_paper(artifact: Artifact, paper: Paper, *, ctx: ChangeContext | None = None) -> Paper:
    previous = artifact.paper
    op = "replace" if previous else "attach"
    target = JournalTarget(kind="paper", id=paper.pdf or paper.source or "paper")
    rationale = _resolve_rationale(artifact, op, target, ctx)
    artifact.paper = paper
    _push_entry(artifact, op, target, rationale, ctx, before=previous, after=paper)
    return paper


def attach_research_agent(
    artifact: Artifact, agent: ResearchAgent, *, ctx: ChangeContext | None = None
) -> ResearchAgent:
    """Attach the optional producer-shipped Q&A witness (spec §2.9)."""
    resolved = replace(agent, path=agent.path or "research-agent.md")
    previous = artifact.research_agent
    op = "replace" if previous else "attach"
    target = JournalTarget(kind="research_agent", id=resolved.path)
    rationale = _resolve_rationale(artifact, op, target, ctx)
    artifact.research_agent = resolved
    _push_entry(artifact, op, target, rationale, ctx, before=previous, after=resolved)
    return resolved


def set_reflection(artifact: Artifact, markdown: str, *, ctx: ChangeContext | None = None) -> None:
    """Set the producer's reflection text, written to ``reflection.md`` on emit."""
    op = "replace" if artifact.reflection is not None else "set"
    target = JournalTarget(kind="reflection", id="reflection.md")
    rationale = _resolve_rationale(artifact, op, target, ctx)
    artifact.reflection = markdown
    _push_entry(artifact, op, target, rationale, ctx)
