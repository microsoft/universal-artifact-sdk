/**
 * The authoring API (spec §4): an ergonomic builder over the object model.
 *
 * `add*` is create-or-replace keyed on the element's id/slug (upsert), so an artifact is
 * edited across iterations rather than rebuilt (spec §4.1). `remove*`/`get*`/`list*` complete
 * the re-entrant editor surface. None of these serialize — that is `writeSubmission` (serialize.ts).
 *
 * Every **mutation** is recorded in the artifact's append-only `journal` (spec §2.8) with a
 * `rationale` elicited per the session's `JournalConfig` (spec §4.2) — so the artifact carries a
 * narrated, diffable history of the research process, not just its final state. Experiments are
 * **soft-removed** (tagged `abandoned`, retained) so what was tried and dropped is never lost.
 */

import {
  Artifact,
  Assessment,
  Claim,
  Dataset,
  Disposition,
  Environment,
  Experiment,
  FORMAT_VERSION,
  JournalConfig,
  JournalEntry,
  JournalOp,
  JournalTarget,
  Paper,
  pinnedDigest,
  ResearchAgent,
  Result,
  SDK_VERSION,
  Trace,
  Validator,
} from "./model.js";

export interface CreateArtifactInput {
  id: string;
  title: string;
  producer?: Record<string, unknown>;
}

/** New, empty artifact held in memory (spec §4). */
export function createArtifact(input: CreateArtifactInput): Artifact {
  if (!input.id) throw new Error("createArtifact: `id` is required");
  if (!input.title) throw new Error("createArtifact: `title` is required");
  return {
    format_version: FORMAT_VERSION,
    sdk_version: SDK_VERSION,
    id: input.id,
    title: input.title,
    producer: input.producer,
    environment: undefined,
    datasets: [],
    experiments: [],
    traces: [],
    results: [],
    claims: [],
    assessments: [],
    paper: undefined,
    research_agent: undefined,
    reflection: undefined,
    journal: [],
  };
}

// --- journaling (spec §2.8, §4.2) -------------------------------------------

/** Optional per-mutation context carrying who made the change and why (spec §4.2). */
export interface ChangeContext {
  actor?: string;
  rationale?: string;
}

/**
 * Configure the session's journaling policy (spec §4.2). Transient — not serialized. Under
 * `policy: "prompt"`, the SDK calls `onMissingRationale` to obtain an explanation when a mutation
 * omits one; this is the seam a producing harness wires its agent-prompting into.
 */
export function configureJournal(
  a: Artifact,
  config: Partial<JournalConfig>,
): void {
  a.journalConfig = {
    policy: config.policy ?? a.journalConfig?.policy ?? "warn",
    actor: config.actor ?? a.journalConfig?.actor ?? "unknown",
    onMissingRationale:
      config.onMissingRationale ?? a.journalConfig?.onMissingRationale,
    now: config.now ?? a.journalConfig?.now,
  };
}

/** The full edit history, oldest first (spec §2.8). Returns a copy. */
export function listJournal(a: Artifact): JournalEntry[] {
  return [...a.journal];
}

function resolveRationale(
  a: Artifact,
  op: JournalOp,
  target: JournalTarget,
  ctx: ChangeContext | undefined,
  requireRationale: boolean,
): string {
  const cfg = a.journalConfig;
  let rationale = (ctx?.rationale ?? "").trim();
  const policy = cfg?.policy ?? "warn";
  if (!rationale && policy === "prompt" && cfg?.onMissingRationale) {
    rationale = (cfg.onMissingRationale({ op, target }) ?? "").trim();
  }
  if (!rationale && (requireRationale || policy === "required")) {
    throw new Error(
      `journal: a rationale is required for '${op}' on ${target.kind}[${target.id}]`,
    );
  }
  return rationale;
}

function pushEntry(
  a: Artifact,
  op: JournalOp,
  target: JournalTarget,
  rationale: string,
  ctx: ChangeContext | undefined,
  extras?: { before?: unknown; after?: unknown },
): void {
  const cfg = a.journalConfig;
  const clock = cfg?.now ?? (() => new Date().toISOString());
  const entry: JournalEntry = {
    seq: a.journal.length + 1,
    timestamp: clock(),
    actor: ctx?.actor ?? cfg?.actor ?? "unknown",
    op,
    target,
    rationale,
    ...(extras && "before" in extras ? { before: extras.before } : {}),
    ...(extras && "after" in extras ? { after: extras.after } : {}),
  };
  a.journal.push(entry);
}

/**
 * Generic add/replace + journal for the simple element lists. The rationale is resolved (and may
 * throw under `policy: "required"`) **before** the model is mutated, so a rejected change leaves
 * the artifact untouched.
 */
function addElement<T>(
  a: Artifact,
  list: T[],
  item: T,
  key: (x: T) => string,
  kind: JournalTarget["kind"],
  ctx: ChangeContext | undefined,
): T {
  const k = key(item);
  const idx = list.findIndex((x) => key(x) === k);
  const prev = idx >= 0 ? list[idx] : undefined;
  const op: JournalOp = prev ? "replace" : "add";
  const rationale = resolveRationale(a, op, { kind, id: k }, ctx, false);
  if (idx >= 0) list[idx] = item;
  else list.push(item);
  pushEntry(
    a,
    op,
    { kind, id: k },
    rationale,
    ctx,
    prev ? { before: prev, after: item } : { after: item },
  );
  return item;
}

/** Generic hard-remove + journal for the simple element lists (resolve before mutate). */
function removeElement<T>(
  a: Artifact,
  list: T[],
  id: string,
  key: (x: T) => string,
  kind: JournalTarget["kind"],
  ctx: ChangeContext | undefined,
): boolean {
  const idx = list.findIndex((x) => key(x) === id);
  if (idx < 0) return false;
  const removed = list[idx];
  const rationale = resolveRationale(a, "remove", { kind, id }, ctx, false);
  list.splice(idx, 1);
  pushEntry(a, "remove", { kind, id }, rationale, ctx, { before: removed });
  return true;
}

// --- environment ------------------------------------------------------------

export function addEnvironment(
  a: Artifact,
  env: Environment,
  ctx?: ChangeContext,
): Environment {
  // Auto-pin: if the reference already embeds a digest (`repo@sha256:…`) but `image.digest`
  // was left unset, lift it into the field so the pin is explicit + machine-readable (spec §4).
  const embedded = pinnedDigest(env.image?.reference);
  const resolved: Environment =
    embedded && env.image && !env.image.digest
      ? { ...env, image: { ...env.image, digest: embedded } }
      : env;
  const prev = a.environment;
  const op: JournalOp = prev ? "replace" : "set";
  const rationale = resolveRationale(
    a,
    op,
    { kind: "environment", id: resolved.name },
    ctx,
    false,
  );
  a.environment = resolved;
  pushEntry(
    a,
    op,
    { kind: "environment", id: resolved.name },
    rationale,
    ctx,
    prev ? { before: prev, after: resolved } : { after: resolved },
  );
  return resolved;
}

// --- datasets ---------------------------------------------------------------

export function addDataset(
  a: Artifact,
  dataset: Dataset,
  ctx?: ChangeContext,
): Dataset {
  return addElement(a, a.datasets, dataset, (d) => d.id, "dataset", ctx);
}
export function getDataset(a: Artifact, id: string): Dataset | undefined {
  return a.datasets.find((d) => d.id === id);
}
export function listDatasets(a: Artifact): Dataset[] {
  return [...a.datasets];
}
export function removeDataset(
  a: Artifact,
  id: string,
  ctx?: ChangeContext,
): boolean {
  return removeElement(a, a.datasets, id, (d) => d.id, "dataset", ctx);
}

// --- experiments ------------------------------------------------------------

export function addExperiment(
  a: Artifact,
  experiment: Experiment,
  ctx?: ChangeContext,
): Experiment {
  return addElement(
    a,
    a.experiments,
    experiment,
    (e) => e.slug,
    "experiment",
    ctx,
  );
}
export function getExperiment(
  a: Artifact,
  slug: string,
): Experiment | undefined {
  return a.experiments.find((e) => e.slug === slug);
}
export function listExperiments(a: Artifact): Experiment[] {
  return [...a.experiments];
}
/** Experiments the agent tried but dropped, retained for process transparency (spec §2.2.2). */
export function listAbandonedExperiments(a: Artifact): Experiment[] {
  return a.experiments.filter(
    (e) => e.disposition && e.disposition.status !== "active",
  );
}

/**
 * **Soft-remove** an experiment (spec §2.2.2): tag it `abandoned` and retain it, rather than
 * deleting it, so what was tried is never lost. Like `failExperiment`/`purgeExperiment`, dropping a
 * tried experiment **requires a rationale** regardless of journal policy (spec §4.2) — pass
 * `ctx.rationale`, or wire a `prompt`-policy `onMissingRationale` callback to supply it. Use
 * `purgeExperiment` for a true hard delete. Returns false if the slug is unknown.
 */
export function removeExperiment(
  a: Artifact,
  slug: string,
  ctx?: ChangeContext,
): boolean {
  return abandonExperiment(a, slug, ctx) !== undefined;
}

function setDisposition(
  a: Artifact,
  slug: string,
  disp: Omit<Disposition, "rationale">,
  op: JournalOp,
  ctx: ChangeContext | undefined,
  requireRationale: boolean,
): Experiment | undefined {
  const e = a.experiments.find((x) => x.slug === slug);
  if (!e) return undefined;
  const before = { ...e };
  const rationale = resolveRationale(
    a,
    op,
    { kind: "experiment", id: slug },
    ctx,
    requireRationale,
  );
  e.disposition = { ...disp, rationale };
  pushEntry(a, op, { kind: "experiment", id: slug }, rationale, ctx, {
    before,
    after: { ...e },
  });
  return e;
}

/** Mark an attempted experiment as deliberately dropped; retained with a required rationale (spec §2.2.2, §4.2). */
export function abandonExperiment(
  a: Artifact,
  slug: string,
  ctx?: ChangeContext,
): Experiment | undefined {
  return setDisposition(a, slug, { status: "abandoned" }, "abandon", ctx, true);
}

/** Record an attempted experiment that failed to produce usable evidence (spec §2.2.2). */
export function failExperiment(
  a: Artifact,
  slug: string,
  failure: { stage: string; summary: string },
  ctx?: ChangeContext,
): Experiment | undefined {
  return setDisposition(
    a,
    slug,
    { status: "failed", failure },
    "abandon",
    ctx,
    true,
  );
}

/** Mark an experiment superseded by a later variant, keeping the lineage (spec §2.2.2, §4.2). */
export function supersedeExperiment(
  a: Artifact,
  slug: string,
  supersededBy: string,
  ctx?: ChangeContext,
): Experiment | undefined {
  return setDisposition(
    a,
    slug,
    { status: "superseded", superseded_by: supersededBy },
    "replace",
    ctx,
    true,
  );
}

/** Hard-delete an experiment (spec §2.2.2). Journaled; a rationale is required. */
export function purgeExperiment(
  a: Artifact,
  slug: string,
  ctx?: ChangeContext,
): boolean {
  const idx = a.experiments.findIndex((e) => e.slug === slug);
  if (idx < 0) return false;
  const removed = a.experiments[idx];
  const rationale = resolveRationale(
    a,
    "remove",
    { kind: "experiment", id: slug },
    ctx,
    true,
  );
  a.experiments.splice(idx, 1);
  pushEntry(a, "remove", { kind: "experiment", id: slug }, rationale, ctx, {
    before: removed,
  });
  return true;
}

// --- traces -----------------------------------------------------------------

export function addTrace(
  a: Artifact,
  trace: Trace,
  ctx?: ChangeContext,
): Trace {
  return addElement(a, a.traces, trace, (t) => t.id, "trace", ctx);
}
export function getTrace(a: Artifact, id: string): Trace | undefined {
  return a.traces.find((t) => t.id === id);
}
export function listTraces(a: Artifact): Trace[] {
  return [...a.traces];
}
export function removeTrace(
  a: Artifact,
  id: string,
  ctx?: ChangeContext,
): boolean {
  return removeElement(a, a.traces, id, (t) => t.id, "trace", ctx);
}

// --- results ----------------------------------------------------------------

export function addResult(
  a: Artifact,
  result: Result,
  ctx?: ChangeContext,
): Result {
  return addElement(a, a.results, result, (r) => r.id, "result", ctx);
}
export function getResult(a: Artifact, id: string): Result | undefined {
  return a.results.find((r) => r.id === id);
}
export function listResults(a: Artifact): Result[] {
  return [...a.results];
}
export function removeResult(
  a: Artifact,
  id: string,
  ctx?: ChangeContext,
): boolean {
  return removeElement(a, a.results, id, (r) => r.id, "result", ctx);
}

// --- claims -----------------------------------------------------------------

/** `validators` list OR singular `validator` sugar (spec §2.4). */
export type AddClaimInput = Omit<Claim, "validators"> & {
  validators?: Validator[];
  validator?: Validator;
};

export function addClaim(
  a: Artifact,
  input: AddClaimInput,
  ctx?: ChangeContext,
): Claim {
  const validators =
    input.validators ?? (input.validator ? [input.validator] : []);
  const claim: Claim = {
    id: input.id,
    statement: input.statement,
    stance: input.stance,
    tested_by: input.tested_by,
    paper_ref: input.paper_ref,
    validators,
  };
  return addElement(a, a.claims, claim, (c) => c.id, "claim", ctx);
}
export function getClaim(a: Artifact, id: string): Claim | undefined {
  return a.claims.find((c) => c.id === id);
}
export function listClaims(a: Artifact): Claim[] {
  return [...a.claims];
}
export function removeClaim(
  a: Artifact,
  id: string,
  ctx?: ChangeContext,
): boolean {
  return removeElement(a, a.claims, id, (c) => c.id, "claim", ctx);
}

// --- assessments ------------------------------------------------------------

export function addAssessment(
  a: Artifact,
  assessment: Assessment,
  ctx?: ChangeContext,
): Assessment {
  return addElement(
    a,
    a.assessments,
    assessment,
    (x) => x.id,
    "assessment",
    ctx,
  );
}
export function getAssessment(a: Artifact, id: string): Assessment | undefined {
  return a.assessments.find((x) => x.id === id);
}
export function listAssessments(a: Artifact): Assessment[] {
  return [...a.assessments];
}
export function removeAssessment(
  a: Artifact,
  id: string,
  ctx?: ChangeContext,
): boolean {
  return removeElement(a, a.assessments, id, (x) => x.id, "assessment", ctx);
}

// --- paper / reflection -----------------------------------------------------

export function attachPaper(
  a: Artifact,
  paper: Paper,
  ctx?: ChangeContext,
): Paper {
  const prev = a.paper;
  const op: JournalOp = prev ? "replace" : "attach";
  const paperId = paper.pdf ?? paper.source ?? "paper";
  const rationale = resolveRationale(
    a,
    op,
    { kind: "paper", id: paperId },
    ctx,
    false,
  );
  a.paper = paper;
  pushEntry(
    a,
    op,
    { kind: "paper", id: paperId },
    rationale,
    ctx,
    prev ? { before: prev, after: paper } : { after: paper },
  );
  return paper;
}

export function attachResearchAgent(
  a: Artifact,
  agent: ResearchAgent,
  ctx?: ChangeContext,
): ResearchAgent {
  const resolved: ResearchAgent = {
    ...agent,
    path: agent.path || "research-agent.md",
  };
  const prev = a.research_agent;
  const op: JournalOp = prev ? "replace" : "attach";
  const rationale = resolveRationale(
    a,
    op,
    { kind: "research_agent", id: resolved.path },
    ctx,
    false,
  );
  a.research_agent = resolved;
  pushEntry(
    a,
    op,
    { kind: "research_agent", id: resolved.path },
    rationale,
    ctx,
    prev ? { before: prev, after: resolved } : { after: resolved },
  );
  return resolved;
}

export function setReflection(
  a: Artifact,
  markdown: string,
  ctx?: ChangeContext,
): void {
  const op: JournalOp = a.reflection !== undefined ? "replace" : "set";
  const rationale = resolveRationale(
    a,
    op,
    { kind: "reflection", id: "reflection.md" },
    ctx,
    false,
  );
  a.reflection = markdown;
  pushEntry(a, op, { kind: "reflection", id: "reflection.md" }, rationale, ctx);
}
