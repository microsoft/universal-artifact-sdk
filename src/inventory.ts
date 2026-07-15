/**
 * Evidence inventory (spec §5.1): an SDK-computed capability list of what the submission
 * actually contains. The evaluator indexes each check/dimension by the evidence it needs and runs
 * it iff the inventory satisfies the precondition — otherwise `unassessable`, never a failure.
 *
 * The SDK only computes and records the inventory (structural); the evaluator acts on it (semantic).
 */

import { Artifact, ValidationMode, ResultKind } from "./model.js";

export interface EvidenceInventory {
  has_runnable_experiments: boolean;
  has_traces: boolean;
  trace_count: number;
  has_released_data: boolean;
  has_paper_source: boolean;
  has_citations_export: boolean;
  has_journal: boolean;
  has_research_agent: boolean;
  experiments_attempted: number;
  experiments_reported: number;
  evidence_kinds: ResultKind[];
  validation_modes: ValidationMode[];
}

/** An experiment is "reported" (active) unless a disposition marks it otherwise (spec §2.2.2). */
function isActive(e: Artifact["experiments"][number]): boolean {
  return !e.disposition || e.disposition.status === "active";
}

export function computeEvidenceInventory(a: Artifact): EvidenceInventory {
  const evidenceKinds = new Set<ResultKind>();
  const modes = new Set<ValidationMode>();
  for (const r of a.results) {
    if (r.kind) evidenceKinds.add(r.kind);
    if (r.validation_mode) modes.add(r.validation_mode);
  }
  const hasReleasedData = a.datasets.some(
    (d) => d.location.kind === "in_artifact" || d.location.kind === "external",
  );
  const reported = a.experiments.filter(isActive).length;
  return {
    has_runnable_experiments: reported > 0,
    has_traces: a.traces.length > 0,
    trace_count: a.traces.length,
    has_released_data: hasReleasedData,
    has_paper_source: Boolean(a.paper?.source || a.paper?.claims_export),
    has_citations_export: Boolean(a.paper?.references_export),
    has_journal: a.journal.length > 0,
    has_research_agent: Boolean(a.research_agent),
    experiments_attempted: a.experiments.length,
    experiments_reported: reported,
    evidence_kinds: [...evidenceKinds].sort(),
    validation_modes: [...modes].sort(),
  };
}
