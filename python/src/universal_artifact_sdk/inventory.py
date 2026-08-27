"""Evidence inventory (spec §5.1): what the submission actually contains.

The evaluator indexes each check by the evidence it needs and runs it only when the
inventory satisfies the precondition — otherwise the check is *unassessable*, never a
failure. The SDK only computes and records the inventory; the evaluator acts on it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .model import Artifact, Experiment


@dataclass
class EvidenceInventory:
    """SDK-computed capability list embedded in ``manifest.evidence_inventory``."""

    has_runnable_experiments: bool
    has_traces: bool
    trace_count: int
    has_exhibits: bool
    exhibit_count: int
    has_released_data: bool
    has_paper_source: bool
    has_citations_export: bool
    has_journal: bool
    has_research_agent: bool
    experiments_attempted: int
    experiments_reported: int
    evidence_kinds: list[str]
    validation_modes: list[str]
    extra: dict[str, Any] = field(default_factory=dict)


def _is_active(experiment: Experiment) -> bool:
    """An experiment is "reported" (active) unless a disposition says otherwise (spec §2.2.2)."""
    return not experiment.disposition or experiment.disposition.status == "active"


def _location_kind(location: Any) -> Any:
    if isinstance(location, dict):
        return location.get("kind")
    return getattr(location, "kind", None)


def compute_evidence_inventory(artifact: Artifact) -> EvidenceInventory:
    """Derive the evidence inventory for ``artifact`` (spec §5.1)."""
    evidence_kinds = sorted({result.kind for result in artifact.results if result.kind})
    validation_modes = sorted(
        {result.validation_mode for result in artifact.results if result.validation_mode}
    )
    reported = sum(1 for experiment in artifact.experiments if _is_active(experiment))
    paper = artifact.paper
    return EvidenceInventory(
        has_runnable_experiments=reported > 0,
        has_traces=len(artifact.traces) > 0,
        trace_count=len(artifact.traces),
        has_exhibits=len(artifact.exhibits) > 0,
        exhibit_count=len(artifact.exhibits),
        has_released_data=any(
            _location_kind(dataset.location) in ("in_artifact", "external")
            for dataset in artifact.datasets
        ),
        has_paper_source=bool(paper and (paper.source or paper.claims_export)),
        has_citations_export=bool(paper and paper.references_export),
        has_journal=len(artifact.journal) > 0,
        has_research_agent=artifact.research_agent is not None,
        experiments_attempted=len(artifact.experiments),
        experiments_reported=reported,
        evidence_kinds=evidence_kinds,
        validation_modes=validation_modes,
    )
